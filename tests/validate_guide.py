#!/usr/bin/env python3
"""Execute exact TP code blocks in a fresh, disposable Compose project."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shlex
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


class LabShell:
    """Keep a student's Bash context, including cwd/umask, between blocks."""

    def __init__(self, command, cwd, env):
        self.process = subprocess.Popen(command, cwd=cwd, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.reader = selectors.DefaultSelector()
        self.reader.register(self.process.stdout, selectors.EVENT_READ)
        self.sequence = 0

    def execute(self, code, timeout=600):
        self.sequence += 1
        marker = f'__CPE_BLOCK_END_{self.sequence}__'
        encoded = base64.b64encode(code.encode()).decode()
        # Source through a separate fd; SSH must not consume the shell's stdin.
        wrapper = ('set +e\nset -o pipefail\n'
            f'source <(printf %s {shlex.quote(encoded)} | base64 -d) </dev/null\n'
            'lab_validation_status=$?\n'
            f'printf "\\n{marker}%s\\n" "$lab_validation_status"\n')
        self.process.stdin.write(wrapper.encode())
        self.process.stdin.flush()
        deadline = time.monotonic() + timeout
        collected = b''
        pattern = re.compile(rb'\n' + marker.encode() + rb'(\d+)\r?\n')
        while time.monotonic() < deadline:
            if not self.reader.select(min(1, deadline - time.monotonic())):
                continue
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('Student shell closed before block completed: ' + collected.decode(errors='replace')[-2000:])
            collected += chunk
            found = pattern.search(collected)
            if found:
                return subprocess.CompletedProcess([], int(found[1]),
                    collected[:found.start()].decode(errors='replace'), '')
        raise TimeoutError('Student shell block exceeded its time limit')

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                self.process.wait(timeout=5)
        self.reader.close()
        self.process.stdout.close()


def interrupted(signum, frame):
    raise SystemExit(128 + signum)


def main():
    signal.signal(signal.SIGTERM, interrupted)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='cpe-guide-validation')
    parser.add_argument('--port', type=int, default=22223)
    parser.add_argument('--order', choices=['teaching', 'reference', 'legacy'], default='teaching')
    parser.add_argument('--extensions', action='store_true')
    parser.add_argument('--persistent-shells', action='store_true',
        help='Reuse student consoles, preserving cwd, variables and umask between blocks')
    parser.add_argument('--keep', action='store_true', help='Keep this disposable project for inspection')
    args = parser.parse_args()
    if not re.fullmatch(r'cpe-[a-z0-9][a-z0-9_-]*', args.project):
        parser.error('Use a dedicated project name beginning cpe-')
    if not 1024 <= args.port <= 65535:
        parser.error('Choose an unprivileged TCP port')
    existing = subprocess.check_output(['docker', 'ps', '-aq', '--filter',
        f'label=com.docker.compose.project={args.project}'], text=True).strip()
    if existing:
        parser.error('Project already contains containers; choose another name or remove it deliberately')
    out = ROOT / 'artifacts' / 'validation' / (args.project + '-' + time.strftime('%Y%m%d-%H%M%S'))
    out.mkdir(parents=True)
    evidence = out / 'evidence'
    evidence.mkdir()
    override = out / 'compose.override.json'
    override.write_text(json.dumps({'services': {'host': {'volumes': [f'{evidence}:/artifacts']}}}))
    env = dict(os.environ, COMPOSE_PROJECT_NAME=args.project, LAB_SSH_PORT=str(args.port),
        COMPOSE_FILE=str(ROOT / 'docker-compose.yml') + ':' + str(override))
    compose = ['docker', 'compose']

    def run(cmd, **kwargs):
        return subprocess.run(cmd, cwd=ROOT, env=env, text=True, **kwargs)

    def output(cmd):
        return run(cmd, check=True, stdout=subprocess.PIPE).stdout.strip()

    guide = (ROOT / 'docs/TP-2026.md').read_text()
    sections = re.split(r'^## (\d+)\.[^\n]*\n', guide, flags=re.M)
    indexed = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    order = [1, 2, 4, 5, 3, 7, 8, 6, 10, 9, 11, 12] if args.order == 'legacy' else sorted(indexed)
    extension = (ROOT / 'docs/EXTENSIONS-2026.md').read_text() if args.extensions else ''
    content = '\n'.join(indexed[n] + ('\n' + extension if n == 7 and args.order != 'legacy' else '') for n in order)
    if args.order == 'legacy':
        content += '\n' + extension
    blocks = re.findall(r'```bash\n(.*?)\n```', content, re.S)
    labels = set()
    for block in blocks:
        marker = re.fullmatch(r'# (TARGET|CLIENT|LAPTOP) \[([^]]+)\](.*)', block.splitlines()[0])
        if not marker or marker[2] in labels:
            raise RuntimeError('Missing or duplicate executable-block marker')
        labels.add(marker[2])
        run(['bash', '-n'], input='\n'.join(block.splitlines()[1:]), check=True)
    rows = []
    shells = {}
    manifest = {'order': order, 'extension_placement': ('after-all-core' if args.order == 'legacy' else 'after-section-7-before-8') if extension else None, 'guide_sha256': hashlib.sha256(guide.encode()).hexdigest(),
        'shell_mode': 'persistent-student-consoles' if args.persistent_shells else 'strict-independent-blocks',
        'extensions_sha256': hashlib.sha256(extension.encode()).hexdigest() if extension else None,
        'architecture': output(['uname', '-m']), 'checks': rows}
    try:
        run(compose + ['up', '-d', '--wait', '--no-build'], check=True, timeout=180)
        container = output(compose + ['ps', '-q', 'host'])
        inspection = json.loads(output(['docker', 'inspect', container]))[0]
        bindings = inspection['NetworkSettings']['Ports']['22/tcp']
        assert all(b['HostIp'] == '127.0.0.1' for b in bindings), bindings
        manifest['images'] = {'host': inspection['Image']}
        client_container = output(compose + ['ps', '-q', 'attacker'])
        manifest['images']['attacker'] = json.loads(output(['docker', 'inspect', client_container]))[0]['Image']
        run(compose + ['exec', '-T', 'host', 'bash', '-ec',
            'printf "phase-0-evidence\n" > /artifacts/setup-proof.txt'], check=True)
        assert (evidence / 'setup-proof.txt').read_text().strip() == 'phase-0-evidence'
        manifest['artifact_mount_visible_on_laptop'] = True
        helper_digest = output(compose + ['exec', '-T', 'host', 'sha256sum', '/usr/local/sbin/install-osquery-lab']).split()[0]
        assert helper_digest == hashlib.sha256((ROOT / 'lab/install-osquery').read_bytes()).hexdigest(), 'Rebuild the host image: installer differs from the source'
        # The same image must create a different host key for another fresh target.
        key = output(compose + ['exec', '-T', 'host', 'cat', '/etc/ssh/ssh_host_ed25519_key.pub'])
        other = output(compose + ['run', '--rm', '-T', '--no-deps', 'host', 'bash', '-ec',
            'ssh-keygen -A >/dev/null; cat /etc/ssh/ssh_host_ed25519_key.pub'])
        assert key.split()[:2] != other.split()[:2], 'Reused SSH host key'
        manifest['fresh_host_keys_differ'] = True
        for block in blocks:
            lines = block.splitlines()
            where, label, options = re.fullmatch(r'# (TARGET|CLIENT|LAPTOP) \[([^]]+)\](.*)', lines[0]).groups()
            expected = int(re.search(r'expect=(\d+)', options)[1]) if 'expect=' in options else 0
            user = re.search(r'user=(\w+)', options)[1] if 'user=' in options else 'root'
            code = '\n'.join(lines[1:])
            cmd = ['bash', '-o', 'pipefail', '-ec', code]
            if where != 'LAPTOP':
                cmd = compose + ['exec', '-T', '--user', user, 'host' if where == 'TARGET' else 'attacker'] + cmd
            start = time.monotonic()
            if args.persistent_shells and where != 'LAPTOP':
                shell_key = (where, user)
                if 'fresh-session' in options and shell_key in shells:
                    shells.pop(shell_key).close()
                if shell_key not in shells:
                    shell_command = compose + ['exec', '-T', '--user', user,
                        'host' if where == 'TARGET' else 'attacker', 'bash', '--noprofile', '--norc']
                    shells[shell_key] = LabShell(shell_command, ROOT, env)
                if label == 'umask':
                    context_before = shells[shell_key].execute('printf "%s\\n" "$PWD"; umask').stdout
                result = shells[shell_key].execute(code)
                if label == 'umask':
                    context_after = shells[shell_key].execute('printf "%s\\n" "$PWD"; umask').stdout
                    assert context_before == context_after, 'umask block leaked its cwd or mask into the next exercise'
                    manifest['umask_restores_terminal_context'] = True
            else:
                result = run(cmd, capture_output=True, timeout=600)
            row = {'check': label, 'where': where, 'user': user, 'exit': result.returncode,
                'expected': expected, 'passed': result.returncode == expected,
                'seconds': round(time.monotonic() - start, 2)}
            rows.append(row)
            (out / (label + '.log')).write_text('$ ' + code + '\n\n' + result.stdout + result.stderr)
            (out / 'results.json').write_text(json.dumps(manifest, indent=2) + '\n')
            print(json.dumps(row), flush=True)
            if not row['passed']:
                raise RuntimeError(f'{label}: expected {expected}, got {result.returncode}\n{result.stderr[-2000:]}')
            if label == 'client-fingerprint':
                known = output(compose + ['exec', '-T', 'attacker', 'cat', '/root/.ssh/known_hosts'])
                assert key.split()[:2] == known.split()[1:3], 'Host fingerprint differs between consoles'
            if label == 'restart-target':
                # Restart ends the target consoles; students reopen them too.
                for shell_key in list(shells):
                    if shell_key[0] == 'TARGET':
                        shells.pop(shell_key).close()
        run(compose + ['exec', '-T', 'host', 'bash', '-ec',
            'test "$(stat -c %a /var/log/auth.log)" = 640; '
            'test "$(stat -c %u /opt/osquery/bin/osqueryd)" = 0; '
            'runuser -u student -- test ! -w /opt/osquery/bin/osqueryd; '
            'runuser -u student -- test ! -r /var/log/auth.log'], check=True)
        manifest['osquery_version'] = output(compose + ['exec', '-T', 'host', 'osqueryi', '--version'])
        run(compose + ['exec', '-T', 'host', 'bash', '-ec',
            'nft list table inet filter > /tmp/nft-before; '
            'printf "not a valid nftables configuration\\n" > /tmp/nft-invalid; '
            'if nft-lab load /tmp/nft-invalid >/tmp/nft-error 2>&1; then exit 1; fi; '
            'nft list table inet filter > /tmp/nft-after; '
            'diff -u /tmp/nft-before /tmp/nft-after'], check=True)
        manifest['invalid_firewall_preserves_table'] = True
        json_files = list(evidence.glob('*.json'))
        assert len(json_files) == 12, 'Expected all twelve osquery evidence files'
        for file in json_files:
            assert isinstance(json.loads(file.read_text()), list), file.name
        manifest['osquery_json_valid'] = True
        manifest['package_versions'] = output(compose + ['exec', '-T', 'host',
            'dpkg-query', '-W', 'openssh-server', 'libpam-modules', 'nftables', 'fail2ban', 'acl', 'aide', 'busybox-static'])
        # Exercise the README lifecycle: stop/start retains state; recreation resets it.
        for shell in shells.values():
            shell.close()
        shells.clear()
        run(compose + ['exec', '-T', 'host', 'touch', '/root/lifecycle-check'], check=True)
        run(compose + ['stop'], check=True, timeout=90)
        run(compose + ['start'], check=True, timeout=90)
        run(compose + ['up', '-d', '--wait', '--no-build'], check=True, timeout=90)
        run(compose + ['exec', '-T', 'host', 'bash', '-ec',
            'test -f /root/lifecycle-check; id alice; test -f /artifacts/setup-proof.txt'], check=True)
        manifest['stop_start_preserves_state'] = True
        run(compose + ['down', '--remove-orphans'], check=True, timeout=120)
        run(compose + ['up', '-d', '--wait', '--no-build'], check=True, timeout=180)
        run(compose + ['exec', '-T', 'host', 'bash', '-ec',
            'test ! -f /root/lifecycle-check; ! id alice; test -f /artifacts/setup-proof.txt'], check=True)
        replacement_key = output(compose + ['exec', '-T', 'host', 'cat', '/etc/ssh/ssh_host_ed25519_key.pub'])
        assert key.split()[:2] != replacement_key.split()[:2]
        manifest['recreation_resets_state_preserves_evidence_changes_host_key'] = True
        manifest['all_passed'] = True
        print(f'Passed {len(rows)}/{len(blocks)} guide blocks. Evidence: {out}', flush=True)
    finally:
        for shell in shells.values():
            shell.close()
        if not args.keep:
            run(compose + ['down', '--remove-orphans'], check=True, timeout=120)
        manifest['cleaned_up'] = not args.keep
        (out / 'results.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()

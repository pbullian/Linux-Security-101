#!/usr/bin/env python3
"""Execute exact TP code blocks in a fresh, disposable Compose project."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def interrupted(signum, frame):
    raise SystemExit(128 + signum)


def main():
    signal.signal(signal.SIGTERM, interrupted)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='cpe-guide-validation')
    parser.add_argument('--port', type=int, default=22223)
    parser.add_argument('--order', choices=['teaching', 'reference', 'legacy'], default='teaching')
    parser.add_argument('--extensions', action='store_true')
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
    manifest = {'order': order, 'extension_placement': ('after-all-core' if args.order == 'legacy' else 'after-section-7-before-8') if extension else None, 'guide_sha256': hashlib.sha256(guide.encode()).hexdigest(),
        'extensions_sha256': hashlib.sha256(extension.encode()).hexdigest() if extension else None,
        'architecture': output(['uname', '-m']), 'checks': rows}
    try:
        run(compose + ['up', '-d', '--wait', '--no-build'], check=True, timeout=180)
        container = output(compose + ['ps', '-q', 'host'])
        inspection = json.loads(output(['docker', 'inspect', container]))[0]
        bindings = inspection['NetworkSettings']['Ports']['22/tcp']
        assert all(b['HostIp'] == '127.0.0.1' for b in bindings), bindings
        manifest['images'] = {'host': inspection['Image']}
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
                run(compose + ['up', '-d', '--wait', '--no-build'], check=True, timeout=90)
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
        manifest['all_passed'] = True
        print(f'Passed {len(rows)}/{len(blocks)} guide blocks. Evidence: {out}', flush=True)
    finally:
        if not args.keep:
            run(compose + ['down', '--remove-orphans'], check=True, timeout=120)
        manifest['cleaned_up'] = not args.keep
        (out / 'results.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()

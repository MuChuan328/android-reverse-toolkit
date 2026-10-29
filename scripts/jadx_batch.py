#!/usr/bin/env python3
"""批量反编译 APK，输出 jadx 工程目录。

用法:
    python jadx_batch.py ./apks -o ./out [--deobf] [--threads 4]

依赖:
    jadx 在 PATH 中，或通过 --jadx 指定可执行文件。
"""
import argparse
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def decompile(jadx: str, apk: Path, out_dir: Path, deobf: bool) -> tuple[str, bool, str]:
    target = out_dir / apk.stem
    if target.exists():
        return apk.name, True, 'skipped(exists)'
    cmd = [jadx, '-d', str(target), '--no-res', '--show-bad-code']
    if deobf:
        cmd.append('--deobf')
    cmd.append(str(apk))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return apk.name, False, (proc.stderr or proc.stdout)[-300:].strip()
    return apk.name, True, 'ok'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('src', help='APK 所在目录')
    ap.add_argument('-o', '--out', default='./out', help='输出目录')
    ap.add_argument('--jadx', default='jadx', help='jadx 可执行文件')
    ap.add_argument('--deobf', action='store_true', help='开启反混淆')
    ap.add_argument('--threads', type=int, default=2)
    args = ap.parse_args()

    src, out = Path(args.src), Path(args.out)
    if not src.is_dir():
        print('源目录不存在:', src)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    apks = sorted([p for p in src.rglob('*') if p.suffix.lower() in ('.apk', '.apks', '.xapk')])
    if not apks:
        print('没有找到 APK')
        return 1

    if not shutil.which(args.jadx) and not Path(args.jadx).is_file():
        print('找不到 jadx:', args.jadx)
        return 2

    fails = 0
    with ThreadPoolExecutor(max_workers=max(1, args.threads)) as pool:
        for name, ok, note in pool.map(lambda p: decompile(args.jadx, p, out, args.deobf), apks):
            print(('OK  ' if ok else 'FAIL') + ' ' + name + '  ' + note)
            fails += 0 if ok else 1
    print('\n完成: %d 个, 失败 %d 个 -> %s' % (len(apks), fails, out))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())

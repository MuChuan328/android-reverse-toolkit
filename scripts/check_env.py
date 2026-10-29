#!/usr/bin/env python3
"""检查 Android/逆向常用工具是否就绪。

用法: python check_env.py
"""
import shutil
import subprocess
import sys

TOOLS = [
    ('jadx', ['jadx', '--version']),
    ('apktool', ['apktool', '--version']),
    ('adb', ['adb', 'version']),
    ('frida', ['frida', '--version']),
    ('python', ['python', '--version']),
    ('java', ['java', '-version']),
    ('openssl', ['openssl', 'version']),
    ('zipalign', ['zipalign', '-h']),
    ('apksigner', ['apksigner', '--version']),
]


def check(name, cmd):
    exe = shutil.which(cmd[0])
    if not exe:
        return name, False, 'not found'
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        text = (out.stdout or out.stderr).strip().splitlines()
        return name, True, text[0][:80] if text else 'ok'
    except Exception as e:
        return name, False, type(e).__name__


def main():
    ok = 0
    for name, cmd in TOOLS:
        n, good, note = check(name, cmd)
        print(('[OK]  ' if good else '[MISS]') + ' %-10s %s' % (n, note))
        ok += 1 if good else 0
    print('\n%d/%d 就绪' % (ok, len(TOOLS)))
    return 0 if ok >= 4 else 1


if __name__ == '__main__':
    sys.exit(main())

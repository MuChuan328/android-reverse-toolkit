# android-reverse-toolkit

Android 逆向日常使用的脚本与模板集合，偏工程化落地：批量反编译、重打包签名、Frida Hook 模板、脱壳检查清单。

> 仅用于**自己拥有或获得授权**的 App 安全研究、CTF 与兼容性分析。

## 目录

```
scripts/
  jadx_batch.py          # 批量反编译 APK/APKS/XAPK，输出 Java 源码
  apk_repack.py          # apktool 反编译 → 修改 smali → 重打包 → 签名
  frida_hook_template.js # 通用 Hook 模板（Java 层 / Native 导出函数）
  check_env.py           # 检查 jadx/apktool/frida/openssl 等工具是否就绪
docs/
  unpack-checklist.md    # 脱壳与加固识别检查清单
  protocol-notes.md      # 协议分析记录模板（抓包→定位→签名→复现）
```

## 快速开始

```bash
python scripts/check_env.py
python scripts/jadx_batch.py ./apks -o ./out
python scripts/apk_repack.py app.apk --smali-patch patch.diff --keystore my.keystore
```

## 工具依赖

- jadx（>= 1.5）
- apktool（>= 2.9）
- apksigner / zipalign（Android SDK build-tools）
- frida（>= 16）+ frida-server
- Python 3.10+

## 说明

- 脚本只做编排，不内置任何目标 App 的私有逻辑；
- 所有路径、包名、密钥均为占位符，使用时替换；
- 遇到加固/反调试，先看 `docs/unpack-checklist.md` 再决定是否上动态调试。

## License

MIT

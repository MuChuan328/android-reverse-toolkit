# 脱壳与加固识别检查清单

> 目标：先用 5 分钟判断「能不能直接静态分析」，再决定是否上动态调试/脱壳。

## 1. 快速判断是否加固

```bash
unzip -l target.apk | head -40
```

关注：

- [ ] `classes.dex` 数量异常（只有壳 dex，业务 dex 缺失）
- [ ] `lib/` 下出现 `libjiagu.so`、`libshell*.so`、`libDexHelper.so`、`libexec.so` 等
- [ ] `assets/` 下有加密的 `.dat/.bin` 大文件
- [ ] `AndroidManifest.xml` 的 `application` 指向壳类（如 `com.stub.StubApp`）

## 2. 常见壳特征

| 壳 | 特征 |
| --- | --- |
| 360 加固 | `libjiagu.so` / `libjiagu_art.so` |
| 梆梆 | `libsecexe.so` / `libDexHelper.so` |
| 腾讯乐固 | `libshell.so` / `libtosprotection` |
| 爱加密 | `libexec.so` / `ijiami` 字样 |
| 网易易盾 | `libnesec.so` |

## 3. 静态能做什么

- 资源、`AndroidManifest.xml`、`assets` 配置仍可直接读；
- 导出组件、权限、URL、第三方 SDK key 往往还在；
- 壳 dex 里可搜到壳的入口类与加载逻辑。

## 4. 动态方案（按成本从低到高）

1. **Frida spawn 后 dump dex**（frida-dexdump）；
2. **脱壳机/虚拟环境**（仅限自有测试设备）；
3. **unidbg 模拟执行 so**：确认目标函数是否纯 native、是否依赖 JNI 环境；
4. **定制 ROM / hook ClassLoader**：定位 `DexClassLoader` 加载点。

## 5. 反调试/反虚拟机排查

- [ ] `ptrace` 自附加（`TracerPid`）
- [ ] `/proc/self/maps` 中出现 `frida`、`xposed`、`magisk`
- [ ] 端口扫描（27042 等）
- [ ] `Debug.isDebuggerConnected()`
- [ ] 模拟器特征（`ro.kernel.qemu`、传感器数量）

## 6. 记录模板

```
目标: <包名> <版本>
加固: <壳类型 / 未加固>
入口: <Activity / Application>
关键类: <签名类 / 网络类>
结论: <可静态 / 需脱壳 / 需动态>
```

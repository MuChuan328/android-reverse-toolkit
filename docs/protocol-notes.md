# 协议分析记录模板（脱敏）

> 每个目标一份，避免把过程散落在聊天记录里。只记录方法，不记录真实账号/密钥。

## 目标

- 应用：`<package>` v`<version>`
- 入口：`<Activity>`
- 传输：HTTP / WebSocket / TCP（选填）

## 1. 抓包与定位

| 步骤 | 工具 | 结果 |
| --- | --- | --- |
| 代理抓包 | Charles / mitmproxy | 域名、路径、关键参数 |
| 反编译 | jadx | 对应的 Retrofit/OkHttp 接口类 |
| 交叉引用 | jadx xrefs | 参数来源、签名函数 |

## 2. 参数与签名

| 参数 | 来源 | 算法 | 备注 |
| --- | --- | --- | --- |
| `sign` | `SignHelper.sign()` | MD5(排序参数+盐) | 盐为常量 |
| `token` | 登录响应 | AES/CBC | key 硬编码在 so |

## 3. 复现

```python
# 最小复现脚本（脱敏）
def sign(params: dict, salt: str) -> str:
    raw = '&'.join(f'{k}={params[k]}' for k in sorted(params)) + salt
    return hashlib.md5(raw.encode()).hexdigest()
```

## 4. 结论

- 可复现接口：`<list>`
- 未解决：`<anti-bot / 设备指纹>`
- 风险：`<频率限制 / 验证码>`

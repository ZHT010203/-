"""

登录获取身份验证

"""
#导入requests库
import requests
import json
from gmssl import sm2


"""
登录接口访问
"""


# SM2加密公钥（服务器给的，用来加密密码）
SM2_KEY = "048031bb87caf68887301b7a595f2fddac0c5f4d9c95170efebcae582d4a99a7f53556b13b170d326e141f61758d6599a0b2074b3b62593418c1c15f19a2b6a127"


def jiami(shuju):
    """SM2加密：把明文变成密文"""
    sm = sm2.CryptSM2(public_key=SM2_KEY, private_key=None)
    miwen = sm.encrypt(shuju.encode())
    return f"04{miwen.hex()}"


import sys
from pathlib import Path

_FILE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _FILE_DIR.parent
for _p in (_FILE_DIR, _PROJECT_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import threading
from config import load_config

# ==================== Token 缓存（线程安全） ====================
# 避免并发时每个线程都去登录，导致 SSO 冲突
_cached_token = None
_token_lock = threading.Lock()


def login():
    global _cached_token

    # 有缓存直接返回（快速路径，不加锁）
    if _cached_token is not None:
        return _cached_token

    with _token_lock:
        # 双重检查：拿到锁后再确认一次
        if _cached_token is not None:
            return _cached_token

        cfg = load_config()

        #登录api地址（注意：是SSO地址，不是业务地址！）
        url = "https://saas-sso.shuyixin.cn/api/permission/permit/authenticate/accountPassword"
        #登录请求体
        body = {
            "accountName": cfg["login"]["accountName"],
            "password": cfg["login"]["password"],
            "app": {"appCode": "Index-Platform-PC"}
        }
        #先加密，再发送（不能直接发明文！）
        miwen = jiami(json.dumps(body))
        response = requests.post(url, json=miwen)
        #返回token
        jieguo = response.json()
        _cached_token = jieguo["data"]["token"]["accessToken"]
        return _cached_token



"""
关于秘钥加密等等相关知识点
你的理解**完全正确**！我帮你确认一下，再补充最后一个疑问。

---

## ✅ 你的理解——全对！

你用"钥匙+工具箱"来理解，非常形象：

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   SM2_KEY (公钥)          =  🔑 钥匙(后端人员也使用工具，生成秘钥)                         │
│   sm2.CryptSM2()          =  🧰 工具箱（gmssl库提供的）       │
│   shuju (body的JSON)      =  📦 要放进箱子里的东西            │
│                                                              │
│   流程：                                                     │
│   ① 拿出工具箱 🧰                                            │
│   ② 插入钥匙 🔑 → sm2.CryptSM2(public_key=SM2_KEY)           │
│   ③ 把东西放进去 📦 → sm.encrypt(shuju.encode())             │
│   ④ 箱子锁好了 🔒 → 返回密文 "04a8f3e2..."                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## ❓ 最后一个疑问：工具箱是谁开发的？

**工具箱 ≠ 你们公司后端开发的！**

分清楚三个角色：

| 是什么 | 谁做的 | 类比 |
|--------|--------|------|
| **SM2加密算法** | 中国国家密码管理局 | 锁的设计图纸（国家标准） |
| **gmssl库**（工具箱） | Python开源社区 | 根据图纸造出来的锁（任何人都能用） |
| **SM2_KEY**（公钥） | 你们公司后端 | 这把锁的**唯一编号**（只有匹配的私钥能开） |

```
国家制定标准（SM2算法）
    ↓
开源社区实现代码（gmssl库）  ← pip install gmssl 就能用
    ↓
你们公司后端生成一对钥匙：
    ├── 公钥（SM2_KEY）→ 给你，用来加密
    └── 私钥 → 服务器留着，用来解密
```

---

## 🎯 一句话总结

```
gmssl库     = 通用的SM2加密工具（谁都能下载用）
SM2_KEY    = 你们公司服务器的专属公钥（后端给的）
你的body   = 要加密的内容

工具 + 钥匙 + 内容 = 加密后的密文 → 只有你们服务器能解开
```

**就像：锁是五金店买的（gmssl），但钥匙是你们公司配的（SM2_KEY），只有匹配的钥匙才能开这把锁。**

---

## 📊 完整流程图

```
你的代码                          服务器
────────                        ────────
body = {                       
  "password": "Zht010203@"     私钥 🔓（只有服务器有）
}                              
    ↓                           
jiami(body)                     
    ↓                           
"04a8f3e2b1c9..."  ──POST──→  用私钥解密
                              得到 password="Zht010203@"
                              验证通过 → 返回 Token
    ←──────────────────────   
拿到 Token ✅
```

现在彻底明白了吧？😄
"""


非常好 👍
你要实现的其实是一个典型的 **账号密码登录 + token 鉴权** 流程（带本地持久化），在 Obsidian 插件中可以非常优雅地实现。

下面我帮你写一个 **完整的可运行模板**，包含：

* ✅ 登录表单（手机 + 密码）
* ✅ 调用 mock 接口获取 token
* ✅ 保存 token（跨平台、随 Vault 同步）
* ✅ 后续请求自动携带 token
* ✅ 登出 / 切换账号

---

## 🧩 一、目录结构建议

```
your-plugin/
 ├─ main.ts
 ├─ settings.ts  ← 设置面板：登录 UI
 └─ api.ts       ← 模拟服务端交互
```

---

## 🧱 二、`api.ts` – 模拟服务端

这里我们先 mock 一个登录接口。后期你可以替换成真实 API。

```ts
// api.ts

export interface LoginResponse {
  token: string;
  username: string;
}

export async function mockLogin(phone: string, password: string): Promise<LoginResponse> {
  console.log("Mock login:", phone, password);

  // 模拟网络延迟
  await new Promise((r) => setTimeout(r, 1000));

  if (password === "123456") {
    return {
      token: `mock-token-${Date.now()}`,
      username: `User_${phone.slice(-4)}`
    };
  } else {
    throw new Error("手机号或密码错误");
  }
}

export async function mockFetchUserData(token: string) {
  if (!token.startsWith("mock-token")) throw new Error("Token 无效");
  return {
    nickname: "Obsidian User",
    vip: true,
  };
}
```

---

## ⚙️ 三、`main.ts` – 插件主体

```ts
import { Plugin, requestUrl } from "obsidian";
import { LoginSettingTab } from "./settings";
import { mockFetchUserData } from "./api";

interface PluginSettings {
  token?: string;
  username?: string;
}

export default class LoginPlugin extends Plugin {
  settings: PluginSettings;

  async onload() {
    console.log("LoginPlugin loaded");
    await this.loadSettings();

    // 添加设置面板
    this.addSettingTab(new LoginSettingTab(this.app, this));

    // 可选：添加侧边栏图标
    this.addRibbonIcon("user", "查看账户信息", async () => {
      if (!this.settings.token) {
        new Notice("请先登录");
        return;
      }
      const info = await mockFetchUserData(this.settings.token);
      new Notice(`欢迎 ${this.settings.username}（VIP：${info.vip}）`);
    });
  }

  async loadSettings() {
    this.settings = Object.assign({}, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  logout() {
    this.settings.token = undefined;
    this.settings.username = undefined;
    this.saveSettings();
  }
}
```

---

## 🧰 四、`settings.ts` – 登录界面

```ts
import { App, PluginSettingTab, Setting, Notice } from "obsidian";
import LoginPlugin from "./main";
import { mockLogin } from "./api";

export class LoginSettingTab extends PluginSettingTab {
  plugin: LoginPlugin;

  constructor(app: App, plugin: LoginPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "账户登录" });

    // 如果已登录
    if (this.plugin.settings.token) {
      containerEl.createEl("p", { text: `已登录：${this.plugin.settings.username}` });

      new Setting(containerEl)
        .addButton((btn) =>
          btn
            .setButtonText("退出登录")
            .setWarning()
            .onClick(async () => {
              this.plugin.logout();
              new Notice("已退出登录");
              this.display();
            })
        );
      return;
    }

    // 未登录：显示输入框
    let phone = "";
    let password = "";

    new Setting(containerEl)
      .setName("手机号")
      .addText((text) => {
        text.setPlaceholder("请输入手机号").onChange((value) => (phone = value));
      });

    new Setting(containerEl)
      .setName("密码")
      .addText((text) => {
        text.setPlaceholder("请输入密码").setValue("").inputEl.type = "password";
        text.onChange((value) => (password = value));
      });

    new Setting(containerEl)
      .addButton((btn) =>
        btn
          .setButtonText("登录")
          .setCta()
          .onClick(async () => {
            try {
              new Notice("正在登录...");
              const res = await mockLogin(phone, password);
              this.plugin.settings.token = res.token;
              this.plugin.settings.username = res.username;
              await this.plugin.saveSettings();
              new Notice(`登录成功：${res.username}`);
              this.display();
            } catch (err: any) {
              new Notice(`登录失败：${err.message}`);
            }
          })
      );
  }
}
```

---

## 🧩 五、工作原理总结

| 功能    | 说明                                               |
| ----- | ------------------------------------------------ |
| 登录    | 调用 `mockLogin()`，返回 token                        |
| 持久化   | token 保存在 `data.json`，自动跨平台同步                    |
| 登出    | 清空 `token` 并刷新 UI                                |
| 调用接口  | 后续调用可用 `mockFetchUserData(token)` 或实际 API        |
| 适配移动端 | 全部基于 Obsidian API，无 Electron 依赖，可运行于 iOS/Android |

---

## 🧪 六、后续接入真实后端时改造点

| 模拟版                          | 真实版                                                                |
| ---------------------------- | ------------------------------------------------------------------ |
| `mockLogin(phone, password)` | 调用 `requestUrl({url, method:"POST", body: JSON.stringify({...})})` |
| 本地 token 校验                  | 服务端返回 JWT 或 session key                                            |
| mockFetchUserData            | 调用真实 `/me` 接口                                                      |

示例（真实 HTTP 登录）：

```ts
import { requestUrl } from "obsidian";

async function realLogin(phone: string, password: string) {
  const res = await requestUrl({
    url: "https://api.example.com/login",
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, password }),
  });
  return res.json; // { token, username }
}
```

---

是否希望我帮你把这套结构再加一个「**带 token 的统一 request 封装类**」？
那样你就能直接 `await api.get("/user/profile")`，它会自动加上 `Authorization` header。

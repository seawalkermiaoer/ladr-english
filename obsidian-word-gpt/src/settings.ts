import { App, PluginSettingTab, Setting, Notice } from "obsidian";
import MyPlugin from "./main";
import { setBaseUrl, setToken, verify } from "./api";

export class LoginSettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "账户设置（Token 通讯）" });

    // If already logged in
    if (this.plugin.settings.token) {
      containerEl.createEl("p", { text: `已登录（Token 已设置）` });
      
      // Display user level if available
      if (this.plugin.settings.level) {
        const levelText = this.plugin.settings.level === 'free' ? '免费版' : 
                         this.plugin.settings.level === 'plus' ? 'Plus版' : '专业版';
        containerEl.createEl("p", { text: `用户等级：${levelText}` });
      }

      new Setting(containerEl)
        .setName("服务器地址")
        .setDesc("例如 http://127.0.0.1:8000")
        .addText((text) => {
          text
            .setPlaceholder("http://127.0.0.1:8000")
            .setValue(this.plugin.settings.serverUrl || "")
            .onChange((value) => (this.plugin.settings.serverUrl = value));
        });

      new Setting(containerEl)
        .setName("Token")
        .addText((text) => {
          text
            .setPlaceholder("请输入 Token")
            .setValue(this.plugin.settings.token || "")
            .onChange((value) => (this.plugin.settings.token = value));
        });

      new Setting(containerEl)
        .addButton((btn) =>
          btn
            .setButtonText("保存并校验")
            .setCta()
            .onClick(async () => {
              try {
                await this.plugin.saveSettings();
                setBaseUrl(this.plugin.settings.serverUrl || "");
                setToken(this.plugin.settings.token || "");
                const res = await verify();
                new Notice(`验证成功：${res.token}`);
              } catch (err: any) {
                new Notice(`校验失败：${err.message}`);
              }
            })
        );

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

    // 未登录：提供服务器地址与 Token 录入
    let serverUrl = this.plugin.settings.serverUrl || "http://127.0.0.1:8000";
    let token = "";

    new Setting(containerEl)
      .setName("服务器地址")
      .setDesc("例如 http://127.0.0.1:8000")
      .addText((text) => {
        text.setPlaceholder("http://127.0.0.1:8000").setValue(serverUrl).onChange((value) => (serverUrl = value));
      });

    new Setting(containerEl)
      .setName("Token")
      .addText((text) => {
        text.setPlaceholder("请输入 Token").onChange((value) => (token = value));
      });

    new Setting(containerEl)
      .addButton((btn) =>
        btn
          .setButtonText("保存并校验")
          .setCta()
          .onClick(async () => {
            try {
              this.plugin.settings.serverUrl = serverUrl;
              this.plugin.settings.token = token;
              await this.plugin.saveSettings();
              setBaseUrl(serverUrl);
              setToken(token);
              const res = await verify();
              new Notice(`验证成功：${res.token}`);
              this.display();
            } catch (err: any) {
              new Notice(`校验失败：${err.message}`);
            }
          })
      );
  }
}

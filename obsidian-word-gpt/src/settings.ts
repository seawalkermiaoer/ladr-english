import { App, PluginSettingTab, Setting, Notice } from "obsidian";
import MyPlugin from "./main";
import { mockLogin } from "./api";

export class LoginSettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl("h2", { text: "账户登录" });

    // If already logged in
    if (this.plugin.settings.token) {
      containerEl.createEl("p", { text: `已登录：${this.plugin.settings.username}` });
      
      // Display user level if available
      if (this.plugin.settings.level) {
        const levelText = this.plugin.settings.level === 'free' ? '免费版' : 
                         this.plugin.settings.level === 'plus' ? 'Plus版' : '专业版';
        containerEl.createEl("p", { text: `用户等级：${levelText}` });
      }

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

    // Not logged in: show input fields
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
              this.plugin.settings.level = res.level;
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
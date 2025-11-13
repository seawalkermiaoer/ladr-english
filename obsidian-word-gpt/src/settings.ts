import { App, PluginSettingTab, Setting, Notice } from "obsidian";
import MyPlugin from "./main";
import { setToken, getUserInfo, UserInfo } from "./api";

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
      
      // Display user level and last update time if available
      if (this.plugin.settings.userInfo) {
        const levelText = this.plugin.settings.userInfo.current_level === 'free' ? '免费版' : 
                         this.plugin.settings.userInfo.current_level === 'plus' ? 'Plus版' : '专业版';
        containerEl.createEl("p", { text: `用户等级：${levelText}` });
        
        // Format the last update time for better readability
        const updatedAt = new Date(this.plugin.settings.userInfo.updated_at);
        containerEl.createEl("p", { text: `最后更新：${updatedAt.toLocaleString()}` });
      }

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
            .setButtonText("保存并获取用户信息")
            .setCta()
            .onClick(async () => {
              try {
                await this.plugin.saveSettings();
                // Check if token is provided
                if (!this.plugin.settings.token || this.plugin.settings.token.trim() === "") {
                  new Notice("请输入有效的 Token");
                  return;
                }
                setToken(this.plugin.settings.token || "");
                const userInfo: UserInfo = await getUserInfo();
                // Store the full user info response
                this.plugin.settings.userInfo = userInfo;
                await this.plugin.saveSettings();
                new Notice(`用户信息获取成功`);
                this.display();
              } catch (err: any) {
                new Notice(`获取用户信息失败：${err.message}`);
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

    // 未登录：提供 Token 录入
    let token = "";

    new Setting(containerEl)
      .setName("Token")
      .addText((text) => {
        text.setPlaceholder("请输入 Token").onChange((value) => (token = value));
      });

    new Setting(containerEl)
      .addButton((btn) =>
        btn
          .setButtonText("保存并获取用户信息")
          .setCta()
          .onClick(async () => {
            try {
              // Check if token is provided
              if (!token || token.trim() === "") {
                new Notice("请输入有效的 Token");
                return;
              }
              this.plugin.settings.token = token;
              await this.plugin.saveSettings();
              setToken(token);
              const userInfo: UserInfo = await getUserInfo();
              // Store the full user info response
              this.plugin.settings.userInfo = userInfo;
              await this.plugin.saveSettings();
              new Notice(`用户信息获取成功`);
              this.display();
            } catch (err: any) {
              new Notice(`获取用户信息失败：${err.message}`);
            }
          })
      );
  }
}
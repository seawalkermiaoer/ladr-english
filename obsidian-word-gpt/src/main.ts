import { App, Editor, MarkdownView, Menu, Modal, Notice, Plugin, PluginSettingTab, Setting, WorkspaceLeaf } from 'obsidian';
import { ExampleView, VIEW_TYPE_WORDGPT } from './views/word_gpt_vewi';
import { LoginSettingTab } from './settings';

// Remember to rename these classes and interfaces!
interface MyPluginSettings {
	mySetting: string;
	token?: string;
	username?: string;
	level?: 'free' | 'plus' | 'pro';
  serverUrl?: string;
}

const DEFAULT_SETTINGS: MyPluginSettings = {
	mySetting: 'default',
  serverUrl: 'http://127.0.0.1:8000'
}

export default class MyPlugin extends Plugin {
	settings: MyPluginSettings;

	async onload() {
		await this.loadSettings();

		// Register the view
    this.registerView(
      VIEW_TYPE_WORDGPT,
      (leaf) => new ExampleView(leaf, this)
    );

		// This adds a simple command that can be triggered anywhere
		this.addCommand({
			id: 'open-sample-modal-simple',
			name: 'Open sample modal (simple)',
			callback: () => {
				new SampleModal(this.app).open();
			}
		});
		// This adds an editor command that can perform some operation on the current editor instance
		this.addCommand({
			id: 'sample-editor-command',
			name: 'Sample editor command',
			editorCallback: (editor: Editor, _view: MarkdownView) => {
				console.log(editor.getSelection());
				// editor.replaceSelection('Sample Editor Command');
			}
		});
		// This adds a complex command that can check whether the current state of the app allows execution of the command
		this.addCommand({
			id: 'open-sample-modal-complex',
			name: 'Open sample modal (complex)',
			checkCallback: (checking: boolean) => {
				// Conditions to check
				const markdownView = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (markdownView) {
					// If checking is true, we're simply "checking" if the command can be run.
					// If checking is false, then we want to actually perform the operation.
					if (!checking) {
						new SampleModal(this.app).open();
					}

					// This command will only show up in Command Palette when the check function returns true
					return true;
				}
			}
		});
		
		// Add command to open the sample view in the right sidebar
		this.addCommand({
			id: 'open-sample-view',
			name: 'Open sample view',
			callback: () => {
				this.activateView();
			}
		});

		// This adds a settings tab so the user can configure various aspects of the plugin
		this.addSettingTab(new LoginSettingTab(this.app, this));

		// When registering intervals, this function will automatically clear the interval when the plugin is disabled.
		this.registerInterval(window.setInterval(() => console.log('setInterval'), 5 * 60 * 1000));
		
		// Open the sample view by default when the plugin loads
		this.activateView();
	}

	onunload() {
		// Clean up the view when the plugin is unloaded
		this.app.workspace.detachLeavesOfType(VIEW_TYPE_WORDGPT);
	}

	async loadSettings() {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}
	
	logout() {
		this.settings.token = undefined;
		this.settings.username = undefined;
		this.settings.level = undefined;
		this.saveSettings();
	}
	
	// Function to activate (open) the view in the right sidebar
	async activateView() {
		const { workspace } = this.app;

		let leaf: WorkspaceLeaf | null = null;
    const leaves = workspace.getLeavesOfType(VIEW_TYPE_WORDGPT);

		if (leaves.length > 0) {
			leaf = leaves[0];
		} else {
			// Our view could not be found in the workspace, create a new leaf
			// in the right sidebar for it
			leaf = workspace.getRightLeaf(false);
			if (leaf) {
        await leaf.setViewState({ type: VIEW_TYPE_WORDGPT, active: true });
			}
		}

		// "Reveal" the leaf in case it is in a collapsed sidebar
		if (leaf) {
			workspace.revealLeaf(leaf);
		}
  	}
}

class SampleModal extends Modal {
	constructor(app: App) {
		super(app);
	}

	onOpen() {
		const {contentEl} = this;
		contentEl.setText('Woah!');
	}

	onClose() {
		const {contentEl} = this;
		contentEl.empty();
	}
}

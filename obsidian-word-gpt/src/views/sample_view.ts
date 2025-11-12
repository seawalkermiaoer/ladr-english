import { ItemView, WorkspaceLeaf, MarkdownView, TFile, Editor, Menu, Notice } from 'obsidian';
import FileInfo from './components/FileInfo.svelte';
import MyPlugin from '../main';

export const VIEW_TYPE_EXAMPLE = 'example-view';

interface FileInfoData {
  fileName: string;
  filePath: string;
  status: string;
  wordCount: number;
  previewContent: string;
  error: string;
  selectedWords: string[];
  vocabularyWords: string[];
  userLevel: string;
}

export class ExampleView extends ItemView {
  private lastActiveFilePath: string | null = null;
  private fileInfoComponent: FileInfo | null = null;
  private currentFileInfo: FileInfoData = {
    fileName: '',
    filePath: '',
    status: '',
    wordCount: 0,
    previewContent: '',
    error: '',
    selectedWords: [],
    vocabularyWords: [],
    userLevel: ''
  };
  private selectedWords: Set<string> = new Set();
  private vocabularyWords: Set<string> = new Set();
  private audioElement: HTMLAudioElement | null = null;
  private plugin: MyPlugin;
  
  constructor(leaf: WorkspaceLeaf, plugin: MyPlugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType() {
    return VIEW_TYPE_EXAMPLE;
  }

  getDisplayText() {
    return 'Last Active File';
  }

  async onOpen() {
    const container = this.contentEl;
    container.empty();
    
    // Create the Svelte component
    this.fileInfoComponent = new FileInfo({
      target: container,
      props: this.currentFileInfo
    });
    
    // Add event listeners for dictionary lookup and audio playback
    window.addEventListener('lookupWord', this.handleLookupWord.bind(this));
    window.addEventListener('playAudio', this.handlePlayAudio.bind(this));
    
    // Register event listener for active leaf change
    this.registerEvent(
      this.app.workspace.on('active-leaf-change', () => {
        // Update last active file path when active leaf changes
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (activeView && activeView.file) {
          this.lastActiveFilePath = activeView.file.path;
        }
        // Update the view
        this.updateLastActiveFileInfo();
      })
    );
    
    // Register event listener for editor changes
    this.registerEvent(
      this.app.workspace.on('editor-change', (editor: Editor) => {
        this.handleSelectionChange(editor);
      })
    );
    
    // Register editor menu event to add "Add Vocabulary" option
    this.registerEvent(
      this.app.workspace.on('editor-menu', (menu: Menu, editor: Editor) => {
        const selection = editor.getSelection();
        if (selection && selection.trim() !== '') {
          menu.addItem((item) => {
            item
              .setTitle('Add to Vocabulary')
              .setIcon('book-plus')
              .onClick(() => {
                // Add the selected text to vocabulary
                this.addVocabularyWord(selection.trim());
              });
          });
        }
      })
    );
    
    // Initial update
    this.updateLastActiveFileInfo();
  }

  async onClose() {
    if (this.fileInfoComponent) {
      this.fileInfoComponent.$destroy();
      this.fileInfoComponent = null;
    }
    
    // Clean up event listeners
    window.removeEventListener('lookupWord', this.handleLookupWord.bind(this));
    window.removeEventListener('playAudio', this.handlePlayAudio.bind(this));
    
    // Clean up audio element
    if (this.audioElement) {
      this.audioElement.pause();
      this.audioElement = null;
    }
  }
  
  private handleLookupWord(event: CustomEvent) {
    const word = event.detail.word;
    this.lookupWordInDictionary(word);
  }
  
  private handlePlayAudio(event: CustomEvent) {
    const audioUrl = event.detail.audioUrl;
    this.playAudio(audioUrl);
  }
  
  private async lookupWordInDictionary(word: string) {
    try {
      new Notice(`Looking up "${word}" in dictionary...`);
      
      // Make API request to dictionary API
      const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
      
      if (!response.ok) {
        new Notice(`Failed to lookup "${word}". Word not found in dictionary.`);
        return;
      }
      
      const data = await response.json();
      
      // Check if we have pronunciation audio
      if (data && data[0] && data[0].phonetics && data[0].phonetics.length > 0) {
        // Find the first phonetic with audio
        const phoneticWithAudio = data[0].phonetics.find((phonetic: any) => phonetic.audio && phonetic.audio !== "");
        
        if (phoneticWithAudio) {
          new Notice(`Playing pronunciation for "${word}"`);
          this.playAudio(phoneticWithAudio.audio);
        } else {
          new Notice(`Found definition for "${word}" but no audio available.`);
        }
      } else {
        new Notice(`Found definition for "${word}" but no pronunciation audio available.`);
      }
    } catch (error) {
      console.error('Error looking up word:', error);
      new Notice(`Error looking up "${word}". Please try again.`);
    }
  }
  
  private playAudio(audioUrl: string) {
    try {
      // If we already have an audio element, pause it
      if (this.audioElement) {
        this.audioElement.pause();
      }
      
      // Create a new audio element
      this.audioElement = new Audio(audioUrl);
      
      // Play the audio
      this.audioElement.play().catch(error => {
        console.error('Error playing audio:', error);
        new Notice('Error playing audio pronunciation.');
      });
      
      // Clean up after playback
      this.audioElement.onended = () => {
        this.audioElement = null;
      };
    } catch (error) {
      console.error('Error creating audio element:', error);
      new Notice('Error playing audio pronunciation.');
    }
  }
  
  private handleSelectionChange(editor: Editor) {
    const selection = editor.getSelection();
    if (selection && selection.trim() !== '') {
      // Add non-empty selections to our set of selected words
      const words = selection.trim().split(/\s+/);
      for (const word of words) {
        if (word.length > 0) {
          this.selectedWords.add(word);
        }
      }
      
      // Update the view with selected words
      this.updateViewWithSelectedWords();
    }
  }
  
  private updateViewWithSelectedWords() {
    // Convert Set to array and limit to last 10 words for display
    const wordsArray = Array.from(this.selectedWords);
    const recentWords = wordsArray.slice(-10);
    
    // Get user level text
    let userLevelText = '';
    if (this.plugin.settings.level) {
      userLevelText = this.plugin.settings.level === 'free' ? '免费版' : 
                     this.plugin.settings.level === 'plus' ? 'Plus版' : '专业版';
    }
    
    // Update the current file info with selected words and vocabulary words
    this.currentFileInfo = {
      ...this.currentFileInfo,
      selectedWords: recentWords,
      vocabularyWords: Array.from(this.vocabularyWords),
      userLevel: userLevelText
    };
    
    // Update the Svelte component
    if (this.fileInfoComponent) {
      this.fileInfoComponent.$set(this.currentFileInfo);
    }
  }
  
  private async updateLastActiveFileInfo() {
    try {
      // If we don't have a last active file path, try to get the current active one
      if (!this.lastActiveFilePath) {
        const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
        if (activeView && activeView.file) {
          this.lastActiveFilePath = activeView.file.path;
        }
      }
      
      // Reset error state
      this.currentFileInfo.error = '';
      
      // Get user level text
      let userLevelText = '';
      if (this.plugin.settings.level) {
        userLevelText = this.plugin.settings.level === 'free' ? '免费版' : 
                       this.plugin.settings.level === 'plus' ? 'Plus版' : '专业版';
      }
      
      // If we have a last active file path, check if it's still open in the editor
      if (this.lastActiveFilePath) {
        // Check if the file is still open in any leaf
        const leaves = this.app.workspace.getLeavesOfType('markdown');
        let isOpen = false;
        let openFile: TFile | null = null;
        
        for (const leaf of leaves) {
          if (leaf.view instanceof MarkdownView && leaf.view.file) {
            if (leaf.view.file.path === this.lastActiveFilePath) {
              isOpen = true;
              openFile = leaf.view.file;
              break;
            }
          }
        }
        
        if (isOpen && openFile) {
          // File is still open, display its content
          try {
            const fileContent = await this.app.vault.read(openFile);
            const fileName = openFile.name;
            const filePath = openFile.path;
            const wordCount = fileContent.split(/\s+/).filter(word => word.length > 0).length;
            
            // Update the file info data
            this.currentFileInfo = {
              fileName,
              filePath,
              status: 'Open in editor',
              wordCount,
              previewContent: fileContent.substring(0, 300) + (fileContent.length > 300 ? '...' : ''),
              error: '',
              selectedWords: Array.from(this.selectedWords).slice(-10),
              vocabularyWords: Array.from(this.vocabularyWords),
              userLevel: userLevelText
            };
          } catch (error) {
            // Handle error in reading file
            this.currentFileInfo = {
              fileName: '',
              filePath: '',
              status: '',
              wordCount: 0,
              previewContent: '',
              error: `Error reading file: ${this.lastActiveFilePath}`,
              selectedWords: Array.from(this.selectedWords).slice(-10),
              vocabularyWords: Array.from(this.vocabularyWords),
              userLevel: userLevelText
            };
          }
        } else {
          // File is no longer open
          this.currentFileInfo = {
            fileName: this.lastActiveFilePath.split('/').pop() || this.lastActiveFilePath,
            filePath: this.lastActiveFilePath,
            status: 'Not open in editor',
            wordCount: 0,
            previewContent: '',
            error: '',
            selectedWords: Array.from(this.selectedWords).slice(-10),
            vocabularyWords: Array.from(this.vocabularyWords),
            userLevel: userLevelText
          };
        }
      } else {
        // No last active file tracked
        this.currentFileInfo = {
          fileName: '',
          filePath: '',
          status: '',
          wordCount: 0,
          previewContent: '',
          error: '',
          selectedWords: Array.from(this.selectedWords).slice(-10),
          vocabularyWords: Array.from(this.vocabularyWords),
          userLevel: userLevelText
        };
      }
      
      // Update the Svelte component
      if (this.fileInfoComponent) {
        this.fileInfoComponent.$set(this.currentFileInfo);
      }
    } catch (error) {
      console.error('Error updating file info:', error);
      
      // Get user level text for error case
      let userLevelText = '';
      if (this.plugin.settings.level) {
        userLevelText = this.plugin.settings.level === 'free' ? '免费版' : 
                       this.plugin.settings.level === 'plus' ? 'Plus版' : '专业版';
      }
      
      this.currentFileInfo = {
        fileName: '',
        filePath: '',
        status: '',
        wordCount: 0,
        previewContent: '',
        error: 'An unexpected error occurred',
        selectedWords: Array.from(this.selectedWords).slice(-10),
        vocabularyWords: Array.from(this.vocabularyWords),
        userLevel: userLevelText
      };
      
      if (this.fileInfoComponent) {
        this.fileInfoComponent.$set(this.currentFileInfo);
      }
    }
  }
  
  // Function to add a vocabulary word
  private addVocabularyWord(word: string) {
    // Add the word to our vocabulary set
    this.vocabularyWords.add(word);
    
    // Update the view to show the new vocabulary word
    this.updateViewWithSelectedWords();
    
    // For now, just show a notice
    new Notice(`Added "${word}" to vocabulary!`);
    
    // TODO: Implement actual vocabulary storage and management
    // This could save to a file, database, or send to an API
  }
}
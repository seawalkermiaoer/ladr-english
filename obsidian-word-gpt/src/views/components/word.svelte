<script lang="ts">
  export let fileName: string = '';
  export let filePath: string = '';
  export let status: string = '';
  export let wordCount: number = 0;
  export let previewContent: string = '';
  export let error: string = '';
  export let selectedWords: string[] = [];
  export let vocabularyWords: string[] = [];
  export let userLevel: string = '';
  function lookupWord(word: string) {
    const event = new CustomEvent('lookupWord', { detail: { word } });
    window.dispatchEvent(event);
  }
  function playAudio(audioUrl: string) {
    const event = new CustomEvent('playAudio', { detail: { audioUrl } });
    window.dispatchEvent(event);
  }
</script>

<div class="file-info-container">
  <h4>Last Active File</h4>
  {#if userLevel}
    <p class="user-level"><strong>User Level:</strong> {userLevel}</p>
  {/if}
  {#if error}
    <p class="error">{error}</p>
  {:else if fileName}
    <div class="file-details">
      <p><strong>File:</strong> {fileName}</p>
      <p><strong>Path:</strong> {filePath}</p>
      <p><strong>Status:</strong> {status}</p>
      <p><strong>Words:</strong> {wordCount}</p>
      {#if selectedWords.length > 0}
        <h5>Selected Words:</h5>
        <div class="selected-words">
          {#each selectedWords as word}
            <span class="word-tag">{word}</span>
          {/each}
        </div>
      {/if}
      {#if vocabularyWords.length > 0}
        <h5>Vocabulary Words:</h5>
        <div class="vocabulary-words">
          {#each vocabularyWords as word}
            <div class="vocabulary-word-line">
              <span class="word-text">{word}</span>
              <button class="lookup-button" on:click={() => lookupWord(word)}>Lookup</button>
            </div>
          {/each}
        </div>
      {/if}
      <h5>Preview:</h5>
      <pre class="preview-content">{previewContent}</pre>
    </div>
  {:else}
    <p>No file activity tracked yet</p>
  {/if}
</div>

<style>
  .file-info-container { padding: 10px; font-family: var(--font-family); }
  .file-info-container h4 { margin-bottom: 10px; }
  .user-level { background-color: var(--interactive-accent); color: var(--text-on-accent); padding: 4px 8px; border-radius: 4px; margin-bottom: 10px; display: inline-block; }
  .file-details p { margin: 5px 0; }
  .selected-words { margin: 10px 0; display: flex; flex-wrap: wrap; gap: 5px; }
  .word-tag { background-color: var(--interactive-accent); color: var(--text-on-accent); padding: 2px 8px; border-radius: 12px; font-size: 0.85em; }
  .vocabulary-words { margin: 10px 0; border: 1px solid var(--background-modifier-border); border-radius: 4px; max-height: 200px; overflow-y: auto; }
  .vocabulary-word-line { display: flex; justify-content: space-between; align-items: center; padding: 4px 8px; border-bottom: 1px solid var(--background-modifier-border); }
  .vocabulary-word-line:last-child { border-bottom: none; }
  .word-text { flex-grow: 1; }
  .lookup-button { background-color: var(--interactive-accent); color: var(--text-on-accent); border: none; border-radius: 4px; padding: 2px 6px; font-size: 0.8em; cursor: pointer; }
  .lookup-button:hover { opacity: 0.8; }
  .preview-content { background-color: #f0f0f0; padding: 10px; border-radius: 4px; font-size: 0.9em; max-height: 200px; overflow: auto; white-space: pre-wrap; }
  .error { color: var(--text-error); }
</style>

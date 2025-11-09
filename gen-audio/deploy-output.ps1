# PowerShell script to deploy the Obsidian Audio Player Plus plugin files
# Copies main.js, manifest.json, and styles.css to the Obsidian plugin directory

# Define source and destination paths
$sourceDir = "E:\best\gen-audio\res"
$destDir = "E:\des_glaneuses\DesGlaneuses\temp"


# Files to copy
$filesToCopy = @("x1.mp3", "x1.md")

# Copy each file to the destination directory
foreach ($file in $filesToCopy) {
    $sourcePath = Join-Path $sourceDir $file
    $destPath = Join-Path $destDir $file
    
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Output "Copied $file to $destDir"
    } else {
        Write-Error "Source file not found: $sourcePath"
    }
}

Write-Output "Plugin deployment completed!"
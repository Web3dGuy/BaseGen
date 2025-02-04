# Codebase: frontend

## Directory Tree

```
frontend >
    .vscode >
        extensions.json
    index.html
    jsconfig.json
    package.json
    src >
        App.svelte
        app.css
        components >
            Chat.svelte
            FlappyBird.svelte
            Logs.svelte
        lib >
            Counter.svelte
        main.js
        stores >
            activityLogs.js
            chatStore.js
            fileTypeFilters.js
            highscores.js
            networkScores.js
        utils >
            messageParser.js
        vite-env.d.ts
    svelte.config.js
    vite.config.js
```

## Files

### frontend\.vscode\extensions.json

```json
{
  "recommendations": ["svelte.svelte-vscode"]
}

```

### frontend\index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>W3D FTP</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>

```

### frontend\jsconfig.json

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "target": "ESNext",
    "module": "ESNext",
    /**
     * svelte-preprocess cannot figure out whether you have
     * a value or a type, so tell TypeScript to enforce using
     * `import type` instead of `import` for Types.
     */
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    /**
     * To have warnings / errors of the Svelte compiler at the
     * correct position, enable source maps by default.
     */
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    /**
     * Typecheck JS in `.svelte` and `.js` files by default.
     * Disable this if you'd like to use dynamic types.
     */
    "checkJs": false
  },
  /**
   * Use global.d.ts instead of compilerOptions.types
   * to avoid limiting type declarations.
   */
  "include": ["src/**/*.d.ts", "src/**/*.js", "src/**/*.svelte"]
}

```

### frontend\package.json

```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/vite-plugin-svelte": "^5.0.3",
    "svelte": "^5.15.0",
    "vite": "^6.0.5"
  },
  "dependencies": {
    "@tailwindcss/vite": "^4.0.0",
    "p5": "^1.11.3",
    "tailwindcss": "^4.0.0"
  }
}

```

### frontend\src\app.css

```css
/* Import Tailwind's base styles, components, and utilities */
@import "tailwindcss";

/* Root variables and themes */
:root {
  --bg-dark: #0b0d0f;
  --text-dark: #f0f0f0;
  --primary-blue: #3b82f6;
  --primary-hover: #2563eb;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* Base styles */
html {
  font-size: 16px;
  height: -webkit-fill-available;
}

body {
  margin: 0;
  min-height: 100vh;
  min-height: -webkit-fill-available;
  background-color: var(--bg-dark);
  color: var(--text-dark);
  font-family: inherit;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

/* Mobile-first typography */
h1, h2, h3, h4, h5, h6 {
  line-height: 1.2;
}

/* Links */
a {
  color: var(--primary-blue);
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--primary-hover);
}

/* Buttons */
button {
  font-family: inherit;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* Form elements */
input,
select,
textarea {
  font-family: inherit;
  font-size: 16px; /* Prevents zoom on iOS */
  border-radius: 0.375rem;
  appearance: none;
  -webkit-appearance: none;
}

/* Select elements */
select {
  background-color: #1a1a1a;
  color: #fff;
  border: 1px solid #444;
  padding: 0.5rem 2rem 0.5rem 1rem;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
}

select:focus {
  outline: 2px solid var(--primary-blue);
  outline-offset: 2px;
}

/* Mobile optimizations */
@media (max-width: 640px) {
  /* Adjust text sizes for better readability on mobile */
  html {
    font-size: 14px;
  }

  /* Increase touch targets for better mobile interaction */
  button,
  input,
  select {
    min-height: 44px; /* Apple's recommended minimum touch target size */
    padding: 0.5rem 1rem;
  }

  /* Improve spacing for mobile */
  .p-4 {
    padding: 0.75rem !important;
  }

  /* Ensure modals are easily readable on mobile */
  .modal-content {
    width: 95% !important;
    max-height: 90vh !important;
    margin: auto;
  }

  /* Optimize tables for mobile */
  table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  /* Improve form elements on mobile */
  input[type="file"] {
    font-size: 16px !important; /* Prevents zoom on iOS */
  }

  /* Better scrolling experience */
  .overflow-auto {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
  }

  /* Optimize grid layouts for mobile */
  .grid {
    gap: 0.75rem !important;
  }
}

/* Tablet optimizations */
@media (min-width: 641px) and (max-width: 1024px) {
  /* Adjust grid for tablets */
  .grid {
    gap: 1rem !important;
  }

  /* Optimize navigation for tablets */
  .nav-items {
    padding: 0.5rem !important;
  }
}

/* Handle safe areas for modern mobile browsers */
@supports (padding: max(0px)) {
  body {
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
    padding-bottom: env(safe-area-inset-bottom);
  }
}

/* Dark mode optimizations */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-dark: #000000;
    --text-dark: #ffffff;
  }

  /* Improve contrast in dark mode */
  input,
  select,
  textarea {
    background-color: #1a1a1a !important;
    border-color: #333333 !important;
  }
}

/* Reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Print styles */
@media print {
  body {
    background: white;
    color: black;
  }

  .no-print {
    display: none !important;
  }
}
  /*
```

### frontend\src\App.svelte

```svelte
<script>
  import FlappyBird from "./components/FlappyBird.svelte";
  import { highScores } from "./stores/highscores.js";
  import { networkScores } from "./stores/networkScores.js";
  import Chat from "./components/Chat.svelte";
  import {
    getFilterForFolder,
    isFileAllowed,
    getAcceptString,
    getFolderDescription,
  } from "./stores/fileTypeFilters";
  import Logs from "./components/Logs.svelte";

  // Configuration
  const host = "dia.whatbox.ca";
  const port = 25850;
  const BASE_URL = "https://ftpserve.w3d.box.ca";
  const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB chunks

  // State management
  let user = "";
  let password = "";
  let connected = false;
  let message = "";
  let currentPath = ".";
  let dirItems = [];
  let isLoading = false;
  let uploadProgress = 0;
  let uploadSpeed = 0;
  let lastUploadSize = 0;
  let timeRemaining = "";
  let isUploading = false; // Separate from isLoading
  let showHighScores = false;
  let uploadId = null;
  let showLogs = false;
  let isChatOpen = false;

  // File upload refs and state
  let fileInputRef;
  let zipFileInputRef;
  let uploadFile = null;
  let uploadZipFile = null;
  let selectedFolder = "";
  let uploadStartTime;
  let currentFolderFilter = null;
  let lastFilterMessage = "";

  $: isMagnetFolder = currentPath
    .split("/")
    .some((part) => part.startsWith("magnet-"));

  // Connect to FTP server
  async function connectFTP() {
    message = "Connecting...";
    isLoading = true;
    connected = false;
    dirItems = [];

    try {
      const res = await fetch(`${BASE_URL}/connect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ host, port, user, password }),
      });
      const data = await res.json();

      if (data.success) {
        connected = true;
        message = "Connection successful!";
        currentPath = ".";
        // Load network scores
        await networkScores.loadScores({ host, port, user, password });
        await listDirectory(currentPath);
      } else {
        message = `Connection error: ${data.error}`;
      }
    } catch (err) {
      message = `Request failed: ${err.message}`;
    } finally {
      isLoading = false;
    }
  }

  function getSizeMB(bytes) {
    return bytes / (1024 * 1024);
  }

  // List directory contents
  async function listDirectory(path) {
    isLoading = true;
    message = `Loading: ${path}`;

    try {
      const res = await fetch(`${BASE_URL}/list`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ host, port, user, password, path }),
      });
      const data = await res.json();

      if (data.success) {
        dirItems = data.items;
        currentPath = path;

        // Update filter message when changing directories
        const folderName = path.split("/").pop();
        currentFolderFilter = getFilterForFolder(folderName);
        lastFilterMessage = currentFolderFilter
          ? `This folder accepts ${getFolderDescription(folderName)}`
          : "";

        message = `Current directory: ${path}${lastFilterMessage ? ` - ${lastFilterMessage}` : ""}`;
        selectedFolder = "";
      } else {
        message = `Error listing directory: ${data.error}`;
      }
    } catch (err) {
      message = `Request failed: ${err.message}`;
    } finally {
      isLoading = false;
    }
  }

  // Navigate up one directory
  function goUp() {
    if (currentPath === "." || currentPath === "/") {
      message = "Already at top-level directory.";
      return;
    }
    const parts = currentPath.split("/");
    parts.pop();
    let newPath = parts.join("/");
    if (!newPath) newPath = ".";
    listDirectory(newPath);
  }

  // Format bytes to human readable size
  function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  // Calculate upload speed and time remaining
  function updateUploadStats(uploaded, total) {
    const now = Date.now();
    const elapsed = (now - uploadStartTime) / 1000; // seconds
    uploadSpeed = uploaded / elapsed; // bytes per second
    const remaining = (total - uploaded) / uploadSpeed;

    if (remaining > 60) {
      timeRemaining = `${Math.round(remaining / 60)}m ${Math.round(remaining % 60)}s`;
    } else {
      timeRemaining = `${Math.round(remaining)}s`;
    }
  }

  async function uploadInChunks(file, uploadType = "regular") {
    isLoading = true;
    isUploading = true;
    lastUploadSize = file.size;
    message = `Preparing to upload ${file.name}...`;
    uploadProgress = 0;
    uploadStartTime = Date.now();

    try {
      // Initialize upload
      const initRes = await fetch(
        `${BASE_URL}/upload${uploadType === "zip" ? "-zip" : ""}/init`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            Origin: window.location.origin,
          },
          body: JSON.stringify({
            fileName: file.name,
            totalSize: file.size,
            totalChunks: Math.ceil(file.size / CHUNK_SIZE),
          }),
        }
      );

      if (!initRes.ok) {
        throw new Error(`Upload initialization failed: ${initRes.statusText}`);
      }

      const initData = await initRes.json();
      uploadId = initData.uploadId;
      const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
      let uploadedBytes = 0;

      // FTP config
      const ftpConfig = {
        host,
        port,
        user,
        password,
        path: currentPath,
      };

      // Upload chunks with exponential backoff retry
      for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
        const start = chunkIndex * CHUNK_SIZE;
        const end = Math.min(start + CHUNK_SIZE, file.size);
        const chunk = file.slice(start, end);

        const retryOptions = {
          maxRetries: 3, // Increased from 3 to 5
          initialDelay: 2000, // Start with 1 second
          maxDelay: 10000, // Max 30 seconds
          backoff: 2, // Double the delay each time
        };

        let lastError = null;
        let delay = retryOptions.initialDelay;

        for (let retry = 0; retry <= retryOptions.maxRetries; retry++) {
          try {
            const res = await fetch(
              `${BASE_URL}/upload${uploadType === "zip" ? "-zip" : ""}/chunk`,
              {
                method: "POST",
                credentials: "include",
                headers: {
                  "Content-Type": "application/octet-stream",
                  Accept: "application/json",
                  Origin: window.location.origin,
                  "X-Upload-ID": uploadId,
                  "X-Chunk-Index": chunkIndex.toString(),
                  "X-FTP-Config": JSON.stringify(ftpConfig),
                },
                body: chunk,
              }
            );

            if (!res.ok) {
              const errorData = await res
                .json()
                .catch(() => ({ error: res.statusText }));
              throw new Error(
                `HTTP error! status: ${res.status}, message: ${errorData.error || "Unknown error"}`
              );
            }

            const data = await res.json();

            if (!data.success && data.error) {
              throw new Error(data.error);
            }

            // Update progress
            uploadedBytes += chunk.size;
            uploadProgress = (uploadedBytes / file.size) * 100;
            updateUploadStats(uploadedBytes, file.size);

            message = `Uploading ${file.name}: ${Math.round(uploadProgress)}% - ${formatBytes(uploadSpeed)}/s - ${timeRemaining} remaining`;

            if (
              data.message === "ZIP uploaded and extracted successfully" ||
              data.message === "File uploaded successfully"
            ) {
              message =
                uploadType === "zip"
                  ? `ZIP "${file.name}" extracted successfully`
                  : `File "${file.name}" uploaded successfully`;
              await listDirectory(currentPath);
            }

            break; // Success - exit retry loop
          } catch (err) {
            lastError = err;

            if (retry < retryOptions.maxRetries) {
              message = `Retrying chunk ${chunkIndex + 1}/${totalChunks} (Attempt ${retry + 2}/${retryOptions.maxRetries + 1})...`;

              // Calculate next delay with exponential backoff
              delay = Math.min(
                delay * retryOptions.backoff,
                retryOptions.maxDelay
              );

              // Add some jitter to prevent thundering herd
              const jitter = Math.random() * 1000;
              await new Promise((resolve) =>
                setTimeout(resolve, delay + jitter)
              );
            } else {
              throw new Error(
                `Failed to upload chunk ${chunkIndex} after ${retryOptions.maxRetries} retries: ${lastError.message}`
              );
            }
          }
        }
      }

      return true;
    } catch (error) {
      message = `Upload failed: ${error.message}`;
      console.error("Upload error:", error);
      throw error;
    } finally {
      isLoading = false;
      isUploading = false;
      showHighScores = getSizeMB(lastUploadSize) >= 40;
      uploadProgress = 0;
      uploadSpeed = 0;
      timeRemaining = "";
    }
  }

  // File upload handlers
  function openFileDialog() {
    uploadFile = null;
    if (isMagnetFolder) {
      fileInputRef.accept = ".torrent";
    } else {
      const folderName = currentPath.split("/").pop();
      fileInputRef.accept = getAcceptString(folderName);

      // Update the current folder filter info
      currentFolderFilter = getFilterForFolder(folderName);
      lastFilterMessage = currentFolderFilter
        ? `This folder accepts ${getFolderDescription(folderName)}`
        : "";
    }
    fileInputRef.click();
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Check if the file is allowed in the current folder
    if (!isFileAllowed(file.name, currentPath.split("/").pop())) {
      const filter = getFilterForFolder(currentPath.split("/").pop());
      message = `Invalid file type. This folder only accepts ${filter.description}.`;
      uploadFile = null;
      return;
    }

    uploadFile = file;
    if (uploadFile) doUpload();
  }

  async function doUpload() {
    if (!uploadFile) {
      openFileDialog();
      return;
    }

    try {
      await uploadInChunks(uploadFile, "regular");
      uploadFile = null;
    } catch (error) {
      console.error("Upload failed:", error);
    }
  }

  // ZIP upload handlers
  function handleZipChange(e) {
    uploadZipFile = e.target.files[0] || null;
    if (uploadZipFile) doUploadZip();
  }

  async function doUploadZip() {
    if (!uploadZipFile) {
      zipFileInputRef.click();
      return;
    }

    try {
      await uploadInChunks(uploadZipFile, "zip");
      uploadZipFile = null;
    } catch (error) {
      console.error("ZIP upload failed:", error);
    }
  }

  function toggleChat() {
    isChatOpen = !isChatOpen;
  }

  // Filter folders from items
  $: subfolders = dirItems.filter((item) => item.type === 2);
</script>

<div class="min-h-screen bg-gray-900 text-gray-100">
  <div class="h-screen flex flex-col">
    {#if !connected}
      <!-- Login Form -->
      <div class="flex items-center justify-center min-h-screen p-4">
        <div class="w-full max-w-md bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-6 text-center">FTP Login</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Username</label>
              <input
                type="text"
                bind:value={user}
                class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500"
                placeholder="Enter username"
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Password</label>
              <input
                type="password"
                bind:value={password}
                class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500"
                placeholder="Enter password"
              />
            </div>
            <button
              on:click={connectFTP}
              disabled={isLoading}
              class="w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed py-2 px-4 rounded-md"
            >
              {#if isLoading}
                <span class="animate-spin">↻</span>
                <span>Connecting...</span>
              {:else}
                <span>Connect</span>
              {/if}
            </button>
          </div>
        </div>
      </div>
    {:else}
      <div class="h-full flex flex-col">
        <!-- Top bar -->
        <div class="bg-gray-800 p-3 sm:p-4 border-b border-gray-700">
          <div class="flex flex-wrap gap-2 items-center mb-2">
            <button
              on:click={goUp}
              disabled={isLoading || currentPath === "."}
              class="flex items-center space-x-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 rounded-md"
            >
              <span>↑</span>
              <span class="hidden sm:inline">Up</span>
            </button>

            <div class="flex flex-wrap gap-2">
              {#if isMagnetFolder}
                <button
                  on:click={openFileDialog}
                  disabled={isLoading}
                  class="flex items-center space-x-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-md"
                >
                  <span>↑</span>
                  <span>Add Magnet</span>
                </button>
              {:else}
                <button
                  on:click={openFileDialog}
                  disabled={isLoading}
                  class="flex items-center space-x-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-md whitespace-nowrap"
                >
                  <span>↑</span>
                  <span class="hidden sm:inline">Upload File</span>
                  <span class="sm:hidden">Upload</span>
                </button>
                <button
                  on:click={() => zipFileInputRef.click()}
                  disabled={isLoading}
                  class="flex items-center space-x-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-md"
                >
                  <span>↑</span>
                  <span class="hidden sm:inline">Upload ZIP</span>
                  <span class="sm:hidden">ZIP</span>
                </button>
              {/if}

              <button
                on:click={toggleChat}
                class="md:hidden flex items-center space-x-2 px-3 py-2 bg-green-600 hover:bg-green-700 rounded-md"
              >
                <span>{isChatOpen ? "📁" : "💬"}</span>
              </button>

              {#if user === "web3dguy"}
                <button
                  on:click={() => (showLogs = true)}
                  class="flex items-center space-x-2 px-3 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800 rounded-md"
                >
                  <span>📊</span>
                  <span class="hidden sm:inline">Activity Logs</span>
                  <span class="sm:hidden">Logs</span>
                </button>
              {/if}
            </div>
          </div>

          <div class="w-full">
            <div
              class="px-3 py-2 bg-gray-700 rounded-md overflow-x-auto whitespace-nowrap text-sm sm:text-base"
            >
              {currentPath}
            </div>
          </div>
        </div>

        <!-- Main content area -->
        <div class="flex-1 flex md:flex-row">
          <!-- File browser section -->
          <div class="flex-1 min-w-0 md:w-3/4">
            <div
              class="flex-1 min-w-0 overflow-auto p-4 md:h-[calc(100vh-8rem)]"
              style="height: {isChatOpen
                ? 'calc(50vh - 8rem)'
                : 'calc(100vh - 8rem)'}"
            >
              <div
                class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
              >
                {#each dirItems as item (item.name)}
                  <div
                    class="p-4 bg-gray-800 rounded-lg hover:bg-gray-700 cursor-pointer"
                    on:click={() => {
                      if (item.type === 2) {
                        listDirectory(
                          currentPath === "."
                            ? item.name
                            : `${currentPath}/${item.name}`
                        );
                      }
                    }}
                  >
                    <div class="flex items-center space-x-2">
                      <span
                        class={item.type === 2
                          ? "text-blue-400"
                          : "text-gray-400"}
                      >
                        {item.type === 2 ? "📁" : "📄"}
                      </span>
                      <span class="truncate">{item.name}</span>
                    </div>
                  </div>
                {/each}
              </div>
            </div>
          </div>

          <!-- Chat section -->
          {#if connected}
            <div
              class="md:w-96 border-t md:border-t-0 md:border-l border-gray-700 {isChatOpen
                ? 'fixed md:relative bottom-0 left-0 right-0 h-[50vh]'
                : 'hidden'} md:block md:h-[calc(100vh-8rem)]"
            >
              <Chat username={user} {password} {connected} />
            </div>
          {/if}
        </div>

        <!-- Progress bar -->
        {#if isLoading}
          <div class="fixed bottom-0 left-0 right-0 z-40 p-3 sm:p-4 bg-gray-800 border-t border-gray-700 shadow-lg">
            <div class="w-full bg-gray-700 rounded-full h-2.5">
              <div
                class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style="width: {uploadProgress}%"
              ></div>
            </div>
            <div class="mt-2 text-sm text-center">{message}</div>
            {#if uploadSpeed > 0}
              <div class="mt-1 text-sm text-center text-gray-400">
                {formatBytes(uploadSpeed)}/s - {timeRemaining} remaining
              </div>
            {/if}
          </div>
        {/if}
        <!-- Hidden file inputs -->
        <input
          type="file"
          bind:this={fileInputRef}
          class="hidden"
          on:change={handleFileChange}
        />
        {#if !isMagnetFolder}
          <input
            type="file"
            accept=".zip"
            bind:this={zipFileInputRef}
            class="hidden"
            on:change={handleZipChange}
          />
        {/if}
      </div>
    {/if}
    {#if isUploading && getSizeMB(lastUploadSize) >= 40}
      <FlappyBird
        {isUploading}
        progress={uploadProgress}
        username={user}
        {password}
      />
    {/if}
    {#if showHighScores && getSizeMB(lastUploadSize) >= 40}
      <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        on:click|self={() => (showHighScores = false)}
      >
        <div
          class="bg-gray-800 p-6 rounded-lg shadow-xl min-w-[300px]"
          on:click|stopPropagation
        >
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">Upload Session Score</h2>
            <button
              class="text-gray-400 hover:text-white"
              on:click={() => (showHighScores = false)}
            >
              ✕
            </button>
          </div>

          {#if $highScores[user]?.currentSession > 0}
            <div class="bg-gray-700 p-4 rounded text-center">
              <h3 class="font-semibold text-blue-400 mb-2">{user}</h3>
              <p class="text-2xl font-bold text-white">
                {$highScores[user].currentSession} points
              </p>
            </div>

            {#if $highScores[user].allTime.length > 0}
              <div class="mt-4 text-sm text-gray-400">
                Your all-time best scores:
                <ul class="mt-2 space-y-1">
                  {#each $highScores[user].allTime.slice(0, 3) as score, i}
                    <li class="text-gray-300">
                      {i + 1}. {score} points
                    </li>
                  {/each}
                </ul>
              </div>
            {/if}

            {#if $networkScores && Object.keys($networkScores).length > 0}
              <div class="mt-6 pt-4 border-t border-gray-600">
                <h3 class="text-lg font-semibold mb-2">Server High Scores</h3>
                {#each Object.entries($networkScores)
                  .sort(([, a], [, b]) => Math.max(...b) - Math.max(...a))
                  .slice(0, 5) as [player, scores]}
                  <div class="mb-2">
                    <span class="text-blue-400">{player}</span>
                    <span class="text-gray-300">
                      - {Math.max(...scores)} points</span
                    >
                  </div>
                {/each}
              </div>
            {/if}
          {:else}
            <p class="text-gray-400 mb-4">
              No score yet for this upload session! Keep playing while your file
              uploads.
            </p>
          {/if}

          <div class="mt-6 flex justify-end">
            <button
              class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
              on:click={() => (showHighScores = false)}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    {/if}

    {#if showLogs}
      <Logs
        username={user}
        {password}
        show={showLogs}
        on:close={() => (showLogs = false)}
      />
    {/if}
  </div>
</div>

```

### frontend\src\components\Chat.svelte

```svelte
<!-- Chat.svelte -->
<script>
  import { onMount, onDestroy } from "svelte";
  import { chatStore } from "../stores/chatStore";

  export let username = "";
  export let password = "";
  export let connected = false;

  let messages = [];
  let newMessage = "";
  let chatContainer;
  let error = null;
  let isLoading = false;
  let refreshInterval;
  let imageModalUrl = null;
  let isExpanded = false;

  // URL and image detection
  const URL_REGEX = /(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/g;
  const IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"];

  function parseMessage(text) {
    if (!text) return [{ type: "text", content: "" }];

    const parts = [];
    let lastIndex = 0;

    try {
      const matches = Array.from(text.matchAll(URL_REGEX));

      matches.forEach((match) => {
        const [url] = match;
        const startIndex = match.index;

        if (startIndex > lastIndex) {
          parts.push({
            type: "text",
            content: text.slice(lastIndex, startIndex),
          });
        }

        const isImage = IMAGE_EXTENSIONS.some((ext) =>
          url.toLowerCase().endsWith(ext)
        );

        parts.push({
          type: isImage ? "image" : "link",
          content: url,
        });

        lastIndex = startIndex + url.length;
      });

      if (lastIndex < text.length) {
        parts.push({
          type: "text",
          content: text.slice(lastIndex),
        });
      }

      return parts.length ? parts : [{ type: "text", content: text }];
    } catch (error) {
      console.error("Error parsing message:", error);
      return [{ type: "text", content: text }];
    }
  }

  const unsubscribe = chatStore.subscribe((state) => {
    messages = state.messages;
    error = state.error;
    isLoading = state.isLoading;
    if (!isLoading) {
      scrollToBottom();
    }
  });

  onMount(() => {
    if (connected) {
      loadMessages();
      refreshInterval = setInterval(loadMessages, 10000);
    }
  });

  onDestroy(() => {
    unsubscribe();
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
  });

  async function loadMessages() {
    const ftpConfig = {
      host: "dia.whatbox.ca",
      port: 25850,
      user: username,
      password,
    };

    await chatStore.loadMessages(ftpConfig);
  }

  async function sendMessage() {
    if (!newMessage.trim()) return;

    const ftpConfig = {
      host: "dia.whatbox.ca",
      port: 25850,
      user: username,
      password,
    };

    try {
      await chatStore.sendMessage(username, newMessage.trim(), ftpConfig);
      newMessage = "";
      scrollToBottom();
    } catch (err) {
      console.error("Error sending message:", err);
    }
  }

  function scrollToBottom() {
    if (chatContainer) {
      setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }, 100);
    }
  }

  function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
  }

  function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  function openImageModal(url) {
    imageModalUrl = url;
  }
</script>

<div
  class="flex flex-col bg-gray-900 h-full max-h-full relative {isExpanded
    ? 'fixed inset-0 z-50'
    : ''}"
>
  <!-- Header with expand/collapse button -->
  <div
    class="flex items-center justify-between p-2 lg:p-4 bg-gray-800 border-b border-gray-700"
  >
    <h2 class="text-lg font-semibold">Group Chat</h2>
    <div class="flex items-center space-x-2">
      <button
        on:click={() => (isExpanded = !isExpanded)}
        class="p-2 hover:bg-gray-700 rounded-lg lg:hidden"
      >
        {#if isExpanded}
          <span class="text-lg">↙</span>
        {:else}
          <span class="text-lg">↗</span>
        {/if}
      </button>
    </div>
  </div>

  <!-- Messages container -->
  <div class="flex-1 min-h-0 overflow-hidden flex flex-col">
    <div
      bind:this={chatContainer}
      class="flex-1 overflow-y-auto p-2 lg:p-4 space-y-2"
    >
      {#if isLoading && messages.length === 0}
        <div class="flex justify-center items-center h-full">
          <span class="animate-spin text-blue-500">↻</span>
        </div>
      {:else if error}
        <div class="text-red-500 text-center">{error}</div>
      {:else if messages.length === 0}
        <div class="text-gray-500 text-center">No messages yet</div>
      {:else}
        {#each messages as message}
          <div
            class="flex flex-col {message.username === username
              ? 'items-end'
              : 'items-start'}"
          >
            <div
              class="max-w-[90%] lg:max-w-[85%] break-words rounded-lg px-3 py-2 {message.username ===
              username
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-100'}"
            >
              <div class="text-sm font-semibold mb-1">
                {message.username}
              </div>
              <div class="text-sm whitespace-pre-wrap break-words">
                {#each parseMessage(message.content) as part}
                  {#if part.type === "text"}
                    {part.content}
                  {:else if part.type === "link"}
                    <a
                      href={part.content}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-blue-300 hover:text-blue-200 underline break-all"
                    >
                      {part.content}
                    </a>
                  {:else if part.type === "image"}
                    <div
                      class="mt-2 cursor-pointer"
                      on:click={() => openImageModal(part.content)}
                    >
                      <img
                        src={part.content}
                        alt="Shared image"
                        class="max-w-full rounded-lg max-h-36 lg:max-h-48 object-contain bg-gray-900"
                        loading="lazy"
                      />
                    </div>
                  {/if}
                {/each}
              </div>
              <div class="text-xs opacity-75 mt-1">
                {formatTimestamp(message.timestamp)}
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>

    <!-- Message input -->
    <div class="p-2 lg:p-4 bg-gray-800 border-t border-gray-700">
      <div class="flex space-x-2">
        <textarea
          bind:value={newMessage}
          on:keypress={handleKeyPress}
          placeholder="Type a message..."
          class="flex-1 bg-gray-700 text-gray-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 resize-none h-[38px] lg:h-[42px] min-h-[38px] lg:min-h-[42px] max-h-[120px] text-sm lg:text-base"
          rows="1"
        ></textarea>
        <button
          on:click={sendMessage}
          disabled={!newMessage.trim() || isLoading}
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white px-3 lg:px-4 py-2 rounded-lg whitespace-nowrap text-sm lg:text-base"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Image modal -->
{#if imageModalUrl}
  <div
    class="fixed inset-0 z-[100] flex items-center justify-center bg-black bg-opacity-75 cursor-pointer"
    on:click={() => (imageModalUrl = null)}
  >
    <div class="max-w-4xl max-h-[90vh] p-2">
      <img
        src={imageModalUrl}
        alt="Full size view"
        class="max-w-full max-h-full rounded-lg object-contain"
      />
    </div>
  </div>
{/if}

<style>
  /* Ensure proper sizing on mobile devices */
  textarea {
    font-size: 16px; /* Prevents iOS zoom on focus */
  }

  /* Prevent zoom on mobile devices */
  @media (max-width: 768px) {
    textarea {
      font-size: 16px;
    }
  }
</style>


```

### frontend\src\components\FlappyBird.svelte

```svelte
<!-- FlappyBird.svelte -->
<script>
  import { onMount, onDestroy } from "svelte";
  import { highScores } from "../stores/highscores";
  import { networkScores } from "../stores/networkScores";

  export let isUploading = false;
  export let progress = 0;
  export let username = "";
  export let password = '';
  let gameEnded = false;

  let gameContainer;
  let p5Instance;

  // Load p5 and p5.sound from CDN
  function loadP5Libraries() {
    return new Promise((resolve) => {
      const p5Script = document.createElement("script");
      p5Script.src = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js";

      const p5SoundScript = document.createElement("script");
      p5SoundScript.src =
        "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/addons/p5.sound.js";

      p5Script.onload = () => {
        document.head.appendChild(p5SoundScript);
      };

      p5SoundScript.onload = () => {
        resolve(window.p5);
      };

      document.head.appendChild(p5Script);
    });
  }

  onMount(async () => {
    const p5 = await loadP5Libraries();

    const sketch = (p) => {
      // Global variables
      let sprite_flappy, sprite_pipe, sprite_city, sprite_floor, sprite_title;
      let sound_point, sound_wing, sound_hit, sound_die, sound_sweetwing;
      let font_flappy;

      let mousePress = false;
      let mousePressEvent = false;
      let mouseReleaseEvent = false;
      let keyPress = false;
      let keyPressEvent = false;
      let keyReleaseEvent = false;

      let pipes = [];
      let score = 0;
      let hightscore = 0;
      let speed = 3;
      let gap = 80;
      let gameover = false;
      let page = "MENU";
      let overflowX = 0;

      // Utility functions
      function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
      }

      function smoothMove(pos, target, speed) {
        return pos + (target - pos) * speed;
      }

      function press(txt, x, y) {
        const tX = p.width / 2;
        const tY = p.height / 2;
        let this_h = false;

        if (
          p.mouseX > tX + x - p.textWidth(txt) / 2 - 10 &&
          p.mouseX < tX + x + p.textWidth(txt) / 2 + 10 &&
          p.mouseY > tY + y - p.textAscent() / 2 - 10 &&
          p.mouseY < tY + y + p.textAscent() / 2 + 10
        ) {
          this_h = true;
        }

        p.push();
        p.textSize(16);

        if (this_h && mousePress) {
          p.noStroke();
          p.fill(83, 56, 71);
          p.rect(x, y + 3, p.textWidth(txt) + 35, p.textAscent() + 20);

          p.fill(250, 117, 49);
          p.stroke(255);
          p.strokeWeight(3);
          p.rect(x, y + 2, p.textWidth(txt) + 25, p.textAscent() + 10);

          p.noStroke();
          p.fill(255);
          p.text(txt, x, y + 2);
        } else {
          p.noStroke();
          p.fill(83, 56, 71);
          p.rect(x, y + 2, p.textWidth(txt) + 35, p.textAscent() + 22);

          if (this_h) {
            p.fill(250, 117, 49);
          } else {
            p.fill(230, 97, 29);
          }
          p.stroke(255);
          p.strokeWeight(3);
          p.rect(x, y, p.textWidth(txt) + 25, p.textAscent() + 10);

          p.noStroke();
          p.fill(255);
          p.text(txt, x, y);
        }
        p.pop();

        if (this_h && mouseReleaseEvent) {
          try {
            sound_sweetwing.play();
          } catch (e) {}
        }

        return this_h && mouseReleaseEvent;
      }

      function resetGame() {
        gameEnded = false;
        gameover = false;
        gap = 80;
        speed = 3;
        score = 0;
        flappy_bird.y = p.height / 2;
        flappy_bird.falls = false;
        flappy_bird.velocityY = 0;
        flappy_bird.angle = 0;
        flappy_bird.flashAnim = 0;
        flappy_bird.flashReturn = false;
        pipes = [];
        flappy_bird.target = 10000;
        menu_gameover.ease = 0;
      }

      const handleGameOver = async () => {
        if (!gameEnded && score > 0) {
          gameEnded = true;
          // Update local high scores
          highScores.addScore(username, score);

          // Save to network scores - use the current FTP config
          try {
            await networkScores.addScore(username, score, {
              host: "dia.whatbox.ca",
              port: 25850,
              user: username,
              password: password, // We need to pass this from App.svelte
            });
          } catch (e) {
            console.warn("Error saving network score:", e);
          }
        }
      };

      const menu_gameover = {
        ease: 0,
        easing: false,
        open: false,

        display() {
          if (!gameEnded) {
            handleGameOver();
          }
          p.push();
          p.translate(p.width / 2, p.height / 2);
          p.scale(this.ease);

          p.stroke(83, 56, 71);
          p.strokeWeight(2);
          p.fill(222, 215, 152);
          p.rect(0, 0, 200, 200);

          p.noStroke();
          p.fill(83, 56, 71);
          p.text("Game Over", -0, -50);

          p.textSize(20);
          p.strokeWeight(5);
          p.stroke(83, 56, 71);
          p.fill(255);
          p.text("Flappy Bird", 0, -80);

          p.push();
          p.textAlign(p.LEFT, p.CENTER);
          p.textSize(12);
          p.noStroke();
          p.fill(83, 56, 71);
          p.text("score : ", -80, 0);
          p.text("hightscore : ", -80, 30);

          p.stroke(0);
          p.strokeWeight(3);
          p.fill(255);
          p.text(score, 20, 0);
          p.text(hightscore, 20, 30);
          p.pop();

          if (press("restart", 0, 140)) {
            resetGame();
          }

          if (press(" menu ", 0, 190)) {
            page = "MENU";
          }
          p.pop();
        },

        update() {
          if (this.easing) {
            this.ease += 0.1;
            if (this.ease > 1) {
              this.open = true;
              this.ease = 1;
              this.easing = false;
            }
          }
        },

        easein() {
          this.easing = true;
        },
      };

      const flappy_bird = {
        x: 100,
        y: 0,
        target: 0,
        velocityY: 0,
        fly: false,
        angle: 0,
        falls: false,
        flashAnim: 0,
        flashReturn: false,
        kinematicAnim: 0,

        display() {
          p.push();
          p.translate(this.x, this.y);
          p.rotate(p.radians(this.angle));
          if (!mousePress || this.falls) {
            p.image(
              sprite_flappy,
              0,
              0,
              sprite_flappy.width * 1.5,
              sprite_flappy.height * 3,
              0,
              0,
              sprite_flappy.width / 2,
              sprite_flappy.height * 3
            );
          } else {
            p.image(
              sprite_flappy,
              0,
              0,
              sprite_flappy.width * 1.5,
              sprite_flappy.height * 3,
              sprite_flappy.width / 2,
              0,
              sprite_flappy.width / 2,
              sprite_flappy.height * 3
            );
          }
          p.pop();
        },

        update() {
          if (this.falls) {
            if (this.flashAnim > 255) {
              this.flashReturn = true;
            }

            if (this.flashReturn) {
              this.flashAnim -= 60;
            } else {
              this.flashAnim += 60;
            }

            if (this.flashReturn && this.flashAnim === 0) {
              gameover = true;
              menu_gameover.easein();
              try {
                sound_die.play();
              } catch (e) {}

              if (score > hightscore) {
                hightscore = score;
              }
            }

            this.y += this.velocityY;
            this.velocityY += 0.4;
            this.angle += 4;

            if (speed > 0) {
              speed = 0;
            }

            if (this.angle > 90) {
              this.angle = 90;
            }
          } else {
            this.y += this.velocityY;
            this.angle += 2.5;

            if (this.angle > 90) {
              this.angle = 90;
            }

            if (mousePressEvent || (keyPressEvent && p.key === " ")) {
              try {
                sound_wing.play();
              } catch (e) {}

              this.velocityY = 0;
              this.fly = true;
              this.target = clamp(this.y - 60, -19, p.height);
              this.angle = -45;
            }

            if (this.y < this.target) {
              this.fly = false;
              this.target = 10000;
            }

            if (!this.fly) {
              this.velocityY += 0.4;
            } else {
              this.y -= 5;
            }

            if (this.y > p.height - 49) {
              if (!this.falls) {
                try {
                  sound_hit.play();
                } catch (e) {}
              }
              this.falls = true;
            }
          }
          this.y = clamp(this.y, -20, p.height - 50);
        },

        kinematicMove() {
          if (gameover) {
            this.x = p.width / 2;
            this.y = p.height / 2;
            gameover = false;
            score = 0;
            gap = 90;
          }

          this.y = p.height / 2 + p.map(p.sin(p.frameCount * 0.1), 0, 1, -2, 2);

          p.push();
          p.translate(this.x, this.y);
          p.image(
            sprite_flappy,
            0,
            0,
            sprite_flappy.width * 1.5,
            sprite_flappy.height * 3,
            0,
            0,
            sprite_flappy.width / 2,
            sprite_flappy.height * 3
          );
          p.pop();
        },
      };

      class Pipe {
        constructor() {
          this.gapSize = gap;
          this.y = p.random(150, p.height - 150);
          this.x = p.width + 50;
          this.potential = true;
        }

        display() {
          p.push();
          p.translate(
            this.x,
            this.y + this.gapSize + sprite_pipe.height / 2 / 2
          );
          p.image(
            sprite_pipe,
            0,
            0,
            sprite_pipe.width / 2,
            sprite_pipe.height / 2
          );
          p.pop();

          p.push();
          p.translate(
            this.x,
            this.y - this.gapSize - sprite_pipe.height / 2 / 2
          );
          p.rotate(p.radians(180));
          p.scale(-1, 1);
          p.image(
            sprite_pipe,
            0,
            0,
            sprite_pipe.width / 2,
            sprite_pipe.height / 2
          );
          p.pop();

          if (
            this.potential &&
            flappy_bird.x > this.x - 25 &&
            flappy_bird.x < this.x + 25
          ) {
            score++;
            try {
              sound_point.play();
            } catch (e) {}
            if (gap > 60) {
              gap--;
            }
            this.potential = false;
          }

          // Collision detection
          if (
            (flappy_bird.x + 20 > this.x - 25 &&
              flappy_bird.x - 20 < this.x + 25 &&
              flappy_bird.y + 20 >
                this.y - this.gapSize - sprite_pipe.height / 2 / 2 - 200 &&
              flappy_bird.y - 20 <
                this.y - this.gapSize - sprite_pipe.height / 2 / 2 + 200) ||
            (flappy_bird.x + 20 > this.x - 25 &&
              flappy_bird.x - 20 < this.x + 25 &&
              flappy_bird.y + 20 >
                this.y + this.gapSize + sprite_pipe.height / 2 / 2 - 200 &&
              flappy_bird.y - 20 <
                this.y + this.gapSize + sprite_pipe.height / 2 / 2 + 200)
          ) {
            if (!flappy_bird.falls) {
              try {
                sound_hit.play();
              } catch (e) {}
            }
            flappy_bird.falls = true;
          }
        }

        update() {
          this.x -= speed;
        }
      }

      function page_game() {
        overflowX += speed;
        if (overflowX > sprite_city.width / 2) {
          overflowX = 0;
        }

        p.image(
          sprite_city,
          sprite_city.width / 2 / 2,
          p.height - sprite_city.height / 2 / 2 - 40,
          sprite_city.width / 2,
          sprite_city.height / 2
        );

        if (!flappy_bird.falls && p.frameCount % 70 === 0) {
          pipes.push(new Pipe());
        }

        for (let i = pipes.length - 1; i >= 0; i--) {
          if (pipes[i].x < -50) {
            pipes.splice(i, 1);
            continue;
          }
          pipes[i].display();
          pipes[i].update();
        }

        p.image(
          sprite_floor,
          sprite_floor.width - overflowX,
          p.height - sprite_floor.height,
          sprite_floor.width * 2,
          sprite_floor.height * 2
        );

        flappy_bird.display();
        flappy_bird.update();
        flappy_bird.x = smoothMove(flappy_bird.x, 90, 0.02);

        if (!gameover) {
          p.push();
          p.stroke(0);
          p.strokeWeight(5);
          p.fill(255);
          p.textSize(30);
          p.text(score, p.width / 2, 50);
          p.pop();
        }

        p.push();
        p.noStroke();
        p.fill(255, flappy_bird.flashAnim);
        p.rect(p.width / 2, p.height / 2, p.width, p.height);
        p.pop();

        if (gameover) {
          menu_gameover.display();
          menu_gameover.update();
        }
      }

      function page_menu() {
        speed = 1;
        overflowX += speed;
        if (overflowX > sprite_city.width / 2) {
          overflowX = 0;
        }

        p.image(
          sprite_city,
          sprite_city.width / 2 / 2,
          p.height - sprite_city.height / 2 / 2 - 40,
          sprite_city.width / 2,
          sprite_city.height / 2
        );

        p.image(
          sprite_floor,
          sprite_floor.width - overflowX,
          p.height - sprite_floor.height,
          sprite_floor.width * 2,
          sprite_floor.height * 2
        );

        p.image(
          sprite_title,
          p.width / 2,
          100,
          sprite_title.width / 4,
          sprite_title.height / 4
        );

        flappy_bird.kinematicMove();

        p.push();
        p.fill(230, 97, 29);
        p.stroke(255);
        p.strokeWeight(3);
        p.text("Tap to play", p.width / 2, p.height / 2 - 50);
        p.pop();

        if (mousePressEvent || (keyPressEvent && p.key === " ")) {
          page = "GAME";
          resetGame();

          flappy_bird.velocityY = 0;
          flappy_bird.fly = true;
          flappy_bird.target = clamp(flappy_bird.y - 60, -19, p.height);
          flappy_bird.angle = -45;
          flappy_bird.update();
        }
        flappy_bird.x = p.width / 2;
      }

      p.preload = () => {
        const assetsPath = "src/assets";

        sprite_flappy = p.loadImage(`${assetsPath}/flappybird.png`);
        sprite_pipe = p.loadImage(`${assetsPath}/pipe.png`);
        sprite_city = p.loadImage(`${assetsPath}/city.png`);
        sprite_floor = p.loadImage(`${assetsPath}/floor.png`);
        sprite_title = p.loadImage(`${assetsPath}/title.png`);

        try {
          sound_point = p.loadSound(`${assetsPath}/sfx_point.wav`);
          sound_hit = p.loadSound(`${assetsPath}/sfx_hit.wav`);
          sound_die = p.loadSound(`${assetsPath}/sfx_die.wav`);
          sound_wing = p.loadSound(`${assetsPath}/sfx_wing.wav`);
          sound_sweetwing = p.loadSound(`${assetsPath}/sfx_swooshing.wav`);
        } catch (e) {
          console.warn("Sound loading failed:", e);
          const dummySound = { play: () => {} };
          sound_point =
            sound_hit =
            sound_die =
            sound_wing =
            sound_sweetwing =
              dummySound;
        }

        try {
          font_flappy = p.loadFont(`${assetsPath}/flappy-font.ttf`);
        } catch (e) {
          console.warn("Font loading failed:", e);
        }
      };

      p.setup = () => {
        const canvas = p.createCanvas(400, 400);
        canvas.parent(gameContainer);

        p.imageMode(p.CENTER);
        p.rectMode(p.CENTER);
        p.ellipseMode(p.CENTER);
        p.textAlign(p.CENTER, p.CENTER);
        p.noSmooth();

        try {
          p.textFont(font_flappy);
        } catch (e) {}

        flappy_bird.y = p.height / 2;
      };

      p.draw = () => {
        p.background(123, 196, 208);

        switch (page) {
          case "GAME":
            page_game();
            break;
          case "MENU":
            page_menu();
            break;
        }

        // Reset events
        mousePressEvent = false;
        mouseReleaseEvent = false;
        keyPressEvent = false;
        keyReleaseEvent = false;
      };

      // Event handlers
      p.mousePressed = () => {
        mousePress = true;
        mousePressEvent = true;
      };

      p.mouseReleased = () => {
        mousePress = false;
        mouseReleaseEvent = true;
      };

      p.keyPressed = () => {
        keyPress = true;
        keyPressEvent = true;
      };

      p.keyReleased = () => {
        keyPress = false;
        keyReleaseEvent = true;
      };
    };

    // Create new p5 instance
    p5Instance = new p5(sketch);
  });

  onDestroy(() => {
    if (p5Instance) {
      p5Instance.remove();
    }
  });
</script>

<div
  class="fixed inset-0 z-50 flex items-center justify-center transition-opacity"
  class:opacity-0={!isUploading}
  class:pointer-events-none={!isUploading}
>
  <div class="bg-grey-800 p-4 rounded-lg shadow-lg">
    <div class="text-center mb-4">
      <h3 class="text-lg font-bold">Uploading... {progress}%</h3>
      <p class="text-sm text-gray-600">Play while you wait!</p>
    </div>
    <div bind:this={gameContainer} class="w-[400px] h-[400px]" />
  </div>
</div>


```

### frontend\src\components\Logs.svelte

```svelte
<!-- Logs.svelte -->
<script>
    import { onMount, createEventDispatcher } from 'svelte';
    import { activityLogs } from '../stores/activityLogs';
    
    const dispatch = createEventDispatcher();
    
    export let username = '';
    export let password = '';
    export let show = false;
    
    let logs = [];
    let error = null;
    let isLoading = false;
    let searchTerm = '';
    let selectedType = 'all';
    let selectedTimeframe = 'all';

    $: filteredLogs = logs
        .filter(log => {
            const matchesSearch = log.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                log.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
                                log.path.toLowerCase().includes(searchTerm.toLowerCase());
                                
            const matchesType = selectedType === 'all' || log.type === selectedType;
            
            const timestamp = new Date(log.timestamp);
            const now = new Date();
            const daysDiff = (now - timestamp) / (1000 * 60 * 60 * 24);
            
            const matchesTimeframe = selectedTimeframe === 'all' ||
                (selectedTimeframe === 'today' && daysDiff < 1) ||
                (selectedTimeframe === 'week' && daysDiff < 7) ||
                (selectedTimeframe === 'month' && daysDiff < 30);
                
            return matchesSearch && matchesType && matchesTimeframe;
        })
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        const unsubscribe = activityLogs.subscribe(state => {
        logs = state.logs;
        error = state.error;
        isLoading = state.isLoading;
    });
    
    onMount(() => {
        if (show) {
            loadLogs();
        }
        return () => unsubscribe();
    });
    
    async function loadLogs() {
        const ftpConfig = {
            host: "dia.whatbox.ca",
            port: 25850,
            user: username,
            password
        };
        
        await activityLogs.loadLogs(ftpConfig);
    }

    function formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleString();
    }
    
    function formatSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 Bytes';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function handleClose() {
        dispatch('close');
    }
</script>

{#if show}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75">
        <div class="bg-gray-800 w-full max-w-6xl h-[80vh] rounded-lg shadow-xl flex flex-col">
            <!-- Header -->
            <div class="p-4 border-b border-gray-700 flex justify-between items-center">
                <h2 class="text-xl font-bold">Activity Logs</h2>
                <button
                    on:click={handleClose}
                    class="text-gray-400 hover:text-white"
                >
                    ✕
                </button>
            </div>

            <!-- Filters -->
            <div class="p-4 border-b border-gray-700 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <input
                        type="text"
                        bind:value={searchTerm}
                        placeholder="Search logs..."
                        class="w-full px-3 py-2 bg-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <div class="flex space-x-2">
                    <select
                        bind:value={selectedType}
                        class="px-3 py-2 bg-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="all">All Types</option>
                        <option value="upload">Uploads</option>
                        <option value="delete">Deletions</option>
                        <option value="mkdir">New Folders</option>
                    </select>
                    <select
                        bind:value={selectedTimeframe}
                        class="px-3 py-2 bg-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="all">All Time</option>
                        <option value="today">Today</option>
                        <option value="week">This Week</option>
                        <option value="month">This Month</option>
                    </select>
                </div>
                <div class="flex justify-end">
                    <button
                        on:click={loadLogs}
                        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg"
                    >
                        Refresh
                    </button>
                </div>
            </div>

            <!-- Logs Table -->
            <div class="flex-1 overflow-auto p-4">
                {#if isLoading}
                    <div class="flex justify-center items-center h-full">
                        <span class="animate-spin text-blue-500">↻</span>
                    </div>
                {:else if error}
                    <div class="text-red-500 text-center p-4">{error}</div>
                {:else if filteredLogs.length === 0}
                    <div class="text-gray-400 text-center p-4">No logs found</div>
                {:else}
                    <table class="w-full">
                        <thead>
                            <tr class="text-left">
                                <th class="pb-2 px-4">Timestamp</th>
                                <th class="pb-2 px-4">User</th>
                                <th class="pb-2 px-4">Action</th>
                                <th class="pb-2 px-4">File/Path</th>
                                <th class="pb-2 px-4">Size</th>
                                <th class="pb-2 px-4">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each filteredLogs as log}
                                <tr class="border-t border-gray-700">
                                    <td class="py-2 px-4">{formatTimestamp(log.timestamp)}</td>
                                    <td class="py-2 px-4">{log.username}</td>
                                    <td class="py-2 px-4">
                                        <span
                                            class="px-2 py-1 rounded text-xs {
                                                log.type === 'upload' ? 'bg-green-600' :
                                                log.type === 'delete' ? 'bg-red-600' :
                                                'bg-blue-600'
                                            }"
                                        >
                                            {log.type}
                                        </span>
                                    </td>
                                    <td class="py-2 px-4">
                                        <div class="truncate max-w-md" title={log.path}>
                                            {log.filename}
                                        </div>
                                        <div class="text-xs text-gray-400 truncate" title={log.path}>
                                            {log.path}
                                        </div>
                                    </td>
                                    <td class="py-2 px-4">{formatSize(log.size)}</td>
                                    <td class="py-2 px-4">
                                        <span
                                            class="px-2 py-1 rounded text-xs {
                                                log.status === 'success' ? 'bg-green-600' :
                                                log.status === 'error' ? 'bg-red-600' :
                                                'bg-yellow-600'
                                            }"
                                        >
                                            {log.status}
                                        </span>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {/if}
            </div>

            <!-- Footer -->
            <div class="p-4 border-t border-gray-700 flex justify-between items-center">
                <div class="text-sm text-gray-400">
                    Showing {filteredLogs.length} of {logs.length} logs
                </div>
                {#if username === 'web3dguy'}
                    <button
                        on:click={() => {
                            if (confirm('Are you sure you want to clear all logs?')) {
                                const ftpConfig = {
                                    host: "dia.whatbox.ca",
                                    port: 25850,
                                    user: username,
                                    password
                                };
                                activityLogs.clearLogs(ftpConfig);
                            }
                        }}
                        class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg"
                    >
                        Clear All Logs
                    </button>
                {/if}
            </div>
        </div>
    </div>
{/if}

```

### frontend\src\lib\Counter.svelte

```svelte
<script>
  let count = $state(0)
  const increment = () => {
    count += 1
  }
</script>

<button onclick={increment}>
  count is {count}
</button>

```

### frontend\src\main.js

```javascript
import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

const app = mount(App, {
  target: document.getElementById('app'),
})

export default app

```

### frontend\src\stores\activityLogs.js

```javascript
import { writable } from 'svelte/store';

const BASE_URL = "https://ftpserve.w3d.box.ca";

function createActivityLogsStore() {
    const { subscribe, set, update } = writable({
        logs: [],
        isLoading: false,
        error: null
    });

    return {
        subscribe,
        loadLogs: async (ftpConfig) => {
            update(state => ({ ...state, isLoading: true, error: null }));
            
            try {
                const response = await fetch(`${BASE_URL}/logs/activity`, {
                    method: 'GET',
                    headers: {
                        'Authorization': JSON.stringify(ftpConfig),
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.success) {
                    update(state => ({
                        ...state,
                        logs: data.logs,
                        isLoading: false
                    }));
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error loading logs:', error);
                update(state => ({
                    ...state,
                    error: `Error loading logs: ${error.message}`,
                    isLoading: false
                }));
            }
        },
        clearLogs: async (ftpConfig) => {
            update(state => ({ ...state, isLoading: true, error: null }));
            
            try {
                const response = await fetch(`${BASE_URL}/logs/clear`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ ftpConfig })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.success) {
                    update(state => ({
                        ...state,
                        logs: [],
                        isLoading: false
                    }));
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error clearing logs:', error);
                update(state => ({
                    ...state,
                    error: `Error clearing logs: ${error.message}`,
                    isLoading: false
                }));
            }
        }
    };
}

export const activityLogs = createActivityLogsStore();

```

### frontend\src\stores\chatStore.js

```javascript
import { writable } from 'svelte/store';

// Make sure the BASE_URL doesn't have a trailing slash
const BASE_URL = "https://ftpserve.w3d.box.ca";
const CHAT_ENDPOINT = "/chat/messages";

function createChatStore() {
    const { subscribe, set, update } = writable({
        messages: [],
        isLoading: false,
        error: null
    });

    return {
        subscribe,
        sendMessage: async (username, message, ftpConfig) => {
            update(state => ({ ...state, isLoading: true, error: null }));
            
            try {
                console.log('Sending message to:', `${BASE_URL}${CHAT_ENDPOINT}`);
                const response = await fetch(`${BASE_URL}${CHAT_ENDPOINT}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username,
                        message,
                        ftpConfig
                    })
                });

                if (!response.ok) {
                    console.error('Response not OK:', response.status, response.statusText);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.success) {
                    update(state => ({
                        ...state,
                        messages: data.messages,
                        isLoading: false
                    }));
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error sending message:', error);
                update(state => ({
                    ...state,
                    error: `Error sending message: ${error.message}`,
                    isLoading: false
                }));
            }
        },
        loadMessages: async (ftpConfig) => {
            update(state => ({ ...state, isLoading: true, error: null }));
            
            try {
                console.log('Loading messages from:', `${BASE_URL}${CHAT_ENDPOINT}`);
                const response = await fetch(`${BASE_URL}${CHAT_ENDPOINT}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': JSON.stringify(ftpConfig),
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    console.error('Response not OK:', response.status, response.statusText);
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                if (data.success) {
                    update(state => ({
                        ...state,
                        messages: data.messages,
                        isLoading: false
                    }));
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error loading messages:', error);
                update(state => ({
                    ...state,
                    error: `Error loading messages: ${error.message}`,
                    isLoading: false
                }));
            }
        },
        clearError: () => {
            update(state => ({ ...state, error: null }));
        }
    };
}

export const chatStore = createChatStore();

```

### frontend\src\stores\fileTypeFilters.js

```javascript
// fileTypeFilters.js
export const folderFilters = {
  "Music": {
    extensions: [".mp3", ".m4a", ".flac", ".wav", ".aac", ".ogg", ".wma"],
    description: "Audio files (mp3, m4a, flac, etc.)"
  },
  "Movies": {
    extensions: [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".webm"],
    description: "Video files (mp4, mkv, avi, etc.)"
  },
  "TV Shows": {
    extensions: [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".m4v", ".webm"],
    description: "Video files (mp4, mkv, avi, etc.)"
  },
  "Pictures": {
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".heic"],
    description: "Image files (jpg, png, gif, etc.)"
  },
  "Audio Books": {
    extensions: [".mp3", ".m4a", ".m4b", ".aac", ".ogg", ".wma"],
    description: "Audio files (mp3, m4a, m4b, etc.)"
  }
};

export function getFilterForFolder(folderName) {
  // Case-insensitive matching for folder names
  const normalizedName = folderName.toLowerCase();
  const match = Object.entries(folderFilters).find(([key]) => 
    key.toLowerCase() === normalizedName
  );
  
  return match ? match[1] : null;
}

export function isFileAllowed(filename, folderName) {
  const filter = getFilterForFolder(folderName);
  if (!filter) return true; // If no filter defined, allow all files
  
  const ext = filename.toLowerCase().slice(filename.lastIndexOf('.'));
  return filter.extensions.includes(ext);
}

export function getAcceptString(folderName) {
  const filter = getFilterForFolder(folderName);
  if (!filter) return '';
  
  return filter.extensions.join(',');
}

export function getFolderDescription(folderName) {
  const filter = getFilterForFolder(folderName);
  return filter ? filter.description : "All files";
}

```

### frontend\src\stores\highscores.js

```javascript
import { writable } from 'svelte/store';

function createHighScoreStore() {
    const { subscribe, set, update } = writable({});

    return {
        subscribe,
        addScore: (username, score) => {
            update(scores => {
                if (!username) return scores;
                
                const newScores = { ...scores };
                if (!newScores[username]) {
                    newScores[username] = {
                        currentSession: 0,
                        allTime: []
                    };
                }

                // Update session high score if new score is higher
                if (score > newScores[username].currentSession) {
                    newScores[username].currentSession = score;
                }

                // Also maintain all-time scores
                newScores[username].allTime.push(score);
                newScores[username].allTime.sort((a, b) => b - a);
                newScores[username].allTime = newScores[username].allTime.slice(0, 5);
                
                localStorage.setItem('flappyScores', JSON.stringify(
                    Object.fromEntries(
                        Object.entries(newScores).map(([user, data]) => [user, data.allTime])
                    )
                ));

                return newScores;
            });
        },
        clearSession: (username) => {
            update(scores => {
                if (!username || !scores[username]) return scores;
                const newScores = { ...scores };
                newScores[username].currentSession = 0;
                return newScores;
            });
        },
        reset: () => {
            localStorage.removeItem('flappyScores');
            set({});
        }
    };
}

export const highScores = createHighScoreStore();

```

### frontend\src\stores\networkScores.js

```javascript
import { writable } from 'svelte/store';

const BASE_URL = "https://ftpserve.w3d.box.ca"; // Match your server URL

function createNetworkScoreStore() {
    const { subscribe, set } = writable({});

    return {
        subscribe,
        addScore: async (username, score, ftpConfig) => {
            try {
                const response = await fetch(`${BASE_URL}/scores`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username,
                        score,
                        ftpConfig
                    })
                });

                const data = await response.json();
                if (data.success) {
                    set(data.scores);
                } else {
                    console.error('Error saving score:', data.error);
                }
            } catch (e) {
                console.error('Error saving network score:', e);
            }
        },
        loadScores: async (ftpConfig) => {
            try {
                const response = await fetch(`${BASE_URL}/scores`, {
                    method: 'GET',
                    headers: {
                        'Authorization': JSON.stringify(ftpConfig)
                    }
                });

                const data = await response.json();
                if (data.success) {
                    set(data.scores);
                } else {
                    console.error('Error loading scores:', data.error);
                }
            } catch (e) {
                console.error('Error loading network scores:', e);
            }
        }
    };
}

export const networkScores = createNetworkScoreStore();

```

### frontend\src\utils\messageParser.js

```javascript
// messageParser.js
const URL_REGEX = /(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/g;
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

export function parseMessage(text) {
    const parts = [];
    let lastIndex = 0;

    // Find all URLs in the text
    const matches = Array.from(text.matchAll(URL_REGEX));
    
    matches.forEach(match => {
        const [url] = match;
        const startIndex = match.index;
        
        // Add text before the URL
        if (startIndex > lastIndex) {
            parts.push({
                type: 'text',
                content: text.slice(lastIndex, startIndex)
            });
        }
        
        // Check if URL is an image
        const isImage = IMAGE_EXTENSIONS.some(ext => 
            url.toLowerCase().endsWith(ext)
        );
        
        // Add the URL/image
        parts.push({
            type: isImage ? 'image' : 'link',
            content: url
        });
        
        lastIndex = startIndex + url.length;
    });
    
    // Add remaining text
    if (lastIndex < text.length) {
        parts.push({
            type: 'text',
            content: text.slice(lastIndex)
        });
    }
    
    return parts;
}

export function sanitizeMessage(text) {
    // Basic XSS protection
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

```

### frontend\src\vite-env.d.ts

```typescript
/// <reference types="svelte" />
/// <reference types="vite/client" />

```

### frontend\svelte.config.js

```javascript
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: vitePreprocess(),
}

```

### frontend\vite.config.js

```javascript
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // If your hosting environment needs to see the domain, also set allowedHosts
    allowedHosts: ['upload.w3d.box.ca'],
  fs: {
    allow: ['..']
  },
  // For HMR to use your domain + SSL:
  hmr: {
    protocol: 'wss',
    host: 'upload.w3d.box.ca',
    port: 5173  // If you're behind an HTTPS proxy, it’s often 443 externally
  }
 },
 assetsInclude: ['**/*.png', '**/*.wav', '**/*.ttf']
})

```

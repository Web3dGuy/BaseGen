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

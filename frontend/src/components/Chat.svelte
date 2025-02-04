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


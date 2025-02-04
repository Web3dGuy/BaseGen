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

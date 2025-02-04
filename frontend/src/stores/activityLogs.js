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

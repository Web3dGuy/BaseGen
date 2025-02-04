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

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

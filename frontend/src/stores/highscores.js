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

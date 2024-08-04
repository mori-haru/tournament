document.addEventListener('DOMContentLoaded', () => {
    const entryForm = document.getElementById('entryForm');
    const participantNameInput = document.getElementById('participantName');
    const createFirstRoundButton = document.getElementById('createFirstRound');
    const createFinalRoundButton = document.getElementById('createFinalRound');
    const resetTournamentButton = document.getElementById('resetTournament');

    if (entryForm) {
        entryForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const participantName = participantNameInput.value.trim();
            if (participantName) {
                fetch('/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({ name: participantName })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        console.error('Error adding participant');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }

    if (createFirstRoundButton) {
        createFirstRoundButton.addEventListener('click', (event) => {
            event.preventDefault();
            fetch('/create_first_round', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    console.error('Error creating first round');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    if (createFinalRoundButton) {
        createFinalRoundButton.addEventListener('click', (event) => {
            event.preventDefault();
            fetch('/create_final_round', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchAndDrawBracket();
                } else {
                    console.error('Error creating final round');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    document.body.addEventListener('submit', (event) => {
        if (event.target.classList.contains('resultForm')) {
            event.preventDefault();
            const form = event.target;
            const matchId = form.getAttribute('data-match-id');
            const winnerId = form.querySelector('.winnerSelect').value;
            fetch('/match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ match_id: matchId, winner_id: winnerId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchAndDrawBracket();
                } else {
                    console.error('Error updating match');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    if (resetTournamentButton) {
        resetTournamentButton.addEventListener('click', (event) => {
            event.preventDefault();
            fetch('/reset', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    console.error('Error resetting tournament');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    const canvas = document.getElementById('tournamentCanvas');
    const context = canvas.getContext('2d');
    const resultModal = document.getElementById('resultModal');
    const resultForm = document.getElementById('resultForm');
    const winnerSelect = document.getElementById('winnerSelect');
    const cancelButton = document.getElementById('cancelButton');
    let selectedMatch = null;

    const playerBoxHeight = 16;
    const boxPadding = 8;
    const matchHeight = 40;
    const matchGap = 20;
    const roundGap = 150;
    let matches = [];

    function drawBracket(matches, x, y) {
        const totalRounds = 4; // ベスト16のトーナメント
        const matchHeight = 40;
        const matchGap = 20;
        const roundGap = 150;
        const playerBoxHeight = 16;
        const boxPadding = 8;

        function drawMatch(player1, player2, x, y) {
            // プレイヤー1の名前を描画し、枠線を描く
            context.fillText(player1, x, y);
            const player1Metrics = context.measureText(player1);
            const player1Width = player1Metrics.width;
            context.strokeRect(x - 2, y - playerBoxHeight, 150, playerBoxHeight + boxPadding);

            // プレイヤー2の名前を描画し、枠線を描く
            context.fillText(player2, x, y + matchHeight);
            const player2Metrics = context.measureText(player2);
            const player2Width = player2Metrics.width;
            context.strokeRect(x - 2, y + matchHeight - playerBoxHeight, 150, playerBoxHeight + boxPadding);

            // 枠線の中央に線を引く
            const midY1 = y - playerBoxHeight + (playerBoxHeight + boxPadding) / 2;
            const midY2 = y + matchHeight - playerBoxHeight + (playerBoxHeight + boxPadding) / 2;
            context.moveTo(x + 150, (midY1 + midY2) / 2);
            context.lineTo(x + roundGap, (midY1 + midY2) / 2);
            context.stroke();
        }

        let matchesPerRound = 8; // 最初のラウンドの試合数
        let yOffset = y;

        for (let round = 1; round <= totalRounds; round++) {
            let currentX = x + (round - 1) * roundGap;
            yOffset = y;

            for (let i = 0; i < matchesPerRound; i++) {
                const match = matches.shift(); // 配列から次の試合を取得
                const player1 = match && match.player1 ? match.player1.name : '不戦勝';
                const player2 = match && match.player2 ? match.player2.name : '不戦勝';
                drawMatch(player1, player2, currentX, yOffset);
                yOffset += matchHeight + matchGap;
            }

            matchesPerRound /= 2; // 次のラウンドの試合数を半分にする
            yOffset += matchGap * matchesPerRound; // 各ラウンド間のスペースを追加
        }
    }

    /*function fetchAndDrawBracket() {
        fetch('/bracket_data')
            .then(response => response.json())
            .then(data => {
                context.clearRect(0, 0, canvas.width, canvas.height);
                matches = data.final_round_matches;
                drawBracket(matches, 20, 20);
            });
    }*/

    function fetchAndDrawBracket() {
        fetch('/bracket_data')
            .then(response => response.json())
            .then(data => {
                const finalRoundBracket = document.getElementById('finalRoundBracket');
                finalRoundBracket.innerHTML = ''; // 既存のトーナメント表をクリア
                const rounds = data.final_round_bracket;
    
                rounds.forEach(round => {
                    const roundDiv = document.createElement('div');
                    roundDiv.classList.add('round');
    
                    round.matches.forEach(match => {
                        const matchDiv = document.createElement('div');
                        matchDiv.classList.add('match');
    
                        const winnerSelect = document.createElement('select');
                        winnerSelect.name = 'winner_id';
                        winnerSelect.classList.add('winnerSelect');
    
                        const optionPlaceholder = document.createElement('option');
                        optionPlaceholder.value = '';
                        optionPlaceholder.selected = true;
                        optionPlaceholder.disabled = true;
                        optionPlaceholder.textContent = '勝者を選択';
                        winnerSelect.appendChild(optionPlaceholder);
    
                        match.players.forEach(player => {
                            const option = document.createElement('option');
                            option.value = player.id;
                            option.textContent = player.name;
                            winnerSelect.appendChild(option);
                        });
    
                        const resultForm = document.createElement('form');
                        resultForm.classList.add('resultForm');
                        resultForm.dataset.matchId = match.id;
    
                        const updateButton = document.createElement('button');
                        updateButton.type = 'submit';
                        updateButton.textContent = '結果を更新';
    
                        resultForm.appendChild(winnerSelect);
                        resultForm.appendChild(updateButton);
                        matchDiv.appendChild(resultForm);
                        roundDiv.appendChild(matchDiv);
                    });
    
                    finalRoundBracket.appendChild(roundDiv);
                });
            });
    }
    

    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        let yOffset = 20;

        matches.forEach((match, index) => {
            if (x > 20 && x < 170 && y > yOffset && y < yOffset + matchHeight + matchGap) {
                selectedMatch = match;
                resultModal.style.display = 'block';
                winnerSelect.innerHTML = `
                    <option value="" selected disabled>勝者を選択</option>
                    <option value="${match.player1.id}">${match.player1.name}</option>
                    ${match.player2 ? `<option value="${match.player2.id}">${match.player2.name}</option>` : ''}
                `;
            }
            yOffset += matchHeight + matchGap;
        });
    });

    resultForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const winnerId = winnerSelect.value;
        fetch('/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ match_id: selectedMatch.id, winner_id: winnerId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultModal.style.display = 'none';
                selectedMatch = null;
                fetchAndDrawBracket();
            } else {
                console.error('Error updating match');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    cancelButton.addEventListener('click', () => {
        selectedMatch = null;
        resultModal.style.display = 'none';
    });

    fetchAndDrawBracket();
});

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
        let yOffset = y;
        matches.forEach((match, index) => {
            const player1 = match.player1 ? match.player1.name : '不戦勝';
            const player2 = match.player2 ? match.player2.name : '不戦勝';

            const midY = yOffset + (matchHeight / 2) + (boxPadding / 2);

            // プレイヤー1の名前を描画し、枠線を描く
            context.fillText(player1, x, yOffset);
            context.strokeRect(x - 2, yOffset - playerBoxHeight, 150, playerBoxHeight + boxPadding);

            // プレイヤー2の名前を描画し、枠線を描く
            context.fillText(player2, x, yOffset + matchHeight);
            context.strokeRect(x - 2, yOffset + matchHeight - playerBoxHeight, 150, playerBoxHeight + boxPadding);

            // 枠線の中央に線を引く
            context.moveTo(x + 150, midY);
            context.lineTo(x + roundGap, midY);
            context.stroke();

            yOffset += matchHeight + matchGap;
        });
    }

    function fetchAndDrawBracket() {
        fetch('/bracket_data')
            .then(response => response.json())
            .then(data => {
                context.clearRect(0, 0, canvas.width, canvas.height);
                matches = data.final_round_matches;
                drawBracket(matches, 20, 20);
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


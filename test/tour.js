window.onload = function() {
    function updateSelectOptions() {
        const mappings = [
            { textboxes: ['player1', 'player2'], select: 'match1' },
            { textboxes: ['player3', 'player4'], select: 'match2' },
            { textboxes: ['player5', 'player6'], select: 'match3' },
            { textboxes: ['player7', 'player8'], select: 'match4' },
            { textboxes: ['player9', 'player10'], select: 'match5' },
            { textboxes: ['player11', 'player12'], select: 'match6' },
            { textboxes: ['player13', 'player14'], select: 'match7' },
            { textboxes: ['player15', 'player16'], select: 'match8' },
            { textboxes: ['player17', 'player18'], select: 'match9' },
            { textboxes: ['player19', 'player20'], select: 'match10' },
            { textboxes: ['player21', 'player22'], select: 'match11' },
            { textboxes: ['player23', 'player24'], select: 'match12' },
            { textboxes: ['player25', 'player26'], select: 'match13' },
            { textboxes: ['player27', 'player28'], select: 'match14' },
            { textboxes: ['player29', 'player30'], select: 'match15' },
            { textboxes: ['player31', 'player32'], select: 'match16' }
        ];

        // 左側と右側のセレクトボックスのオプションを更新
        mappings.forEach(mapping => {
            const player1 = document.getElementById(mapping.textboxes[0]).value.trim();
            const player2 = document.getElementById(mapping.textboxes[1]).value.trim();
            const match = document.getElementById(mapping.select);
            const selectedOption = match.value; // 現在選択されているオプションを保存

            const option1 = player1 ? player1 : '-- 未入力 --';
            const option2 = player2 ? player2 : '-- 未入力 --';

            match.innerHTML = `
                <option value="${option1}">${option1}</option>
                <option value="${option2}">${option2}</option>
            `;

            match.value = selectedOption; // 前の選択状態を復元
        });

        // 第二ラウンドのセレクトボックスのオプションを更新
        const secondRoundMappings = [
            { selects: ['match1', 'match2'], select: 'match17' },
            { selects: ['match3', 'match4'], select: 'match18' },
            { selects: ['match5', 'match6'], select: 'match19' },
            { selects: ['match7', 'match8'], select: 'match20' },
            { selects: ['match9', 'match10'], select: 'match21' },
            { selects: ['match11', 'match12'], select: 'match22' },
            { selects: ['match13', 'match14'], select: 'match23' },
            { selects: ['match15', 'match16'], select: 'match24' },
            { selects: ['match17', 'match18'], select: 'match25' },
            { selects: ['match19', 'match20'], select: 'match26' },
            { selects: ['match21', 'match22'], select: 'match27' },
            { selects: ['match23', 'match24'], select: 'match28' },
            { selects: ['match25', 'match26'], select: 'match29' },
            { selects: ['match27', 'match28'], select: 'match30' },
            { selects: ['match29', 'match30'], select: 'match31' },
        ];

        secondRoundMappings.forEach(mapping => {
            const match1 = document.getElementById(mapping.selects[0]).value;
            const match2 = document.getElementById(mapping.selects[1]).value;
            const nextMatch = document.getElementById(mapping.select);
            const selectedOption = nextMatch.value; // 現在選択されているオプションを保存

            nextMatch.innerHTML = `
                <option value="${match1}">${match1}</option>
                <option value="${match2}">${match2}</option>
            `;

            nextMatch.value = selectedOption; // 前の選択状態を復元

        });
    }

    document.querySelectorAll('.textbox[type="text"]').forEach(input => {
        input.addEventListener('input', updateSelectOptions);
    });

    document.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', updateSelectOptions);
    });

    updateSelectOptions(); // 初期状態でオプションを更新


    document.getElementById('match1').addEventListener('change', function() {
        // セレクトボックスの選択肢の値を取得
        const selectedOption = this.value;
      
        // 線を赤くする関数
        function setLinesRed() {
          document.getElementById('line1').style.stroke = 'red';
          document.getElementById('line3').style.stroke = 'red';
          document.getElementById('line5').style.stroke = 'red';
        }
      
        // 線を黒に戻す関数
        function setLinesBlack() {
          document.getElementById('line1').style.stroke = 'black';
          document.getElementById('line3').style.stroke = 'black';;
        }
      
        // プレイヤー1が選ばれた場合
        if (selectedOption === 'player1') {
          setLinesRed();
        } 
        // プレイヤー2が選ばれた場合
        else if (selectedOption === 'player2') {
          // プレイヤー1の線を黒に戻す
          setLinesBlack();
          // プレイヤー2の線を赤くする処理を追加する場合はここに記述
        } 
      });
      
};



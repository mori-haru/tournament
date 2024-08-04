

# 最初のスクリプト
'''from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    matches = Match.query.all()
    return render_template('index.html', participants=participants, matches=matches)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants), 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id)
        matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)'''

# 3番目のスクリプト
'''from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()

    # 決勝トーナメントの作成
    if all(m.winner_id is not None for m in Match.query.filter_by(round='first').all()):
        create_final_round()

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
        matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

if __name__ == '__main__':
    app.run(debug=True)'''

# エラーなし
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)  # 追加
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()

    # 決勝トーナメントの作成
    if all(m.winner_id is not None for m in Match.query.filter_by(round='first').all()):
        create_final_round()

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
        matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

if __name__ == '__main__':
    app.run(debug=True)'''

# エラーなし改善版
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
        matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

if __name__ == '__main__':
    app.run(debug=True)'''
    

# no.6  
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            # 奇数の場合、最後の勝者は不戦勝で次のラウンドに進む
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

if __name__ == '__main__':
    app.run(debug=True)'''
# no.7  
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    print(f"First round complete: {all_first_round_matches_complete}")  # デバッグ用出力
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    print(f"Winners: {[winner.name for winner in winners]}")  # デバッグ用出力
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            # 奇数の場合、最後の勝者は不戦勝で次のラウンドに進む
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info


if __name__ == '__main__':
    app.run(debug=True)'''
  
# no.8 デバッグ追加 
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    print(f"First round matches: {first_round_matches}")  # デバッグ用出力
    print(f"All first round matches complete: {all_first_round_matches_complete}")  # デバッグ用出力
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = Match.query.get(match_id)
    match.winner_id = winner_id
    db.session.commit()
    print(f"Updated match {match_id} with winner {winner_id}")  # デバッグ用出力
    
    # 追加: 試合結果を更新後に全試合結果が完了しているかを確認
    first_round_matches = Match.query.filter_by(round='first').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    print(f"After update, all first round matches complete: {all_first_round_matches_complete}")  # デバッグ用出力
    
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()
    print(f"First round matches created: {matches}")  # デバッグ用出力

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    print(f"Winners: {[winner.name for winner in winners]}")  # デバッグ用出力
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            # 奇数の場合、最後の勝者は不戦勝で次のラウンドに進む
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

if __name__ == '__main__':
    app.run(debug=True)'''
# no.9 正常に動作するやつ
'''import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    print(f"First round matches: {first_round_matches}")  # デバッグ用出力
    for match in first_round_matches:
        print(f"Match {match.id}: Player 1 - {match.player1.name}, Player 2 - {match.player2.name if match.player2 else '不戦勝'}, Winner - {match.winner.name if match.winner else '未決定'}")
    print(f"All first round matches complete: {all_first_round_matches_complete}")  # デバッグ用出力
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)  # 修正: Query.get() から Session.get() へ変更
    match.winner_id = winner_id
    db.session.commit()
    print(f"Updated match {match_id} with winner {winner_id}")  # デバッグ用出力
    
    # 追加: 試合結果を更新後に全試合結果が完了しているかを確認
    first_round_matches = Match.query.filter_by(round='first').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    for match in first_round_matches:
        print(f"After update - Match {match.id}: Player 1 - {match.player1.name}, Player 2 - {match.player2.name if match.player2 else '不戦勝'}, Winner - {match.winner.name if match.winner else '未決定'}")
    print(f"After update, all first round matches complete: {all_first_round_matches_complete}")  # デバッグ用出力
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()
    print(f"First round matches created: {matches}")  # デバッグ用出力

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    print(f"Winners: {[winner.name for winner in winners]}")  # デバッグ用出力
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            # 奇数の場合、最後の勝者は不戦勝で次のラウンドに進む
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/create_first_round')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

@app.route('/debug')
def debug():
    matches = Match.query.all()
    debug_info = {
        "matches": [{
            "id": match.id,
            "player1": match.player1.name,
            "player2": match.player2.name if match.player2 else "不戦勝",
            "winner": match.winner.name if match.winner else "未決定",
            "round": match.round
        } for match in matches]
    }
    return debug_info

if __name__ == '__main__':
    app.run(debug=True)'''
    

'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join('/Users/tomimorisatoshihare/Scraping/Ore/scrapingEnv/tournament_app', 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'},
    'participant': {'password': 'participant_pass', 'role': 'participant'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('login'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete, role=session.get('role'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required(role='participant')
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return redirect(url_for('index'))

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return redirect(url_for('index'))

@app.route('/match', methods=['POST'])
@login_required()
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)  # 修正: Query.get() から Session.get() へ変更
    match.winner_id = winner_id
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('index'))

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    # 奇数の参加者がいる場合、最後の参加者は不戦勝
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            # 奇数の場合、最後の勝者は不戦勝で次のラウンドに進む
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = {
        "tables": inspector.get_table_names(),
        "columns": {table_name: [col['name'] for col in inspector.get_columns(table_name)] for table_name in inspector.get_table_names()}
    }
    return schema_info

@app.route('/debug')
def debug():
    matches = Match.query.all()
    debug_info = {
        "matches": [{
            "id": match.id,
            "player1": match.player1.name,
            "player2": match.player2.name if match.player2 else "不戦勝",
            "winner": match.winner.name if match.winner else "未決定",
            "round": match.round
        } for match in matches]
    }
    return debug_info

if __name__ == '__main__':
    app.run(debug=True)'''

'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

# 上から順番にトーナメント決定
def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()
    
# ランダム
import random

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)'''

'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

# ランダムで決勝ラウンドを生成
def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)'''


'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

# ランダムで決勝ラウンドを生成
def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
            matches.append(match)
        else:
            match = Match(player1_id=winners[i].id, player2_id=None, round='final')
            matches.append(match)
    db.session.add_all(matches)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)'''


'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Ensure unique names

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    if Participant.query.filter_by(name=name).first():
        return jsonify(success=False, message="Participant already exists")
    
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    
    # すでに存在する初戦トーナメントマッチを削除
    Match.query.filter_by(round='first').delete()
    
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

# 決勝トーナメントをベスト16として設定
def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    winners = winners[:16]  # ベスト16に制限
    matches = []
    
    # すでに存在する決勝トーナメントマッチを削除
    Match.query.filter_by(round='final').delete()
    
    for i in range(0, len(winners), 2):
        match = Match(player1_id=winners[i].id, player2_id=winners[i+1].id, round='final')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)'''

'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Ensure unique names

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    if Participant.query.filter_by(name=name).first():
        return jsonify(success=False, message="Participant already exists")
    
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants) - 1, 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

# 決勝トーナメントをベスト16として設定
def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    
    # 不戦勝を追加して16人に満たす
    while len(winners) < 16:
        winners.append(None)
    
    matches = []
    for i in range(0, 16, 2):
        player1 = winners[i]
        player2 = winners[i + 1] if i + 1 < len(winners) else None
        match = Match(player1_id=player1.id if player1 else None, player2_id=player2.id if player2 else None, round='final')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)'''


'''import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Ensure unique names

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    if Participant.query.filter_by(name=name).first():
        return jsonify(success=False, message="Participant already exists")
    
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data')
def bracket_data():
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter_by(round='final').all()

    def match_to_dict(match):
        return {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
            'winner_id': match.winner_id
        }

    return jsonify({
        'first_round_matches': [match_to_dict(m) for m in first_round_matches],
        'final_round_matches': [match_to_dict(m) for m in final_round_matches]
    })
    
@app.route('/bracket_data', methods=['GET'])
def bracket_data():
    final_round_matches = Match.query.filter_by(round='final').all()
    matches_data = []
    for match in final_round_matches:
        match_data = {
            'id': match.id,
            'player1': {'id': match.player1.id, 'name': match.player1.name} if match.player1 else None,
            'player2': {'id': match.player2.id, 'name': match.player2.name} if match.player2 else None,
        }
        matches_data.append(match_data)
    return jsonify({'final_round_matches': matches_data})

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants), 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()
    
@app.route('/bracket_data', methods=['GET'])
def bracket_data():
    rounds = {}
    final_round_matches = Match.query.filter(Match.round.like('round_%')).all()
    
    for match in final_round_matches:
        round_number = int(match.round.split('_')[1])
        if round_number not in rounds:
            rounds[round_number] = []
        player1 = Participant.query.get(match.player1_id)
        player2 = Participant.query.get(match.player2_id)
        rounds[round_number].append({
            'id': match.id,
            'players': [
                {'id': player1.id, 'name': player1.name} if player1 else {'id': None, 'name': '不戦勝'},
                {'id': player2.id, 'name': player2.name} if player2 else {'id': None, 'name': '不戦勝'}
            ]
        })
    
    return jsonify({'final_round_bracket': [{'matches': matches} for round_number, matches in sorted(rounds.items())]})

def create_final_round():
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    
    # 不戦勝を追加して16人に満たす
    while len(winners) < 16:
        winners.append(None)
    
    matches = []
    for i in range(0, 16, 2):
        player1 = winners[i]
        player2 = winners[i + 1] if winners[i + 1] else None
        match = Match(player1_id=player1.id if player1 else None, player2_id=player2.id if player2 else None, round='final')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()
    
    
@app.route('/create_final_round', methods=['POST'])
def create_final_round():
    # ベスト16の試合を作成
    participants = Participant.query.all()
    num_participants = len(participants)
    
    # ランダムで不戦勝を選択する
    if num_participants % 2 != 0:
        bye_participant = random.choice(participants)
        # 不戦勝を設定
        match = Match(player1_id=bye_participant.id, round='final')
        db.session.add(match)
        participants.remove(bye_participant)
    
    # 残りの参加者でトーナメントを作成
    for i in range(0, len(participants), 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i + 1].id, round='final')
        db.session.add(match)
    
    db.session.commit()
    return jsonify({'success': True})
    

@app.route('/create_final_round', methods=['POST'])
def create_final_round():
    # ベスト16の試合を作成
    participants = Participant.query.all()
    num_participants = len(participants)
    
    # 残りの参加者でトーナメントを作成
    matches = []
    round = 1
    
    # ランダムで不戦勝を選択する（参加者が奇数の場合）
    if num_participants % 2 != 0:
        bye_participant = random.choice(participants)
        match = Match(player1_id=bye_participant.id, round=f'round_{round}')
        db.session.add(match)
        participants.remove(bye_participant)
        matches.append(match)
    
    # 最初のラウンドの試合を作成
    for i in range(0, len(participants), 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i + 1].id, round=f'round_{round}')
        db.session.add(match)
        matches.append(match)
    
    db.session.commit()
    
    # 次のラウンドの試合を作成
    while len(matches) > 1:
        next_round_matches = []
        round += 1
        
        for i in range(0, len(matches), 2):
            if i + 1 < len(matches):
                match = Match(round=f'round_{round}')
                db.session.add(match)
                next_round_matches.append(match)
            else:
                # 奇数の場合、不戦勝を設定
                match = matches[i]
                next_round_matches.append(match)
        
        matches = next_round_matches
    
    db.session.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)'''


import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import random

app = Flask(__name__)

# データベースファイルのパスを指定
db_path = os.path.join(os.path.dirname(__file__), 'tournament.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Ensure unique names

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    round = db.Column(db.String(50), nullable=False)
    player1 = db.relationship("Participant", foreign_keys=[player1_id])
    player2 = db.relationship("Participant", foreign_keys=[player2_id])
    winner = db.relationship("Participant", foreign_keys=[winner_id])

# アプリケーションコンテキスト内でcreate_all()を呼び出す
with app.app_context():
    db.create_all()

users = {
    'admin': {'password': 'admin_pass', 'role': 'admin'}
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('admin'))
            if role and users[session['username']]['role'] != role:
                return redirect(url_for('choose'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/participant')
def participant():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter(Match.round.like('round_%')).all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('index.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin.html')

@app.route('/admin_dashboard')
@login_required(role='admin')
def admin_dashboard():
    participants = Participant.query.all()
    first_round_matches = Match.query.filter_by(round='first').all()
    final_round_matches = Match.query.filter(Match.round.like('round_%')).all()
    all_first_round_matches_complete = all(m.winner_id is not None for m in first_round_matches)
    return render_template('admin_dashboard.html', participants=participants, first_round_matches=first_round_matches, final_round_matches=final_round_matches, all_first_round_matches_complete=all_first_round_matches_complete)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('choose'))

@app.route('/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    if Participant.query.filter_by(name=name).first():
        return jsonify(success=False, message="Participant already exists")
    
    new_participant = Participant(name=name)
    db.session.add(new_participant)
    db.session.commit()
    return jsonify(success=True)

@app.route('/create_first_round', methods=['POST'])
@login_required(role='admin')
def create_first_round_route():
    create_first_round()
    return jsonify(success=True)

@app.route('/create_final_round', methods=['POST'])
@login_required(role='admin')
def create_final_round_route():
    create_final_round()
    return jsonify(success=True)

@app.route('/match', methods=['POST'])
def update_match():
    match_id = request.form.get('match_id')
    winner_id = request.form.get('winner_id')
    match = db.session.get(Match, match_id)
    match.winner_id = winner_id
    db.session.commit()
    return jsonify(success=True)

@app.route('/reset', methods=['POST'])
@login_required(role='admin')
def reset():
    db.drop_all()
    db.create_all()
    return jsonify(success=True)

@app.route('/bracket_data', methods=['GET'])
def bracket_data():
    rounds = {}
    final_round_matches = Match.query.filter(Match.round.like('round_%')).all()
    
    for match in final_round_matches:
        round_number = int(match.round.split('_')[1])
        if round_number not in rounds:
            rounds[round_number] = []
        player1 = Participant.query.get(match.player1_id)
        player2 = Participant.query.get(match.player2_id)
        rounds[round_number].append({
            'id': match.id,
            'players': [
                {'id': player1.id, 'name': player1.name} if player1 else {'id': None, 'name': '不戦勝'},
                {'id': player2.id, 'name': player2.name} if player2 else {'id': None, 'name': '不戦勝'}
            ]
        })
    
    return jsonify({'final_round_bracket': [{'matches': matches} for round_number, matches in sorted(rounds.items())]})

def create_first_round():
    participants = Participant.query.all()
    random.shuffle(participants)
    matches = []
    for i in range(0, len(participants), 2):
        match = Match(player1_id=participants[i].id, player2_id=participants[i+1].id, round='first')
        matches.append(match)
    
    if len(participants) % 2 == 1:
        last_participant = participants[-1]
        match = Match(player1_id=last_participant.id, player2_id=None, round='first')
        matches.append(match)
    
    db.session.add_all(matches)
    db.session.commit()

def create_final_round():
    # 初戦の勝者を取得
    winners = [match.winner for match in Match.query.filter_by(round='first').all() if match.winner_id is not None]
    random.shuffle(winners)
    
    # 残りの参加者でトーナメントを作成
    matches = []
    round_number = 1
    
    # 最初のラウンドの試合を作成
    for i in range(0, len(winners), 2):
        player1 = winners[i]
        player2 = winners[i + 1] if i + 1 < len(winners) else None
        match = Match(player1_id=player1.id if player1 else None, player2_id=player2.id if player2 else None, round=f'round_{round_number}')
        db.session.add(match)
        matches.append(match)
    
    db.session.commit()
    
    # 次のラウンドの試合を作成
    while len(matches) > 1:
        next_round_matches = []
        round_number += 1
        
        for i in range(0, len(matches), 2):
            if i + 1 < len(matches):
                match = Match(round=f'round_{round_number}')
                db.session.add(match)
                next_round_matches.append(match)
            else:
                # 奇数の場合、不戦勝を設定
                match = matches[i]
                next_round_matches.append(match)
        
        matches = next_round_matches
    
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)


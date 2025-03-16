import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ai_analysis import analyze_brainstorming, generate_action_items, suggest_improvements, summarize_text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcripts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    transcripts = db.relationship('Transcript', backref='user', lazy=True)

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    transcripts = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
    return render_template('index.html', transcripts=transcripts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/save_transcript', methods=['POST'])
@login_required
def save_transcript():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
        
        transcript = Transcript(
            title=title,
            content=content,
            user_id=current_user.id
        )
        
        db.session.add(transcript)
        db.session.commit()
        
        return jsonify({
            'id': transcript.id,
            'title': transcript.title,
            'created_at': transcript.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_transcript/<int:id>')
@login_required
def get_transcript(id):
    try:
        transcript = Transcript.query.get_or_404(id)
        if transcript.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        return jsonify({
            'id': transcript.id,
            'title': transcript.title,
            'content': transcript.content,
            'created_at': transcript.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_transcript/<int:id>')
@login_required
def analyze_transcript(id):
    try:
        transcript = Transcript.query.get_or_404(id)
        if transcript.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Debug log
        app.logger.info(f"Analyzing transcript {id} with content: {transcript.content}")
            
        # Get analysis results with better error handling
        try:
            analysis = analyze_brainstorming(transcript.content)
            app.logger.info(f"Analysis result: {analysis}")
            if not analysis.get('success'):
                return jsonify({'error': analysis.get('error', 'Analysis failed')}), 500
                
            action_items = generate_action_items(transcript.content)
            app.logger.info(f"Action items result: {action_items}")
            if not action_items.get('success'):
                return jsonify({'error': action_items.get('error', 'Action items generation failed')}), 500
                
            suggestions = suggest_improvements(transcript.content)
            app.logger.info(f"Suggestions result: {suggestions}")
            if not suggestions.get('success'):
                return jsonify({'error': suggestions.get('error', 'Suggestions generation failed')}), 500
                
            summary = summarize_text(transcript.content)
            app.logger.info(f"Summary result: {summary}")
            if not summary.get('success'):
                return jsonify({'error': summary.get('error', 'Summary generation failed')}), 500
            
            return jsonify({
                'analysis': analysis.get('analysis', ''),
                'action_items': action_items.get('action_items', ''),
                'suggestions': suggestions.get('suggestions', ''),
                'summary': summary.get('summary', '')
            })
            
        except Exception as e:
            app.logger.error(f"Analysis error: {str(e)}")
            return jsonify({'error': f"Analysis error: {str(e)}"}), 500
        
    except Exception as e:
        app.logger.error(f"Route error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_transcript/<int:id>', methods=['POST'])
@login_required
def delete_transcript(id):
    try:
        transcript = Transcript.query.get_or_404(id)
        if transcript.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        db.session.delete(transcript)
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)

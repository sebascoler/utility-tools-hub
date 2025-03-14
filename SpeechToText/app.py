from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ai_analysis import analyze_brainstorming, generate_action_items, suggest_improvements
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        transcripts = Transcript.query.filter_by(user_id=current_user.id).order_by(Transcript.created_at.desc()).all()
        return render_template('index.html', transcripts=transcripts)
    return redirect(url_for('login'))

@app.route('/analyze_transcript/<int:transcript_id>')
@login_required
def analyze_transcript(transcript_id):
    transcript = Transcript.query.get_or_404(transcript_id)
    if transcript.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get comprehensive analysis
    analysis = analyze_brainstorming(transcript.content)
    if not analysis['success']:
        return jsonify(analysis), 500
    
    # Get action items
    actions = generate_action_items(transcript.content)
    if not actions['success']:
        return jsonify(actions), 500
    
    # Get improvement suggestions
    suggestions = suggest_improvements(transcript.content)
    if not suggestions['success']:
        return jsonify(suggestions), 500
    
    return jsonify({
        'success': True,
        'analysis': analysis['analysis'],
        'action_items': actions['action_items'],
        'suggestions': suggestions['suggestions']
    })

@app.route('/get_transcript/<int:transcript_id>')
@login_required
def get_transcript(transcript_id):
    transcript = Transcript.query.get_or_404(transcript_id)
    if transcript.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': transcript.id,
        'title': transcript.title,
        'content': transcript.content,
        'created_at': transcript.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/save_transcript', methods=['POST'])
@login_required
def save_transcript():
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

@app.route('/delete_transcript/<int:transcript_id>', methods=['POST'])
@login_required
def delete_transcript(transcript_id):
    transcript = Transcript.query.get_or_404(transcript_id)
    if transcript.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(transcript)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
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
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/test_analysis')
def test_analysis():
    sample_text = """
    Ideas for improving our team's productivity:
    - Daily standup meetings at 9am
    - Use project management software to track tasks
    - Set up dedicated quiet hours for focused work
    - Regular feedback sessions every Friday
    - Create documentation templates for common tasks
    - Implement code review process
    - Schedule monthly team building activities
    """
    
    analysis = analyze_brainstorming(sample_text)
    action_items = generate_action_items(sample_text)
    suggestions = suggest_improvements(sample_text)
    
    return jsonify({
        'text': sample_text,
        'analysis': analysis,
        'action_items': action_items,
        'suggestions': suggestions
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        # Get analysis results
        analysis_result = analyze_brainstorming(text)
        action_items = generate_action_items(text)
        suggestions = suggest_improvements(text)
        
        return jsonify({
            'text': text,
            'analysis': analysis_result,
            'action_items': action_items,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5064)

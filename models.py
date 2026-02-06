from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)  # JSON格式存储选项
    correct_id = db.Column(db.String(10))  # 正确选项的ID（A/B/C/D）
    correct_answer = db.Column(db.String(10), nullable=False)
    explanation = db.Column(db.Text)
    language = db.Column(db.String(10), nullable=False)  # zh 或 en
    category = db.Column(db.String(50))
    source = db.Column(db.String(100))  # 题目来源
    image_path = db.Column(db.String(200))  # 图片路径
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'

class WrongAnswer(db.Model):
    __tablename__ = 'wrong_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.String(10), nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # 关联题目
    question = db.relationship('Question', backref=db.backref('wrong_answers', lazy=True))
    
    def __repr__(self):
        return f'<WrongAnswer {self.id}: Question {self.question_id}>'

class PracticeSession(db.Model):
    __tablename__ = 'practice_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_type = db.Column(db.String(20), nullable=False)  # practice, review等
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<PracticeSession {self.id}: {self.session_type} - {self.correct_answers}/{self.total_questions}>'
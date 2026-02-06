import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from models import db, Question, WrongAnswer, PracticeSession
from scraper import scrape_questions
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///g1study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_folder = 'static'
db.init_app(app)

# 初始化数据库
with app.app_context():
    db.create_all()

# 静态文件路由
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# 首页
@app.route('/')
def index():
    # 获取统计信息
    total_questions = Question.query.count()
    zh_questions = Question.query.filter_by(language='zh').count()
    en_questions = Question.query.filter_by(language='en').count()
    wrong_answers_count = WrongAnswer.query.count()
    
    # 获取最近的5次练习记录
    recent_sessions = PracticeSession.query.order_by(PracticeSession.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                          total_questions=total_questions,
                          zh_questions=zh_questions,
                          en_questions=en_questions,
                          wrong_answers_count=wrong_answers_count,
                          recent_sessions=recent_sessions)

# 练习页面
@app.route('/practice')
def practice():
    return render_template('practice.html')

# 错题本页面
@app.route('/wrong-answers')
def wrong_answers():
    wrong_items = WrongAnswer.query.order_by(WrongAnswer.timestamp.desc()).all()
    return render_template('wrong_answers.html', wrong_items=wrong_items)

# 练习历史页面
@app.route('/practice-history')
def practice_history():
    sessions = PracticeSession.query.order_by(PracticeSession.created_at.desc()).all()
    return render_template('practice_history.html', sessions=sessions)

# 题库管理页面
@app.route('/question-management')
def question_management():
    return render_template('question_management.html')

# API端点：获取题目（用于题库管理）
@app.route('/api/questions')
def api_questions():
    # 获取筛选参数
    language = request.args.get('language', '')
    source = request.args.get('source', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询
    query = Question.query
    
    if language:
        query = query.filter_by(language=language)
    
    if source:
        query = query.filter_by(source=source)
    
    # 分页查询
    pagination = query.order_by(Question.id).paginate(
        page=page, per_page=per_page, error_out=False)
    
    questions = pagination.items
    
    return jsonify({
        'questions': [{
            'id': q.id,
            'question_text': q.question_text,
            'options': q.options,
            'correct_answer': q.correct_answer,
            'correct_id': q.correct_id,
            'explanation': q.explanation,
            'language': q.language,
            'category': q.category,
            'source': q.source,
            'image_path': q.image_path
        } for q in questions],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page
    })

# API端点：获取练习题目（用于练习模式）
@app.route('/api/practice/questions')
def api_practice_questions():
    # 获取筛选参数
    language = request.args.get('language', 'zh')
    source = request.args.get('source', '')
    limit = request.args.get('limit', 10, type=int)
    
    # 构建查询
    query = Question.query.filter_by(language=language)
    
    if source:
        query = query.filter_by(source=source)
    
    # 随机获取指定数量的题目
    questions = query.order_by(db.func.random()).limit(limit).all()
    
    return jsonify([{
        'id': q.id,
        'question_text': q.question_text,
        'options': json.loads(q.options),
        'correct_answer': q.correct_answer,
        'correct_id': q.correct_id,
        'explanation': q.explanation,
        'language': q.language,
        'category': q.category,
        'source': q.source,
        'image_path': q.image_path
    } for q in questions])

# API端点：获取题目来源列表
@app.route('/api/question-sources')
def api_question_sources():
    sources = db.session.query(Question.source).distinct().all()
    source_list = [source[0] for source in sources if source[0] is not None]
    return jsonify({'sources': source_list})

# API端点：添加题目
@app.route('/api/questions', methods=['POST'])
def api_add_question():
    try:
        data = request.get_json()
        
        # 创建新题目
        question = Question(
            question_text=data['question_text'],
            options=data['options'],
            correct_answer=data['correct_answer'],
            correct_id=data['correct_id'],
            language=data['language'],
            category=data.get('category'),
            source=data.get('source'),
            explanation=data.get('explanation'),
            image_path=data.get('image_path')
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({'success': True, 'id': question.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# API端点：更新题目正确答案
@app.route('/api/questions/<int:question_id>/correct-answer', methods=['PUT'])
def api_update_correct_answer(question_id):
    try:
        data = request.get_json()
        correct_id = data['correct_id']
        
        # 查找题目
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': '题目不存在'}), 404
        
        # 更新正确答案
        question.correct_id = correct_id
        # 同时更新correct_answer字段
        options = json.loads(question.options)
        question.correct_answer = options.get(correct_id, '')
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# API端点：删除题目
@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
def api_delete_question(question_id):
    try:
        # 查找题目
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': '题目不存在'}), 404
        
        # 删除题目
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# API端点：开始练习
@app.route('/api/practice', methods=['POST'])
def api_start_practice():
    data = request.get_json()
    language = data.get('language', 'zh')
    total_questions = data.get('total_questions', 10)
    
    # 创建练习会话
    session = PracticeSession(
        session_type='practice',
        total_questions=total_questions,
        correct_answers=0,
        wrong_answers=0,
        start_time=datetime.now()
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'session_id': session.id})

# API端点：提交答案
@app.route('/api/practice/answer', methods=['POST'])
def api_submit_answer():
    data = request.get_json()
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    
    # 获取题目信息
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': '题目不存在'}), 404
    
    # 使用correct_id判断答案是否正确
    is_correct = user_answer == question.correct_id
    
    # 如果答案错误，记录到错题本
    if not is_correct:
        wrong_answer = WrongAnswer(
            question_id=question_id,
            user_answer=user_answer,
            correct_answer=question.correct_id,  # 使用correct_id而不是correct_answer
            timestamp=datetime.now()
        )
        db.session.add(wrong_answer)
    
    # 更新练习会话
    session = PracticeSession.query.get(session_id)
    if session:  # 确保会话存在
        if is_correct:
            session.correct_answers += 1
        else:
            session.wrong_answers += 1
        db.session.commit()
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question.correct_id  # 返回正确答案ID
    })

# API端点：完成练习
@app.route('/api/practice/finish', methods=['POST'])
def api_finish_practice():
    data = request.get_json()
    session_id = data.get('session_id')
    
    # 更新练习会话结束时间
    session = PracticeSession.query.get(session_id)
    session.end_time = datetime.now()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'total_questions': session.total_questions,
        'correct_answers': session.correct_answers,
        'wrong_answers': session.wrong_answers,
        'score': round((session.correct_answers / session.total_questions) * 100, 2)
    })

# API端点：获取错题列表
@app.route('/api/wrong-answers')
def api_wrong_answers():
    wrong_items = WrongAnswer.query.order_by(WrongAnswer.timestamp.desc()).all()
    result = []
    
    for item in wrong_items:
        question = Question.query.get(item.question_id)
        if question:
            result.append({
                'id': item.id,
                'question_text': question.question_text,
                'user_answer': item.user_answer,
                'correct_answer': item.correct_answer,
                'explanation': question.explanation,
                'timestamp': item.timestamp.isoformat()
            })
    
    return jsonify(result)

# API端点：获取练习历史
@app.route('/api/practice-history')
def api_practice_history():
    sessions = PracticeSession.query.order_by(PracticeSession.created_at.desc()).all()
    result = []
    
    for session in sessions:
        result.append({
            'id': session.id,
            'session_type': session.session_type,
            'total_questions': session.total_questions,
            'correct_answers': session.correct_answers,
            'wrong_answers': session.wrong_answers,
            'start_time': session.start_time.isoformat() if session.start_time else None,
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'created_at': session.created_at.isoformat(),
            'score': round((session.correct_answers / session.total_questions) * 100, 2) if session.total_questions > 0 else 0
        })
    
    return jsonify(result)

# API端点：获取统计信息
@app.route('/api/stats')
def api_stats():
    total_questions = Question.query.count()
    zh_questions = Question.query.filter_by(language='zh').count()
    en_questions = Question.query.filter_by(language='en').count()
    wrong_answers_count = WrongAnswer.query.count()
    
    # 最近5次练习的成绩
    recent_sessions = PracticeSession.query.order_by(PracticeSession.created_at.desc()).limit(5).all()
    recent_scores = []
    for session in recent_sessions:
        if session.total_questions > 0:
            score = round((session.correct_answers / session.total_questions) * 100, 2)
            recent_scores.append({
                'date': session.created_at.strftime('%Y-%m-%d'),
                'score': score
            })
    
    return jsonify({
        'total_questions': total_questions,
        'zh_questions': zh_questions,
        'en_questions': en_questions,
        'wrong_answers_count': wrong_answers_count,
        'recent_scores': recent_scores
    })

# API端点：爬取题目
@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    data = request.get_json()
    url = data.get('url')
    
    try:
        questions = scrape_questions(url)
        saved_count = 0
        
        for q in questions:
            # 检查题目是否已存在
            existing = Question.query.filter_by(question_text=q['question_text']).first()
            if not existing:
                question = Question(
                    question_text=q['question_text'],
                    options=json.dumps(q['options']),
                    correct_answer=q['correct_answer'],
                    explanation=q['explanation'],
                    language=q['language'],
                    category=q['category']
                )
                db.session.add(question)
                saved_count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'saved_count': saved_count})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)
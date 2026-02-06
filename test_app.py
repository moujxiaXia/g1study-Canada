import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Question, WrongAnswer, PracticeSession
import json

class G1StudyTestCase(unittest.TestCase):
    def setUp(self):
        """在每个测试之前设置应用"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # 添加测试数据
            question = Question(
                question_text="测试题目",
                options=json.dumps({"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}),
                correct_answer="A",
                explanation="这是测试题目的解释",
                language="zh",
                category="测试"
            )
            db.session.add(question)
            db.session.commit()

    def tearDown(self):
        """在每个测试之后清理"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_page(self):
        """测试首页"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'加拿大G1驾驶考试学习软件', response.data)

    def test_practice_page(self):
        """测试练习页面"""
        response = self.app.get('/practice')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'练习模式', response.data)

    def test_wrong_answers_page(self):
        """测试错题本页面"""
        response = self.app.get('/wrong-answers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'错题本', response.data)

    def test_practice_history_page(self):
        """测试练习历史页面"""
        response = self.app.get('/practice-history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'练习历史', response.data)

    def test_question_management_page(self):
        """测试题库管理页面"""
        response = self.app.get('/question-management')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'题库管理', response.data)

    def test_api_questions(self):
        """测试获取题目API"""
        with app.app_context():
            response = self.app.get('/api/questions?language=zh&limit=5')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

    def test_api_stats(self):
        """测试获取统计信息API"""
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_questions', data)
        self.assertIn('zh_questions', data)
        self.assertIn('en_questions', data)
        self.assertIn('wrong_answers_count', data)

if __name__ == '__main__':
    unittest.main()
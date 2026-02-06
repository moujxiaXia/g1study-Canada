import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Question, WrongAnswer, PracticeSession
import json

def init_db():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表
        db.drop_all()
        print("所有表已删除")
        # 创建所有表
        db.create_all()
        print("数据库表已创建")
        
        

if __name__ == "__main__":
    init_db()
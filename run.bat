@echo off
echo 加拿大G1驾驶考试学习软件启动脚本
echo ======================================

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate

REM 检查并安装依赖
echo 检查依赖...
pip install -r requirements.txt >nul 2>&1

REM 检查数据库是否存在
if not exist "g1study.db" (
    echo 初始化数据库...
    python init_db.py
)

REM 启动应用
echo 启动应用...
echo 请在浏览器中访问: http://localhost:5000
python app.py
# 加拿大 G1 驾驶考试学习软件

一个功能完整的加拿大 G1 驾驶考试学习软件，支持题库管理、练习模式、错题本等功能。

## 项目文件结构

```
g1study-qwen/
├── app.py                 # Flask 主应用文件
├── models.py              # 数据库模型定义
├── init_db.py             # 数据库初始化脚本
├── requirements.txt       # Python 依赖包列表
├── README.md              # 项目说明文档
├── run.bat                # Windows 运行脚本
├── test_app.py            # 测试脚本
├── templates/             # HTML 模板文件夹
│   ├── index.html         # 首页模板
│   ├── practice.html      # 练习模式模板
│   ├── wrong_answers.html # 错题本模板
│   ├── practice_history.html # 练习历史模板
│   └── question_management.html # 题库管理模板
├── static/                # 静态文件夹
│   └── images/            # 题目图片文件夹
└── instance/              # 实例数据文件夹
    └── g1study.db         # SQLite 数据库文件
```

## 运行所需的核心文件

要运行此软件，必须包含以下核心文件：

1. **app.py** - Flask 主应用文件
2. **models.py** - 数据库模型定义
3. **templates/** - 包含所有 HTML 模板文件的文件夹
4. **static/images/** - 包含题目图片的文件夹
5. **instance/g1study.db** - SQLite 数据库文件（首次运行时会自动创建）
6. **requirements.txt** - Python 依赖包列表

## 功能特性

### 🎯 核心功能
- **智能题库管理**：支持中文和英文题库
- **随机试题生成**：从题库中随机选择题目形成练习
- **练习模式**：实时答题，即时反馈
- **错题本**：自动记录错题，方便复习
- **练习历史**：记录学习进度和成绩

### 🎨 界面设计
- 现代化响应式设计
- 直观的用户界面
- 美观的动画效果
- 移动端友好

### 📊 数据统计
- 题目总数统计
- 中英文题目分类
- 错题数量统计
- 练习成绩分析

## 技术架构

### 后端技术
- **Python Flask**：Web 框架
- **SQLite**：数据库

### 前端技术
- **Bootstrap 5**：UI 框架
- **Font Awesome**：图标库
- **原生 JavaScript**：交互逻辑

## 安装和运行

### 1. 环境要求
- Python 3.7+

### 2. 克隆项目
```bash
git clone <项目地址>
cd g1study-qwen
```

### 3. 创建虚拟环境（推荐）
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 初始化数据库
```bash
python init_db.py
```

### 6. 运行应用
```bash
python app.py
```

### 7. 访问应用
打开浏览器访问：`http://localhost:5000`

## 使用说明

### 首页
- 查看学习统计信息
- 快速开始练习
- 查看错题本

### 练习模式
1. 选择语言（中文/英文）
2. 设置题目数量（5/10/20/50 题）
3. 点击"开始练习"
4. 选择答案并提交
5. 查看正确答案和解释
6. 继续下一题或完成练习

### 错题本
- 自动记录答错的题目
- 显示正确答案和解释
- 按时间排序
- 支持刷新查看最新错题

### 练习历史
- 查看所有练习记录
- 显示正确率和成绩
- 按时间排序

### 题库管理
- 手动添加题目
- 编辑题目答案
- 删除题目
- 按来源和语言筛选

## 数据库结构

### questions 表（题库）
- id：题目 ID
- question_text：题目文本
- options：选项（JSON 格式）
- correct_answer：正确答案
- correct_id：正确答案 ID（A/B/C/D）
- explanation：解释
- language：语言（zh/en）
- category：分类
- source：题目来源
- image_path：图片路径
- created_at：创建时间

### wrong_answers 表（错题）
- id：记录 ID
- question_id：题目 ID
- user_answer：用户答案
- correct_answer：正确答案
- timestamp：时间戳

### practice_sessions 表（练习记录）
- id：会话 ID
- session_type：会话类型
- total_questions：总题数
- correct_answers：正确数
- wrong_answers：错误数
- start_time：开始时间
- end_time：结束时间
- created_at：创建时间

## API 接口

### 题目相关
- `GET /api/questions`：获取题目
- `GET /api/practice/questions`：获取练习题目
- `POST /api/questions`：添加题目
- `PUT /api/questions/<id>/correct-answer`：更新正确答案
- `DELETE /api/questions/<id>`：删除题目

### 错题相关
- `GET /api/wrong-answers`：获取错题列表

### 历史记录
- `GET /api/practice-history`：获取练习历史

### 统计信息
- `GET /api/stats`：获取统计信息
- `GET /api/question-sources`：获取题目来源列表

### 练习相关
- `POST /api/practice`：开始练习
- `POST /api/practice/answer`：提交答案
- `POST /api/practice/finish`：完成练习

## 自定义配置

### 调整题目数量
在练习模式中选择不同的题目数量。

### 添加新的题目分类
在数据库中添加新的 category 字段值。

## 注意事项

1. **数据备份**：定期备份数据库文件
2. **浏览器兼容性**：建议使用现代浏览器

## 故障排除

### 常见问题

1. **Python 环境问题**
   - 确保 Python 3.7+ 已正确安装
   - 检查 PATH 环境变量
   - 使用 `python --version` 验证

2. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **数据库错误**
   - 检查数据库文件权限
   - 重新初始化数据库：`python init_db.py`
   - 删除数据库文件重新创建

4. **页面显示异常**
   - 清除浏览器缓存
   - 检查 JavaScript 控制台错误
   - 使用现代浏览器

5. **端口占用**
   - 修改 app.py 中的端口号
   - 或关闭占用端口的程序


## 开发计划

### 未来功能
- [ ] 用户账户系统
- [ ] 题目难度分级
- [ ] 学习计划制定
- [ ] 移动端 APP
- [ ] 多语言支持
- [ ] 题目导入导出
- [ ] 学习数据分析

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

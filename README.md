# 招标参数分析工具 (Bidding Analysis Tool)

一个智能化的招标文件参数提取和规律分析工具，帮助用户从多种格式的招标文件中自动提取评分标准、技术参数、商务参数，进而分析厂商的投标规律和参数变化趋势。

## 🎯 核心功能

### Phase 1（当前）- 数据导入和参数提取
- ✅ **多格式文件支持**：PDF、Word (DOC/DOCX)、Excel (XLS/XLSX)、TXT、图片 (PNG/JPG/JPEG) 等
- ✅ **智能参数提取**：自动从招标文件中识别并提取评分标准、技术参数、商务参数
- ✅ **Web 上传界面**：现代化的用户界面，支持拖拽上传
- ✅ **数据管理**：结构化存储提取结果，便于查看和编辑
- ✅ **文本识别**：支持 OCR 识别扫描件和图片

### Phase 2（规划中）- 规律分析
- 📊 参数对比分析
- 📈 趋势挖掘
- 🎨 数据可视化
- 📋 报表生成

## 🏗️ 技术栈

### 后端
- **框架**：FastAPI (Python)
- **Web 服务器**：Uvicorn
- **数据库**：SQLAlchemy ORM + SQLite/PostgreSQL
- **文件处理**：
  - PDF: pdfplumber (表格提取), pdf2image (图片转换)
  - Word: python-docx
  - Excel: openpyxl, pandas
  - 图片: Tesseract OCR (文字识别)

### 前端
- **框架**：React with TypeScript
- **UI 库**：Ant Design
- **文件上传**：React Dropzone
- **HTTP 客户端**：Axios

### 部署
- **容器化**：Docker & Docker Compose
- **反向代理**：Nginx

## 📁 项目结构

```
bidding-analysis-tool/
├── backend/                      # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── models.py            # SQLAlchemy 数据模型
│   │   ├── database.py          # 数据库连接
│   │   ├── schemas.py           # Pydantic 数据验证模式
│   │   ├── routes/              # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── upload.py        # 文件上传路由
│   │   │   ├── projects.py      # 项目管理路由
│   │   │   └── analysis.py      # 分析路由
│   │   └── services/            # 业务逻辑服务
│   │       ├── __init__.py
│   │       ├── file_parser.py   # 多格式文件解析
│   │       └── parameter_extractor.py # 参数提取
│   ├── requirements.txt          # Python 依赖
│   ├── .env.example             # 环境变量示例
│   └── Dockerfile               # Docker 配置
│
├── frontend/                     # React 前端
│   ├── src/
│   │   ├── components/          # React 组件
│   │   │   ├── FileUpload.tsx   # 文件上传组件
│   │   │   ├── ProjectList.tsx  # 项目列表组件
│   │   │   └── ParameterViewer.tsx # 参数查看组件
│   │   ├── pages/               # 页面
│   │   │   ├── HomePage.tsx
│   │   │   ├── UploadPage.tsx
│   │   │   └── ProjectPage.tsx
│   │   ├── services/            # API 调用
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env.example
│   └── Dockerfile
│
├── docker-compose.yml           # Docker 编排配置
├── .gitignore
└── README.md
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose (可选)
- Tesseract OCR (可选，用于图片识别)

### 本地开发

#### 1. 克隆项目
```bash
git clone https://github.com/juan9455/bidding-analysis-tool.git
cd bidding-analysis-tool
```

#### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件（如需要）

# 启动应用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端 API 文档自动生成：http://localhost:8000/docs

#### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

前端应用：http://localhost:3000

### Docker 部署（推荐）

```bash
# 在项目根目录执行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

服务地址：
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 📡 API 端点

### 文件上传
```
POST /api/v1/upload
Content-Type: multipart/form-data
Body: {
  "file": <招标文件>,
  "project_name": "string" (可选)
}
Response: {
  "file_id": "uuid",
  "project_id": "uuid",
  "file_name": "string",
  "status": "extracting" | "completed" | "failed",
  "extracted_parameters": { ... }
}
```

### 获取项目列表
```
GET /api/v1/projects
Response: [
  {
    "project_id": "uuid",
    "project_name": "string",
    "created_at": "2024-01-01T00:00:00Z",
    "file_count": 5,
    "status": "completed"
  }
]
```

### 获取项目详情
```
GET /api/v1/projects/{project_id}
Response: {
  "project_id": "uuid",
  "project_name": "string",
  "files": [ ... ],
  "parameters": {
    "scoring_criteria": [ ... ],
    "technical_params": [ ... ],
    "commercial_params": [ ... ]
  }
}
```

### 删除项目
```
DELETE /api/v1/projects/{project_id}
Response: { "success": true }
```

## 📊 参数提取规则

### 支持提取的参数类型

#### 1. 评分标准 (Scoring Criteria)
- 评分项名称
- 权重百分比
- 满分分值
- 评分描述

#### 2. 技术参数 (Technical Parameters)
- 技术要求
- 规格参数
- 性能指标
- 配置要求
- 功能特性

#### 3. 商务参数 (Commercial Parameters)
- 价格范围
- 付款条件
- 交货周期
- 保修期限
- 售后服务

#### 4. 基本信息 (Basic Info)
- 招标单位
- 代理机构
- 项目名称
- 招标日期
- 开标日期
- 项目预算

## 🔧 配置说明

### 环境变量 (.env)

```env
# 应用
DEBUG=True
APP_NAME=Bidding Analysis Tool

# 文件上传
UPLOAD_DIR=uploads
MAX_FILE_SIZE=52428800  # 50MB

# 数据库
DATABASE_URL=sqlite:///./bidding_analysis.db
# 或使用 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/bidding_db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# 前端
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 📈 开发路线图

### ✅ Phase 1 (当前)
- [x] 项目结构搭建
- [x] 多格式文件解析
- [x] 参数提取引擎
- [x] Web 上传界面
- [x] 基础数据管理

### 📅 Phase 2 (规划中)
- [ ] 数据对比分析
- [ ] 参数趋势分析
- [ ] 数据可视化仪表板
- [ ] 报表生成和导出
- [ ] AI 增强参数提取 (Claude/GPT API)

### 🚀 Phase 3 (远期)
- [ ] 机器学习模型训练
- [ ] 自动化工作流
- [ ] 团队协作功能
- [ ] 移动应用

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 开启 Pull Request

### 代码规范
- Python: PEP 8 (使用 Black 格式化)
- JavaScript/TypeScript: ESLint + Prettier
- 提交信息：使用 Conventional Commits 格式

## 📝 许可证

MIT License

## 💬 联系和支持

- 提交 Issue：https://github.com/juan9455/bidding-analysis-tool/issues
- 讨论功能：https://github.com/juan9455/bidding-analysis-tool/discussions

---

**开发状态**：Phase 1 - 积极开发中 🚀

**最后更新**：2026-05-03

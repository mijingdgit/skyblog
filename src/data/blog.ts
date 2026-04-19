// 博客数据

export interface Article {
  id: number
  title: string
  excerpt: string
  content: string
  category: string
  tags: string[]
  date: string
  readTime: string
  views: number
  cover?: string
}

export interface Category {
  name: string
  slug: string
  description: string
  icon: string
  count: number
}

export interface Project {
  id: number
  title: string
  description: string
  techStack: string[]
  image: string
  github?: string
  demo?: string
  highlights: string[]
}

// 分类数据
export const categories: Category[] = [
  {
    name: '大模型实战',
    slug: 'llm',
    description: 'LLM 应用开发、Prompt 工程、RAG、Agent 架构实战',
    icon: '🧠',
    count: 8
  },
  {
    name: 'AI 动漫生成',
    slug: 'ai-anime',
    description: 'Stable Diffusion、ComfyUI、AnimeGAN 等技术实践',
    icon: '🎨',
    count: 5
  },
  {
    name: 'Python 开发',
    slug: 'python',
    description: 'Python 进阶、异步编程、装饰器、设计模式',
    icon: '🐍',
    count: 12
  },
  {
    name: '踩坑记录',
    slug: 'debug',
    description: '问题排查、异常处理、性能优化经验总结',
    icon: '🔧',
    count: 6
  }
]

// 标签数据
export const tags = [
  'Python', 'LLM', 'GPT', 'Claude', 'RAG', 'Agent',
  'Stable Diffusion', 'ComfyUI', 'WebSocket', 'FastAPI',
  'Docker', 'Linux', '异步编程', '设计模式', '性能优化',
  'AI', 'Midjourney', '动漫生成', 'Vue3', 'Three.js'
]

// 文章数据
export const articles: Article[] = [
  {
    id: 1,
    title: '基于 LangChain + OpenAI API 构建企业级 RAG 问答系统',
    excerpt: '详细讲解如何使用 LangChain 框架结合向量数据库构建私有知识库问答系统，包含完整的代码实现和优化策略。',
    content: `
## 前言

在企业场景中，我们经常需要让 AI 模型回答基于私有文档的问题。RAG（Retrieval Augmented Generation）技术正是解决这一问题的最佳方案。

### 技术架构

本文将介绍以下技术栈：
- **LangChain**: 大语言模型应用开发框架
- **OpenAI API**: GPT-4 模型能力
- **Chroma**: 开源向量数据库
- **FastAPI**: 高性能 Python Web 框架

### 核心实现

\`\`\`python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# 1. 加载文档
loader = PyPDFLoader("knowledge.pdf")
documents = loader.load()

# 2. 文档分块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 3. 向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings
)

# 4. 构建问答链
llm = ChatOpenAI(model_name="gpt-4")
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    vectorstore.as_retriever()
)
\`\`\`

### 优化策略

1. **检索优化**: 调整 chunk_size 和 overlap
2. **混合搜索**: 结合关键词和语义搜索
3. **重新排序**: 使用 CrossEncoder 重排序结果

### 总结

RAG 技术能够有效解决私有知识库问答问题，是企业 AI 应用的必备技能。
    `,
    category: 'llm',
    tags: ['LLM', 'RAG', 'LangChain', 'Python'],
    date: '2026-04-06',
    readTime: '15 分钟',
    views: 1234
  },
  {
    id: 2,
    title: '使用 ComfyUI 工作流实现 AI 动漫角色生成',
    excerpt: '深入讲解 ComfyUI 工作流设计，手把手教你构建自动化的动漫角色生成 pipeline。',
    content: `
## 什么是 ComfyUI

ComfyUI 是一个基于节点的工作流 UI，专门用于生成式 AI 图像创作。它的高度模块化设计让创作者可以自由组合各种 AI 模型和处理节点。

### 工作流设计

本教程将构建一个完整的动漫角色生成工作流：

\`\`\`
1. ControlNet 姿态控制
2. LoRA 模型加载
3. 提示词优化
4. VAE 编码
5. KSampler 采样
6. VAE 解码
7. FaceDetailer 增强
\`\`\`

### 核心节点配置

#### 1. Checkpoint Loader
选择合适的动漫模型：
- Anything V5
- DreamShaper
- Counterfeit

#### 2. ControlNet 设置
\`\`\`python
controlnet = {
    "preprocessor": "openpose",
    "model": "control_v11p_sd15_openpose",
    "weight": 0.8,
    "guidance_start": 0.0,
    "guidance_end": 0.8
}
\`\`\`

### 自动化脚本

我们可以使用 Python API 自动化执行工作流：
\`\`\`python
import subprocess
import json

def run_workflow(workflow_path, output_dir):
    cmd = [
        "python", "comfyui_manager.py",
        "--workflow", workflow_path,
        "--output", output_dir
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout
\`\`\`
    `,
    category: 'ai-anime',
    tags: ['Stable Diffusion', 'ComfyUI', 'AI', '动漫生成'],
    date: '2026-04-04',
    readTime: '20 分钟',
    views: 892
  },
  {
    id: 3,
    title: 'Python 异步编程深度解析：asyncio 实战指南',
    excerpt: '从基础概念到高级应用，详细讲解 Python 异步编程的核心知识与最佳实践。',
    content: `
## 为什么需要异步编程

在 I/O 密集型任务中，传统的同步编程会导致大量时间浪费在等待上。异步编程能够让程序在等待 I/O 时执行其他任务。

### 基本概念

\`\`\`python
import asyncio

async def fetch_data(url: str) -> dict:
    """模拟异步请求"""
    await asyncio.sleep(1)  # 模拟网络请求
    return {"url": url, "data": "sample"}

async def main():
    # 并发执行多个任务
    tasks = [
        fetch_data("api1.example.com"),
        fetch_data("api2.example.com"),
        fetch_data("api3.example.com")
    ]
    results = await asyncio.gather(*tasks)
    return results
\`\`\`

### 异步上下文管理器

\`\`\`python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        await asyncio.sleep(0.5)
        print("Connected")

    async def disconnect(self):
        print("Disconnected")
\`\`\`

### 最佳实践

1. 使用 \`asyncio.gather\` 并发执行独立任务
2. 合理设置超时时间避免无限等待
3. 使用 \`asyncio.Semaphore\` 控制并发数量
    `,
    category: 'python',
    tags: ['Python', '异步编程', 'asyncio'],
    date: '2026-04-02',
    readTime: '12 分钟',
    views: 567
  },
  {
    id: 4,
    title: '一次 Docker 容器内存泄漏的排查与修复',
    excerpt: '记录线上环境 Docker 容器内存持续增长的问题排查过程，分享实用的问题定位技巧。',
    content: `
## 问题现象

线上服务运行一段时间后，容器内存使用率持续上升，最终导致 OOM kill。

### 排查步骤

#### 1. 监控指标观察
\`\`\`bash
# 查看容器内存使用
docker stats container_id

# 查看详细内存信息
docker inspect container_id | jq '.[0].MemoryStats'
\`\`\`

#### 2. 内存分析
使用 \`memory_profiler\` 分析代码内存占用：
\`\`\`python
from memory_profiler import profile

@profile
def process_data(data):
    # 处理逻辑
    result = heavy_computation(data)
    return result
\`\`\`

#### 3. 定位泄漏点
\`\`\`python
import tracemalloc

tracemalloc.start()

# 执行可能泄漏的操作
process_large_data()

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024} MB")
print(f"Peak: {peak / 1024 / 1024} MB")

tracemalloc.stop()
\`\`\`

### 根本原因

发现是 \`requests.Session()\` 对象未正确关闭，导致连接池持续增长。

### 修复方案
\`\`\`python
# 使用上下文管理器
with requests.Session() as session:
    response = session.get(url)
    # 自动释放资源
\`\`\`
    `,
    category: 'debug',
    tags: ['Docker', 'Linux', '性能优化', 'Python'],
    date: '2026-03-30',
    readTime: '10 分钟',
    views: 445
  },
  {
    id: 5,
    title: '使用 FastAPI 构建高并发 RESTful API',
    excerpt: '讲解如何使用 FastAPI 构建高性能 RESTful API，包含依赖注入、异步数据库操作等高级特性。',
    content: `
## FastAPI 简介

FastAPI 是一个现代、快速的 Python Web 框架，基于类型提示自动生成 API 文档。

### 项目结构

\`\`\`
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   └── schemas/
└── tests/
\`\`\`

### 核心代码

\`\`\`python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI(title="My API", version="1.0.0")

class User(BaseModel):
    username: str
    email: str | None = None

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
\`\`\`
    `,
    category: 'python',
    tags: ['Python', 'FastAPI', 'WebSocket'],
    date: '2026-03-28',
    readTime: '18 分钟',
    views: 789
  },
  {
    id: 6,
    title: 'Claude API 实战：构建智能对话助手',
    excerpt: '深入探索 Anthropic Claude API 的能力，构建一个具备多轮对话能力的智能助手。',
    content: `
## Claude API 概述

Claude 是 Anthropic 开发的 AI 助手，在代码理解、长文本处理方面表现优异。

### 基本调用

\`\`\`python
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "帮我解释一下什么是装饰器"}
    ]
)

print(message.content[0].text)
\`\`\`

### 系统提示词设计

\`\`\`python
SYSTEM_PROMPT = """你是一个专业的 Python 开发顾问。
- 回答要简洁、准确
- 代码示例要完整可运行
- 适当给出最佳实践建议
- 遇到不确定的问题要明确说明
"""
\`\`\`
    `,
    category: 'llm',
    tags: ['LLM', 'Claude', 'Python', 'Agent'],
    date: '2026-03-25',
    readTime: '14 分钟',
    views: 923
  },
  {
    id: 7,
    title: 'AI 视频生成工具全家桶',
    excerpt: '盘点当前主流的 AI 视频生成工具，从 Runway 到 Pika 全面对比分析。',
    content: `
## AI 视频生成工具对比

### Runway Gen-2/Gen-3
- 优点：质量高，稳定性好
- 缺点：付费，价格较高

### Pika Labs
- 优点：免费，生成速度快
- 缺点：时长限制

### Stability AI
- 优点：开源可自部署
- 缺点：需要 GPU 资源
    `,
    category: 'ai-anime',
    tags: ['AI', 'Midjourney', '动漫生成'],
    date: '2026-03-22',
    readTime: '8 分钟',
    views: 654
  },
  {
    id: 8,
    title: 'Python 设计模式：装饰器模式完全指南',
    excerpt: '深入理解装饰器模式，通过实际案例掌握这一强大设计模式。',
    content: `
## 装饰器模式

装饰器模式允许在运行时动态添加对象的功能。

### 基本实现

\`\`\`python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b
\`\`\`

### 类装饰器

\`\`\`python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    pass
\`\`\`
    `,
    category: 'python',
    tags: ['Python', '设计模式'],
    date: '2026-03-20',
    readTime: '16 分钟',
    views: 432
  }
]

// 项目数据
export const projects: Project[] = [
  {
    id: 1,
    title: 'AI 知识库问答系统',
    description: '基于 RAG 技术构建的企业级私有知识库问答系统，支持文档上传、智能检索、多轮对话。',
    techStack: ['LangChain', 'FastAPI', 'Chroma', 'Vue3', 'PostgreSQL'],
    image: 'knowledge',
    github: 'https://github.com',
    demo: 'https://demo.example.com',
    highlights: ['向量检索', '混合搜索', '引用溯源']
  },
  {
    id: 2,
    title: 'ComfyUI 工作流市场',
    description: 'AI 动漫图像生成工作流分享平台，支持一键导入、社区评分、在线生成。',
    techStack: ['React', 'Node.js', 'Three.js', 'Docker'],
    image: 'comfyui',
    github: 'https://github.com',
    highlights: ['工作流可视化', '社区分享', 'API 集成']
  },
  {
    id: 3,
    title: 'GPT-4 聊天助手',
    description: '支持多模型切换、对话历史管理、自定义提示词的 AI 聊天应用。',
    techStack: ['Vue3', 'FastAPI', 'OpenAI API', 'SQLite'],
    image: 'chat',
    demo: 'https://demo.example.com',
    highlights: ['多模型支持', 'Markdown 渲染', '代码高亮']
  },
  {
    id: 4,
    title: 'AI 动漫头像生成器',
    description: '基于 Stable Diffusion 的个性化动漫头像生成应用，支持风格迁移。',
    techStack: ['Python', 'Stable Diffusion', 'FastAPI', 'React'],
    image: 'avatar',
    github: 'https://github.com',
    highlights: ['风格迁移', '批量生成', '自定义训练']
  },
  {
    id: 5,
    title: '自动化测试平台',
    description: '支持 API 测试、UI 自动化、性能测试的一站式测试平台。',
    techStack: ['Python', 'Playwright', 'Docker', 'Redis'],
    image: 'test',
    highlights: ['可视化配置', '定时任务', '测试报告']
  },
  {
    id: 6,
    title: '实时协作代码编辑器',
    description: '支持多人实时协作的 Web IDE，支持代码高亮、自动补全、语音聊天。',
    techStack: ['Monaco Editor', 'WebSocket', 'Yjs', 'Vue3'],
    image: 'editor',
    demo: 'https://demo.example.com',
    highlights: ['实时同步', 'CRDT 算法', '低延迟']
  }
]

// 获取最新文章
export function getLatestArticles(count: number = 5): Article[] {
  return [...articles]
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, count)
}

// 获取热门文章
export function getPopularArticles(count: number = 5): Article[] {
  return [...articles]
    .sort((a, b) => b.views - a.views)
    .slice(0, count)
}

// 根据分类获取文章
export function getArticlesByCategory(category: string): Article[] {
  return articles.filter(article => article.category === category)
}

// 根据 ID 获取文章
export function getArticleById(id: number): Article | undefined {
  return articles.find(article => article.id === id)
}

// 获取所有标签及使用次数
export function getTagsWithCount(): { name: string; count: number }[] {
  const tagCount: Record<string, number> = {}
  articles.forEach(article => {
    article.tags.forEach(tag => {
      tagCount[tag] = (tagCount[tag] || 0) + 1
    })
  })
  return Object.entries(tagCount)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
}
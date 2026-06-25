---
title: 从 0 搭建本地 Ollama 知识库：模型、向量库与检索链路
slug: ollama-rag-local-knowledge-base
excerpt: 用 Ollama、Python 和轻量向量库搭一个可在本地运行的 RAG 知识库，重点梳理文档切分、召回、重排和回答生成的工程取舍。
category_slug: python-ai
category_name: Python
category_icon: PY
category_description: Python、AI 应用、自动化脚本与后端实践。
category_order: 1
tags: Python, Ollama, RAG, LLM, 向量数据库
published_at: 2026-04-23
is_published: true
is_featured: true
views: 0
---

## 为什么先做本地知识库

本地知识库的价值不在于把大模型变得“无所不知”，而是把回答范围收束到你真正掌握的材料里。对个人博客、学习笔记、项目文档来说，RAG 的第一目标是减少翻找成本：输入一个问题，系统能先从自己的资料里找证据，再让模型组织答案。

用 Ollama 做本地模型有两个好处。第一，调试成本低，模型服务可以在自己的机器上跑起来；第二，链路透明，文档切分、向量入库、召回和回答生成都能逐步替换，不会一开始就被复杂平台绑住。

## 最小可用架构

一个能跑起来的本地 RAG，通常包含四层：

1. 文档层：Markdown、PDF、Word 或网页内容。
2. 索引层：把文档切成块，再生成向量。
3. 检索层：根据问题召回相关片段。
4. 生成层：把问题和片段交给模型，让模型基于材料回答。

先不要急着上复杂 Agent。RAG 的可用性很大程度取决于“材料是否干净”和“召回是否准确”，这两件事比换一个更大的模型更重要。

## 环境准备

先拉取一个可用的本地模型：

```bash
ollama pull qwen2.5:7b
ollama serve
```

Python 侧可以先用最少依赖搭建：

```bash
pip install langchain langchain-community langchain-ollama chromadb
```

如果机器资源有限，可以从 7B 量级模型开始。RAG 初期调试时，重点不是追求最强回答，而是先把检索结果稳定下来。

## 文档切分

切分策略建议从“语义完整”开始，而不是机械地按固定字数切。比如一篇 Markdown，可以优先按二级标题和三级标题拆分，再给每段设置合理长度上限。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=120,
    separators=["\n## ", "\n### ", "\n\n", "。", "\n", ""],
)

chunks = splitter.create_documents([markdown_text])
```

`chunk_overlap` 不要设得太大。重叠过多会让召回结果看起来很多，实际信息却高度重复，最后模型容易写出“像是回答了，但没有新增信息”的内容。

## 向量入库

用 Chroma 做本地向量库就足够入门：

```python
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./data/chroma",
)
```

这里有一个容易忽略的点：生成回答的模型和生成向量的模型可以不同。回答模型负责表达，向量模型负责语义匹配。优先选择稳定的 embedding 模型，比盲目追求同一个大模型包打天下更靠谱。

## 检索与提示词

召回时可以先取 4 到 6 个片段：

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke("如何部署 SkyBlog 的 Django 后台？")
context = "\n\n".join(doc.page_content for doc in docs)
```

提示词要把模型的边界说清楚：

```text
你是一个技术博客助手。请只依据给定资料回答。
如果资料中没有答案，请明确说明“当前资料未覆盖”。

资料：
{context}

问题：
{question}
```

这段约束很朴素，但很实用。它让模型少一点自由发挥，多一点证据意识。

## 调试清单

当回答质量不稳定时，不要只看最终答案。可以按下面顺序排查：

1. 问题是否被正确传给检索器。
2. 召回片段是否真的包含答案。
3. 片段是否过长，导致关键信息被稀释。
4. 文档里是否有重复标题、残缺代码块或无意义目录。
5. 提示词是否允许模型在资料不足时承认不知道。

我习惯先把召回片段打印出来，再看模型回答。只要召回错了，后面生成得再流畅也只是漂亮地偏题。

## 后续优化

最小版本跑通后，可以继续加三类能力：

1. 元数据过滤：按分类、标签、项目名限制检索范围。
2. 重排：用更精细的模型对初次召回结果重新排序。
3. 引用来源：把文档标题、段落链接或文件名附到答案后面。

本地 RAG 的核心不是堆工具，而是建立一条可观察、可替换、可持续维护的链路。先让它朴素地正确，再让它慢慢变聪明。

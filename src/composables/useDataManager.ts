import { ref } from 'vue'
import { articles as defaultArticles, projects as defaultProjects, categories as defaultCategories, type Article, type Project, type Category } from '../data/blog'

// 数据存储键
const ARTICLES_KEY = 'skyblog_articles'
const PROJECTS_KEY = 'skyblog_projects'

// 初始化数据
const initData = () => {
  if (!localStorage.getItem(ARTICLES_KEY)) {
    localStorage.setItem(ARTICLES_KEY, JSON.stringify(defaultArticles))
  }
  if (!localStorage.getItem(PROJECTS_KEY)) {
    localStorage.setItem(PROJECTS_KEY, JSON.stringify(defaultProjects))
  }
}

// 获取文章列表
export function useArticles() {
  const articles = ref<Article[]>([])

  const loadArticles = () => {
    initData()
    const stored = localStorage.getItem(ARTICLES_KEY)
    articles.value = stored ? JSON.parse(stored) : defaultArticles
  }

  const saveArticles = () => {
    localStorage.setItem(ARTICLES_KEY, JSON.stringify(articles.value))
  }

  // 获取单个文章
  const getArticle = (id: number): Article | undefined => {
    return articles.value.find(a => a.id === id)
  }

  // 添加文章
  const addArticle = (article: Omit<Article, 'id'>) => {
    const maxId = Math.max(...articles.value.map(a => a.id), 0)
    articles.value.push({ ...article, id: maxId + 1 })
    saveArticles()
  }

  // 更新文章
  const updateArticle = (id: number, updates: Partial<Article>) => {
    const index = articles.value.findIndex(a => a.id === id)
    if (index >= 0) {
      articles.value[index] = { ...articles.value[index], ...updates }
      saveArticles()
    }
  }

  // 删除文章
  const deleteArticle = (id: number) => {
    articles.value = articles.value.filter(a => a.id !== id)
    saveArticles()
  }

  // 获取所有分类
  const getCategories = (): Category[] => {
    return defaultCategories
  }

  return {
    articles,
    loadArticles,
    getArticle,
    addArticle,
    updateArticle,
    deleteArticle,
    getCategories
  }
}

// 获取项目列表
export function useProjects() {
  const projects = ref<Project[]>([])

  const loadProjects = () => {
    initData()
    const stored = localStorage.getItem(PROJECTS_KEY)
    projects.value = stored ? JSON.parse(stored) : defaultProjects
  }

  const saveProjects = () => {
    localStorage.setItem(PROJECTS_KEY, JSON.stringify(projects.value))
  }

  // 获取单个项目
  const getProject = (id: number): Project | undefined => {
    return projects.value.find(p => p.id === id)
  }

  // 添加项目
  const addProject = (project: Omit<Project, 'id'>) => {
    const maxId = Math.max(...projects.value.map(p => p.id), 0)
    projects.value.push({ ...project, id: maxId + 1 })
    saveProjects()
  }

  // 更新项目
  const updateProject = (id: number, updates: Partial<Project>) => {
    const index = projects.value.findIndex(p => p.id === id)
    if (index >= 0) {
      projects.value[index] = { ...projects.value[index], ...updates }
      saveProjects()
    }
  }

  // 删除项目
  const deleteProject = (id: number) => {
    projects.value = projects.value.filter(p => p.id !== id)
    saveProjects()
  }

  return {
    projects,
    loadProjects,
    getProject,
    addProject,
    updateProject,
    deleteProject
  }
}

// 导出数据
export function exportData() {
  const data = {
    articles: JSON.parse(localStorage.getItem(ARTICLES_KEY) || '[]'),
    projects: JSON.parse(localStorage.getItem(PROJECTS_KEY) || '[]'),
    exportTime: new Date().toISOString()
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `skyblog_backup_${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// 导入数据
export function importData(file: File): Promise<boolean> {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string)

        if (data.articles) {
          localStorage.setItem(ARTICLES_KEY, JSON.stringify(data.articles))
        }
        if (data.projects) {
          localStorage.setItem(PROJECTS_KEY, JSON.stringify(data.projects))
        }

        resolve(true)
      } catch {
        resolve(false)
      }
    }
    reader.readAsText(file)
  })
}

// 重置为默认数据
export function resetData() {
  localStorage.setItem(ARTICLES_KEY, JSON.stringify(defaultArticles))
  localStorage.setItem(PROJECTS_KEY, JSON.stringify(defaultProjects))
}
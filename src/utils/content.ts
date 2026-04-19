import type { AdminArticle, AdminCategory, AdminProject } from '../types/admin'

export function getArticleDisplayDate(article: AdminArticle) {
  return article.published_at || article.created_at
}

export function formatDate(value?: string | null) {
  if (!value) {
    return '未设置'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date)
}

export function sortArticlesByLatest(articles: AdminArticle[]) {
  return [...articles].sort(
    (left, right) =>
      new Date(getArticleDisplayDate(right)).getTime() -
      new Date(getArticleDisplayDate(left)).getTime(),
  )
}

export function sortArticlesByViews(articles: AdminArticle[]) {
  return [...articles].sort((left, right) => right.views - left.views)
}

export function buildTagCounts(articles: AdminArticle[]) {
  const counts = new Map<string, number>()

  for (const article of articles) {
    for (const tag of article.tags) {
      counts.set(tag.name, (counts.get(tag.name) || 0) + 1)
    }
  }

  return Array.from(counts.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((left, right) => right.count - left.count)
}

export function categoryById(categories: AdminCategory[], id: number | null) {
  return categories.find((category) => category.id === id) || null
}

export function categoryBySlug(categories: AdminCategory[], slug: string) {
  return categories.find((category) => category.slug === slug) || null
}

export function filterProjectsByPreset(projects: AdminProject[], preset: string) {
  if (preset === 'all') {
    return projects
  }

  return projects.filter((project) => {
    if (preset === 'llm') {
      return project.tech_stack.some((tech) => ['LangChain', 'OpenAI API', 'Claude'].includes(tech))
    }

    if (preset === 'frontend') {
      return project.tech_stack.some((tech) => ['Vue3', 'React', 'Three.js'].includes(tech))
    }

    if (preset === 'backend') {
      return project.tech_stack.some((tech) => ['FastAPI', 'Node.js', 'Python', 'Django'].includes(tech))
    }

    return true
  })
}

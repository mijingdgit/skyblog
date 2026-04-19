import { apiRequest } from './client'
import type { AdminArticle, AdminCategory, AdminProject } from '../types/admin'

export function fetchPublicCategories() {
  return apiRequest<AdminCategory[]>('/api/articles/categories/')
}

export function fetchPublishedArticles() {
  return apiRequest<AdminArticle[]>('/api/articles/?is_published=true')
}

export function fetchPublishedArticle(id: number) {
  return apiRequest<AdminArticle>(`/api/articles/${id}/?is_published=true`)
}

export function fetchPublishedProjects() {
  return apiRequest<AdminProject[]>('/api/projects/?is_published=true')
}

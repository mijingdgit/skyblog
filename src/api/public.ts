import { apiRequest } from './client'
import type {
  AboutProfile,
  AdminArticle,
  AdminCategory,
  AdminProject,
  AdminTag,
  ProjectPageContent,
} from '../types/admin'

export function fetchPublicCategories() {
  return apiRequest<AdminCategory[]>('/api/articles/categories/')
}

export function fetchPublicTags() {
  return apiRequest<AdminTag[]>('/api/articles/tags/')
}

export function fetchPublishedArticles() {
  return apiRequest<AdminArticle[]>('/api/articles/?is_published=true')
}

export function fetchPublishedArticle(id: number) {
  return apiRequest<AdminArticle>(`/api/articles/${id}/?is_published=true`)
}

export function incrementArticleView(id: number) {
  return apiRequest<{ views: number }>(`/api/articles/${id}/increment_view/`, {
    method: 'POST',
  })
}

export function fetchPublishedProjects() {
  return apiRequest<AdminProject[]>('/api/projects/?is_published=true')
}

export function fetchProjectPageContent() {
  return apiRequest<ProjectPageContent>('/api/projects/page-content/')
}

export function fetchAboutProfile() {
  return apiRequest<AboutProfile>('/api/articles/about-profile/')
}

export interface UserPermission {
  can_manage_users: boolean
  can_manage_articles: boolean
  can_manage_projects: boolean
  can_export_data: boolean
  can_import_data: boolean
}

export interface AuthUser {
  id: number
  username: string
  nickname: string
  email: string
  role: string
  avatar?: string | null
  phone?: string
  bio?: string
  is_active: boolean
  date_joined: string
  permission?: UserPermission
}

export interface AdminCategory {
  id: number
  name: string
  slug: string
  icon: string
  description: string
  order: number
  article_count: number
  created_at: string
}

export interface AdminTag {
  id: number
  name: string
  article_count?: number
  created_at: string
}

export interface AdminArticle {
  id: number
  title: string
  slug: string
  excerpt: string
  content: string
  xmind_file?: string
  category: number | null
  category_name?: string
  tags: AdminTag[]
  author?: number | null
  author_name?: string
  cover?: string
  views: number
  is_published: boolean
  is_featured: boolean
  created_at: string
  updated_at: string
  published_at?: string | null
}

export interface AdminProject {
  id: number
  title: string
  slug: string
  description: string
  tech_stack: string[]
  image: string
  github?: string
  demo?: string
  highlights: string[]
  order: number
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface ProjectPageFilter {
  key: string
  label: string
}

export interface ProjectPageContent {
  id: number
  title_prefix: string
  title_accent: string
  description: string
  filters: ProjectPageFilter[]
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface AboutSkillGroup {
  category: string
  items: string[]
}

export interface AboutDirection {
  icon: string
  title: string
  desc: string
}

export interface AboutExperience {
  period: string
  title: string
  company: string
  description: string
}

export interface AboutTool {
  icon: string
  name: string
}

export interface AboutAbility {
  icon: string
  title: string
  desc: string
}

export interface AboutProfile {
  id: number
  name: string
  title: string
  location: string
  email: string
  github: string
  slogan: string
  avatar_text: string
  page_title: string
  page_description: string
  intro_title: string
  intro_paragraphs: string[]
  skills: AboutSkillGroup[]
  directions: AboutDirection[]
  experiences: AboutExperience[]
  certifications: string[]
  tools: AboutTool[]
  abilities: AboutAbility[]
  contact_title: string
  contact_description: string
  is_active: boolean
  created_at: string
  updated_at: string
}

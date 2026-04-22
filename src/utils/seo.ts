const siteName = 'SkyBlog'
const defaultDescription = 'SkyBlog 是一个记录 Python、Django、Vue 和 AI 大模型应用实践的个人技术博客。'

type SeoOptions = {
  title?: string
  description?: string
  image?: string
  path?: string
  type?: 'website' | 'article'
}

function setMeta(name: string, content: string, attribute: 'name' | 'property' = 'name') {
  let element = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${name}"]`)

  if (!element) {
    element = document.createElement('meta')
    element.setAttribute(attribute, name)
    document.head.appendChild(element)
  }

  element.setAttribute('content', content)
}

function setCanonical(url: string) {
  let element = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')

  if (!element) {
    element = document.createElement('link')
    element.setAttribute('rel', 'canonical')
    document.head.appendChild(element)
  }

  element.setAttribute('href', url)
}

function removeMeta(name: string, attribute: 'name' | 'property' = 'name') {
  const element = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${name}"]`)
  element?.remove()
}

function absoluteUrl(pathOrUrl: string) {
  if (/^https?:\/\//.test(pathOrUrl)) {
    return pathOrUrl
  }

  const normalizedPath = pathOrUrl.startsWith('/') ? pathOrUrl : `/${pathOrUrl}`
  return `${window.location.origin}${normalizedPath}`
}

export function applySeo(options: SeoOptions = {}) {
  const title = options.title ? `${options.title} | ${siteName}` : siteName
  const description = options.description?.trim() || defaultDescription
  const canonicalUrl = absoluteUrl(options.path || window.location.pathname)

  document.title = title
  setMeta('description', description)
  setMeta('og:type', options.type || 'website', 'property')
  setMeta('og:title', title, 'property')
  setMeta('og:description', description, 'property')
  setMeta('og:url', canonicalUrl, 'property')
  setMeta('og:site_name', siteName, 'property')
  setMeta('twitter:card', options.image ? 'summary_large_image' : 'summary')
  setMeta('twitter:title', title)
  setMeta('twitter:description', description)

  if (options.image) {
    const imageUrl = absoluteUrl(options.image)
    setMeta('og:image', imageUrl, 'property')
    setMeta('twitter:image', imageUrl)
  } else {
    removeMeta('og:image', 'property')
    removeMeta('twitter:image')
  }

  setCanonical(canonicalUrl)
}

export { defaultDescription, siteName }

const defaultApiBase = import.meta.env.DEV ? '' : ''

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || defaultApiBase).replace(/\/$/, '')

export class ApiError extends Error {
  status: number
  data: unknown

  constructor(message: string, status: number, data: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

function buildUrl(path: string) {
  if (/^https?:\/\//.test(path)) {
    return path
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE_URL}${normalizedPath}`
}

function readCookie(name: string) {
  const pattern = new RegExp(`(?:^|; )${name}=([^;]*)`)
  const match = document.cookie.match(pattern)
  return match ? decodeURIComponent(match[1]) : ''
}

export async function ensureCsrfCookie() {
  if (readCookie('csrftoken')) {
    return readCookie('csrftoken')
  }

  const response = await fetch(buildUrl('/api/csrf/'), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new ApiError('无法获取 CSRF Token', response.status, null)
  }

  const data = await response.json()
  return data.csrfToken || readCookie('csrftoken')
}

type RequestOptions = Omit<RequestInit, 'body'> & {
  body?: BodyInit | object | null
  skipCsrf?: boolean
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}) {
  const method = options.method || 'GET'
  const headers = new Headers(options.headers)
  const isJsonBody =
    options.body !== null &&
    options.body !== undefined &&
    !(options.body instanceof FormData) &&
    !(options.body instanceof URLSearchParams) &&
    typeof options.body !== 'string' &&
    !(options.body instanceof Blob)

  if (method !== 'GET' && method !== 'HEAD' && !options.skipCsrf) {
    const csrfToken = await ensureCsrfCookie()
    headers.set('X-CSRFToken', csrfToken)
  }

  let body = options.body as BodyInit | undefined
  if (isJsonBody) {
    headers.set('Content-Type', 'application/json')
    body = JSON.stringify(options.body)
  }

  const response = await fetch(buildUrl(path), {
    ...options,
    method,
    headers,
    body,
    credentials: 'include',
  })

  if (response.status === 204) {
    return null as T
  }

  const contentType = response.headers.get('content-type') || ''
  const data = contentType.includes('application/json')
    ? await response.json()
    : await response.text()

  if (!response.ok) {
    const message =
      typeof data === 'object' && data && 'message' in data
        ? String(data.message)
        : `请求失败(${response.status})`
    throw new ApiError(message, response.status, data)
  }

  return data as T
}

export { API_BASE_URL }

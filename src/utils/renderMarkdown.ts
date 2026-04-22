import DOMPurify from 'dompurify'
import hljs from 'highlight.js/lib/core'
import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import django from 'highlight.js/lib/languages/django'
import javascript from 'highlight.js/lib/languages/javascript'
import json from 'highlight.js/lib/languages/json'
import markdownLanguage from 'highlight.js/lib/languages/markdown'
import python from 'highlight.js/lib/languages/python'
import sql from 'highlight.js/lib/languages/sql'
import typescript from 'highlight.js/lib/languages/typescript'
import xml from 'highlight.js/lib/languages/xml'
import MarkdownIt from 'markdown-it'

const XMIND_SOURCE_MARKER = '<!-- source:xmind -->'

export interface XmindNode {
  id: string
  title: string
  children: XmindNode[]
}

export interface MarkdownHeading {
  id: string
  level: 2 | 3
  text: string
}

hljs.registerLanguage('bash', bash)
hljs.registerLanguage('css', css)
hljs.registerLanguage('django', django)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('json', json)
hljs.registerLanguage('markdown', markdownLanguage)
hljs.registerLanguage('python', python)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('xml', xml)
hljs.registerAliases(['js'], { languageName: 'javascript' })
hljs.registerAliases(['ts'], { languageName: 'typescript' })
hljs.registerAliases(['md'], { languageName: 'markdown' })
hljs.registerAliases(['py'], { languageName: 'python' })
hljs.registerAliases(['shell', 'sh', 'zsh', 'powershell', 'ps1'], { languageName: 'bash' })
hljs.registerAliases(['vue'], { languageName: 'html' })

const escapeHtml = (value: string) =>
  value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')

const normalizeHeadingText = (value: string) =>
  value
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/[*_~>#]/g, '')
    .trim()

const buildHeadingId = (value: string, counts: Map<string, number>) => {
  const normalized = normalizeHeadingText(value)
  const fallback = `section-${counts.size + 1}`
  const base =
    normalized
      .toLowerCase()
      .replace(/[^\p{Script=Han}\p{Letter}\p{Number}\s-]/gu, '')
      .trim()
      .replace(/\s+/g, '-') || fallback
  const nextCount = (counts.get(base) || 0) + 1
  counts.set(base, nextCount)
  return nextCount === 1 ? base : `${base}-${nextCount}`
}

const markdown: MarkdownIt = new MarkdownIt({
  html: true,
  linkify: true,
  breaks: true,
  highlight(code: string, language: string): string {
    const validLanguage = language && hljs.getLanguage(language) ? language : 'plaintext'
    const highlighted: string =
      validLanguage === 'plaintext'
        ? escapeHtml(code)
        : hljs.highlight(code, { language: validLanguage }).value

    return `<pre><code class="hljs language-${validLanguage}">${highlighted}</code></pre>`
  },
})

const defaultLinkRenderer =
  markdown.renderer.rules.link_open ||
  ((tokens: any[], idx: number, options: any, _env: any, self: any) =>
    self.renderToken(tokens, idx, options))

markdown.renderer.rules.link_open = (
  tokens: any[],
  idx: number,
  options: any,
  env: any,
  self: any,
) => {
  const token = tokens[idx]
  token.attrSet('target', '_blank')
  token.attrSet('rel', 'noreferrer noopener')
  return defaultLinkRenderer(tokens, idx, options, env, self)
}

const defaultImageRenderer =
  markdown.renderer.rules.image ||
  ((tokens: any[], idx: number, options: any, env: any, self: any) =>
    self.renderToken(tokens, idx, options, env))

markdown.renderer.rules.image = (
  tokens: any[],
  idx: number,
  options: any,
  env: any,
  self: any,
) => {
  const token = tokens[idx]
  token.attrSet('loading', 'lazy')
  token.attrSet('decoding', 'async')
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const defaultHeadingRenderer =
  markdown.renderer.rules.heading_open ||
  ((tokens: any[], idx: number, options: any, _env: any, self: any) =>
    self.renderToken(tokens, idx, options))

markdown.renderer.rules.heading_open = (
  tokens: any[],
  idx: number,
  options: any,
  env: { headingCounts?: Map<string, number> },
  self: any,
) => {
  const token = tokens[idx]
  const level = Number(token.tag.replace('h', ''))

  if (level === 2 || level === 3) {
    const headingCounts = env.headingCounts || new Map<string, number>()
    env.headingCounts = headingCounts
    const title = tokens[idx + 1]?.content || ''
    token.attrSet('id', buildHeadingId(title, headingCounts))
  }

  return defaultHeadingRenderer(tokens, idx, options, env, self)
}

export function renderMarkdown(content: string) {
  if (!content.trim()) {
    return ''
  }

  const rawHtml = markdown.render(stripXmindMarker(content), {
    headingCounts: new Map<string, number>(),
  })
  return DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['target', 'rel', 'id', 'loading', 'decoding'],
  })
}

export function extractMarkdownHeadings(content: string): MarkdownHeading[] {
  const counts = new Map<string, number>()

  return stripXmindMarker(content)
    .split(/\r?\n/)
    .map((line) => line.match(/^(#{2,3})\s+(.+)$/))
    .filter((match): match is RegExpMatchArray => Boolean(match))
    .map((match) => {
      const text = normalizeHeadingText(match[2])
      return {
        id: buildHeadingId(text, counts),
        level: match[1].length as 2 | 3,
        text,
      }
    })
    .filter((heading) => heading.text.length > 0)
}

export function isXmindContent(content: string) {
  if (!content.trim()) {
    return false
  }

  if (content.includes(XMIND_SOURCE_MARKER)) {
    return true
  }

  const normalized = stripXmindMarker(content)
  const lines = normalized
    .split(/\r?\n/)
    .map((line) => line.trimEnd())
    .filter((line) => line.trim().length > 0)

  if (lines.length < 3 || !lines[0].trim().startsWith('#')) {
    return false
  }

  const outlineLines = lines.slice(1)
  const bulletLines = outlineLines.filter((line) => /^(\s{0,12}-\s+.+)$/.test(line)).length
  const plainLines = outlineLines.filter((line) => !/^(\s{0,12}-\s+.+)$/.test(line)).length

  return bulletLines >= 3 && bulletLines > plainLines
}

export function parseXmindContent(content: string): XmindNode | null {
  if (!isXmindContent(content)) {
    return null
  }

  const normalized = stripXmindMarker(content)
  const lines = normalized
    .split(/\r?\n/)
    .map((line) => line.replace(/\t/g, '  ').trimEnd())
    .filter((line) => line.trim().length > 0)

  if (lines.length === 0) {
    return null
  }

  const rootLine = lines.find((line) => line.trim().startsWith('#'))
  if (!rootLine) {
    return null
  }

  let id = 0
  const root: XmindNode = {
    id: `xmind-node-${id++}`,
    title: rootLine.replace(/^#+\s*/, '').trim(),
    children: [],
  }

  const stack: Array<{ depth: number; node: XmindNode }> = [{ depth: -1, node: root }]
  let lastNode = root

  for (const line of lines.slice(lines.indexOf(rootLine) + 1)) {
    const bulletMatch = line.match(/^(\s*)[-*]\s+(.+)$/)

    if (!bulletMatch) {
      const plainText = line.trim()
      if (plainText && !plainText.startsWith('#')) {
        lastNode.title = `${lastNode.title} ${plainText}`.trim()
      }
      continue
    }

    const indent = bulletMatch[1].length
    const depth = Math.floor(indent / 2)
    const title = bulletMatch[2].trim()
    const node: XmindNode = {
      id: `xmind-node-${id++}`,
      title,
      children: [],
    }

    while (stack.length > 0 && stack[stack.length - 1].depth >= depth) {
      stack.pop()
    }

    const parent = stack[stack.length - 1]?.node ?? root
    parent.children.push(node)
    stack.push({ depth, node })
    lastNode = node
  }

  return root
}

function stripXmindMarker(content: string) {
  return content.replace(XMIND_SOURCE_MARKER, '').trim()
}

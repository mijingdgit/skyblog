import DOMPurify from 'dompurify'
import hljs from 'highlight.js'
import MarkdownIt from 'markdown-it'

const escapeHtml = (value: string) =>
  value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')

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

export function renderMarkdown(content: string) {
  if (!content.trim()) {
    return ''
  }

  const rawHtml = markdown.render(content)
  return DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['target', 'rel'],
  })
}

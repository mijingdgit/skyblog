(function () {
  const MODE_META = {
    markdown: {
      label: "Markdown 文档",
      shortLabel: "MD",
      hint: "像新建文档一样写作：左侧编辑、右侧预览，自动生成大纲与草稿。",
      foot: "Markdown 原稿会保存到正文；上传 Markdown 文件后保存，后台会自动提取正文并处理可访问的本地图片。",
    },
    xmind: {
      label: "XMind 大纲",
      shortLabel: "XMind",
      hint: "编辑导入后的层级大纲，并用思维导图方式预览结构。",
      foot: "浏览器中不能直接编辑 .xmind 二进制文件；这里编辑的是导入后的 Markdown 大纲，重新上传 .xmind 后保存会覆盖正文。",
    },
    text: {
      label: "普通文本",
      shortLabel: "Text",
      hint: "适合 Word 导入后的文本整理，保留正文编辑、统计与基础预览。",
      foot: "上传 .doc/.docx 后保存会提取正文；复杂排版建议整理成 Markdown 后再发布。",
    },
  }

  const toolbarActions = [
    { label: "H1", title: "一级标题", type: "prefix", before: "# " },
    { label: "H2", title: "二级标题", type: "prefix", before: "## " },
    { label: "H3", title: "三级标题", type: "prefix", before: "### " },
    { label: "B", title: "加粗", type: "wrap", before: "**", after: "**" },
    { label: "I", title: "斜体", type: "wrap", before: "*", after: "*" },
    { label: "引用", title: "引用块", type: "prefix", before: "> " },
    { label: "代码", title: "代码块", type: "wrap", before: "```\n", after: "\n```" },
    { label: "无序", title: "无序列表", type: "prefix", before: "- " },
    { label: "有序", title: "有序列表", type: "ordered" },
    { label: "任务", title: "任务清单", type: "prefix", before: "- [ ] " },
    { label: "表格", title: "插入表格", type: "insert", value: "\n| 字段 | 说明 |\n| --- | --- |\n| 标题 | 内容 |\n" },
    { label: "分割", title: "分割线", type: "insert", value: "\n---\n" },
  ]

  const insertActions = [
    {
      label: "图片",
      icon: "▧",
      group: "基础",
      description: "上传图片并插入 Markdown",
      uploadType: "image",
      accept: "image/*,.svg",
    },
    {
      label: "表格",
      icon: "▦",
      group: "基础",
      description: "插入两列表格",
      value: "\n| 字段 | 说明 |\n| --- | --- |\n| 标题 | 内容 |\n",
    },
    {
      label: "附件",
      icon: "⇧",
      group: "基础",
      description: "上传附件并插入链接",
      uploadType: "attachment",
      accept: ".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.7z,.txt,.md,.csv,.json,.xmind,image/*",
    },
    {
      label: "状态",
      icon: "☑",
      group: "基础",
      description: "插入待办状态清单",
      value: "\n- [ ] 待处理\n- [x] 已完成\n",
    },
    {
      label: "AI 写作助手",
      icon: "AI",
      group: "智能专区",
      description: "整理写作目标和约束",
      value: "\n> AI 写作提示：请在这里写清楚目标、背景、读者和约束。\n",
    },
    {
      label: "思维导图",
      icon: "◎",
      group: "画板类",
      description: "插入可被 XMind 模式预览的大纲",
      value: "\n:::xmind\n# 思维导图主题\n- 一级分支\n  - 二级节点\n- 另一个分支\n:::\n",
      mode: "xmind",
    },
    {
      label: "流程图",
      icon: "◇",
      group: "画板类",
      description: "插入 Mermaid 流程图代码块",
      value: "\n```mermaid\ngraph TD\n  A[开始] --> B[处理]\n  B --> C[结束]\n```\n",
    },
    {
      label: "代码块",
      icon: "</>",
      group: "最近使用",
      description: "插入代码块",
      value: "\n```python\nprint(\"hello skyblog\")\n```\n",
    },
  ]

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;")
  }

  function slugId(value, index) {
    const slug = value
      .trim()
      .toLowerCase()
      .replace(/[^\u4e00-\u9fa5a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
    return `doc-heading-${slug || index}`
  }

  function inlineMarkdown(value) {
    let escaped = escapeHtml(value)
    escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>")
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    escaped = escaped.replace(/\*([^*]+)\*/g, "<em>$1</em>")
    escaped = escaped.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
    return escaped
  }

  function parseTable(lines, startIndex) {
    const rows = []
    let index = startIndex

    while (index < lines.length && lines[index].includes("|")) {
      rows.push(lines[index])
      index += 1
    }

    if (rows.length < 2 || !/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(rows[1])) {
      return null
    }

    const cells = rows.map((row) =>
      row
        .trim()
        .replace(/^\|/, "")
        .replace(/\|$/, "")
        .split("|")
        .map((cell) => inlineMarkdown(cell.trim())),
    )

    const head = cells[0].map((cell) => `<th>${cell}</th>`).join("")
    const body = cells
      .slice(2)
      .map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`)
      .join("")

    return {
      nextIndex: index,
      html: `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`,
    }
  }

  function renderMarkdown(source) {
    const lines = source.replace(/^<!-- source:xmind -->\s*/i, "").split(/\r?\n/)
    const html = []
    let inCode = false
    let paragraph = []
    let listType = ""
    let blockquote = []
    let headingIndex = 0

    function flushParagraph() {
      if (paragraph.length) {
        html.push(`<p>${inlineMarkdown(paragraph.join(" "))}</p>`)
        paragraph = []
      }
    }

    function flushList() {
      if (listType) {
        html.push(`</${listType}>`)
        listType = ""
      }
    }

    function flushBlockquote() {
      if (blockquote.length) {
        html.push(`<blockquote>${blockquote.map(inlineMarkdown).join("<br>")}</blockquote>`)
        blockquote = []
      }
    }

    for (let lineIndex = 0; lineIndex < lines.length; lineIndex += 1) {
      const line = lines[lineIndex]

      if (line.trim().startsWith("```")) {
        flushParagraph()
        flushList()
        flushBlockquote()
        if (inCode) {
          html.push("</code></pre>")
          inCode = false
        } else {
          html.push("<pre><code>")
          inCode = true
        }
        continue
      }

      if (inCode) {
        html.push(`${escapeHtml(line)}\n`)
        continue
      }

      const trimmed = line.trim()
      if (!trimmed) {
        flushParagraph()
        flushList()
        flushBlockquote()
        continue
      }

      const table = parseTable(lines, lineIndex)
      if (table) {
        flushParagraph()
        flushList()
        flushBlockquote()
        html.push(table.html)
        lineIndex = table.nextIndex - 1
        continue
      }

      if (/^---+$/.test(trimmed)) {
        flushParagraph()
        flushList()
        flushBlockquote()
        html.push("<hr>")
        continue
      }

      const heading = /^(#{1,4})\s+(.+)$/.exec(trimmed)
      if (heading) {
        flushParagraph()
        flushList()
        flushBlockquote()
        const level = heading[1].length
        const text = heading[2]
        html.push(`<h${level} id="${slugId(text, headingIndex)}">${inlineMarkdown(text)}</h${level}>`)
        headingIndex += 1
        continue
      }

      const task = /^[-*]\s+\[( |x|X)\]\s+(.+)$/.exec(trimmed)
      const unordered = /^[-*]\s+(.+)$/.exec(trimmed)
      const ordered = /^\d+[.)]\s+(.+)$/.exec(trimmed)
      if (task || unordered || ordered) {
        flushParagraph()
        flushBlockquote()
        const nextType = ordered ? "ol" : "ul"
        if (listType && listType !== nextType) {
          flushList()
        }
        if (!listType) {
          html.push(`<${nextType}>`)
          listType = nextType
        }
        if (task) {
          const checked = task[1].toLowerCase() === "x" ? " checked" : ""
          html.push(`<li class="task-list-item"><input type="checkbox" disabled${checked}> ${inlineMarkdown(task[2])}</li>`)
        } else {
          html.push(`<li>${inlineMarkdown((unordered || ordered)[1])}</li>`)
        }
        continue
      }

      if (trimmed.startsWith(">")) {
        flushParagraph()
        flushList()
        blockquote.push(trimmed.replace(/^>\s?/, ""))
        continue
      }

      paragraph.push(trimmed)
    }

    flushParagraph()
    flushList()
    flushBlockquote()
    if (inCode) {
      html.push("</code></pre>")
    }

    return html.join("\n") || '<p class="skyblog-editor-empty">暂无内容，开始输入后这里会显示预览。</p>'
  }

  function extractXmindBlocks(source) {
    const blocks = []
    const pattern = /:::xmind\s*([\s\S]*?)\s*:::/gi
    let match

    while ((match = pattern.exec(source)) !== null) {
      blocks.push(match[1].trim())
    }

    if (blocks.length) {
      return blocks
    }

    const lines = source.replace(/^<!-- source:xmind -->\s*/i, "").split(/\r?\n/)
    const fallback = []
    let started = false

    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed) {
        if (started) {
          break
        }
        continue
      }

      if (!started && /^#\s+/.test(trimmed)) {
        started = true
        fallback.push(line)
        continue
      }

      if (started && /^(\s*)[-*]\s+/.test(line.replace(/\t/g, "  "))) {
        fallback.push(line)
        continue
      }

      if (started) {
        break
      }
    }

    return fallback.length ? [fallback.join("\n")] : []
  }

  function stripXmindBlocks(source) {
    return source.replace(/:::xmind\s*[\s\S]*?\s*:::/gi, "").trim()
  }

  function extractHeadings(source) {
    const headings = []
    source.replace(/^<!-- source:xmind -->\s*/i, "").split(/\r?\n/).forEach((line) => {
      const heading = /^(#{1,4})\s+(.+)$/.exec(line.trim())
      if (heading) {
        headings.push({
          level: heading[1].length,
          text: heading[2],
          id: slugId(heading[2], headings.length),
        })
      }
    })
    return headings
  }

  function renderXmind(source) {
    const xmindBlocks = extractXmindBlocks(source)
    const xmindSource = xmindBlocks[0] || ""
    const lines = xmindSource.replace(/^<!-- source:xmind -->\s*/i, "").split(/\r?\n/)
    const root = { text: "", children: [] }
    const stack = [{ depth: -1, node: root }]

    lines.forEach((line) => {
      if (!line.trim()) {
        return
      }

      const trimmed = line.trim()
      if (trimmed.startsWith("#")) {
        const node = { text: trimmed.replace(/^#+\s*/, ""), children: [] }
        root.children.push(node)
        stack.length = 1
        stack.push({ depth: 0, node })
        return
      }

      const bullet = /^(\s*)[-*]\s+(.+)$/.exec(line.replace(/\t/g, "  "))
      if (bullet) {
        const depth = Math.floor(bullet[1].length / 2) + 1
        const node = { text: bullet[2].trim(), children: [] }
        while (stack.length > 1 && stack[stack.length - 1].depth >= depth) {
          stack.pop()
        }
        stack[stack.length - 1].node.children.push(node)
        stack.push({ depth, node })
      }
    })

    if (!root.children.length) {
      return '<p class="skyblog-editor-empty">XMind 大纲会以标题和列表层级生成预览。</p>'
    }

    function renderNode(node, depth = 0) {
      const children = node.children
        .map((child) => renderNode(child, depth + 1))
        .join("")
      return `
        <li class="skyblog-xmind-branch" data-depth="${Math.min(depth, 8)}">
          <div class="skyblog-xmind-node" data-xmind-node>${inlineMarkdown(node.text)}</div>
          ${children ? `<ul>${children}</ul>` : ""}
        </li>
      `
    }

    const topic = root.children[0]
    const extraRoots = root.children.slice(1)
    if (extraRoots.length) {
      topic.children.push(...extraRoots)
    }

    return `
      <div class="skyblog-xmind-map">
        <svg class="skyblog-xmind-links" aria-hidden="true"></svg>
        <div class="skyblog-xmind-root" data-xmind-root>${inlineMarkdown(topic.text)}</div>
        <ul class="skyblog-xmind-tree">
          ${topic.children.map((child) => renderNode(child, 1)).join("")}
        </ul>
      </div>
    `
  }

  function drawXmindLinks(preview) {
    const map = preview.querySelector(".skyblog-xmind-map")
    const svg = preview.querySelector(".skyblog-xmind-links")
    const root = preview.querySelector("[data-xmind-root]")
    if (!map || !svg || !root) {
      return
    }

    const mapRect = map.getBoundingClientRect()
    const paths = []

    function centerRight(element) {
      const rect = element.getBoundingClientRect()
      return {
        x: rect.right - mapRect.left,
        y: rect.top - mapRect.top + rect.height / 2,
      }
    }

    function centerLeft(element) {
      const rect = element.getBoundingClientRect()
      return {
        x: rect.left - mapRect.left,
        y: rect.top - mapRect.top + rect.height / 2,
      }
    }

    function addLink(fromElement, toElement) {
      const start = centerRight(fromElement)
      const end = centerLeft(toElement)
      const dx = Math.max(34, (end.x - start.x) / 2)
      paths.push(
        `<path d="M ${start.x} ${start.y} C ${start.x + dx} ${start.y}, ${end.x - dx} ${end.y}, ${end.x} ${end.y}" />`,
      )
    }

    map.querySelectorAll(":scope > .skyblog-xmind-tree > .skyblog-xmind-branch").forEach((branch) => {
      const node = branch.querySelector(":scope > [data-xmind-node]")
      if (node) {
        addLink(root, node)
      }
    })

    map.querySelectorAll(".skyblog-xmind-branch").forEach((branch) => {
      const parentNode = branch.querySelector(":scope > [data-xmind-node]")
      if (!parentNode) {
        return
      }
      branch.querySelectorAll(":scope > ul > .skyblog-xmind-branch").forEach((childBranch) => {
        const childNode = childBranch.querySelector(":scope > [data-xmind-node]")
        if (childNode) {
          addLink(parentNode, childNode)
        }
      })
    })

    svg.setAttribute("viewBox", `0 0 ${Math.max(1, map.scrollWidth)} ${Math.max(1, map.scrollHeight)}`)
    svg.setAttribute("width", String(map.scrollWidth))
    svg.setAttribute("height", String(map.scrollHeight))
    svg.innerHTML = paths.join("")
  }

  function selectedLineRange(textarea) {
    const value = textarea.value
    let start = textarea.selectionStart
    let end = textarea.selectionEnd

    while (start > 0 && value[start - 1] !== "\n") {
      start -= 1
    }
    while (end < value.length && value[end] !== "\n") {
      end += 1
    }

    return [start, end]
  }

  function wrapSelection(textarea, before, after) {
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const selected = textarea.value.slice(start, end) || "内容"
    textarea.setRangeText(`${before}${selected}${after}`, start, end, "select")
    textarea.dispatchEvent(new Event("input", { bubbles: true }))
    textarea.focus()
  }

  function prefixSelectedLines(textarea, prefix) {
    const [start, end] = selectedLineRange(textarea)
    const selected = textarea.value.slice(start, end) || "内容"
    const next = selected
      .split(/\n/)
      .map((line) => (line ? `${prefix}${line}` : line))
      .join("\n")
    textarea.setRangeText(next, start, end, "select")
    textarea.dispatchEvent(new Event("input", { bubbles: true }))
    textarea.focus()
  }

  function orderedSelectedLines(textarea) {
    const [start, end] = selectedLineRange(textarea)
    const selected = textarea.value.slice(start, end) || "内容"
    const next = selected
      .split(/\n/)
      .map((line, index) => (line ? `${index + 1}. ${line}` : line))
      .join("\n")
    textarea.setRangeText(next, start, end, "select")
    textarea.dispatchEvent(new Event("input", { bubbles: true }))
    textarea.focus()
  }

  function insertText(textarea, value) {
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    textarea.setRangeText(value, start, end, "end")
    textarea.dispatchEvent(new Event("input", { bubbles: true }))
    textarea.focus()
  }

  function readCookie(name) {
    const pattern = new RegExp(`(?:^|; )${name}=([^;]*)`)
    const match = document.cookie.match(pattern)
    return match ? decodeURIComponent(match[1]) : ""
  }

  function markdownForUploadedAsset(asset) {
    const name = asset.name || "附件"
    if (asset.type === "image") {
      return `\n![${name}](${asset.url})\n`
    }
    return `\n[${name}](${asset.url})\n`
  }

  async function uploadEditorAsset(file, assetType) {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("type", assetType)

    const response = await fetch("/api/articles/assets/upload/", {
      method: "POST",
      body: formData,
      credentials: "include",
      headers: {
        "X-CSRFToken": readCookie("csrftoken"),
      },
    })
    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.message || `上传失败(${response.status})`)
    }

    return data
  }

  function detectMode(textarea, sourceInput) {
    const fileName = sourceInput && sourceInput.files && sourceInput.files[0]
      ? sourceInput.files[0].name.toLowerCase()
      : ""
    const content = textarea.value.trim()

    if (fileName.endsWith(".xmind") || /^<!-- source:xmind -->/i.test(content)) {
      return "xmind"
    }
    if (fileName.endsWith(".doc") || fileName.endsWith(".docx")) {
      return "text"
    }
    if (fileName.endsWith(".md") || fileName.endsWith(".markdown")) {
      return "markdown"
    }
    if (/^#{1,4}\s/m.test(content) || /```/.test(content) || /\|.+\|/.test(content)) {
      return "markdown"
    }
    return "text"
  }

  function formatTime(timestamp) {
    if (!timestamp) {
      return "尚未保存草稿"
    }
    const date = new Date(timestamp)
    return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")} 已保存草稿`
  }

  function enhanceTitleField() {
    const title = document.getElementById("id_title")
    const excerpt = document.getElementById("id_excerpt")
    if (!title || title.dataset.skyblogTitle === "ready") {
      return
    }

    title.dataset.skyblogTitle = "ready"
    title.placeholder = "输入文章标题"
    title.closest(".form-row")?.classList.add("skyblog-doc-title-row")
    excerpt?.closest(".form-row")?.classList.add("skyblog-doc-excerpt-row")
  }

  function enhanceArticleEditor() {
    const textarea = document.getElementById("id_content")
    if (!textarea || textarea.dataset.skyblogEditor === "ready") {
      return
    }

    enhanceTitleField()

    const form = textarea.closest("form")
    const titleInput = document.getElementById("id_title")
    const sourceInput = document.getElementById("id_source_file")
    const draftKey = `skyblog:article-draft:${window.location.pathname}`
    const shell = document.createElement("div")
    shell.className = "skyblog-article-editor"
    shell.dataset.view = "split"

    const head = document.createElement("div")
    head.className = "skyblog-article-editor__head"
    head.innerHTML = `
      <div class="skyblog-article-editor__title">
        <span class="skyblog-article-editor__badge"></span>
        <span class="skyblog-article-editor__hint"></span>
      </div>
      <div class="skyblog-article-editor__actions" aria-label="正文类型"></div>
    `

    const tabs = document.createElement("div")
    tabs.className = "skyblog-article-editor__tabs"
    tabs.innerHTML = `
      <button type="button" data-view="edit">编辑</button>
      <button type="button" data-view="split">分屏</button>
      <button type="button" data-view="preview">预览</button>
      <button type="button" data-action="focus">专注</button>
      <button type="button" data-action="restore" hidden>恢复草稿</button>
    `

    const toolbar = document.createElement("div")
    toolbar.className = "skyblog-article-editor__toolbar"
    const insertPanel = document.createElement("div")
    insertPanel.className = "skyblog-insert-panel"
    insertPanel.hidden = true

    const body = document.createElement("div")
    body.className = "skyblog-article-editor__body"
    const edit = document.createElement("div")
    edit.className = "skyblog-article-editor__edit"
    const preview = document.createElement("div")
    preview.className = "skyblog-article-editor__preview"
    const outline = document.createElement("aside")
    outline.className = "skyblog-article-editor__outline"
    const foot = document.createElement("div")
    foot.className = "skyblog-article-editor__foot"

    textarea.parentNode.insertBefore(shell, textarea)
    edit.appendChild(textarea)
    body.appendChild(edit)
    body.appendChild(preview)
    body.appendChild(outline)
    shell.appendChild(head)
    shell.appendChild(tabs)
    shell.appendChild(toolbar)
    shell.appendChild(insertPanel)
    shell.appendChild(body)
    shell.appendChild(foot)
    textarea.dataset.skyblogEditor = "ready"

    const modeActions = head.querySelector(".skyblog-article-editor__actions")
    const badge = head.querySelector(".skyblog-article-editor__badge")
    const hint = head.querySelector(".skyblog-article-editor__hint")
    const restoreButton = tabs.querySelector('[data-action="restore"]')
    const focusButton = tabs.querySelector('[data-action="focus"]')
    const assetInput = document.createElement("input")
    assetInput.type = "file"
    assetInput.className = "skyblog-asset-input"
    assetInput.hidden = true
    shell.appendChild(assetInput)
    let pendingUploadAction = null

    Object.keys(MODE_META).forEach((mode) => {
      const button = document.createElement("button")
      button.type = "button"
      button.dataset.mode = mode
      button.textContent = MODE_META[mode].shortLabel
      button.title = MODE_META[mode].label
      button.addEventListener("click", () => setMode(mode))
      modeActions.appendChild(button)
    })

    tabs.querySelectorAll("[data-view]").forEach((button) => {
      button.addEventListener("click", () => {
        shell.dataset.view = button.dataset.view
        updateActiveButtons()
      })
    })

    function syncFocusState(active) {
      shell.classList.toggle("is-focus", active)
      document.body.classList.toggle("skyblog-editor-focus-mode", active)
      focusButton.textContent = active ? "退出专注" : "专注"
      focusButton.classList.toggle("is-active", active)
    }

    async function enterFocusMode() {
      syncFocusState(true)
      shell.dataset.view = shell.dataset.view || "split"
      updateActiveButtons()
      try {
        if (shell.requestFullscreen && document.fullscreenElement !== shell) {
          await shell.requestFullscreen()
        }
      } catch {
        // Browser fullscreen can be blocked by permissions; CSS fullscreen still works.
      }
      textarea.focus()
    }

    async function exitFocusMode() {
      syncFocusState(false)
      try {
        if (document.fullscreenElement === shell && document.exitFullscreen) {
          await document.exitFullscreen()
        }
      } catch {
        // Keep the editor usable even when the browser rejects fullscreen exit.
      }
    }

    focusButton.addEventListener("click", () => {
      if (shell.classList.contains("is-focus")) {
        void exitFocusMode()
      } else {
        void enterFocusMode()
      }
    })

    document.addEventListener("fullscreenchange", () => {
      if (document.fullscreenElement !== shell && shell.classList.contains("is-focus")) {
        syncFocusState(false)
      }
    })

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && shell.classList.contains("is-focus")) {
        void exitFocusMode()
      }
    })

    restoreButton.addEventListener("click", () => {
      const draft = readDraft()
      if (!draft) {
        return
      }
      if (!window.confirm("恢复本地草稿会覆盖当前编辑区内容，确定继续吗？")) {
        return
      }
      textarea.value = draft.content || ""
      if (titleInput && draft.title) {
        titleInput.value = draft.title
      }
      textarea.dispatchEvent(new Event("input", { bubbles: true }))
      titleInput?.dispatchEvent(new Event("input", { bubbles: true }))
    })

    const insertTrigger = document.createElement("button")
    insertTrigger.type = "button"
    insertTrigger.className = "skyblog-insert-trigger"
    insertTrigger.textContent = "+"
    insertTrigger.title = "插入内容"
    toolbar.appendChild(insertTrigger)

    const toolbarDivider = document.createElement("span")
    toolbarDivider.className = "skyblog-toolbar-divider"
    toolbar.appendChild(toolbarDivider)

    function renderInsertPanel(keyword = "") {
      const normalizedKeyword = keyword.trim().toLowerCase()
      const filtered = insertActions.filter((action) => {
        const haystack = `${action.label} ${action.group} ${action.description}`.toLowerCase()
        return !normalizedKeyword || haystack.includes(normalizedKeyword)
      })
      const groups = [...new Set(filtered.map((action) => action.group))]
      const content = groups
        .map((group) => {
          const items = filtered
            .filter((action) => action.group === group)
            .map(
              (action) => `
                <button type="button" class="skyblog-insert-item" data-insert-label="${escapeHtml(action.label)}">
                  <span class="skyblog-insert-icon" aria-hidden="true">${escapeHtml(action.icon || action.label.slice(0, 2))}</span>
                  <span>
                    <strong>${escapeHtml(action.label)}</strong>
                    <small>${escapeHtml(action.description)}</small>
                  </span>
                </button>
              `,
            )
            .join("")
          return `
            <section class="skyblog-insert-group">
              <p>${escapeHtml(group)}</p>
              <div>${items}</div>
            </section>
          `
        })
        .join("")

      insertPanel.innerHTML = `
        <div class="skyblog-insert-search">
          <input type="search" placeholder="请输入要搜索的功能名称" value="${escapeHtml(keyword)}">
        </div>
        ${content || '<p class="skyblog-editor-empty">没有找到匹配的插入项。</p>'}
      `

      insertPanel.querySelector("input")?.addEventListener("input", (event) => {
        renderInsertPanel(event.target.value)
      })
      insertPanel.querySelectorAll(".skyblog-insert-item").forEach((button) => {
        button.addEventListener("click", () => {
          const action = insertActions.find((item) => item.label === button.dataset.insertLabel)
          if (!action) {
            return
          }
          if (action.uploadType) {
            pendingUploadAction = action
            assetInput.accept = action.accept || ""
            assetInput.value = ""
            assetInput.click()
          } else {
            insertText(textarea, action.value)
            if (action.mode) {
              setMode(action.mode)
            }
            closeInsertPanel()
          }
        })
      })
    }

    function setUploadState(message, isError = false) {
      let status = insertPanel.querySelector(".skyblog-upload-status")
      if (!status) {
        status = document.createElement("p")
        status.className = "skyblog-upload-status"
        insertPanel.appendChild(status)
      }
      status.textContent = message
      status.classList.toggle("is-error", isError)
    }

    assetInput.addEventListener("change", async () => {
      const file = assetInput.files && assetInput.files[0]
      if (!file || !pendingUploadAction) {
        return
      }

      insertPanel.hidden = false
      insertTrigger.classList.add("is-active")
      setUploadState(`正在上传：${file.name}`)

      try {
        const asset = await uploadEditorAsset(file, pendingUploadAction.uploadType)
        insertText(textarea, markdownForUploadedAsset(asset))
        setUploadState(`已上传：${asset.name}`)
        window.setTimeout(() => {
          closeInsertPanel()
        }, 650)
      } catch (error) {
        setUploadState(error.message || "上传失败，请重试。", true)
      } finally {
        pendingUploadAction = null
        assetInput.value = ""
      }
    })

    insertTrigger.addEventListener("click", () => {
      insertPanel.hidden = !insertPanel.hidden
      insertTrigger.classList.toggle("is-active", !insertPanel.hidden)
      if (!insertPanel.hidden) {
        renderInsertPanel()
        insertPanel.querySelector("input")?.focus()
      }
    })

    function closeInsertPanel() {
      insertPanel.hidden = true
      insertTrigger.classList.remove("is-active")
    }

    document.addEventListener("pointerdown", (event) => {
      if (
        insertPanel.hidden ||
        insertPanel.contains(event.target) ||
        insertTrigger.contains(event.target)
      ) {
        return
      }
      closeInsertPanel()
    })

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !insertPanel.hidden) {
        closeInsertPanel()
        insertTrigger.focus()
      }
    })

    toolbarActions.forEach((action) => {
      const button = document.createElement("button")
      button.type = "button"
      button.textContent = action.label
      button.title = action.title
      button.addEventListener("click", () => {
        if (action.type === "prefix") {
          prefixSelectedLines(textarea, action.before)
        } else if (action.type === "wrap") {
          wrapSelection(textarea, action.before, action.after)
        } else if (action.type === "ordered") {
          orderedSelectedLines(textarea)
        } else if (action.type === "insert") {
          insertText(textarea, action.value)
        }
      })
      toolbar.appendChild(button)
    })

    let draftTimer

    function readDraft() {
      try {
        return JSON.parse(window.localStorage.getItem(draftKey) || "null")
      } catch {
        return null
      }
    }

    function scheduleDraftSave() {
      window.clearTimeout(draftTimer)
      draftTimer = window.setTimeout(() => {
        window.localStorage.setItem(
          draftKey,
          JSON.stringify({
            content: textarea.value,
            title: titleInput?.value || "",
            updatedAt: Date.now(),
          }),
        )
        render()
      }, 450)
    }

    function setMode(mode) {
      shell.dataset.mode = mode
      badge.textContent = MODE_META[mode].label
      hint.textContent = MODE_META[mode].hint
      foot.textContent = MODE_META[mode].foot
      toolbar.classList.toggle("is-text-mode", mode === "text")
      updateActiveButtons()
      render()
    }

    function renderOutline(headings) {
      const cleanTextLength = textarea.value.replace(/\s+/g, "").length
      const minutes = Math.max(1, Math.round(cleanTextLength / 500))
      const draft = readDraft()
      const draftChanged = draft && draft.content && draft.content !== textarea.value
      restoreButton.hidden = !draftChanged

      const headingList = headings.length
        ? headings
            .map(
              (heading) =>
                `<button type="button" class="skyblog-outline-link level-${heading.level}" data-heading-id="${heading.id}">${escapeHtml(heading.text)}</button>`,
            )
            .join("")
        : '<p class="skyblog-editor-empty">用 #、##、### 写标题后，这里会生成文档大纲。</p>'

      outline.innerHTML = `
        <div class="skyblog-outline-card">
          <p class="skyblog-outline-kicker">文档状态</p>
          <div class="skyblog-outline-stats">
            <span>${cleanTextLength} 字</span>
            <span>${minutes} 分钟阅读</span>
          </div>
          <p class="skyblog-outline-draft">${formatTime(draft?.updatedAt)}</p>
        </div>
        <div class="skyblog-outline-card">
          <p class="skyblog-outline-kicker">大纲</p>
          <div class="skyblog-outline-list">${headingList}</div>
        </div>
      `

      outline.querySelectorAll(".skyblog-outline-link").forEach((button) => {
        button.addEventListener("click", () => {
          preview.querySelector(`#${CSS.escape(button.dataset.headingId)}`)?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          })
        })
      })
    }

    function render() {
      const headings = extractHeadings(stripXmindBlocks(textarea.value))
      if (shell.dataset.mode === "xmind") {
        const articleMarkdown = stripXmindBlocks(textarea.value)
        const articleHtml = articleMarkdown
          ? `<div class="skyblog-xmind-article">${renderMarkdown(articleMarkdown)}</div>`
          : ""
        preview.innerHTML = `${renderXmind(textarea.value)}${articleHtml}`
      } else {
        preview.innerHTML = renderMarkdown(textarea.value)
      }
      renderOutline(headings)
      if (shell.dataset.mode === "xmind") {
        window.requestAnimationFrame(() => drawXmindLinks(preview))
      }
    }

    function updateActiveButtons() {
      modeActions.querySelectorAll("button").forEach((button) => {
        button.classList.toggle("is-active", button.dataset.mode === shell.dataset.mode)
      })
      tabs.querySelectorAll("[data-view]").forEach((button) => {
        button.classList.toggle("is-active", button.dataset.view === shell.dataset.view)
      })
    }

    function handleShortcuts(event) {
      if (!event.ctrlKey && !event.metaKey) {
        return
      }

      const key = event.key.toLowerCase()
      if (key === "b") {
        event.preventDefault()
        wrapSelection(textarea, "**", "**")
      } else if (key === "i") {
        event.preventDefault()
        wrapSelection(textarea, "*", "*")
      } else if (event.altKey && ["1", "2", "3"].includes(key)) {
        event.preventDefault()
        prefixSelectedLines(textarea, `${"#".repeat(Number(key))} `)
      }
    }

    textarea.addEventListener("input", () => {
      render()
      scheduleDraftSave()
    })
    textarea.addEventListener("keydown", handleShortcuts)
    titleInput?.addEventListener("input", scheduleDraftSave)
    preview.addEventListener("scroll", () => {
      if (shell.dataset.mode === "xmind") {
        drawXmindLinks(preview)
      }
    })
    window.addEventListener("resize", () => {
      if (shell.dataset.mode === "xmind") {
        drawXmindLinks(preview)
      }
    })

    if (sourceInput) {
      sourceInput.addEventListener("change", () => setMode(detectMode(textarea, sourceInput)))
    }

    form?.addEventListener("submit", () => {
      window.localStorage.removeItem(draftKey)
      document.body.classList.remove("skyblog-editor-focus-mode")
      if (document.fullscreenElement === shell && document.exitFullscreen) {
        void document.exitFullscreen()
      }
    })

    setMode(detectMode(textarea, sourceInput))
    render()
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceArticleEditor)
  } else {
    enhanceArticleEditor()
  }
})()

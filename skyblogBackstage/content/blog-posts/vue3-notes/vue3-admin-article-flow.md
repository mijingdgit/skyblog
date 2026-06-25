---
title: Vue3 博客后台的文章管理页面拆解：列表、筛选与状态流
slug: vue3-admin-article-flow
excerpt: 以博客后台文章管理为例，整理 Vue3 页面中数据加载、筛选排序、状态提示和路由同步的设计方式。
category_slug: vue3-notes
category_name: Vue3
category_icon: V3
category_description: Vue3、TypeScript、组件设计与前端工程化笔记。
category_order: 2
tags: Vue3, TypeScript, API, 后台管理
published_at: 2026-04-22
is_published: true
is_featured: false
views: 0
---

## 页面不只是把接口数据显示出来

文章管理页看起来很简单：请求列表，渲染卡片或表格，再提供搜索和筛选。但真正影响体验的地方往往藏在细节里，比如加载失败时用户能否理解问题、筛选条件能否被分享、列表状态是否会突然跳动。

在 Vue3 项目里，我更倾向于把这类页面看成一条状态流：路由参数进入页面，触发数据加载，用户操作改变筛选条件，筛选结果再反馈到界面。

## 数据加载

页面初始化时可以并行请求分类、标签和文章：

```ts
const categories = ref<AdminCategory[]>([])
const tags = ref<AdminTag[]>([])
const articles = ref<AdminArticle[]>([])
const isLoading = ref(true)
const loadError = ref('')

onMounted(async () => {
  try {
    const [categoryData, tagData, articleData] = await Promise.all([
      fetchPublicCategories(),
      fetchPublicTags(),
      fetchPublishedArticles(),
    ])

    categories.value = categoryData
    tags.value = tagData
    articles.value = articleData
  } catch {
    loadError.value = '文章内容加载失败，请确认 Django API 已启动。'
  } finally {
    isLoading.value = false
  }
})
```

这里的重点不是代码有多复杂，而是三个状态要明确：加载中、加载失败、加载成功。没有这三个状态，页面一旦接口异常，就会变成空白，用户只能猜。

## 筛选条件放进路由

文章列表的筛选条件适合写进 query。这样刷新页面不会丢状态，也方便把某个分类或标签链接发给别人。

```ts
function syncRouteFromFilters() {
  const nextQuery: Record<string, string> = {}

  if (activeCategory.value !== 'all') {
    nextQuery.category = activeCategory.value
  }

  if (activeTag.value) {
    nextQuery.tag = activeTag.value
  }

  if (searchKeyword.value.trim()) {
    nextQuery.search = searchKeyword.value.trim()
  }

  void router.replace({ query: nextQuery })
}
```

如果路由同步做得好，页面就天然具备“可恢复”的能力。用户按刷新、复制链接、浏览器后退，都不会打断当前上下文。

## computed 负责派生数据

筛选和排序不要直接改原始数组。保留接口返回的 `articles`，用 `computed` 派生展示列表：

```ts
const filteredArticles = computed(() => {
  let result = [...articles.value]

  if (activeCategory.value !== 'all') {
    const category = categoryBySlug(categories.value, activeCategory.value)
    result = result.filter((article) => article.category === category?.id)
  }

  if (activeTag.value) {
    result = result.filter((article) =>
      article.tags.some((tag) => tag.name === activeTag.value),
    )
  }

  return sortBy.value === 'views'
    ? sortArticlesByViews(result)
    : sortArticlesByLatest(result)
})
```

这样做的好处是清晰：接口数据是一层，用户输入是一层，最终展示结果是一层。任何一层变化，Vue 都会自动计算出新的列表。

## 搜索体验

搜索不一定要一开始就做后端接口。文章数量不大时，前端搜索足够快：

```ts
const keyword = searchKeyword.value.trim().toLowerCase()

result = result.filter((article) => {
  const searchableText = [
    article.title,
    article.excerpt,
    article.content,
    ...article.tags.map((tag) => tag.name),
  ].join(' ').toLowerCase()

  return searchableText.includes(keyword)
})
```

等数据量上来以后，再把搜索迁移到后端也不晚。关键是先把搜索范围设计清楚：标题、摘要、正文、分类和标签是否都要参与搜索。

## 空状态要给出口

筛选后没有结果时，不要只显示“暂无内容”。更好的空状态应该提供一个恢复入口：

```vue
<div v-if="filteredArticles.length === 0" class="empty-state">
  <p>当前筛选条件下还没有已发布文章。</p>
  <button @click="clearFilters">恢复默认视图</button>
</div>
```

这类小按钮很容易被忽略，但它能减少用户来回取消筛选的成本。

## 组件边界

文章列表页后续可以拆出三个组件：

1. `ArticleFilters`：分类、标签、排序和搜索。
2. `ArticleListItem`：单篇文章卡片。
3. `ArticleEmptyState`：空状态和重置操作。

拆组件的时机不必太早。当页面逻辑还在变化时，单文件更利于调整；当同一块结构开始重复，或文件已经明显影响阅读，再拆会更自然。

## 小结

一个好用的后台页面，靠的不是炫技，而是状态稳、入口清楚、错误可理解。Vue3 的 `ref`、`computed` 和 `watch` 已经足够支撑大部分列表页，把它们用在正确的边界上，页面就会变得轻而可靠。

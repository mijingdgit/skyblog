---
title: 一次 Vue + Django 部署排查：静态资源、CORS 与 Nginx 路由
slug: vue-django-deploy-debug
excerpt: 记录 Vue3 前台和 Django 后台分离部署时常见的三类问题：静态资源路径、跨域配置和 Nginx history 路由回退。
category_slug: deploy
category_name: 部署运维
category_icon: Ops
category_description: 项目上线、服务器配置、日志排查和生产环境稳定性记录。
category_order: 4
tags: Deploy, Nginx, Django, Vue3, CORS
published_at: 2026-04-19
is_published: true
is_featured: false
views: 0
---

## 部署问题通常不是一个点

Vue + Django 分离部署时，最常见的情况是：本地都正常，服务器上页面能打开，但文章接口失败；或者接口正常，刷新详情页却 404；再或者后台能登录，上传图片后前台看不到。

这类问题不要一股脑归因到“服务器配置错了”。更好的排查方式是按请求链路拆开：浏览器请求什么，Nginx 转发到哪里，Django 返回什么，静态文件是否能被直接访问。

## 问题一：前台刷新 404

Vue Router 如果使用 history 模式，用户访问 `/article/12` 时，服务器实际上会收到这个路径。如果 Nginx 只按文件查找，就会返回 404。

解决方式是给前台站点加回退：

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

这行配置的含义是：先找真实文件，再找目录，都没有就交给 `index.html`，让前端路由接管。

## 问题二：API 跨域失败

前台运行在 `http://127.0.0.1:5173`，后台运行在 `http://127.0.0.1:8000`，浏览器会把它们视为不同源。生产环境里，域名、端口或协议不同也会触发跨域。

Django 侧需要明确允许前台来源：

```python
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "https://example.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://example.com",
]
```

如果接口需要携带 Cookie，还要确认：

```python
CORS_ALLOW_CREDENTIALS = True
```

排查时优先看浏览器 Network 面板。跨域错误通常不是接口逻辑失败，而是浏览器在请求前或响应后把它拦下了。

## 问题三：媒体文件无法访问

Django 上传的封面图、文章图片通常放在 `MEDIA_ROOT`，对外通过 `MEDIA_URL` 暴露。生产环境不能只依赖 Django 开发服务器，需要让 Nginx 提供媒体文件访问：

```nginx
location /media/ {
    alias /var/www/skyblog/media/;
}
```

注意 `alias` 后面的路径要和 Django 的 `MEDIA_ROOT` 对齐。路径末尾的斜杠也要保留，否则很容易拼出错误文件路径。

## 问题四：接口路径被前端吞掉

如果前台和 API 在同一个域名下，常见做法是：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000/api/;
}

location /admin/ {
    proxy_pass http://127.0.0.1:8000/admin/;
}
```

这两个 `location` 要放在前台回退规则之前。否则 `/api/articles/` 可能被 `try_files` 回退到 `index.html`，浏览器收到一段 HTML，再把它当 JSON 解析，自然会报错。

## 排查顺序

我一般按这个顺序看：

1. 浏览器 Network：请求 URL、状态码、响应内容。
2. Nginx access log：请求是否到达 Nginx。
3. Nginx error log：静态路径或代理是否出错。
4. Django 日志：视图是否执行，是否有异常。
5. 服务器文件：静态目录和媒体目录是否真实存在。

不要跳过第一步。Network 面板能直接告诉你请求是 404、403、500，还是跨域拦截。

## 发布前清单

部署前可以逐项确认：

1. `npm run build` 能通过。
2. Django `python manage.py migrate` 已执行。
3. `collectstatic` 已执行并且 Nginx 指向正确目录。
4. `/api/articles/` 能返回 JSON。
5. 前台详情页刷新不会 404。
6. 上传媒体文件后 URL 可以直接打开。

## 小结

部署排查的关键是把“页面坏了”拆成具体请求。只要能看清楚每个 URL 由谁处理、文件从哪里读取、接口被转发到哪里，大部分 Vue + Django 部署问题都能很快定位。

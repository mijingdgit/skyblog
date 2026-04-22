# SkyBlog

SkyBlog 是一个个人技术博客项目，前台使用 Vue 3 + TypeScript + Vite，后台使用 Django + Django REST Framework。内容管理集中在 Django Admin，支持文章、分类、标签、项目、关于页资料，以及 Markdown、Word、XMind 内容导入。

## 项目结构

```text
.
├── src/                 # Vue 前台源码
├── public/              # 前台公共静态资源
├── skyblogBackstage/    # Django 后台与 API
├── deploy/              # 部署配置示例
├── DEPLOY.md            # 部署说明
└── package.json
```

## 本地开发

启动 Django：

```bash
cd skyblogBackstage
py -X utf8 manage.py migrate
py -X utf8 manage.py runserver 127.0.0.1:8000
```

启动 Vue：

```bash
npm install
npm run dev
```

常用地址：

- 前台：`http://127.0.0.1:5173/`
- 后台：`http://127.0.0.1:8000/admin/`
- API：`http://127.0.0.1:8000/api/`

## 环境变量

前端环境变量模板：

- `.env.example`

后端环境变量模板：

- `skyblogBackstage/.env.example`

真实 `.env` 文件不会提交到 Git，请在本地或服务器上复制模板后填写。

## 部署

部署说明见：

- `DEPLOY.md`

部署配置示例：

- `deploy/nginx.skyblog.conf.example`
- `deploy/systemd.skyblog.service.example`
- `deploy/backup_skyblog.py`
- `deploy/restore_skyblog.py`
- `deploy/skyblog-backup.cron.example`

推荐生产路由：

- `/`：Vue 前台 `dist/`
- `/api/`：Django API
- `/admin/`：Django Admin
- `/robots.txt`：动态爬虫规则
- `/sitemap.xml`：动态站点地图
- `/static/`：Django 静态文件
- `/media/`：上传文件，包括文章封面、项目封面、Markdown 图片、XMind 文件

## 发布前检查

```bash
npm run release:check
```

如果当前环境没有 `python` 命令，可以直接使用：

```bash
py -X utf8 deploy/preflight_check.py
```

Linux 服务器可以使用：

```bash
python3 deploy/preflight_check.py
```

## 备份

本地或服务器可执行：

```bash
python deploy/backup_skyblog.py --backend-dir skyblogBackstage --output-dir backups --keep 14
```

备份会包含 SQLite 数据库和 `media/` 上传文件。恢复流程见 `DEPLOY.md`。

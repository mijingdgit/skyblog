# SkyBlog 部署说明

本文档说明 SkyBlog 的推荐部署结构。当前项目由 Vue 前台和 Django 后台组成，推荐生产环境使用 Nginx 托管前端静态文件，并把 `/api/`、`/admin/` 请求反向代理到 Django。

## 1. 推荐目录

以下路径可按服务器实际情况调整，文档示例统一使用 `/var/www/skyblog`：

```text
/var/www/skyblog/
├── dist/                       # Vue 构建产物，由 npm run build 生成
├── skyblogBackstage/
│   ├── .env                    # Django 生产环境变量，不提交 Git
│   ├── db.sqlite3              # SQLite 数据库，需备份
│   ├── media/                  # 上传文件，需持久化和备份
│   ├── staticfiles/            # collectstatic 生成的静态文件
│   └── manage.py
└── .env.production             # Vue 生产构建变量，不提交 Git
```

## 2. 前端构建

如果 Vue 和 Django 使用同一个域名，例如 `https://example.com`，前端 `.env.production` 可以这样写：

```env
VITE_API_BASE_URL=
VITE_DJANGO_ADMIN_URL=/admin/
```

如果前端和后端分开部署，例如前端 `https://www.example.com`，后端 `https://api.example.com`：

```env
VITE_API_BASE_URL=https://api.example.com
VITE_DJANGO_ADMIN_URL=https://api.example.com/admin/
```

构建命令：

```bash
npm install
npm run build
```

构建完成后，Nginx 指向项目根目录下的 `dist/`。

## 3. 后端环境变量

在 `skyblogBackstage/` 下复制环境变量模板：

```bash
cp .env.example .env
```

生产环境至少需要修改这些值：

```env
SKYBLOG_SECRET_KEY=replace-with-a-long-random-secret-key
SKYBLOG_DEBUG=False
SKYBLOG_ALLOWED_HOSTS=example.com,www.example.com
SKYBLOG_CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
SKYBLOG_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
SKYBLOG_STATIC_URL=/static/
SKYBLOG_STATIC_ROOT=staticfiles
SKYBLOG_MEDIA_URL=/media/
SKYBLOG_MEDIA_ROOT=media
```

如果站点已经启用 HTTPS，并且 Django 在 Nginx 反向代理后面：

```env
SKYBLOG_SESSION_COOKIE_SECURE=True
SKYBLOG_CSRF_COOKIE_SECURE=True
SKYBLOG_USE_X_FORWARDED_PROTO=True
```

`SKYBLOG_SECURE_SSL_REDIRECT=True` 只建议在 HTTPS 全链路确认无误后再打开，避免本地或代理配置不完整时循环跳转。

HTTPS 稳定后，再逐步打开 HSTS：

```env
SKYBLOG_SECURE_SSL_REDIRECT=True
SKYBLOG_SECURE_HSTS_SECONDS=31536000
SKYBLOG_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SKYBLOG_SECURE_HSTS_PRELOAD=False
SKYBLOG_SECURE_CONTENT_TYPE_NOSNIFF=True
SKYBLOG_SECURE_REFERRER_POLICY=same-origin
SKYBLOG_X_FRAME_OPTIONS=DENY
```

注意：HSTS 会让浏览器强制使用 HTTPS。只有当域名、证书、反向代理都确认稳定后再开启，首次上线建议先保持 `SKYBLOG_SECURE_HSTS_SECONDS=0`。

## 4. 后端初始化

进入 Django 目录：

```bash
cd skyblogBackstage
```

安装依赖：

```bash
pip install -r requirements.txt
```

迁移数据库：

```bash
python manage.py migrate
```

收集静态文件：

```bash
python manage.py collectstatic --noinput
```

创建管理员：

```bash
python manage.py createsuperuser
```

## 5. 媒体文件策略

`skyblogBackstage/media/` 是生产环境最重要的可写目录，包含：

- 文章封面图
- 项目封面图
- Markdown 导入时复制的图片
- XMind 源文件
- 后续可能增加的头像或项目图片

上线时必须确保：

- Nginx 的 `/media/` 指向这个目录。
- Django 进程对这个目录有写入权限。
- 服务器备份策略包含 `db.sqlite3` 和 `media/`。
- 如果后续换成云存储，需要同步调整 Django 的 storage 配置。

## 6. Nginx 路由关系

推荐路由关系：

- `/`：Vue 前台，指向 `dist/`
- `/api/`：反向代理到 Django
- `/admin/`：反向代理到 Django Admin
- `/robots.txt`：反向代理到 Django，返回动态爬虫规则
- `/sitemap.xml`：反向代理到 Django，返回动态站点地图
- `/static/`：Django 静态文件，指向 `staticfiles/`
- `/media/`：上传文件，指向 `media/`

可参考 `deploy/nginx.skyblog.conf.example`。

## 7. 服务进程

生产环境不要使用 `python manage.py runserver`。Linux 服务器可用 Gunicorn、uWSGI 或 Daphne 等 WSGI/ASGI 服务启动 Django。

可参考 `deploy/systemd.skyblog.service.example`，其中默认使用 Gunicorn。若使用该示例，需要在服务器虚拟环境中安装 Gunicorn：

```bash
pip install gunicorn
```

## 8. 上线前检查

每次发布前建议执行：

```bash
npm run release:check
```

如果服务器没有 `python` 命令，可直接执行：

```bash
python3 deploy/preflight_check.py
```

如果想同时查看 Django 生产安全检查提示：

```bash
python3 deploy/preflight_check.py --deploy-check
```

注意：`check --deploy` 可能会提示更多安全项，例如 HSTS、SSL 重定向、Cookie Secure。这些需要结合你的 HTTPS 和代理配置逐项打开。

## 9. 备份与恢复

生产环境至少需要备份两类数据：

- `skyblogBackstage/db.sqlite3`
- `skyblogBackstage/media/`

项目提供了备份脚本：

```bash
cd /var/www/skyblog
python3 deploy/backup_skyblog.py \
  --backend-dir /var/www/skyblog/skyblogBackstage \
  --output-dir /var/backups/skyblog \
  --keep 14
```

备份产物类似：

```text
/var/backups/skyblog/skyblog-backup-20260422-103000.tar.gz
```

建议每天定时备份。可参考：

```bash
crontab -e
```

然后加入 `deploy/skyblog-backup.cron.example` 中的示例命令。

恢复前建议先停止 Django 服务：

```bash
sudo systemctl stop skyblog
python3 deploy/restore_skyblog.py /var/backups/skyblog/skyblog-backup-YYYYMMDD-HHMMSS.tar.gz \
  --backend-dir /var/www/skyblog/skyblogBackstage
python3 skyblogBackstage/manage.py migrate
sudo systemctl start skyblog
```

恢复脚本不会直接删除现有数据；它会把当前 `db.sqlite3` 和 `media/` 移动为带 `before-restore` 时间戳的副本，然后再恢复归档内容。

## 10. 安全上线清单

- 生产 `.env` 中必须设置长随机 `SKYBLOG_SECRET_KEY`。
- 生产 `.env` 中必须设置 `SKYBLOG_DEBUG=False`。
- `SKYBLOG_ALLOWED_HOSTS` 只能填写真实域名和必要的内网地址。
- `SKYBLOG_CORS_ALLOWED_ORIGINS` 和 `SKYBLOG_CSRF_TRUSTED_ORIGINS` 只填写真实前台域名。
- HTTPS 稳定后启用 `SESSION_COOKIE_SECURE`、`CSRF_COOKIE_SECURE` 和 `SECURE_SSL_REDIRECT`。
- Nginx 不要暴露 `.env`、`db.sqlite3`、备份目录或源码目录。
- `media/` 必须持久化，并纳入服务器备份策略。
- 定期把备份下载到服务器之外的位置，避免服务器磁盘损坏时备份一起丢失。
- 每次发布后执行 `python manage.py check --deploy`，根据实际 HTTPS 配置处理剩余警告。

# SkyBlog 后台管理系统

基于 Django + Django REST Framework 构建的后台管理系统，风格与前台一致。

## 功能特性

- ✅ 用户管理（增删改查、权限管理）
- ✅ 文章管理（分类、标签、发布/草稿）
- ✅ 项目作品管理
- ✅ 搜索、筛选、分页
- ✅ 数据导入/导出
- ✅ 权限管理（管理员/编辑/普通用户）

## 技术栈

- Python 3.x
- Django 4.2+
- Django REST Framework
- SQLite（默认）

## 快速开始

### 1. 安装依赖

```bash
cd skyblogBackstage
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 启动服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/admin/login/

## 默认账户

- 用户名: `admin`
- 密码: `skyblog123`

## 目录结构

```
skyblogBackstage/
├── manage.py
├── requirements.txt
├── skyblog/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── users/           # 用户管理
├── articles/        # 文章管理
├── projects/        # 项目管理
└── templates/       # 前端模板
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login/` | POST | 登录 |
| `/api/logout/` | POST | 登出 |
| `/api/me/` | GET | 当前用户 |
| `/api/users/` | GET/POST | 用户列表/创建 |
| `/api/users/{id}/` | GET/PUT/DELETE | 用户详情 |
| `/api/articles/` | GET/POST | 文章列表/创建 |
| `/api/projects/` | GET/POST | 项目列表/创建 |
| `/api/export/` | GET | 导出数据 |
| `/api/import/` | POST | 导入数据 |

# FastAPI SaaS/API Starter (可商用基础模板)

一个极简但可扩展的 **SaaS / API** 起步项目，内置：
- 用户注册/登录（JWT）
- 受保护的 API 路由（示例：`/api/v1/echo`）
- 速率限制（简单内存版）
- 健康检查 `/health`
- Stripe Webhook 占位（可自行替换支付服务）
- SQLite + SQLAlchemy
- Dockerfile / `.env` 示例

> 适合先上线 MVP，再逐步替换为更健壮的实现（例如 Redis 限流、PostgreSQL、生产级日志与监控）。

## 快速开始（本地）

```bash
# 1) 创建并填写环境变量
cp .env.example .env

# 2) 建议使用虚拟环境
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) 安装依赖
pip install -r requirements.txt

# 4) 初始化数据库（首次自动建表）并启动
uvicorn app.main:app --reload
```

启动后：
- 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`GET /health`
- 注册：`POST /auth/register`
- 登录：`POST /auth/login`（返回 `access_token`）
- 受保护测试：`POST /api/v1/echo`（需 `Authorization: Bearer <token>`）

## Docker 运行

```bash
docker build -t saas-api-starter .
docker run --env-file .env -p 8000:8000 saas-api-starter
```

## 环境变量

见 `.env.example`：
- `SECRET_KEY`：JWT 密钥（必填，生产请使用 32+ 字符随机值）
- `ACCESS_TOKEN_EXPIRE_MINUTES`：JWT 过期分钟数（默认 60）
- `DATABASE_URL`：数据库连接串（默认 SQLite：`sqlite:///./data.db`）
- `STRIPE_WEBHOOK_SECRET`：Stripe Webhook 密钥（占位，可为空）

## 目录结构

```
app/
  ├─ main.py
  ├─ config.py
  ├─ db.py
  ├─ models.py
  ├─ schemas.py
  ├─ security.py
  ├─ rate_limit.py
  ├─ routers/
  │    ├─ auth.py
  │    ├─ protected.py
  │    └─ billing.py
  └─ middleware/
       └─ errors.py
```

## 接口速览

- `POST /auth/register` `{email, password}`
- `POST /auth/login` `{email, password}` → `{access_token}`
- `POST /api/v1/echo` `{message}`（需 Bearer Token）
- `POST /billing/stripe/webhook`（占位，校验 `STRIPE_WEBHOOK_SECRET`）

## 安全与生产建议

- 使用 **PostgreSQL + 连接池**，并将 `DATABASE_URL` 指向托管数据库
- 将速率限制切换为 **Redis**（或 API 网关）
- 打开 CORS 白名单、增加请求体大小限制
- 引入结构化日志（JSON）、APM（如 OpenTelemetry）
- 使用反向代理（Nginx/Caddy）与 HTTPS（Let’s Encrypt）
- Webhook 校验务必启用签名验证（示例已给出）

**License**: MIT

# FastAPI Backend Template

基于 **FastAPI + uv** 的 Python 后端项目模板。

目标是提供一个尽量精简、可直接用于新项目的基础工程，包含：

* FastAPI
* uv
* Ruff
* ty
* pytest / pytest-cov
* pre-commit
* pydantic-settings
* Docker
* API versioning 基础结构
* Health Check

模板本身不包含具体业务域。业务代码可以根据项目需求选择按 layer-based 或 feature-based 方式组织。

## Requirements

* Python 3.13
* uv
* Git
* Docker（可选）

检查 uv：

```bash
uv --version
```

如果尚未安装 uv，请参考官方文档进行安装。

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           └── __init__.py
│   └── core/
│       ├── __init__.py
│       └── config.py
├── docs/
│   └── .gitkeep
├── tests/
│   └── test_health.py
├── .dockerignore
├── .editorconfig
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

安装项目依赖：

```bash
uv sync
```

安装 Git pre-commit hooks：

```bash
uv run pre-commit install
```

如果需要本地环境变量：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

`.env` 不应提交到 Git。

## Development

启动开发服务器：

```bash
uv run fastapi dev
```

默认地址：

```text
http://127.0.0.1:8000
```

Health Check：

```text
http://127.0.0.1:8000/health
```

Swagger UI：

```text
http://127.0.0.1:8000/docs
```

ReDoc：

```text
http://127.0.0.1:8000/redoc
```

## API Structure

API 路由采用版本化结构：

```text
/api/v1
```

基础路由关系：

```text
app/main.py
    ↓
app/api/router.py
    ↓
app/api/v1/router.py
    ↓
app/api/v1/endpoints/
```

新增接口时，可以在：

```text
app/api/v1/endpoints/
```

下创建对应模块。

例如：

```text
app/api/v1/endpoints/users.py
```

再在：

```text
app/api/v1/router.py
```

中注册对应的 `APIRouter`。

模板不会预设具体业务目录结构。项目可以根据实际需求选择：

```text
models/
schemas/
services/
```

这样的分层结构，或者：

```text
features/
├── users/
├── orders/
└── auth/
```

这样的 feature-based 结构。

## Code Quality

### Format

格式化代码：

```bash
uv run ruff format .
```

检查格式：

```bash
uv run ruff format --check .
```

### Lint

检查：

```bash
uv run ruff check .
```

自动修复可修复问题：

```bash
uv run ruff check . --fix
```

### Type Check

```bash
uv run ty check
```

## Testing

运行测试：

```bash
uv run pytest
```

运行测试并查看覆盖率：

```bash
uv run pytest --cov=app --cov-report=term-missing
```

## Recommended Local Workflow

开发完成后先执行自动修复和格式化：

```bash
uv run ruff check . --fix
uv run ruff format .
```

然后执行完整检查：

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest --cov=app --cov-report=term-missing
```

全部通过后再提交代码。

## Pre-commit

项目使用 `pre-commit` 在 Git commit 前执行基础代码检查。

首次 Clone 项目后执行：

```bash
uv run pre-commit install
```

手动检查所有文件：

```bash
uv run pre-commit run --all-files
```

之后执行：

```bash
git commit
```

时会自动运行配置的 hooks。

`pytest` 和完整类型检查建议放在 CI 中，而不是全部放入普通 pre-commit hook，以避免影响本地提交速度。

## Dependency Management

添加运行时依赖：

```bash
uv add package-name
```

例如：

```bash
uv add sqlalchemy
```

添加开发依赖：

```bash
uv add --dev package-name
```

例如：

```bash
uv add --dev pytest
```

删除依赖：

```bash
uv remove package-name
```

同步环境：

```bash
uv sync
```

项目使用：

```text
pyproject.toml
uv.lock
```

管理依赖。

`uv.lock` 应提交到 Git。

不建议手工维护 `requirements.txt`。

如果某个外部部署平台明确要求 `requirements.txt`，可以临时导出：

```bash
uv export -o requirements.txt
```

## Configuration

项目配置通过环境变量管理。

示例配置位于：

```text
.env.example
```

本地实际配置位于：

```text
.env
```

不要提交 `.env`。

基础配置代码位于：

```text
app/core/config.py
```

新增配置时，应优先通过 `pydantic-settings` 统一管理，而不是在业务代码中直接读取环境变量。

## Docker

构建镜像：

```bash
docker build -t fastapi-app .
```

运行：

```bash
docker run --rm -p 8000:8000 fastapi-app
```

启动后访问：

```text
http://localhost:8000/health
```

以及：

```text
http://localhost:8000/docs
```

如果需要传递环境变量，可以使用：

```bash
docker run --rm \
  --env-file .env \
  -p 8000:8000 \
  fastapi-app
```

PowerShell 同样可以执行：

```powershell
docker run --rm --env-file .env -p 8000:8000 fastapi-app
```

## Production

生产环境使用：

```bash
uv run fastapi run
```

或者通过 Docker 启动。

开发环境不要使用：

```bash
fastapi dev
```

作为生产启动方式。

## Git Workflow

建议基于 `main` 创建功能分支：

```bash
git switch main
git pull
git switch -c feat/example
```

开发完成并通过检查后：

```bash
git add .
git diff --cached
git commit -m "feat: add example"
git push -u origin feat/example
```

推荐使用 Conventional Commits 的简单子集：

```text
feat:     新功能
fix:      Bug 修复
refactor: 重构
test:     测试
docs:     文档
chore:    工程或依赖调整
ci:       CI/CD
build:    构建相关
```

## Health Check

模板默认提供：

```http
GET /health
```

成功响应：

```json
{
  "status": "ok"
}
```

该接口可用于：

* Docker health check
* Kubernetes probes
* Load Balancer health check
* CI/CD 部署验证
* 服务存活检查

## Template Philosophy

该模板只负责提供稳定的工程基线，包括：

* Python 环境
* 依赖管理
* API 版本结构
* 配置管理
* 测试
* 格式化
* Lint
* 类型检查
* Git hooks
* Docker

模板不会提前决定：

* 数据库
* ORM
* Repository pattern
* 用户认证
* Redis
* Celery
* 消息队列
* 具体业务目录结构
* CI/CD 平台

这些能力应在项目真正需要时再引入，避免基础模板过度工程化。

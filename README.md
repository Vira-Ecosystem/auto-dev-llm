# 🤖 Auto-Dev-LLM

> سیستم خودکار توسعه‌دهنده با هوش مصنوعی (LLM)

یک سیستم کامل برای توسعه خودکار پروژه‌ها با استفاده از LLM (آفلاین، آنلاین یا MCP Server). این سیستم قادر است به طور خودکار:
- کد تولید کند
- تست بنویسد
- Commit و Push کند
- Deploy کاناری انجام دهد
- Version Management کند
- در صورت خطا Rollback کند

---

## ✨ ویژگی‌ها

### 🎯 هسته اصلی
- ✅ **Orchestrator**: هماهنگ‌کننده اصلی سیستم
- ✅ **Task Manager**: مدیریت صف و وضعیت tasks
- ✅ **Config Loader**: خواندن و اعتبارسنجی تنظیمات
- ✅ **Logger**: سیستم logging پیشرفته با rotation

### 🤖 LLM Integration
- ✅ **MCP Client**: اتصال به MCP Server
- ✅ **Offline LLM**: پشتیبانی از LLaMA/StarCoder
- ✅ **Online Fallback**: بازگشت به OpenAI/Anthropic
- ✅ **Prompt Templates**: قالب‌های بهینه برای تولید کد

### ⏰ Scheduler
- ✅ **Time-based**: کنترل ساعات کاری
- ✅ **Resource Monitor**: مانیتورینگ CPU/RAM
- ✅ **Concurrent Limit**: محدودیت همزمانی tasks
- ✅ **Adaptive Learning**: یادگیری ساعات بهینه

### 📦 Managers
- 🚧 **Version Manager**: Semantic versioning خودکار
- 🚧 **Rollback Manager**: بازگشت خودکار در صورت خطا
- 🚧 **Deploy Manager**: استقرار کاناری
- 🚧 **Git Automation**: commit و push خودکار

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

```bash
# Python 3.11+
python --version

# Docker (اختیاری برای MCP)
docker --version

# Git
git --version
```

### نصب

```bash
# 1. Clone کردن پروژه
git clone https://github.com/your-repo/auto-dev-llm.git
cd auto-dev-llm

# 2. ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate  # Windows

# 3. نصب کتابخانه‌ها
pip install -r requirements.txt

# 4. ایجاد فایل .env
cp .env.example .env
# ویرایش .env و قرار دادن API keys
```

### راه‌اندازی MCP Server (اختیاری)

```bash
# 1. دانلود مدل LLaMA
mkdir models
cd models
# دانلود llama-3.1-7b-4bit.gguf از HuggingFace

# 2. راه‌اندازی با Docker Compose
cd docker
docker-compose up -d mcp-server

# 3. بررسی سلامت
curl http://localhost:5005/health
```

---

## 📝 استفاده

### 1. ایجاد project_spec.yaml

```yaml
project_name: "my-awesome-project"
description: "پروژه من"
version: "0.1.0"

llm:
  mode: "mcp"  # mcp | offline | online
  mcp:
    api_url: "http://localhost:5005"
  fallback_online: true

features:
  - name: "user-authentication"
    priority: 1
    description: "سیستم احراز هویت کاربر"
    tasks:
      - name: "auth-models"
        description: "ایجاد مدل‌های User و Session"
        files:
          - "src/models/user.py"
        tests:
          - "tests/test_user.py"
```

### 2. اجرای حالت تعاملی

```bash
python main.py --spec specs/project_spec.yaml
```

سیستم:
1. تنظیمات را بارگذاری می‌کند
2. Features را نمایش می‌دهد
3. از شما تایید می‌خواهد
4. شروع به تولید کد می‌کند

### 3. اجرای حالت Batch

```bash
# اجرای خودکار features خاص
python main.py --batch --features user-auth payment-system

# اجرای همه features
python main.py --batch --features $(python -c "from config import ConfigLoader; c=ConfigLoader(); c.load(); print(' '.join([f.name for f in c.config.features]))")
```

### 4. بررسی تنظیمات

```bash
python main.py --check
```

---

## 📁 ساختار پروژه

```
auto-dev-llm/
├── specs/
│   └── project_spec.yaml          # مشخصات پروژه
├── src/
│   ├── core/
│   │   ├── orchestrator.py        # هماهنگ‌کننده اصلی ✅
│   │   ├── task_manager.py        # مدیر tasks ✅
│   │   └── config.py              # مدیریت تنظیمات ✅
│   ├── llm/
│   │   ├── llama_wrapper.py       # رابط LLM ✅
│   │   ├── mcp_client.py          # کلاینت MCP ✅
│   │   └── prompt_templates.py    # قالب‌های prompt 🚧
│   ├── managers/
│   │   ├── scheduler.py           # زمان‌بند ✅
│   │   ├── version_manager.py     # مدیر نسخه 🚧
│   │   ├── rollback_manager.py    # مدیر بازگشت 🚧
│   │   └── deploy_manager.py      # مدیر استقرار 🚧
│   └── utils/
│       ├── logger.py              # سیستم لاگ ✅
│       ├── git_utils.py           # عملیات Git 🚧
│       └── file_utils.py          # عملیات فایل 🚧
├── logs/                          # فایل‌های لاگ
├── backups/                       # نسخه‌های پشتیبان
├── tests/                         # تست‌ها
├── docker/
│   ├── Dockerfile                 # Docker image ✅
│   └── docker-compose.yml         # Compose file ✅
├── requirements.txt               # وابستگی‌ها ✅
├── main.py                        # نقطه ورود ✅
└── README.md                      # این فایل

✅ = آماده | 🚧 = در دست توسعه
```

---

## 🎮 مثال‌های کاربردی

### مثال 1: ساخت REST API

```yaml
features:
  - name: "rest-api"
    priority: 1
    description: "API ساده با FastAPI"
    tasks:
      - name: "api-setup"
        description: "راه‌اندازی FastAPI با CORS"
        files:
          - "src/api/main.py"
          - "src/api/routes.py"
        tests:
          - "tests/test_api.py"
      
      - name: "database"
        description: "اتصال به PostgreSQL با SQLAlchemy"
        files:
          - "src/database/connection.py"
          - "src/database/models.py"
        tests:
          - "tests/test_database.py"
```

اجرا:
```bash
python main.py --spec specs/api_spec.yaml
```

### مثال 2: توسعه CLI Tool

```yaml
features:
  - name: "cli-tool"
    priority: 1
    description: "ابزار خط فرمان با Click"
    tasks:
      - name: "cli-base"
        description: "ساختار اصلی CLI با subcommands"
        files:
          - "src/cli/main.py"
          - "src/cli/commands.py"
        tests:
          - "tests/test_cli.py"
```

### مثال 3: Data Processing Pipeline

```yaml
features:
  - name: "data-pipeline"
    priority: 1
    description: "Pipeline پردازش داده"
    tasks:
      - name: "data-loader"
        description: "خواندن CSV/JSON/Parquet"
        files:
          - "src/pipeline/loader.py"
        tests:
          - "tests/test_loader.py"
      
      - name: "transformers"
        description: "تبدیل و پاکسازی داده"
        files:
          - "src/pipeline/transformers.py"
        tests:
          - "tests/test_transformers.py"
```

---

## ⚙️ تنظیمات پیشرفته

### تنظیم LLM Mode

**1. MCP Server (پیشنهادی)**
```yaml
llm:
  mode: "mcp"
  mcp:
    api_url: "http://localhost:5005"
    timeout: 300
    retry: 3
  fallback_online: true
```

**2. Offline (بدون اینترنت)**
```yaml
llm:
  mode: "offline"
  offline_model:
    name: "llama-3.1-7b-4bit"
    path: "./models/llama-3.1-7b-4bit.gguf"
  fallback_online: false
```

**3. Online Only**
```yaml
llm:
  mode: "online"
  online:
    provider: "openai"  # or "anthropic"
    api_key_env: "OPENAI_API_KEY"
    model: "gpt-4"
```

### تنظیم Scheduler

```yaml
scheduler:
  active_hours:
    start: 9    # شروع ساعت 9 صبح
    end: 18     # پایان ساعت 6 عصر
  max_concurrent_tasks: 2
  check_interval: 60  # هر 60 ثانیه بررسی
  cpu_threshold: 80   # حداکثر CPU 80%
```

### تنظیم Logging

```yaml
logging:
  log_path: "./logs"
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  per_feature_log: true
  rotation: "1 day"
  retention: "30 days"
```

---

## 🔍 مانیتورینگ و دیباگ

### مشاهده لاگ‌ها

```bash
# لاگ اصلی
tail -f logs/auto-dev-llm.log

# لاگ یک feature خاص
tail -f logs/user-auth.log

# لاگ JSON format
cat logs/auto-dev-llm.log | jq
```

### بررسی وضعیت Tasks

```python
from src.core.task_manager import TaskManager

manager = TaskManager()
stats = manager.get_statistics()
print(stats)

# پیشرفت یک feature
progress = manager.get_feature_progress("user-auth")
print(f"Progress: {progress['progress_percent']:.1f}%")
```

### مانیتورینگ منابع

```python
from src.managers.scheduler import ResourceMonitor

monitor = ResourceMonitor()
print(f"CPU: {monitor.get_cpu_usage():.1f}%")
print(f"Memory: {monitor.get_memory_usage():.1f}%")
print(monitor.get_system_info())
```

---

## 🐳 استفاده با Docker

### راه‌اندازی کامل

```bash
cd docker
docker-compose up -d
```

سرویس‌ها:
- `mcp-server`: LLM Backend (port 5005)
- `auto-dev`: برنامه اصلی
- `postgres`: دیتابیس (اختیاری)
- `redis`: کش (اختیاری)

### دستورات مفید

```bash
# مشاهده لاگ‌ها
docker-compose logs -f auto-dev

# ورود به container
docker-compose exec auto-dev bash

# توقف سرویس‌ها
docker-compose down

# پاک کردن کامل
docker-compose down -v
```

---

## 🧪 تست

### اجرای تست‌ها

```bash
# همه تست‌ها
pytest

# با coverage
pytest --cov=src --cov-report=html

# تست‌های خاص
pytest tests/test_config.py -v

# تست‌های async
pytest -v -s tests/test_llm_wrapper.py
```

### نوشتن تست

```python
import pytest
from src.core.config import ConfigLoader

def test_config_loader():
    loader = ConfigLoader("specs/test_spec.yaml")
    config = loader.load()
    
    assert config.project_name == "test-project"
    assert len(config.features) > 0

@pytest.mark.asyncio
async def test_llm_wrapper():
    from src.llm.llama_wrapper import LLMWrapper
    
    wrapper = LLMWrapper({"mode": "mcp"})
    response = await wrapper.generate_code(
        task_description="تابع hello world",
        file_path="test.py"
    )
    
    assert response.success
    assert len(response.content) > 0
```

---

## 🛠️ توسعه و مشارکت

### راهنمای مشارکت

1. Fork کردن پروژه
2. ایجاد branch جدید: `git checkout -b feature/amazing-feature`
3. Commit تغییرات: `git commit -m 'Add amazing feature'`
4. Push به branch: `git push origin feature/amazing-feature`
5. ایجاد Pull Request

### استانداردهای کد

```bash
# Format با Black
black src/ tests/

# Lint با Flake8
flake8 src/ tests/

# Type check با mypy
mypy src/
```

### ساختار Commit Messages

```
🎉 feat: اضافه کردن ویژگی جدید
🐛 fix: رفع باگ
📝 docs: بهبود مستندات
♻️  refactor: بازسازی کد
✅ test: اضافه کردن تست
🚀 perf: بهبود کارایی
```

---

## 📊 نقشه راه (Roadmap)

### نسخه 0.2.0 (ماه آینده)
- [ ] Version Manager کامل
- [ ] Git Automation
- [ ] Rollback Manager
- [ ] Deploy Manager (Canary)
- [ ] Prompt Templates پیشرفته

### نسخه 0.3.0 (2 ماه آینده)
- [ ] Web Dashboard
- [ ] Real-time monitoring
- [ ] Multi-project support
- [ ] Plugin system
- [ ] CI/CD Integration

### نسخه 1.0.0 (3 ماه آینده)
- [ ] Production-ready
- [ ] کامل شدن مستندات
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Enterprise features

---

## ❓ سوالات متداول (FAQ)

### Q: چرا کد تولید نمی‌شود؟
**A:** بررسی کنید:
1. MCP Server روشن است؟ `curl http://localhost:5005/health`
2. API Key تنظیم شده؟ (برای fallback)
3. لاگ‌ها را چک کنید: `tail -f logs/auto-dev-llm.log`

### Q: چگونه از مدل خودم استفاده کنم؟
**A:** مدل را در `models/` قرار دهید و در `project_spec.yaml`:
```yaml
llm:
  mode: "offline"
  offline_model:
    path: "./models/my-model.gguf"
```

### Q: چگونه همزمانی را افزایش دهم؟
**A:** در `project_spec.yaml`:
```yaml
scheduler:
  max_concurrent_tasks: 4  # افزایش به 4
```

### Q: سیستم خارج از ساعات کاری کار می‌کند؟
**A:** بله، با تنظیم:
```yaml
scheduler:
  active_hours:
    start: 0
    end: 24  # 24 ساعته
```

---

## 📄 لایسنس

MIT License - آزاد برای استفاده تجاری و شخصی

---

## 🙏 تشکر

- [LLaMA](https://github.com/facebookresearch/llama) - Meta AI
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Georgi Gerganov
- [FastAPI](https://fastapi.tiangolo.com/) - Sebastián Ramírez
- [Rich](https://rich.readthedocs.io/) - Will McGugan

---

## 📞 پشتیبانی

- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📧 Email: support@auto-dev-llm.com

---

**ساخته شده با ❤️ توسط تیم Auto-Dev-LLM**
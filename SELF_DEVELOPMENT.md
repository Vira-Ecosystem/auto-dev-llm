# 🤖 Auto-Dev-LLM Self-Development Guide

## خودت را توسعه بده! 🚀

این راهنما نحوه اجرای سیستم روی **خودش** را توضیح می‌دهد.

---

## 🎯 هدف

سیستم Auto-Dev-LLM قرار است **8 feature** و **18 task** جدید را برای خودش بنویسد:

### Features List:
1. **Git Automation** - عملیات Git خودکار
2. **Version Control** - Semantic versioning
3. **Rollback Recovery** - بازگشت و backup
4. **Deploy Automation** - استقرار کاناری
5. **Prompt System** - Prompt engineering پیشرفته
6. **Quality Assurance** - تست و تحلیل کد
7. **File Operations** - مدیریت فایل
8. **Orchestrator V2** - بهبود هسته اصلی

---

## ⚡ Quick Start (5 دقیقه)

### مرحله 1: آماده‌سازی

```bash
# 1. فعال کردن محیط مجازی
source venv/bin/activate  # Linux/Mac
# یا: venv\Scripts\activate  # Windows

# 2. تنظیم API Key
export ANTHROPIC_API_KEY="sk-ant-xxx..."
# یا: export OPENAI_API_KEY="sk-xxx..."

# 3. کپی فایل spec
cp specs/self_development_spec.yaml specs/project_spec.yaml
```

### مرحله 2: اجرا! 🚀

```bash
python bootstrap_self_dev.py
```

یا:

```bash
python main.py --spec specs/self_development_spec.yaml
```

### مرحله 3: مشاهده نتایج

```bash
# مشاهده فایل‌های تولید شده
ls -la src/managers/
ls -la src/utils/

# اجرای تست‌ها
pytest tests/ -v

# مشاهده لاگ‌ها
tail -f logs/auto-dev-llm.log
```

---

## 📊 چه اتفاقی می‌افتد؟

### 1. **Initialization** (30 ثانیه)
- بارگذاری config
- راه‌اندازی logger
- اتصال به LLM

### 2. **Feature Approval** (فوری)
- نمایش 8 feature
- تایید خودکار همه

### 3. **Code Generation** (15-30 دقیقه)
- تولید 18 فایل کد
- تولید 18 فایل تست
- هر task حدود 1-2 دقیقه

### 4. **Validation** (2-3 دقیقه)
- بررسی syntax
- اجرای lint
- اجرای تست‌ها

---

## 🎛️ تنظیمات پیشرفته

### حالت Batch (بدون تعامل)

```bash
python main.py \
  --spec specs/self_development_spec.yaml \
  --batch \
  --features git-automation version-control rollback-recovery
```

### تنظیم همزمانی

در `self_development_spec.yaml`:

```yaml
scheduler:
  max_concurrent_tasks: 3  # افزایش به 3 برای سرعت بیشتر
```

### استفاده از MCP (اگر دارید)

```yaml
llm:
  mode: "mcp"
  mcp:
    api_url: "http://localhost:5005"
  fallback_online: true  # بازگشت به online در صورت خطا
```

---

## 📁 ساختار خروجی

```
auto-dev-llm/
├── src/
│   ├── managers/
│   │   ├── backup_manager.py      ✨ NEW
│   │   ├── commit_manager.py      ✨ NEW
│   │   ├── deploy_manager.py      ✨ NEW
│   │   ├── deploy_strategy.py     ✨ NEW
│   │   ├── rollback_manager.py    ✨ NEW
│   │   └── version_manager.py     ✨ NEW
│   ├── utils/
│   │   ├── changelog.py           ✨ NEW
│   │   ├── code_analyzer.py       ✨ NEW
│   │   ├── file_utils.py          ✨ NEW
│   │   ├── git_utils.py           ✨ NEW
│   │   ├── health_checker.py      ✨ NEW
│   │   ├── project_structure.py   ✨ NEW
│   │   ├── quality_gate.py        ✨ NEW
│   │   └── test_runner.py         ✨ NEW
│   ├── llm/
│   │   ├── context_builder.py     ✨ NEW
│   │   ├── prompt_optimizer.py    ✨ NEW
│   │   └── prompt_templates.py    ✨ NEW (enhanced)
│   └── core/
│       └── orchestrator_v2.py     ✨ NEW
└── tests/
    ├── test_backup_manager.py     ✨ NEW
    ├── test_commit_manager.py     ✨ NEW
    └── ... (18 فایل تست جدید)
```

---

## ⚠️ نکات مهم

### 1. API Costs
- هر task حدود 2000-4000 token مصرف می‌کند
- کل پروژه: ~80,000 tokens
- هزینه تقریبی با Claude: $0.80-$1.20
- هزینه تقریبی با GPT-4: $2.40-$3.60

### 2. زمان اجرا
- **سریع** (3 همزمانی): 15-20 دقیقه
- **عادی** (2 همزمانی): 20-30 دقیقه
- **آهسته** (1 همزمانی): 30-45 دقیقه

### 3. نیاز به بررسی دستی
بعد از تولید کد:
- ✅ کد تولید شده را review کنید
- ✅ تست‌ها را اجرا کنید
- ✅ در صورت نیاز refactor کنید
- ✅ مستندات را کامل کنید

---

## 🐛 عیب‌یابی

### مشکل: LLM اتصال ندارد

```bash
# بررسی API key
echo $ANTHROPIC_API_KEY

# تست اتصال
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### مشکل: Task ناموفق است

```bash
# مشاهده لاگ دقیق
tail -f logs/auto-dev-llm.log

# لاگ feature خاص
tail -f logs/git-automation.log
```

### مشکل: کد تولید شده syntax error دارد

```bash
# بررسی syntax
python -m py_compile src/managers/new_file.py

# اجرای black برای format
black src/managers/new_file.py
```

### مشکل: تست‌ها fail می‌شوند

```bash
# اجرای تست با خروجی کامل
pytest tests/test_git_utils.py -vv

# اجرای با pdb برای دیباگ
pytest tests/test_git_utils.py --pdb
```

---

## 📈 مانیتورینگ پیشرفت

### حین اجرا

```bash
# Terminal 1: اجرای اصلی
python bootstrap_self_dev.py

# Terminal 2: مانیتورینگ لاگ
tail -f logs/auto-dev-llm.log | grep "✅\|❌"

# Terminal 3: مانیتورینگ فایل‌ها
watch -n 5 "ls -lh src/managers/ src/utils/"
```

### بررسی وضعیت Task ها

```python
# در Python REPL
from src.core.task_manager import TaskManager

manager = TaskManager()
manager._load_state()

# وضعیت کلی
print(manager.get_statistics())

# پیشرفت هر feature
for feature in ["git-automation", "version-control", "rollback-recovery"]:
    progress = manager.get_feature_progress(feature)
    print(f"{feature}: {progress['progress_percent']:.1f}%")
```

---

## 🎯 بعد از اتمام

### 1. بررسی کیفیت

```bash
# اجرای تمام تست‌ها
pytest tests/ -v --cov=src --cov-report=html

# بررسی style
flake8 src/

# بررسی type hints
mypy src/
```

### 2. Commit تغییرات

```bash
# مشاهده تغییرات
git status
git diff

# Stage files
git add src/ tests/

# Commit
git commit -m "🤖 Phase 2: Self-generated features

- Git automation
- Version control
- Rollback system
- Deploy automation
- Prompt engineering
- Quality assurance
- File operations
- Enhanced orchestrator

Generated by Auto-Dev-LLM v0.2.0"
```

### 3. تست یکپارچگی

```bash
# تست کل سیستم با features جدید
python main.py --check

# اجرای یک feature تست
python main.py --batch --features git-automation
```

---

## 🚀 استفاده از Features جدید

### Git Automation

```python
from src.utils.git_utils import GitWrapper

git = GitWrapper()
git.init_repo()
git.stage_files(["src/new_file.py"])
git.commit("Added new feature")
git.push()
```

### Version Management

```python
from src.managers.version_manager import VersionManager

vm = VersionManager()
current = vm.get_current_version()  # "0.2.0"
vm.bump_version("minor")  # "0.3.0"
vm.create_tag()
```

### Rollback

```python
from src.managers.rollback_manager import RollbackManager

rm = RollbackManager()
backup_id = rm.create_backup()
# ... do some changes ...
rm.rollback(backup_id)  # برگشت به قبل
```

### Deploy

```python
from src.managers.deploy_manager import DeployManager

dm = DeployManager()
await dm.deploy_canary(
    app_path="./app",
    health_endpoint="/health"
)
```

---

## 📊 مثال خروجی

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🤖 AUTO-DEV-LLM SELF-IMPROVEMENT MODE 🤖             ║
║                                                               ║
║              "I am about to improve myself!"                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📋 Plan for Self-Development:

┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Priority ┃ Feature                 ┃ Tasks  ┃ Description                      ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1      │ git-automation          │ 2      │ Git operations & commit mgmt     │
│ 2      │ version-control         │ 2      │ Semantic versioning & changelog  │
│ 3      │ rollback-recovery       │ 2      │ Backup & rollback system         │
│ 4      │ deploy-automation       │ 3      │ Canary deploy & health checks    │
│ 5      │ prompt-system           │ 3      │ Advanced prompt engineering      │
│ 6      │ quality-assurance       │ 3      │ Testing & code analysis          │
│ 7      │ file-operations         │ 2      │ File management utilities        │
│ 8      │ orchestrator-v2         │ 1      │ Enhanced orchestrator            │
└────────┴─────────────────────────┴────────┴──────────────────────────────────┘

Total: 8 Features, 18 Tasks

Ready to start self-development? (y/n): y

⏳ Checking prerequisites...

   ✓ Python version
   ✓ specs/ directory
   ✓ src/ directory
   ✓ project_spec.yaml
   ✓ API key found

✅ All prerequisites met!

🚀 Starting self-development process...

✓ System initialized

[🚀 Feature 1/8: git-automation ━━━━━━━━━━━━━━━━━━ 12%]
   🚀 Task: git-wrapper
   🤖 Generating code with LLM...
   ✅ Generated: src/utils/git_utils.py (1247 bytes)
   ✅ Generated: tests/test_git_utils.py (856 bytes)
   
[🚀 Feature 2/8: version-control ━━━━━━━━━━━━━━━━ 25%]
   ...

══════════════════════════════════════════════════════════════════
🎉 SELF-DEVELOPMENT COMPLETE! 🎉
══════════════════════════════════════════════════════════════════

Total Tasks        18
✅ Completed       17
❌ Failed          1
⏱️  Avg Duration   42.3s
📈 Success Rate    94.4%

📁 Generated Files:
   ✓ src/utils/git_utils.py (1247 bytes)
   ✓ src/managers/commit_manager.py (982 bytes)
   ✓ src/managers/version_manager.py (1456 bytes)
   ...

Total: 36 files generated

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                              ┃
┃                   🎊 Congratulations! 🎊                     ┃
┃                                                              ┃
┃           The system has successfully improved itself!       ┃
┃                                                              ┃
┃  Next steps:                                                 ┃
┃    1. Review generated code                                  ┃
┃    2. Run tests: pytest tests/ -v                            ┃
┃    3. Commit changes                                         ┃
┃    4. Deploy! 🚀                                             ┃
┃                                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✅ Completed in 1247.83 seconds
```

---

## 🎓 یادگیری از فرآیند

### چیزهایی که سیستم یاد می‌گیرد:

1. **خودآگاهی**: سیستم یاد می‌گیرد چگونه خودش را بهبود دهد
2. **الگوها**: شناسایی الگوهای کدنویسی موفق
3. **بهینه‌سازی**: یافتن بهترین ساعات و روش‌ها
4. **خودترمیمی**: رفع خطاهای خود به صورت خودکار

### Metrics که ذخیره می‌شوند:

- زمان تولید هر نوع فایل
- میزان موفقیت prompts
- کیفیت کد تولید شده
- نرخ خطا در هر feature

---

## 💡 Tips & Best Practices

### 1. شروع با Features کوچک
```bash
# اول فقط git-automation را تست کنید
python main.py --batch --features git-automation
```

### 2. استفاده از Dry Run
```python
# تست بدون اجرای واقعی
orchestrator.config.git.auto_commit = False
orchestrator.config.deploy.enabled = False
```

### 3. Backup دستی
```bash
# قبل از شروع
cp -r src/ src.backup/
cp -r tests/ tests.backup/
```

### 4. مانیتورینگ مداوم
```bash
# اسکریپت مانیتورینگ
while true; do
  clear
  echo "=== Tasks Status ==="
  python -c "from src.core.task_manager import TaskManager; \
    m = TaskManager(); m._load_state(); \
    print(m.get_statistics())"
  sleep 10
done
```

---

## 🔗 منابع بیشتر

- 📖 [Main README](README.md)
- 📋 [Architecture](docs/ARCHITECTURE.md)
- 🔧 [API Reference](docs/API.md)
- 🎯 [Examples](examples/)

---

## ❓ سوالات؟

اگر مشکلی داشتید:
1. لاگ‌ها را چک کنید: `logs/auto-dev-llm.log`
2. Issue در GitHub باز کنید
3. به تیم پشتیبانی پیام دهید

---

**آماده‌اید؟ بیایید سیستم را به حال خودش بگذاریم!** 🚀

```bash
python bootstrap_self_dev.py
```
# 🚀 اجرای فوری: توسعه خودکار سیستم

## ⚡ 3 دقیقه تا شروع!

### گام 1: آماده‌سازی (30 ثانیه)

```bash
# کپی فایل‌ها به پروژه خود
# همه artifact ها را ذخیره کنید

# ساختار مورد نیاز:
auto-dev-llm/
├── specs/
│   ├── project_spec.yaml              # از artifact 1
│   └── self_development_spec.yaml     # از artifact 16
├── src/
│   ├── core/
│   │   ├── config.py                  # از artifact 2
│   │   ├── task_manager.py            # از artifact 4
│   │   └── orchestrator.py            # از artifact 6
│   ├── llm/
│   │   └── llama_wrapper.py           # از artifact 5
│   ├── managers/
│   │   └── scheduler.py               # از artifact 7
│   └── utils/
│       └── logger.py                  # از artifact 3
├── docker/
│   ├── Dockerfile                     # از artifact 9
│   └── docker-compose.yml             # از artifact 10
├── requirements.txt                    # از artifact 8
├── main.py                            # از artifact 9
├── bootstrap_self_dev.py              # از artifact 17
├── dry_run_test.py                    # از artifact 19
└── README.md                          # از artifact 11
```

### گام 2: نصب (1 دقیقه)

```bash
# ایجاد محیط مجازی
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# یا: venv\Scripts\activate  # Windows

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### گام 3: تنظیم API Key (30 ثانیه)

```bash
# ایجاد .env
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# یا برای OpenAI
echo "OPENAI_API_KEY=your-key-here" > .env
```

### گام 4: تست (30 ثانیه)

```bash
# تست خشک (بدون هزینه)
python dry_run_test.py
```

### گام 5: اجرا! 🚀

```bash
# حالت کامل (توصیه می‌شود)
python bootstrap_self_dev.py

# یا حالت manual
python main.py --spec specs/self_development_spec.yaml
```

---

## 📊 چه انتظاری داشته باشید؟

### خروجی موفق:

```
🚀 Starting self-development...
✓ System initialized

[Feature 1/8: git-automation ━━━━━━ 12%]
   🤖 Generating: src/utils/git_utils.py
   ✅ Generated successfully

[Feature 2/8: version-control ━━━━━ 25%]
   ...

═══════════════════════════════════════
🎉 SELF-DEVELOPMENT COMPLETE!
═══════════════════════════════════════

Total Tasks: 18
✅ Completed: 17
❌ Failed: 1
📈 Success Rate: 94.4%

📁 Generated 36 files
⏱️  Duration: 20.5 minutes
```

### پس از اتمام:

```bash
# بررسی فایل‌های جدید
ls -la src/managers/
ls -la src/utils/

# اجرای تست‌ها
pytest tests/ -v

# مشاهده لاگ
tail -f logs/auto-dev-llm.log
```

---

## 🎯 حالت‌های مختلف اجرا

### 1️⃣ حالت کامل (توصیه می‌شود)

```bash
python bootstrap_self_dev.py
```

- همه 8 feature
- 18 task
- تایید خودکار
- مانیتورینگ real-time

### 2️⃣ حالت Batch سفارشی

```bash
python main.py \
  --spec specs/self_development_spec.yaml \
  --batch \
  --features git-automation version-control
```

- فقط features انتخابی
- بدون تعامل
- سریع‌تر

### 3️⃣ حالت تعاملی

```bash
python main.py --spec specs/self_development_spec.yaml
```

- تایید دستی features
- کنترل بیشتر
- مناسب برای تست

### 4️⃣ حالت تست (بدون هزینه)

```bash
python dry_run_test.py
```

- بدون فراخوانی LLM
- تست ساختار
- رایگان!

---

## 💰 هزینه‌ها

### با Claude Sonnet 4:
- هر task: ~3000 tokens
- کل پروژه: ~54,000 tokens  
- هزینه: **$0.50 - $0.80**

### با GPT-4:
- هر task: ~3000 tokens
- کل پروژه: ~54,000 tokens
- هزینه: **$1.60 - $2.40**

### با MCP (مدل محلی):
- **رایگان!** 🎉
- نیاز به GPU
- کمی کندتر

---

## ⏱️ زمان اجرا

| Concurrent Tasks | Duration      |
|------------------|---------------|
| 1                | 30-45 min     |
| 2 (پیش‌فرض)     | 20-30 min     |
| 3 (پیشنهادی)    | 15-20 min     |

---

## 🛑 نکات مهم

### ✅ قبل از شروع:

1. حتماً `dry_run_test.py` را اجرا کنید
2. API key معتبر داشته باشید
3. فضای کافی روی دیسک (حداقل 100MB)
4. اتصال اینترنت پایدار

### ⚠️ حین اجرا:

1. سیستم را متوقف نکنید (Ctrl+C)
2. لاگ‌ها را مانیتور کنید
3. در صورت خطا، سیستم retry می‌کند
4. پیشرفت در `task_state.json` ذخیره می‌شود

### 📝 پس از اتمام:

1. کد تولید شده را review کنید
2. تست‌ها را اجرا کنید
3. در صورت نیاز refactor کنید
4. تغییرات را commit کنید

---

## 🐛 عیب‌یابی سریع

### مشکل: "Module not found"

```bash
# تنظیم PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# یا اجرا به صورت module
python -m src.core.orchestrator
```

### مشکل: "API key invalid"

```bash
# بررسی API key
echo $ANTHROPIC_API_KEY

# تست دستی
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### مشکل: Task fail می‌شود

```bash
# مشاهده لاگ دقیق
tail -100 logs/auto-dev-llm.log

# بررسی task state
cat task_state.json | jq

# اجرای مجدد (از جایی که قطع شد)
python bootstrap_self_dev.py
```

### مشکل: "Out of memory"

```bash
# کاهش همزمانی
# در self_development_spec.yaml:
scheduler:
  max_concurrent_tasks: 1  # کاهش به 1
```

---

## 📊 مانیتورینگ Real-Time

### Terminal 1: اجرای اصلی
```bash
python bootstrap_self_dev.py
```

### Terminal 2: مانیتورینگ لاگ
```bash
tail -f logs/auto-dev-llm.log | grep -E "✅|❌|🚀"
```

### Terminal 3: وضعیت Tasks
```bash
watch -n 5 "python -c \"
from src.core.task_manager import TaskManager
m = TaskManager()
m._load_state()
stats = m.get_statistics()
print(f'Completed: {stats[\"completed\"]}/{stats[\"total_tasks\"]}')
print(f'Running: {stats[\"running\"]}')
print(f'Failed: {stats[\"failed\"]}')
\""
```

### Terminal 4: مانیتورینگ فایل‌ها
```bash
watch -n 10 "ls -lh src/managers/ src/utils/ | grep -v '^total'"
```

---

## 🎯 بعد از اتمام موفق

### 1. بررسی کیفیت

```bash
# تست همه چیز
pytest tests/ -v --cov=src --cov-report=term-missing

# Style check
flake8 src/ --max-line-length=100

# Type check
mypy src/ --ignore-missing-imports
```

### 2. نمایش درخت پروژه

```bash
tree -L 3 -I '__pycache__|*.pyc|venv'
```

خروجی مورد انتظار:
```
auto-dev-llm/
├── src/
│   ├── core/
│   │   ├── config.py
│   │   ├── task_manager.py
│   │   ├── orchestrator.py
│   │   └── orchestrator_v2.py        ⭐ NEW
│   ├── managers/
│   │   ├── scheduler.py
│   │   ├── backup_manager.py         ⭐ NEW
│   │   ├── commit_manager.py         ⭐ NEW
│   │   ├── deploy_manager.py         ⭐ NEW
│   │   ├── deploy_strategy.py        ⭐ NEW
│   │   ├── rollback_manager.py       ⭐ NEW
│   │   └── version_manager.py        ⭐ NEW
│   ├── utils/
│   │   ├── logger.py
│   │   ├── changelog.py              ⭐ NEW
│   │   ├── code_analyzer.py          ⭐ NEW
│   │   ├── file_utils.py             ⭐ NEW
│   │   ├── git_utils.py              ⭐ NEW
│   │   ├── health_checker.py         ⭐ NEW
│   │   ├── project_structure.py      ⭐ NEW
│   │   ├── quality_gate.py           ⭐ NEW
│   │   └── test_runner.py            ⭐ NEW
│   └── llm/
│       ├── llama_wrapper.py
│       ├── mcp_client.py
│       ├── context_builder.py        ⭐ NEW
│       ├── prompt_optimizer.py       ⭐ NEW
│       └── prompt_templates.py       ⭐ ENHANCED
└── tests/
    ├── test_*.py (18 فایل جدید)    ⭐ NEW
```

### 3. Commit تغییرات

```bash
# مشاهده تغییرات
git status

# بررسی diff
git diff src/

# Stage new files
git add src/managers/*.py src/utils/*.py src/llm/*.py src/core/orchestrator_v2.py tests/

# Commit با پیام زیبا
git commit -m "🤖 Phase 2: Self-Generated Features

Auto-Dev-LLM has successfully improved itself!

New Features:
✨ Git Automation - Complete Git workflow automation
✨ Version Control - Semantic versioning & changelog
✨ Rollback System - Backup and recovery
✨ Deploy Automation - Canary deployment with health checks
✨ Prompt Engineering - Advanced prompt optimization
✨ Quality Assurance - Automated testing & analysis
✨ File Operations - Safe file management utilities
✨ Enhanced Orchestrator - Improved core functionality

Statistics:
- 18 tasks completed
- 36 files generated
- ~3500 lines of code
- 94% success rate
- Generated in 20.5 minutes

Generated by: Auto-Dev-LLM v0.2.0
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
"
```

### 4. تست نهایی

```bash
# تست یکپارچگی کل سیستم
python -m pytest tests/ -v --tb=short

# اگر همه تست‌ها pass شد:
git tag -a v0.2.0 -m "🎉 Phase 2: Self-Improvement Complete"
```

---

## 🚀 استفاده از Features جدید

### Git Automation
```python
from src.utils.git_utils import GitWrapper

git = GitWrapper()
git.add_files(["src/new_feature.py"])
git.commit("Add new feature")
git.push()
```

### Version Management
```python
from src.managers.version_manager import VersionManager

vm = VersionManager()
print(vm.get_current_version())  # "0.2.0"
vm.bump_minor()  # "0.3.0"
vm.create_tag()
```

### Deploy with Canary
```python
from src.managers.deploy_manager import DeployManager

dm = DeployManager()
await dm.canary_deploy(
    app_path="./app",
    stages=[
        {"traffic": 10, "duration": 300},
        {"traffic": 50, "duration": 600},
        {"traffic": 100, "duration": 0}
    ]
)
```

### Code Quality Check
```python
from src.utils.quality_gate import QualityGate

qg = QualityGate()
result = qg.check_quality("src/")

if result.passed:
    print("✅ Quality gate passed!")
else:
    print(f"❌ Issues: {result.issues}")
```

---

## 📈 آمار پیش‌بینی شده

| Metric | Expected Value |
|--------|----------------|
| **Files Generated** | 36 files |
| **Lines of Code** | ~3,500 lines |
| **Test Coverage** | 80-90% |
| **Success Rate** | 90-95% |
| **Time to Complete** | 15-30 min |
| **API Calls** | ~50-60 calls |
| **Total Cost** | $0.50-$2.50 |

---

## 🎓 یادگیری از فرآیند

### چیزهایی که می‌آموزید:

1. **Self-Referential AI**: سیستمی که خودش را می‌سازد
2. **Prompt Engineering**: بهترین روش‌های prompt
3. **Code Generation**: تولید کد با کیفیت
4. **Automation Patterns**: الگوهای خودکارسازی
5. **AI-Driven Development**: توسعه هدایت شده با AI

### Metrics که ثبت می‌شود:

```json
{
  "feature": "git-automation",
  "tasks": [
    {
      "name": "git-wrapper",
      "duration": 42.3,
      "tokens_used": 3247,
      "success": true,
      "code_quality": 8.5
    }
  ]
}
```

---

## 🔄 اگر مشکلی پیش آمد

### سناریو 1: Task ناموفق شد

```bash
# سیستم به طور خودکار 3 بار retry می‌کند
# اگر باز هم fail شد، ادامه می‌دهد

# برای اجرای مجدد فقط همان task:
python main.py --batch --features git-automation
```

### سناریو 2: کد تولید شده خطا دارد

```bash
# بررسی syntax
python -m py_compile src/managers/new_file.py

# اصلاح دستی یا regenerate
rm src/managers/new_file.py
python main.py --batch --features git-automation
```

### سناریو 3: Out of API credits

```bash
# تغییر به مدل ارزان‌تر
# در self_development_spec.yaml:
llm:
  online:
    model: "gpt-3.5-turbo"  # ارزان‌تر

# یا استفاده از MCP (رایگان)
llm:
  mode: "mcp"
```

---

## 🎉 پیام نهایی

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                  🎊 شما آماده هستید! 🎊                     ║
║                                                               ║
║         سیستم قادر است خودش را بهبود دهد                    ║
║              فقط کافی است دکمه را بزنید!                    ║
║                                                               ║
║                    python bootstrap_self_dev.py              ║
║                                                               ║
║                     Let the magic begin! ✨                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📞 پشتیبانی

اگر به کمک نیاز دارید:

1. **لاگ‌ها را چک کنید**: `logs/auto-dev-llm.log`
2. **README را بخوانید**: [README.md](README.md)
3. **راهنمای کامل**: [SELF_DEVELOPMENT.md](SELF_DEVELOPMENT.md)
4. **تست خشک اجرا کنید**: `python dry_run_test.py`

---

**آماده‌اید؟ 3... 2... 1... 🚀**

```bash
python bootstrap_self_dev.py
```

**بگذارید سیستم خودش را بسازد!** 🤖✨
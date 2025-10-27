# 💰 برآورد دقیق هزینه با Claude Sonnet 4.5

## 📊 قیمت‌گذاری Claude Sonnet 4.5

| Type | Price | Per |
|------|-------|-----|
| **Input Tokens** | $3.00 | 1M tokens |
| **Output Tokens** | $15.00 | 1M tokens |
| **Cache Write** | $3.75 | 1M tokens |
| **Cache Read** | $0.30 | 1M tokens |

---

## 🔢 محاسبه برای هر Task

### ساختار یک Task:

```
Prompt (Input):
- System Prompt: ~500 tokens
- Task Description: ~200 tokens
- Context: ~300 tokens
- Examples: ~500 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Input: ~1,500 tokens

Response (Output):
- Code Generation: ~2,000 tokens
- Docstrings: ~300 tokens
- Comments: ~200 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Output: ~2,500 tokens
```

### هزینه یک Task:

```
Input:  1,500 tokens × $3.00  / 1M = $0.0045
Output: 2,500 tokens × $15.00 / 1M = $0.0375
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total per Task: $0.042
```

---

## 📦 هزینه کل پروژه

### Features و Tasks:

| Feature | Tasks | Input Tokens | Output Tokens |
|---------|-------|-------------|---------------|
| git-automation | 2 | 3,000 | 5,000 |
| version-control | 2 | 3,000 | 5,000 |
| rollback-recovery | 2 | 3,000 | 5,000 |
| deploy-automation | 3 | 4,500 | 7,500 |
| prompt-system | 3 | 4,500 | 7,500 |
| quality-assurance | 3 | 4,500 | 7,500 |
| file-operations | 2 | 3,000 | 5,000 |
| orchestrator-v2 | 1 | 1,500 | 2,500 |

### جمع کل:

```
Total Tasks: 18

Input Tokens:  27,000 tokens
Output Tokens: 45,000 tokens

Cost Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input:  27,000 × $3.00  / 1M = $0.081
Output: 45,000 × $15.00 / 1M = $0.675
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL COST: $0.756

≈ $0.76 (76 سنت)
```

---

## 🎯 سناریوهای مختلف

### 1️⃣ حالت عادی (بدون cache):
```
18 tasks × $0.042 = $0.756
```

### 2️⃣ با Prompt Caching (بعد از اولین task):
```
Task 1: $0.042
Tasks 2-18: 17 × $0.028 = $0.476
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: $0.518 (52 سنت)

صرفه‌جویی: 31%
```

### 3️⃣ با خطا و retry (worst case):
```
18 tasks + 3 retries = 21 calls
21 × $0.042 = $0.882 (88 سنت)
```

### 4️⃣ فقط یک feature (تست):
```
git-automation (2 tasks):
2 × $0.042 = $0.084 (8 سنت)
```

---

## 📊 مقایسه با مدل‌های دیگر

| Model | Input | Output | Total Cost |
|-------|-------|--------|------------|
| **Claude Sonnet 4.5** | $0.081 | $0.675 | **$0.76** ⭐ |
| Claude Opus 4 | $0.405 | $2.025 | $2.43 |
| GPT-4o | $0.135 | $0.675 | $0.81 |
| GPT-4 Turbo | $0.270 | $1.350 | $1.62 |
| GPT-3.5 Turbo | $0.014 | $0.045 | $0.06 |

**✨ Sonnet 4.5 بهترین نسبت قیمت/کیفیت!**

---

## 💡 نکات کاهش هزینه

### 1. استفاده از Prompt Caching
```yaml
llm:
  online:
    use_cache: true  # صرفه‌جویی 30%
```

### 2. کاهش Output Tokens
```yaml
llm:
  max_tokens: 2048  # به جای 4096
```

### 3. Batch Processing
```bash
# اجرای دسته‌ای features مشابه
python main.py --batch --features git-automation version-control
```

### 4. استفاده از MCP (رایگان!)
```yaml
llm:
  mode: "mcp"  # مدل محلی
  fallback_online: true  # فقط در صورت خطا
```

---

## 🧮 ماشین‌حساب تعاملی

```python
def calculate_cost(
    num_tasks: int,
    input_tokens_per_task: int = 1500,
    output_tokens_per_task: int = 2500,
    use_cache: bool = False
):
    """محاسبه هزینه"""
    
    # قیمت‌ها (per million tokens)
    input_price = 3.00
    output_price = 15.00
    cache_write_price = 3.75
    cache_read_price = 0.30
    
    total_cost = 0
    
    for i in range(num_tasks):
        if use_cache and i > 0:
            # از task دوم cache استفاده می‌شود
            input_cost = (input_tokens_per_task * cache_read_price) / 1_000_000
        else:
            input_cost = (input_tokens_per_task * input_price) / 1_000_000
        
        output_cost = (output_tokens_per_task * output_price) / 1_000_000
        
        total_cost += input_cost + output_cost
    
    return total_cost


# مثال‌ها:
print(f"بدون cache: ${calculate_cost(18):.3f}")
print(f"با cache: ${calculate_cost(18, use_cache=True):.3f}")
print(f"یک feature: ${calculate_cost(2):.3f}")
```

---

## 📈 هزینه بر اساس تعداد Features

```
1 feature  (2 tasks):  $0.08
2 features (4 tasks):  $0.17
3 features (6 tasks):  $0.25
4 features (9 tasks):  $0.38
5 features (12 tasks): $0.50
6 features (15 tasks): $0.63
7 features (17 tasks): $0.71
8 features (18 tasks): $0.76 ⭐ همه
```

---

## 🎯 توصیه‌ها

### برای تست:
```bash
# فقط 1 feature = 8 سنت
python main.py --batch --features git-automation
```

### برای production:
```bash
# همه features با cache = 52 سنت
python bootstrap_self_dev.py
```

### برای صرفه‌جویی:
```bash
# استفاده از MCP (رایگان) + fallback
# در صورت خطا به Sonnet 4.5 برمی‌گردد
```

---

## 📊 خلاصه نهایی

| سناریو | Tasks | Cost | Time |
|--------|-------|------|------|
| **تست (1 feature)** | 2 | $0.08 | 2 min |
| **نیمه (4 features)** | 9 | $0.38 | 10 min |
| **کامل (بدون cache)** | 18 | $0.76 | 20 min |
| **کامل (با cache)** | 18 | $0.52 | 20 min |
| **با retry (worst)** | 21 | $0.88 | 25 min |

---

## 💳 برآورد ماهانه

اگر روزانه 1 بار اجرا کنید:

```
روزانه: $0.76
هفتگی: $5.32
ماهانه: $22.80

با cache:
ماهانه: $15.60

با MCP (90% وقت):
ماهانه: $2.28
```

---

**✅ نتیجه: با Claude Sonnet 4.5 و استفاده از cache، کل پروژه فقط 52 سنت هزینه دارد!** 🎉
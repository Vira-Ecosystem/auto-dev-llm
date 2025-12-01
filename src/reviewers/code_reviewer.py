“””
سیستم AI Code Review خودکار
این ماژول کدهای تولید شده را بررسی می‌کند و نمره کیفیت، باگ‌ها و پیشنهادات می‌دهد
“””

import ast
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(**name**)

class IssueSeverity(Enum):
“”“سطح شدت مشکلات”””
CRITICAL = “critical”  # باگ‌های خطرناک
HIGH = “high”  # مشکلات مهم
MEDIUM = “medium”  # بهبودهای پیشنهادی
LOW = “low”  # نکات جزئی
INFO = “info”  # اطلاعات

@dataclass
class CodeIssue:
“”“یک مشکل در کد”””
severity: IssueSeverity
line: int
message: str
category: str  # security, performance, style, bug
suggestion: Optional[str] = None

@dataclass
class ReviewResult:
“”“نتیجه بررسی کد”””
quality_score: float  # نمره 0-100
issues: List[CodeIssue]
strengths: List[str]  # نقاط قوت
metrics: Dict[str, any]  # متریک‌های کد
summary: str

class AICodeReviewer:
“”“بررسی‌کننده خودکار کد با AI”””

```
def __init__(self, llm_wrapper=None):
    """
    Args:
        llm_wrapper: اتصال به LLM برای تحلیل پیشرفته‌تر
    """
    self.llm_wrapper = llm_wrapper
    
    # الگوهای خطرناک
    self.dangerous_patterns = {
        r'eval\(': 'استفاده از eval() خطرناک است',
        r'exec\(': 'استفاده از exec() خطرناک است',
        r'__import__\(': 'import دینامیک می‌تواند خطرناک باشد',
        r'pickle\.loads?\(': 'pickle می‌تواند کد اجرا کند',
        r'subprocess\.(call|run|Popen).*shell=True': 'shell=True خطر command injection',
        r'sqlite3\.connect.*:\w+': 'SQL injection احتمالی'
    }
    
    # الگوهای بد برای Performance
    self.performance_antipatterns = {
        r'for .+ in .+:\s+.*\.append\(': 'از list comprehension استفاده کن',
        r'time\.sleep\(\d+\)': 'sleep طولانی ممکنه مشکل ساز باشه',
        r'\.copy\(\).*\.copy\(\)': 'کپی‌های زیاد حافظه رو پر می‌کنن',
    }

def review_code(self, code: str, file_path: str) -> ReviewResult:
    """
    بررسی کامل کد
    
    Args:
        code: محتوای کد
        file_path: مسیر فایل
        
    Returns:
        ReviewResult با نتایج بررسی
    """
    logger.info(f"شروع بررسی کد: {file_path}")
    
    issues = []
    strengths = []
    
    # 1. بررسی Syntax
    syntax_ok, syntax_issues = self._check_syntax(code)
    issues.extend(syntax_issues)
    
    if not syntax_ok:
        return ReviewResult(
            quality_score=0,
            issues=issues,
            strengths=[],
            metrics={},
            summary="❌ کد خطای Syntax دارد و قابل اجرا نیست"
        )
    
    # 2. بررسی Security
    security_issues = self._check_security(code)
    issues.extend(security_issues)
    if not security_issues:
        strengths.append("✅ مشکل امنیتی جدی پیدا نشد")
    
    # 3. بررسی Performance
    perf_issues = self._check_performance(code)
    issues.extend(perf_issues)
    
    # 4. بررسی Style
    style_issues = self._check_style(code)
    issues.extend(style_issues)
    
    # 5. محاسبه متریک‌ها
    metrics = self._calculate_metrics(code)
    
    # 6. بررسی با LLM (اگر موجود باشد)
    if self.llm_wrapper:
        llm_insights = self._get_llm_insights(code, file_path)
        if llm_insights:
            issues.extend(llm_insights)
    
    # 7. محاسبه نمره
    quality_score = self._calculate_score(issues, metrics)
    
    # 8. تولید خلاصه
    summary = self._generate_summary(quality_score, issues, strengths)
    
    logger.info(f"بررسی تمام شد. نمره: {quality_score:.1f}/100")
    
    return ReviewResult(
        quality_score=quality_score,
        issues=sorted(issues, key=lambda x: x.severity.value),
        strengths=strengths,
        metrics=metrics,
        summary=summary
    )

def _check_syntax(self, code: str) -> Tuple[bool, List[CodeIssue]]:
    """بررسی صحت Syntax"""
    issues = []
    try:
        ast.parse(code)
        return True, issues
    except SyntaxError as e:
        issues.append(CodeIssue(
            severity=IssueSeverity.CRITICAL,
            line=e.lineno or 0,
            message=f"خطای Syntax: {e.msg}",
            category="syntax",
            suggestion="کد رو اصلاح کن تا قابل اجرا باشه"
        ))
        return False, issues

def _check_security(self, code: str) -> List[CodeIssue]:
    """بررسی مشکلات امنیتی"""
    issues = []
    lines = code.split('\n')
    
    for pattern, message in self.dangerous_patterns.items():
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                issues.append(CodeIssue(
                    severity=IssueSeverity.CRITICAL,
                    line=i,
                    message=f"⚠️ خطر امنیتی: {message}",
                    category="security",
                    suggestion="از روش‌های امن‌تر استفاده کن"
                ))
    
    # بررسی hardcoded secrets
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']'
    ]
    
    for pattern in secret_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(CodeIssue(
                    severity=IssueSeverity.HIGH,
                    line=i,
                    message="🔑 اطلاعات حساس Hardcode شده",
                    category="security",
                    suggestion="از environment variables استفاده کن"
                ))
    
    return issues

def _check_performance(self, code: str) -> List[CodeIssue]:
    """بررسی مشکلات Performance"""
    issues = []
    lines = code.split('\n')
    
    for pattern, message in self.performance_antipatterns.items():
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                issues.append(CodeIssue(
                    severity=IssueSeverity.MEDIUM,
                    line=i,
                    message=f"⚡ بهبود Performance: {message}",
                    category="performance"
                ))
    
    # بررسی حلقه‌های تو در تو
    nested_loops = re.findall(r'for .+ in .+:\s+.*for .+ in', code)
    if len(nested_loops) > 2:
        issues.append(CodeIssue(
            severity=IssueSeverity.MEDIUM,
            line=0,
            message="⚡ حلقه‌های تو در تو زیاد (O(n²) یا بدتر)",
            category="performance",
            suggestion="بررسی کن آیا می‌تونی الگوریتم بهتری استفاده کنی"
        ))
    
    return issues

def _check_style(self, code: str) -> List[CodeIssue]:
    """بررسی Style و Best Practices"""
    issues = []
    lines = code.split('\n')
    
    # بررسی خطوط خیلی طولانی
    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            issues.append(CodeIssue(
                severity=IssueSeverity.LOW,
                line=i,
                message="📏 خط خیلی طولانیه (>120 کاراکتر)",
                category="style",
                suggestion="خط رو بشکون برای خوانایی بهتر"
            ))
    
    # بررسی docstring
    if 'def ' in code or 'class ' in code:
        if '"""' not in code and "'''" not in code:
            issues.append(CodeIssue(
                severity=IssueSeverity.LOW,
                line=0,
                message="📝 Docstring نداره",
                category="style",
                suggestion="برای تابع‌ها و کلاس‌ها docstring بنویس"
            ))
    
    # بررسی import
    if 'import *' in code:
        issues.append(CodeIssue(
            severity=IssueSeverity.MEDIUM,
            line=0,
            message="⚠️ از 'import *' استفاده نکن",
            category="style",
            suggestion="import‌های خاص رو به صورت صریح بنویس"
        ))
    
    # بررسی نام‌گذاری
    bad_names = re.findall(r'\b([a-z])\b\s*=', code)
    if len(bad_names) > 3:
        issues.append(CodeIssue(
            severity=IssueSeverity.LOW,
            line=0,
            message="🏷️ اسم‌های متغیر خیلی کوتاه (a, b, c, ...)",
            category="style",
            suggestion="از اسم‌های معنادار استفاده کن"
        ))
    
    return issues

def _calculate_metrics(self, code: str) -> Dict[str, any]:
    """محاسبه متریک‌های کد"""
    lines = code.split('\n')
    
    return {
        'total_lines': len(lines),
        'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
        'blank_lines': len([l for l in lines if not l.strip()]),
        'functions': len(re.findall(r'\bdef\s+\w+', code)),
        'classes': len(re.findall(r'\bclass\s+\w+', code)),
        'imports': len(re.findall(r'^\s*(?:from|import)\s+', code, re.MULTILINE)),
        'complexity': self._estimate_complexity(code)
    }

def _estimate_complexity(self, code: str) -> str:
    """تخمین پیچیدگی کد"""
    # تعداد شاخه‌های منطقی
    branches = len(re.findall(r'\b(if|elif|else|for|while|try|except)\b', code))
    
    if branches < 5:
        return "Low"
    elif branches < 15:
        return "Medium"
    else:
        return "High"

async def _get_llm_insights(self, code: str, file_path: str) -> List[CodeIssue]:
    """دریافت پیشنهادات از LLM"""
    if not self.llm_wrapper:
        return []
    
    try:
        prompt = f"""بررسی این کد Python و مشکلات احتمالی رو پیدا کن:
```

```python
{code[:1000]}  # محدود به 1000 کاراکتر اول
```

فقط موارد مهم رو بگو (باگ‌ها، مشکلات امنیتی، یا بهبودهای قابل توجه).
پاسخ رو به فرمت JSON بده:
[{{“severity”: “high/medium/low”, “line”: 10, “message”: “…”, “suggestion”: “…”}}]
“””

```
        response = await self.llm_wrapper.generate_code(
            task_description=prompt,
            file_path=file_path
        )
        
        if response.success:
            # پردازش پاسخ LLM و تبدیل به CodeIssue
            # این قسمت رو می‌تونی بسته به فرمت خروجی LLM پیاده کنی
            pass
            
    except Exception as e:
        logger.warning(f"خطا در دریافت نظر از LLM: {e}")
    
    return []

def _calculate_score(self, issues: List[CodeIssue], metrics: Dict) -> float:
    """محاسبه نمره کیفیت (0-100)"""
    base_score = 100.0
    
    # کسر امتیاز بر اساس مشکلات
    penalties = {
        IssueSeverity.CRITICAL: 25,
        IssueSeverity.HIGH: 15,
        IssueSeverity.MEDIUM: 8,
        IssueSeverity.LOW: 3,
        IssueSeverity.INFO: 1
    }
    
    for issue in issues:
        base_score -= penalties.get(issue.severity, 5)
    
    # جایزه برای کامنت‌ها
    comment_ratio = metrics['comment_lines'] / max(metrics['code_lines'], 1)
    if comment_ratio > 0.1:
        base_score += 5
    
    # جایزه برای docstring
    # اگر تابع داریم ولی docstring نداریم، جریمه شده
    
    return max(0, min(100, base_score))

def _generate_summary(self, score: float, issues: List[CodeIssue], 
                     strengths: List[str]) -> str:
    """تولید خلاصه نتیجه"""
    emoji = "🎉" if score >= 90 else "✅" if score >= 75 else "⚠️" if score >= 50 else "❌"
    
    critical = len([i for i in issues if i.severity == IssueSeverity.CRITICAL])
    high = len([i for i in issues if i.severity == IssueSeverity.HIGH])
    
    summary = f"{emoji} نمره کیفیت: {score:.1f}/100\n\n"
    
    if critical > 0:
        summary += f"🚨 {critical} مشکل CRITICAL\n"
    if high > 0:
        summary += f"⚠️ {high} مشکل HIGH\n"
    
    summary += f"\n📊 کل مشکلات: {len(issues)}\n"
    
    if strengths:
        summary += f"\n💪 نقاط قوت:\n"
        for s in strengths[:3]:
            summary += f"  • {s}\n"
    
    if score >= 90:
        summary += "\n✨ کد با کیفیت عالی!"
    elif score >= 75:
        summary += "\n👍 کد خوبه، چند نکته کوچیک داره"
    elif score >= 50:
        summary += "\n🔧 نیاز به بهبود داره"
    else:
        summary += "\n⚠️ مشکلات جدی دارد، باید اصلاح بشه"
    
    return summary

def generate_report(self, result: ReviewResult, output_format: str = "markdown") -> str:
    """تولید گزارش کامل"""
    if output_format == "markdown":
        return self._generate_markdown_report(result)
    elif output_format == "json":
        return self._generate_json_report(result)
    else:
        return result.summary

def _generate_markdown_report(self, result: ReviewResult) -> str:
    """تولید گزارش Markdown"""
    report = f"# 📋 Code Review Report\n\n"
    report += f"{result.summary}\n\n"
    
    report += f"## 📊 Metrics\n\n"
    for key, value in result.metrics.items():
        report += f"- **{key}**: {value}\n"
    
    if result.issues:
        report += f"\n## 🔍 Issues Found ({len(result.issues)})\n\n"
        
        # گروه‌بندی بر اساس severity
        by_severity = {}
        for issue in result.issues:
            sev = issue.severity.value
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(issue)
        
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            if severity in by_severity:
                report += f"\n### {severity.upper()}\n\n"
                for issue in by_severity[severity]:
                    report += f"- **Line {issue.line}** [{issue.category}]: {issue.message}\n"
                    if issue.suggestion:
                        report += f"  💡 *{issue.suggestion}*\n"
    
    return report

def _generate_json_report(self, result: ReviewResult) -> str:
    """تولید گزارش JSON"""
    import json
    return json.dumps({
        'quality_score': result.quality_score,
        'summary': result.summary,
        'metrics': result.metrics,
        'issues': [
            {
                'severity': i.severity.value,
                'line': i.line,
                'category': i.category,
                'message': i.message,
                'suggestion': i.suggestion
            }
            for i in result.issues
        ],
        'strengths': result.strengths
    }, ensure_ascii=False, indent=2)
```

# مثال استفاده

if **name** == “**main**”:
# کد نمونه برای تست
sample_code = ‘’’
def process_data(data):
“”“پردازش داده‌ها”””
result = []
for item in data:
if item > 0:
result.append(item * 2)
return result

def unsafe_query(user_input):
# این تابع مشکل امنیتی داره
query = f”SELECT * FROM users WHERE name = ‘{user_input}’”
return query

password = “mysecret123”  # Hardcoded!
‘’’

```
reviewer = AICodeReviewer()
result = reviewer.review_code(sample_code, "example.py")

print(reviewer.generate_report(result, "markdown"))
```

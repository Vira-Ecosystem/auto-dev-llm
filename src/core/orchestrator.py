
"""
Orchestrator - هماهنگ‌کننده اصلی سیستم
"""

import asyncio
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import sys

# Import ماژول‌های داخلی
sys.path.append(str(Path(__file__).parent.parent))

from core.config import ConfigLoader, Feature, Task, ProjectConfig
from core.task_manager import TaskManager, TaskExecution, TaskResult, TaskStatus
from llm.llama_wrapper import LLMWrapper, LLMRequest
from utils.logger import AutoDevLogger
from reviewers.code_reviewer import AICodeReviewer


class Orchestrator:
    """هماهنگ‌کننده اصلی سیستم توسعه خودکار"""
    
    def __init__(self, spec_path: str = "./specs/project_spec.yaml"):
        self.spec_path = spec_path
        self.config: Optional[ProjectConfig] = None
        self.config_loader = ConfigLoader(spec_path)
        self.code_reviewer = None

        self.task_manager: Optional[TaskManager] = None
        self.llm_wrapper: Optional[LLMWrapper] = None
        self.code_reviewer = AICodeReviewer(llm_wrapper=self.llm_wrapper)

        self.logger: Optional[AutoDevLogger] = None
        
        # وضعیت اجرا
        self.is_running = False
        self.current_feature: Optional[str] = None
    
    def initialize(self):
        """راه‌اندازی اولیه سیستم"""
        print("🚀 در حال راه‌اندازی Auto-Dev-LLM...")
        
        # 1. بارگذاری تنظیمات
        print("📋 بارگذاری تنظیمات...")
        self.config = self.config_loader.load()
        print(f"✅ پروژه: {self.config.project_name}")
        print(f"✅ نسخه: {self.config.version}")
        print(f"✅ تعداد Features: {len(self.config.features)}")
        
        # 2. راه‌اندازی Logger
        print("\n📝 راه‌اندازی سیستم لاگ...")
        self.logger = AutoDevLogger(
            name=self.config.project_name,
            log_path=self.config.logging.log_path,
            level=self.config.logging.level,
            per_feature_log=self.config.logging.per_feature_log
        )
        self.logger.info("سیستم Auto-Dev-LLM راه‌اندازی شد")
        
        # 3. راه‌اندازی Task Manager
        print("📊 راه‌اندازی Task Manager...")
        self.task_manager = TaskManager()
        self.task_manager.max_concurrent_tasks = self.config.scheduler.max_concurrent_tasks
        
        # 4. راه‌اندازی LLM
        print("🤖 راه‌اندازی LLM...")
        llm_config = {
            'mode': self.config.llm.mode.value,
            'mcp': self.config.llm.mcp,
            'offline_model': self.config.llm.offline_model,
            'online': self.config.llm.online,
            'fallback_online': self.config.llm.fallback_online
        }
        self.llm_wrapper = LLMWrapper(llm_config)
        print(f"✅ حالت LLM: {self.config.llm.mode.value}")
        
        print("\n✅ راه‌اندازی کامل شد!\n")
    
    def display_features(self):
        """نمایش features به کاربر"""
        print("=" * 70)
        print("📦 Features موجود برای توسعه:")
        print("=" * 70)
        
        for i, feature in enumerate(self.config.features, 1):
            status = "✅ تایید شده" if feature.approved else "⏳ در انتظار تایید"
            print(f"\n{i}. {feature.name} (اولویت: {feature.priority}) - {status}")
            print(f"   📝 {feature.description}")
            print(f"   📋 تعداد Tasks: {len(feature.tasks)}")
            
            for j, task in enumerate(feature.tasks, 1):
                print(f"      {j}. {task.name}")
                print(f"         - {task.description}")
                print(f"         - فایل‌ها: {', '.join(task.files)}")
        
        print("\n" + "=" * 70)
    
    async def request_approval(self) -> List[Feature]:
        """درخواست تایید از کاربر"""
        self.display_features()
        
        print("\n🔔 گزینه‌های تایید:")
        print("1. تایید همه features")
        print("2. تایید feature های خاص (با شماره)")
        print("3. تایید batch (features با اولویت مشخص)")
        print("0. خروج")
        
        choice = input("\n👉 انتخاب شما: ").strip()
        
        if choice == "0":
            print("❌ خروج از برنامه...")
            sys.exit(0)
        
        elif choice == "1":
            # تایید همه
            for feature in self.config.features:
                feature.approved = True
            print("✅ همه features تایید شدند")
            return self.config.features
        
        elif choice == "2":
            # تایید خاص
            numbers = input("شماره features (با کاما جدا شوند): ").strip()
            try:
                indices = [int(n.strip()) - 1 for n in numbers.split(",")]
                approved = []
                for idx in indices:
                    if 0 <= idx < len(self.config.features):
                        self.config.features[idx].approved = True
                        approved.append(self.config.features[idx])
                        print(f"✅ {self.config.features[idx].name} تایید شد")
                return approved
            except:
                print("❌ ورودی نامعتبر!")
                return await self.request_approval()
        
        elif choice == "3":
            # تایید batch
            priority = input("اولویت (مثلاً 1-3): ").strip()
            try:
                if "-" in priority:
                    start, end = map(int, priority.split("-"))
                    approved = [
                        f for f in self.config.features
                        if start <= f.priority <= end
                    ]
                else:
                    p = int(priority)
                    approved = [f for f in self.config.features if f.priority == p]
                
                for feature in approved:
                    feature.approved = True
                    print(f"✅ {feature.name} تایید شد")
                
                return approved
            except:
                print("❌ ورودی نامعتبر!")
                return await self.request_approval()
        
        else:
            print("❌ گزینه نامعتبر!")
            return await self.request_approval()
    
    async def execute_task(self, task: Task, feature: Feature) -> TaskResult:
        """اجرای یک task"""
        task_id = f"{feature.name}.{task.name}"
        feature_logger = self.logger.create_feature_logger(feature.name)
        
        start_time = datetime.now()
        feature_logger.info(
            f"🚀 شروع task: {task.name}",
            task_name=task.name
        )
        
        try:
            # 1. ایجاد پوشه‌ها
            for file_path in task.files:
                file_obj = Path(file_path)
                file_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # 2. تولید کد با LLM
            feature_logger.info(
                "🤖 تولید کد با LLM...",
                task_name=task.name
            )
            
            generated_files = []
            for file_path in task.files:
                self.logger.log_llm_request(
                    prompt=task.description,
                    model=self.config.llm.mode.value,
                    tokens=0
                )
                
                response = await self.llm_wrapper.generate_code(
                    task_description=task.description,
                    file_path=file_path,
                    context=f"Feature: {feature.description}"
                )
                
                if not response.success:
                    raise Exception(f"تولید کد ناموفق بود: {response.error}")
                
                # ذخیره کد تولید شده
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.content)
                
                generated_files.append(file_path)
                
                feature_logger.info(
                    f"✅ فایل تولید شد: {file_path}",
                    task_name=task.name
                )
                
                self.logger.log_llm_response(
                    response=response.content,
                    tokens=response.tokens_used,
                    duration=response.duration
                )
            
            # 3. تولید تست‌ها
            for i, test_path in enumerate(task.tests):
                if i < len(generated_files):
                    with open(generated_files[i], 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    test_response = await self.llm_wrapper.generate_tests(
                        code=code,
                        file_path=test_path
                    )
                    
                    if test_response.success:
                        test_file = Path(test_path)
                        test_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(test_path, 'w', encoding='utf-8') as f:
                            f.write(test_response.content)
                        
                        feature_logger.info(
                            f"✅ تست تولید شد: {test_path}",
                            task_name=task.name
                        )
            
            # 4. محاسبه مدت زمان
            duration = (datetime.now() - start_time).total_seconds()
            
            feature_logger.info(
                f"✅ Task تکمیل شد: {task.name} ({duration:.2f}s)",
                task_name=task.name
            )
            
            return TaskResult(
                success=True,
                output=f"تولید شد: {', '.join(generated_files)}",
                duration=duration,
                generated_files=generated_files
            )
        
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            feature_logger.error(
                f"❌ خطا در task: {task.name} - {str(e)}",
                task_name=task.name,
                exc_info=True
            )
            
            return TaskResult(
                success=False,
                error=str(e),
                duration=duration
            )
    
    async def process_feature(self, feature: Feature):
        """پردازش یک feature کامل"""
        self.current_feature = feature.name
        
        print(f"\n{'='*70}")
        print(f"📦 شروع Feature: {feature.name}")
        print(f"{'='*70}\n")
        
        # اضافه کردن tasks به صف
        self.task_manager.add_feature_tasks(
            feature.name,
            feature.tasks,
            feature.priority
        )
        
        # پردازش tasks
        while True:
            # بررسی امکان شروع task جدید
            task_exec = self.task_manager.get_next_pending_task()
            
            if not task_exec:
                # صبر برای اتمام tasks در حال اجرا
                if self.task_manager.queue.get_running_count() > 0:
                    await asyncio.sleep(2)
                    continue
                else:
                    # همه tasks این feature تمام شد
                    break
            
            # یافتن Task object
            task = next(
                (t for t in feature.tasks if t.name == task_exec.task_name),
                None
            )
            
            if not task:
                continue
            
            # شروع task
            task_id = self.task_manager.start_task(task_exec)
            
            # اجرای task
            result = await self.execute_task(task, feature)
            
            # ثبت نتیجه
            if result.success:
                self.task_manager.complete_task(task_id, result)

                # بررسی خودکار کد
                try:
                    review_result = self.code_reviewer.review_code(
                        code=result.content,
                        file_path=task.files[0] if task.files else "generated_code.py"
                    )
                    
                    self.logger.info(f"نمره کیفیت: {review_result.quality_score}/100")
                    
                    import os
                    os.makedirs("logs", exist_ok=True)
                    report_path = f"logs/review_{task.name}.md"
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(self.code_reviewer.generate_report(review_result))
                    
                except Exception as e:
                    self.logger.warning(f"خطا در Review: {e}")

            else:
                self.task_manager.fail_task(task_id, result, retry=True)
        
        # نمایش پیشرفت
        progress = self.task_manager.get_feature_progress(feature.name)
        print(f"\n📊 پیشرفت {feature.name}:")
        print(f"   ✅ تکمیل شده: {progress['completed']}/{progress['total']}")
        print(f"   ❌ ناموفق: {progress['failed']}")
        print(f"   📈 درصد: {progress['progress_percent']:.1f}%")
    
    async def run(self):
        """اجرای اصلی سیستم"""
        self.is_running = True
        
        try:
            # راه‌اندازی
            self.initialize()
            
            # درخواست تایید
            approved_features = await self.request_approval()
            
            if not approved_features:
                print("❌ هیچ feature تایید نشده!")
                return
            
            print(f"\n🎯 {len(approved_features)} feature تایید شد. شروع توسعه...\n")
            
            # پردازش features
            for feature in approved_features:
                await self.process_feature(feature)
            
            # نمایش آمار نهایی
            stats = self.task_manager.get_statistics()
            print(f"\n{'='*70}")
            print("📊 آمار نهایی:")
            print(f"{'='*70}")
            print(f"کل Tasks: {stats['total_tasks']}")
            print(f"✅ موفق: {stats['completed']}")
            print(f"❌ ناموفق: {stats['failed']}")
            print(f"⏱️  میانگین زمان: {stats['average_duration']:.2f}s")
            print(f"{'='*70}\n")
            
            print("🎉 توسعه خودکار با موفقیت انجام شد!")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  متوقف شد توسط کاربر")
            self.is_running = False
        
        except Exception as e:
            print(f"\n❌ خطای کلی: {e}")
            self.logger.critical(f"خطای کلی در orchestrator: {e}", exc_info=True)
        
        finally:
            self.is_running = False


# نقطه ورود
if __name__ == "__main__":
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.run())

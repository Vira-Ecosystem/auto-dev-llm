"""
Scheduler - زمان‌بندی و کنترل منابع سیستم
"""

import asyncio
from datetime import datetime, time
from typing import Optional, Callable
import psutil
import platform


class ResourceMonitor:
    """مانیتورینگ منابع سیستم"""
    
    @staticmethod
    def get_cpu_usage() -> float:
        """دریافت درصد استفاده CPU"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage() -> float:
        """دریافت درصد استفاده RAM"""
        return psutil.virtual_memory().percent
    
    @staticmethod
    def get_disk_usage(path: str = "/") -> float:
        """دریافت درصد استفاده دیسک"""
        return psutil.disk_usage(path).percent
    
    @staticmethod
    def is_system_idle(cpu_threshold: int = 80, memory_threshold: int = 80) -> bool:
        """بررسی آماده بودن سیستم"""
        cpu = ResourceMonitor.get_cpu_usage()
        memory = ResourceMonitor.get_memory_usage()
        
        return cpu < cpu_threshold and memory < memory_threshold
    
    @staticmethod
    def get_system_info() -> dict:
        """اطلاعات کامل سیستم"""
        return {
            'platform': platform.system(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=0.5),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'memory_percent': psutil.virtual_memory().percent
        }


class TimeScheduler:
    """زمان‌بند وظایف"""
    
    def __init__(
        self,
        active_start_hour: int = 9,
        active_end_hour: int = 18,
        check_interval: int = 60,
        cpu_threshold: int = 80
    ):
        self.active_start_hour = active_start_hour
        self.active_end_hour = active_end_hour
        self.check_interval = check_interval
        self.cpu_threshold = cpu_threshold
        self.is_active = False
        self.monitor = ResourceMonitor()
    
    def is_within_active_hours(self) -> bool:
        """بررسی ساعت کاری"""
        now = datetime.now().time()
        start_time = time(self.active_start_hour, 0)
        end_time = time(self.active_end_hour, 0)
        
        return start_time <= now < end_time
    
    def can_execute(self) -> tuple[bool, str]:
        """بررسی امکان اجرا"""
        # بررسی ساعت کاری
        if not self.is_within_active_hours():
            current_time = datetime.now().strftime("%H:%M")
            return False, f"خارج از ساعات کاری ({current_time}). ساعات مجاز: {self.active_start_hour}:00 - {self.active_end_hour}:00"
        
        # بررسی منابع سیستم
        if not self.monitor.is_system_idle(self.cpu_threshold):
            cpu = self.monitor.get_cpu_usage()
            return False, f"سیستم مشغول است (CPU: {cpu:.1f}%)"
        
        return True, "آماده اجرا"
    
    async def wait_for_ready(self, callback: Optional[Callable] = None):
        """صبر تا آماده شدن سیستم"""
        while True:
            can_run, reason = self.can_execute()
            
            if can_run:
                self.is_active = True
                if callback:
                    await callback("ready", reason)
                return
            else:
                self.is_active = False
                if callback:
                    await callback("waiting", reason)
                
                await asyncio.sleep(self.check_interval)
    
    def get_next_active_time(self) -> str:
        """زمان شروع بعدی"""
        now = datetime.now()
        
        if now.hour < self.active_start_hour:
            next_time = now.replace(
                hour=self.active_start_hour,
                minute=0,
                second=0
            )
        else:
            # فردا
            next_day = now.replace(
                hour=self.active_start_hour,
                minute=0,
                second=0
            ) + timedelta(days=1)
            next_time = next_day
        
        return next_time.strftime("%Y-%m-%d %H:%M:%S")


class TaskScheduler:
    """زمان‌بند پیشرفته با قابلیت‌های اضافی"""
    
    def __init__(
        self,
        active_hours: dict,
        max_concurrent_tasks: int = 2,
        check_interval: int = 60,
        cpu_threshold: int = 80
    ):
        self.time_scheduler = TimeScheduler(
            active_start_hour=active_hours.get('start', 9),
            active_end_hour=active_hours.get('end', 18),
            check_interval=check_interval,
            cpu_threshold=cpu_threshold
        )
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks = 0
        self.paused = False
    
    def can_start_task(self) -> tuple[bool, str]:
        """بررسی امکان شروع task جدید"""
        # بررسی توقف دستی
        if self.paused:
            return False, "سیستم به صورت دستی متوقف شده است"
        
        # بررسی تعداد همزمانی
        if self.running_tasks >= self.max_concurrent_tasks:
            return False, f"حداکثر تعداد همزمانی ({self.max_concurrent_tasks}) رسیده"
        
        # بررسی ساعت و منابع
        return self.time_scheduler.can_execute()
    
    async def wait_for_slot(self, task_name: str, logger=None):
        """صبر برای آزاد شدن slot"""
        while True:
            can_start, reason = self.can_start_task()
            
            if can_start:
                return
            
            if logger:
                logger.debug(f"⏳ صبر برای {task_name}: {reason}")
            
            await asyncio.sleep(5)
    
    def acquire_slot(self):
        """گرفتن یک slot"""
        self.running_tasks += 1
    
    def release_slot(self):
        """آزاد کردن یک slot"""
        self.running_tasks = max(0, self.running_tasks - 1)
    
    def pause(self):
        """توقف دستی"""
        self.paused = True
    
    def resume(self):
        """ادامه پس از توقف"""
        self.paused = False
    
    def get_status(self) -> dict:
        """وضعیت فعلی scheduler"""
        can_run, reason = self.time_scheduler.can_execute()
        
        return {
            'active': can_run and not self.paused,
            'paused': self.paused,
            'reason': reason,
            'running_tasks': self.running_tasks,
            'max_concurrent': self.max_concurrent_tasks,
            'available_slots': self.max_concurrent_tasks - self.running_tasks,
            'within_hours': self.time_scheduler.is_within_active_hours(),
            'system_info': self.time_scheduler.monitor.get_system_info()
        }
    
    async def schedule_with_retry(
        self,
        task_func: Callable,
        task_name: str,
        max_retries: int = 3,
        retry_delay: int = 60,
        logger=None
    ):
        """اجرای task با retry خودکار"""
        attempt = 0
        
        while attempt < max_retries:
            try:
                # صبر برای slot آزاد
                await self.wait_for_slot(task_name, logger)
                
                # گرفتن slot
                self.acquire_slot()
                
                try:
                    # اجرای task
                    if logger:
                        logger.info(f"🚀 شروع {task_name} (تلاش {attempt + 1}/{max_retries})")
                    
                    result = await task_func()
                    
                    if logger:
                        logger.info(f"✅ {task_name} با موفقیت اجرا شد")
                    
                    return result
                
                finally:
                    # آزاد کردن slot
                    self.release_slot()
            
            except Exception as e:
                attempt += 1
                
                if logger:
                    logger.error(f"❌ خطا در {task_name} (تلاش {attempt}/{max_retries}): {e}")
                
                if attempt >= max_retries:
                    raise
                
                # صبر قبل از retry
                if logger:
                    logger.info(f"⏳ صبر {retry_delay}s قبل از تلاش مجدد...")
                
                await asyncio.sleep(retry_delay)


from datetime import timedelta


class AdaptiveScheduler(TaskScheduler):
    """زمان‌بند هوشمند با یادگیری الگوهای استفاده"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_history = []  # تاریخچه اجرای tasks
        self.optimal_hours = None  # ساعات بهینه
    
    def record_task_execution(self, task_name: str, duration: float, success: bool):
        """ثبت اجرای task"""
        self.task_history.append({
            'task_name': task_name,
            'timestamp': datetime.now(),
            'duration': duration,
            'success': success,
            'cpu_usage': self.time_scheduler.monitor.get_cpu_usage(),
            'memory_usage': self.time_scheduler.monitor.get_memory_usage()
        })
        
        # نگهداری آخرین 1000 اجرا
        if len(self.task_history) > 1000:
            self.task_history = self.task_history[-1000:]
    
    def analyze_optimal_hours(self) -> dict:
        """تحلیل ساعات بهینه بر اساس تاریخچه"""
        if len(self.task_history) < 10:
            return None
        
        hour_stats = {}
        
        for record in self.task_history:
            hour = record['timestamp'].hour
            
            if hour not in hour_stats:
                hour_stats[hour] = {
                    'total': 0,
                    'success': 0,
                    'avg_duration': 0,
                    'avg_cpu': 0
                }
            
            hour_stats[hour]['total'] += 1
            if record['success']:
                hour_stats[hour]['success'] += 1
            hour_stats[hour]['avg_duration'] += record['duration']
            hour_stats[hour]['avg_cpu'] += record['cpu_usage']
        
        # محاسبه میانگین‌ها
        for hour in hour_stats:
            total = hour_stats[hour]['total']
            hour_stats[hour]['success_rate'] = hour_stats[hour]['success'] / total
            hour_stats[hour]['avg_duration'] /= total
            hour_stats[hour]['avg_cpu'] /= total
        
        # پیدا کردن بهترین ساعات
        sorted_hours = sorted(
            hour_stats.items(),
            key=lambda x: (x[1]['success_rate'], -x[1]['avg_cpu']),
            reverse=True
        )
        
        self.optimal_hours = [h[0] for h in sorted_hours[:8]]  # 8 ساعت برتر
        
        return {
            'optimal_hours': self.optimal_hours,
            'statistics': hour_stats
        }
    
    def should_execute_now(self) -> tuple[bool, str]:
        """آیا الان زمان مناسبی برای اجراست؟ (بر اساس یادگیری)"""
        # اگر تاریخچه کافی نداریم، از روش پایه استفاده می‌کنیم
        if not self.optimal_hours:
            return self.can_start_task()
        
        # بررسی ساعت بهینه
        current_hour = datetime.now().hour
        
        if current_hour not in self.optimal_hours:
            return False, f"ساعت فعلی ({current_hour}) در بازه بهینه نیست"
        
        return self.can_start_task()


# تست سریع
if __name__ == "__main__":
    async def test_scheduler():
        # ایجاد scheduler
        scheduler = TaskScheduler(
            active_hours={'start': 9, 'end': 18},
            max_concurrent_tasks=2,
            check_interval=5,
            cpu_threshold=80
        )
        
        # نمایش وضعیت
        status = scheduler.get_status()
        print("📊 وضعیت Scheduler:")
        print(f"   Active: {status['active']}")
        print(f"   Reason: {status['reason']}")
        print(f"   Running Tasks: {status['running_tasks']}/{status['max_concurrent']}")
        print(f"   Within Hours: {status['within_hours']}")
        print(f"\n💻 اطلاعات سیستم:")
        print(f"   Platform: {status['system_info']['platform']}")
        print(f"   CPU: {status['system_info']['cpu_percent']:.1f}%")
        print(f"   Memory: {status['system_info']['memory_percent']:.1f}%")
        
        # تست اجرای task
        async def sample_task():
            print("   🔄 Task در حال اجرا...")
            await asyncio.sleep(2)
            print("   ✅ Task تکمیل شد")
            return "success"
        
        try:
            print("\n🚀 تست اجرای task با scheduler...")
            result = await scheduler.schedule_with_retry(
                task_func=sample_task,
                task_name="test-task",
                max_retries=2
            )
            print(f"📊 نتیجه: {result}")
        except Exception as e:
            print(f"❌ خطا: {e}")
    
    # اجرای تست
    asyncio.run(test_scheduler())
#!/usr/bin/env python3
"""
Dry Run Test - تست سیستم بدون تولید کد واقعی
برای بررسی اینکه همه چیز درست کار می‌کند
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

sys.path.insert(0, str(Path(__file__).parent / "src"))


async def dry_run_test():
    """تست خشک سیستم"""
    
    console.print("\n[bold cyan]🧪 DRY RUN TEST MODE[/bold cyan]\n")
    console.print("[dim]This will test the system without generating real code[/dim]\n")
    
    # Test 1: Config Loading
    console.print("[yellow]Test 1:[/yellow] Config Loading...")
    try:
        from core.config import ConfigLoader
        
        loader = ConfigLoader("specs/self_development_spec.yaml")
        config = loader.load()
        
        console.print(f"   ✅ Project: {config.project_name}")
        console.print(f"   ✅ Features: {len(config.features)}")
        console.print(f"   ✅ Total Tasks: {sum(len(f.tasks) for f in config.features)}")
        
    except Exception as e:
        console.print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Task Manager
    console.print("\n[yellow]Test 2:[/yellow] Task Manager...")
    try:
        from core.task_manager import TaskManager
        
        manager = TaskManager()
        
        # اضافه کردن task های تست
        manager.add_feature_tasks("test-feature", config.features[0].tasks, 1)
        
        stats = manager.get_statistics()
        console.print(f"   ✅ Queue created: {stats['total_tasks']} tasks")
        
    except Exception as e:
        console.print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Logger
    console.print("\n[yellow]Test 3:[/yellow] Logger System...")
    try:
        from utils.logger import AutoDevLogger
        
        logger = AutoDevLogger(
            name="dry-run-test",
            log_path="./logs",
            level="DEBUG"
        )
        
        logger.info("Test log message")
        console.print("   ✅ Logger initialized")
        console.print("   ✅ Log file created")
        
    except Exception as e:
        console.print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: LLM Wrapper (without actual call)
    console.print("\n[yellow]Test 4:[/yellow] LLM Wrapper...")
    try:
        from llm.llama_wrapper import LLMWrapper
        
        llm_config = {
            'mode': config.llm.mode.value,
            'mcp': config.llm.mcp,
            'online': config.llm.online,
            'fallback_online': config.llm.fallback_online
        }
        
        wrapper = LLMWrapper(llm_config)
        console.print("   ✅ LLM Wrapper initialized")
        console.print(f"   ✅ Mode: {config.llm.mode.value}")
        
    except Exception as e:
        console.print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: Scheduler
    console.print("\n[yellow]Test 5:[/yellow] Scheduler...")
    try:
        from managers.scheduler import TaskScheduler
        
        scheduler = TaskScheduler(
            active_hours=config.scheduler.active_hours,
            max_concurrent_tasks=config.scheduler.max_concurrent_tasks,
            check_interval=config.scheduler.check_interval,
            cpu_threshold=config.scheduler.cpu_threshold
        )
        
        status = scheduler.get_status()
        console.print("   ✅ Scheduler initialized")
        console.print(f"   ✅ Can execute: {status['active']}")
        console.print(f"   ✅ Available slots: {status['available_slots']}")
        
    except Exception as e:
        console.print(f"   ❌ Error: {e}")
        return False
    
    # Test 6: Feature Simulation
    console.print("\n[yellow]Test 6:[/yellow] Feature Processing Simulation...")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Feature", style="cyan")
    table.add_column("Priority", style="yellow", justify="center")
    table.add_column("Tasks", style="green", justify="center")
    table.add_column("Est. Time", style="blue", justify="right")
    
    total_tasks = 0
    total_time = 0
    
    for feature in config.features:
        num_tasks = len(feature.tasks)
        est_time = num_tasks * 60  # 60s per task
        total_tasks += num_tasks
        total_time += est_time
        
        table.add_row(
            feature.name,
            str(feature.priority),
            str(num_tasks),
            f"{est_time}s"
        )
    
    console.print(table)
    
    console.print(f"\n   📊 Total Tasks: [green]{total_tasks}[/green]")
    console.print(f"   ⏱️  Estimated Time: [yellow]{total_time}s ({total_time/60:.1f} min)[/yellow]")
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold green]✅ ALL TESTS PASSED![/bold green]")
    console.print("="*60)
    
    console.print("\n[bold]System is ready for self-development![/bold]")
    console.print("\nTo start actual development, run:")
    console.print("  [cyan]python bootstrap_self_dev.py[/cyan]")
    console.print()
    
    return True


async def quick_validation():
    """اعتبارسنجی سریع فایل‌ها"""
    
    console.print("\n[bold yellow]📁 File Structure Validation[/bold yellow]\n")
    
    required_files = [
        ("specs/self_development_spec.yaml", "Spec file"),
        ("src/core/config.py", "Config module"),
        ("src/core/task_manager.py", "Task Manager"),
        ("src/core/orchestrator.py", "Orchestrator"),
        ("src/llm/llama_wrapper.py", "LLM Wrapper"),
        ("src/managers/scheduler.py", "Scheduler"),
        ("src/utils/logger.py", "Logger"),
        ("main.py", "Main entry"),
        ("bootstrap_self_dev.py", "Bootstrap script"),
    ]
    
    all_ok = True
    
    for file_path, description in required_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            console.print(f"   ✅ {description:25} ({size:>6} bytes)")
        else:
            console.print(f"   ❌ {description:25} [red]MISSING[/red]")
            all_ok = False
    
    if all_ok:
        console.print("\n[green]✅ All required files exist[/green]")
    else:
        console.print("\n[red]❌ Some files are missing[/red]")
    
    return all_ok


async def main():
    """تابع اصلی"""
    
    console.print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           🧪 DRY RUN TEST SUITE 🧪                   ║
    ║                                                       ║
    ║       Testing system before actual development       ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Validation
    if not await quick_validation():
        console.print("\n[red]❌ Validation failed![/red]")
        return False
    
    # Tests
    if not await dry_run_test():
        console.print("\n[red]❌ Tests failed![/red]")
        return False
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)
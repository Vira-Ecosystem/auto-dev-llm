#!/usr/bin/env python3
"""
Bootstrap Script - شروع توسعه خودکار سیستم
این اسکریپت سیستم را روی خودش اجرا می‌کند!
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.prompt import Confirm
import time

console = Console()

# اضافه کردن src به path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def print_epic_banner():
    """بنر حماسی برای شروع! 🚀"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         🤖 AUTO-DEV-LLM SELF-IMPROVEMENT MODE 🤖             ║
    ║                                                               ║
    ║              "I am about to improve myself!"                 ║
    ║                                                               ║
    ║         The system will now develop its own features         ║
    ║              using AI-powered code generation                ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", border_style="bright_magenta"))


def show_feature_plan():
    """نمایش برنامه توسعه"""
    console.print("\n[bold yellow]📋 Plan for Self-Development:[/bold yellow]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Priority", style="cyan", width=8)
    table.add_column("Feature", style="green", width=25)
    table.add_column("Tasks", style="yellow", width=8)
    table.add_column("Description", style="white")
    
    features = [
        ("1", "git-automation", "2", "Git operations & commit management"),
        ("2", "version-control", "2", "Semantic versioning & changelog"),
        ("3", "rollback-recovery", "2", "Backup & rollback system"),
        ("4", "deploy-automation", "3", "Canary deploy & health checks"),
        ("5", "prompt-system", "3", "Advanced prompt engineering"),
        ("6", "quality-assurance", "3", "Testing & code analysis"),
        ("7", "file-operations", "2", "File management utilities"),
        ("8", "orchestrator-v2", "1", "Enhanced orchestrator"),
    ]
    
    for priority, feature, tasks, desc in features:
        table.add_row(priority, feature, tasks, desc)
    
    console.print(table)
    console.print(f"\n[bold green]Total: 8 Features, 18 Tasks[/bold green]\n")


async def check_prerequisites():
    """بررسی پیش‌نیازها"""
    console.print("[yellow]⏳ Checking prerequisites...[/yellow]\n")
    
    checks = [
        ("Python version", sys.version_info >= (3, 11)),
        ("specs/ directory", Path("specs").exists()),
        ("src/ directory", Path("src").exists()),
        ("project_spec.yaml", Path("specs/self_development_spec.yaml").exists()),
    ]
    
    all_ok = True
    for name, result in checks:
        if result:
            console.print(f"   [green]✓[/green] {name}")
        else:
            console.print(f"   [red]✗[/red] {name}")
            all_ok = False
    
    if not all_ok:
        console.print("\n[red]❌ Prerequisites not met![/red]")
        return False
    
    # Check API key
    import os
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("\n[yellow]⚠️  Warning: No API key found in environment[/yellow]")
        console.print("[dim]Set ANTHROPIC_API_KEY or OPENAI_API_KEY[/dim]")
        
        if not Confirm.ask("\nContinue anyway?"):
            return False
    else:
        console.print(f"   [green]✓[/green] API key found")
    
    console.print("\n[green]✅ All prerequisites met![/green]\n")
    return True


async def run_self_development():
    """اجرای توسعه خودکار"""
    
    from core.orchestrator import Orchestrator
    
    console.print("[bold cyan]🚀 Starting self-development process...[/bold cyan]\n")
    
    # ایجاد orchestrator
    orchestrator = Orchestrator("specs/self_development_spec.yaml")
    
    try:
        # راه‌اندازی
        with console.status("[bold green]Initializing system..."):
            orchestrator.initialize()
        
        console.print("[green]✓[/green] System initialized\n")
        
        # نمایش features
        orchestrator.display_features()
        
        # تایید اتوماتیک همه features
        console.print("\n[bold yellow]🤔 Auto-approving all features...[/bold yellow]")
        
        for feature in orchestrator.config.features:
            feature.approved = True
            console.print(f"   [green]✓[/green] Approved: {feature.name}")
        
        console.print("\n[bold green]✅ All features approved! Starting development...[/bold green]\n")
        
        # شروع توسعه
        approved_features = orchestrator.config_loader.get_approved_features()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            
            main_task = progress.add_task(
                "[cyan]Overall Progress", 
                total=len(approved_features)
            )
            
            for i, feature in enumerate(approved_features, 1):
                progress.update(
                    main_task,
                    description=f"[cyan]Feature {i}/{len(approved_features)}: {feature.name}"
                )
                
                # پردازش feature
                await orchestrator.process_feature(feature)
                
                progress.advance(main_task)
        
        # نمایش آمار نهایی
        stats = orchestrator.task_manager.get_statistics()
        
        console.print("\n" + "="*70)
        console.print("[bold green]🎉 SELF-DEVELOPMENT COMPLETE! 🎉[/bold green]")
        console.print("="*70 + "\n")
        
        result_table = Table(show_header=False, box=None)
        result_table.add_column("Metric", style="cyan")
        result_table.add_column("Value", style="green")
        
        result_table.add_row("Total Tasks", str(stats['total_tasks']))
        result_table.add_row("✅ Completed", str(stats['completed']))
        result_table.add_row("❌ Failed", str(stats['failed']))
        result_table.add_row("⏱️  Avg Duration", f"{stats['average_duration']:.2f}s")
        result_table.add_row(
            "📈 Success Rate", 
            f"{(stats['completed']/stats['total_tasks']*100):.1f}%"
        )
        
        console.print(result_table)
        console.print()
        
        # نمایش فایل‌های تولید شده
        console.print("[bold cyan]📁 Generated Files:[/bold cyan]")
        
        all_tasks = orchestrator.task_manager.get_all_tasks()
        generated_files = []
        
        for task in all_tasks:
            if task.result and task.result.generated_files:
                generated_files.extend(task.result.generated_files)
        
        for file in sorted(set(generated_files)):
            if Path(file).exists():
                size = Path(file).stat().st_size
                console.print(f"   [green]✓[/green] {file} ([dim]{size} bytes[/dim])")
        
        console.print(f"\n[bold green]Total: {len(set(generated_files))} files generated[/bold green]\n")
        
        # پیام نهایی
        console.print(Panel(
            "[bold yellow]🎊 Congratulations! 🎊[/bold yellow]\n\n"
            "The system has successfully improved itself!\n"
            "Check the generated files and run tests:\n\n"
            "  [cyan]pytest tests/ -v[/cyan]\n\n"
            "Next steps:\n"
            "  1. Review generated code\n"
            "  2. Run tests\n"
            "  3. Commit changes\n"
            "  4. Deploy! 🚀",
            style="green",
            border_style="bright_green"
        ))
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user[/yellow]")
        return False
    
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """تابع اصلی"""
    
    # بنر
    print_epic_banner()
    
    # نمایش برنامه
    show_feature_plan()
    
    # تایید کاربر
    if not Confirm.ask("\n[bold yellow]Ready to start self-development?[/bold yellow]"):
        console.print("\n[yellow]Cancelled by user[/yellow]")
        return
    
    console.print()
    
    # بررسی پیش‌نیازها
    if not await check_prerequisites():
        sys.exit(1)
    
    # شروع!
    start_time = time.time()
    
    success = await run_self_development()
    
    duration = time.time() - start_time
    
    if success:
        console.print(f"\n[bold green]✅ Completed in {duration:.2f} seconds[/bold green]\n")
    else:
        console.print(f"\n[bold red]❌ Failed after {duration:.2f} seconds[/bold red]\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Bye! 👋[/yellow]")
        sys.exit(0)
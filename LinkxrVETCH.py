import os
import sys
import time
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException

# استيراد أدوات واجهة المستخدم من مكتبة Rich
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("[!] يرجى تثبيت مكتبة rich أولاً عبر الأمر: pip install rich")
    sys.exit(1)

console = Console()

def show_banner():
    """عرض شعار الأداة وحقوق التليجرام بشكل مميز"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner_text = """
 [bold cyan]       _    __     _______ _____ ____ _   _   [/bold cyan]
 [bold cyan] __  _ | |__ \\ \\   / / ____|_   _/ ___| | | |  [/bold cyan]
 [bold cyan] \\ \\/ /| '_ \\ \\ \\ / /|  _|   | || |   | |_| |  [/bold cyan]
 [bold cyan]  >  < | | | | \\ V / | |___  | || |___|  _  |  [/bold cyan]
 [bold cyan] /_/\\_\\|_| |_|  \\_/  |_____| |_| \\____|_| |_|  [/bold cyan]
                                                 
 [bold magenta]>> xrVETCH bot - Advanced Website Scanner <<[/bold magenta]
 [bold yellow]>> Telegram Bot: @xrVETCH_bot <<[/bold yellow]
 [bold white]--------------------------------------------- [/bold white]
    """
    console.print(banner_text)

def clean_url(url):
    """تنظيف الرابط وإضافة http إذا لم تكن موجودة"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def scan_website(url):
    """فحص الموقع وجمع البيانات"""
    url = clean_url(url)
    domain = urlparse(url).netloc
    
    show_banner()
    console.print(Panel(f"[bold yellow]جاري فحص الموقع:[/bold yellow] [green]{url}[/green]\n[bold yellow]النطاق:[/bold yellow] [white]{domain}[/white]", title="[bold blue]بدء الفحص[/bold blue]"))
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) xrVETCH bot/1.0 (@xrVETCH_bot)'
    }
    
    # تأثير حركي أثناء الفحص
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="[cyan]جاري الاتصال بالخادم وجمع البيانات...[/cyan]", total=None)
        
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response_time = round((time.time() - start_time) * 1000, 2)
        except RequestException as e:
            console.print(f"\n[bold red][!] خطأ في الاتصال بالموقع:[/bold red] {e}\n")
            return

    # إنشاء جدول النتائج
    table = Table(title=f"[bold magenta]نتائج فحص: {domain}[/bold magenta]", show_header=True, header_style="bold magenta")
    table.add_column("النوع (Parameter)", style="cyan", justify="right")
    table.add_column("النتيجة (Value)", style="white", justify="left")

    # 1. حالة الموقع (Status Code)
    status = response.status_code
    status_color = "green" if status == 200 else "yellow" if status < 400 else "red"
    table.add_row("حالة الاستجابة (Status Code)", f"[{status_color}]{status}[/{status_color}]")

    # 2. سرعة الاستجابة
    table.add_row("سرعة الاستجابة (Response Time)", f"[yellow]{response_time} ms[/yellow]")

    # 3. نوع الخادم (Server)
    server = response.headers.get('Server', 'غير معلن (Hidden)')
    table.add_row("نوع الخادم (Server)", f"[green]{server}[/green]")

    # 4. بروتوكول الحماية (SSL/HTTPS)
    is_ssl = "آمن (HTTPS)" if url.startswith('https://') else "غير آمن (HTTP)"
    ssl_color = "green" if url.startswith('https://') else "bold red"
    table.add_row("بروتوكول الاتصال (SSL)", f"[{ssl_color}]{is_ssl}[/{ssl_color}]")

    # 5. فحص جدران الحماية الأساسية (Security Headers)
    security_headers = ['X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Strict-Transport-Security']
    found_headers = [h for h in security_headers if h in response.headers]
    
    protection_score = f"{len(found_headers)}/{len(security_headers)}"
    score_color = "green" if len(found_headers) >= 3 else "yellow" if len(found_headers) > 0 else "red"
    table.add_row("مؤشر حماية العناوين (Security Headers)", f"[{score_color}]{protection_score}[/{score_color}]")

    # عرض الجدول
    console.print(table)
    
    # تفصيل الحماية والوصول
    if found_headers:
        console.print(f"\n[bold green][✓] العناوين الأمنية المكتشفة:[/bold green] {', '.join(found_headers)}")
    else:
        console.print("\n[bold red][!] تحذير: الموقع يفتقر إلى جدران الحماية الأساسية (Security Headers).[/bold red]")
        
    console.print("\n[bold cyan]--------------------------------------------------[/bold cyan]")
    console.print("[bold yellow][⚡] تم الفحص بواسطة أداة xrVETCH bot | تابعنا على تليجرام: @xrVETCH_bot[/bold yellow]")

def main():
    while True:
        show_banner()
        console.print("[bold white][1][/bold white] [cyan]فحص موقع جديد[/cyan]")
        console.print("[bold white][2][/bold white] [red]خروج من الأداة[/red]\n")
        
        choice = console.input("[bold yellow]اختر رقم الأمر هنا -> [/bold yellow]")
        
        if choice == '1':
            target = console.input("\n[bold yellow]أدخل رابط الموقع (مثال: google.com): [/bold yellow]")
            if target.strip():
                scan_website(target)
            else:
                console.print("[bold red][!] لا يمكن ترك الرابط فارغاً[/bold red]")
            
            console.input("\n[bold white]اضغط Enter للعودة للقائمة الرئيسية...[/bold white]")
        elif choice == '2':
            console.print("\n[bold magenta]شكرًا لاستخدامك xrVETCH bot. تابعنا على تليجرام: @xrVETCH_bot[/bold magenta]\n")
            break
        else:
            console.print("[bold red][!] اختيار غير صحيح، جرب ثاني مرة.[/bold red]")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red][!] تم إغلاق الأداة. تابعنا على: @xrVETCH_bot[/bold red]\n")

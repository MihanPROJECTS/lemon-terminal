import os
import random
from datetime import datetime
import platform
import psutil
import time
import customtkinter as ctk
import getpass
import shutil
import subprocess
import socket
ULTRA_MODE = False
VARIABLES = {} #это нужно для будущих обновлений
START_TIME = datetime.now()

#if not ULTRA_MODE:
#            insert_output("  Error: Permission denied. Use 'ultra on' to enable\n", "error")       #Данный шаблон на будущее чтобы удобней проверять в команде привилегии пользователя.
#            insert_output(show_user(), "green")
#            return

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")                     

#def show_user():
#    return "&\\"


font_index = -1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTOS_DIR = os.path.join(BASE_DIR, "fontos")
note_mode = False
note_content = ""
custom_image_path = ""
help_users = {
    "system": {
        "desc": "System commands",
        "commands": ["sysinfo", "memory", "cpu", "disk", "ip", "systime", "pslist", "pkill", "whoami", ]
    },
    "files": {
        "desc": "File management",
        "commands": ["ls", "cd", "mkdir", "rmdir", "touch", "rmrf", "cat", "echo", "writefile", "pwd", "fcount", "fview", "b64encode"]
    },
    "themes": {
        "desc": "Themes and customization",
        "commands": ["theme <name>", "font size <number>", "fullscreen"]
    },
    "tools": {
        "desc": "Tools",
        "commands": ["date", "calc", "random 3", "random 10", "random 100"]
    },
    "terminal": {
        "desc": "Terminal commands",
        "commands": ["ver", "help", "clear", "exit", "clearhistory", "uptime", "history", "ultra", "&&", "run", "sleep","which"]
    }
}

def start_gui():
    window = ctk.CTk()
    window.title("Lemon Terminal") #название окна
    window.configure(fg_color="#1a1a1a")
    window.geometry("800x500")
    window.minsize(400, 460)

    def toggle_fullscreen(event=None):
        state = window.attributes('-fullscreen')
        window.attributes('-fullscreen', not state)

    window.bind("<F11>", toggle_fullscreen)
    output = ctk.CTkTextbox(
        window, 
        font=("monospace", 14), 
        activate_scrollbars=True,
        corner_radius=1,        
        fg_color="#1a1a1a"       
    )
    output.pack(fill="both", expand=True, padx=10, pady=10)
    output.configure(state="disabled")

    #цвета
    output.tag_config("green", foreground="#73d65a")
    output.tag_config("gray_hint", foreground="#757575")
    output.tag_config("error", foreground="#ff4444")

    def show_user():
        user = getpass.getuser()
        if ULTRA_MODE:
            return f"{user}# "
        else:
            return f"{user}$ "

    def insert_output(text, tag=None):
        output.configure(state="normal")
        if tag:
            output.insert("end", text, tag) 
        else:
            output.insert("end", text)
        output.configure(state="disabled")
        output.see("end")
    insert_output("Lemon Terminal v1.5s2b\n")
    insert_output("Type 'help' for categories of commands.\n") 
    insert_output("|To type, click on the input bar.\n\n", "gray_hint")

    entry = ctk.CTkEntry(
        window, 
        placeholder_text="Enter the command...", 
        font=("Consolas", 13),
        height=25,
        corner_radius=0,
        
        fg_color="#FFE600",     
        text_color="black",    
        border_color="#FFE600"  
    )
    entry.pack(fill="x", padx=10, pady=(0, 10))
    entry.focus()

    entry.bind("<Enter>", lambda e: entry.configure(border_color="#F0F0F0")) 
    entry.bind("<Leave>", lambda e: entry.configure(border_color="#FFE600")) 
    rgb_active = False
    rgb_colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    rgb_index = 0

    def rgb_plus_fps():
        nonlocal rgb_index
        if rgb_active:
            entry.configure(fg_color=rgb_colors[rgb_index], text_color="black")
            rgb_index = (rgb_index + 1) % len(rgb_colors)
            window.after(300, rgb_plus_fps)


    entry.bind("<Return>", lambda event: handle_user(event))

    def handle_user(event):
        nonlocal rgb_active
        user = entry.get().strip()
        
        if user:
            if not hasattr(window, 'history'):
                window.history = []
                window.history_index = -1

            if not window.history or window.history[-1] != user:
                window.history.append(user)

            window.history_index = -1
            
        user = user.lower() 
        entry.delete(0, "end")    

        if not user:
            return
        insert_output(show_user(), "green")
        insert_output(user + "\n")

        if user == "help":
            # Категории хэлп
            insert_output(" HELP - Available categories:\n")
            insert_output("─" * 40 + "\n")
            for key, value in help_users.items():
                insert_output(f"  {key}  - {value['desc']}\n")
            insert_output("─" * 40 + "\n")
            insert_output("Type 'help <category>' for detailed commands\n")
            insert_output("  Example: help system\n")       
            return                    
        elif user == "ver":
            ver_text = """
                                                            
     __                         _____               _         _ 
    |  |   ___ _____ ___ ___   |_   _|___ ___ _____|_|___ ___| |
    |  |__| -_|     | . |   |    | | | -_|  _|     | |   | .'| |
    |_____|___|_|_|_|___|_|_|    |_| |___|_| |_|_|_|_|_|_|__,|_|
        
    - made by M1hail
    - 40+ commands
    - theme support
    - run scripts
    - write 'help'
                                                            
"""
            insert_output(ver_text)
            return

        elif user.startswith("run "):
            cmd = user[4:].strip()
            try:
                import subprocess
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                if stdout:
                    insert_output(stdout)
                if stderr:
                    insert_output("⚠️ " + stderr)
                if process.returncode != 0:
                    insert_output(f" command failed (exit code: {process.returncode})\n")
                else:
                    insert_output(f" command finished (exit code: {process.returncode})\n")
            except FileNotFoundError:
                insert_output(f" command not found: {cmd}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
            return
        elif user == "date":
            insert_output(datetime.now().strftime("%d %B %Y") + "\n")
            return
        elif user == "theme":
            insert_output("AVAILABLE THEMES:\n")
            insert_output("─" * 40 + "\n")
            insert_output("  night      - Black background, white text\n")
            insert_output("  light      - White background, black text\n")
            insert_output("  normal     - Classic black + blue input\n")
            insert_output("─" * 40 + "\n")
            return
            
        elif user.startswith("calc "):
            expression = user[5:].strip()
            try:
                #ЛУЧШЕ НЕ МЕНЯЙТЕ ДАННЫЙ НАБОР ЗНАКОВ ДЛЯ КАЛЬКУЛЯТОРА, ЭТО ЗАЩИТА, ВЕДЬ ДАННАЯ ФУНКЦИЯ МОЖЕТ ВЫПОЛНЯТЬ ЛЮБОЙ КОД!
                allowed = "0123456789+-*/().% "
                if not all(c in allowed for c in expression):
                    insert_output(" Invalid characters in expression\n")
                    return
        
                result = eval(expression)
                insert_output(str(result) + "\n")
            except ZeroDivisionError:
                insert_output(" Division by zero!\n")
            except:
                insert_output(" Invalid expression\n")
        elif user == "fullscreen":
            state = window.attributes('-fullscreen')
            window.attributes('-fullscreen', not state)
            if state:
                insert_output("Fullscreen: OFF\n")
                return
            else:
                insert_output("Fullscreen: ON\n")
                return

        elif user == "extra help":
            insert_output("This is a fallback version of the help command, without the full directories.")
            insert_output("commands: clear, exit, sysinfo, calc, date, theme < directory >")
            return

        elif user == "clearhistory":
            window.history = []
            window.history_index = -1
            insert_output("History cleared!\n")
            return

        elif user == "history":
            if hasattr(window, 'history') and window.history:
                for i, cmd in enumerate(window.history, 1):
                    insert_output(f"  {i}  {cmd}\n")
            else:
                insert_output("  History is empty.\n")
                return

        elif user.startswith("which "):
            cmd = user[6:].strip()
            if not cmd:
                insert_output("  Usage: which <command>\n")
                return
            else:
                try:
                    import shutil
                    path = shutil.which(cmd)
                    if path:
                        insert_output(f"  {path}\n")
                    else:
                        insert_output(f"  {cmd} not found\n")
                except Exception as e:
                    insert_output(f"  Error: {e}\n")
                    return

        elif user.startswith("sleep "):
            try:
                seconds = float(user[6:].strip())
                if seconds < 0:
                    insert_output("  Error: cannot sleep negative time\n", "error")
                    return
                elif seconds > 3600:
                    insert_output("  Error: maximum sleep time is 3600 seconds (1 hour)\n", "error")
                    return
                else:
                    insert_output(f"  Sleeping for {seconds} seconds...\n")
                    output.update()
                    import time
                    intervals = int(seconds * 10)
                    for i in range(intervals):
                        time.sleep(0.1)
                        if i % 10 == 0 and i > 0:
                            pass
                    
                    insert_output("  Done.\n")
                    return
            except ValueError:
                insert_output("  Error: invalid number. Usage: sleep <seconds>\n", "error")
                return

        elif user == "ultra":
            global ULTRA_MODE
            ULTRA_MODE = not ULTRA_MODE
            if ULTRA_MODE:
                insert_output("  Ultra mode: ON\n", "warning")
                insert_output("  You now have elevated privileges. Be careful!\n", "warning")
                return
            else:
                insert_output("  Ultra mode: OFF\n")
                insert_output("  Privileges restored to normal.\n")
                return

        if "&&" in user:
            commands = [cmd.strip() for cmd in user.split("&&") if cmd.strip()]
            
            if not commands:
                insert_output("  Error: empty command chain\n", "error")
                return
            
            insert_output(f"  Running {len(commands)} commands...\n")
            
            for i, cmd in enumerate(commands, 1):
                insert_output(f"  [{i}/{len(commands)}] {cmd}\n")

                try:
                    import subprocess
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate()
                    if stdout:
                        insert_output(stdout)
                    if stderr:
                        insert_output(stderr, "error")
                    if process.returncode != 0:
                        insert_output(f"  Command failed (exit code: {process.returncode})\n", "error")
                        break 
                except Exception as e:
                    insert_output(f"  Error: {e}\n", "error")
                    break
            
            return

        elif user == "pwd":
            insert_output(os.getcwd() + "\n")
            return

                # Дальше идут команды файловые

        elif user == "ls":
            try:
                files = os.listdir(".")
                insert_output(" Files:\n")
                for f in files:
                    insert_output(f"  {f}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
                return
        elif user == "ip":
            try:
                import socket
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                insert_output(f" Hostname: {hostname}\n")
                insert_output(f" IP Address: {ip}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
                return
        elif user.startswith("cat "):
            name = user[4:].strip()
            try:
                with open(name, "r") as f:
                    content = f.read()
                    insert_output(content + "\n")
            except FileNotFoundError:
                insert_output(f" File not found: {name}\n")
                return
            except Exception as e:
                insert_output(f" Error: {e}\n")
                return
        elif user == "cd":
            insert_output(os.getcwd() + "\n")
            return

        elif user.startswith("rmdir "):
            name = user[6:].strip()
            current_dir = os.getcwd()
            target = os.path.abspath(name)
            
            insert_output(f" Debug: Current dir: {current_dir}\n")
            insert_output(f" Debug: Target: {target}\n")
            insert_output(f" Debug: Exists: {os.path.exists(target)}\n")
            insert_output(f" Debug: Is dir: {os.path.isdir(target)}\n")
            
            if not os.path.exists(target):
                insert_output(f" Directory not found: {name}\n")
                return
            
            if not os.path.isdir(target):
                insert_output(f" Not a directory: {name}\n")
                return
            try:
                contents = os.listdir(target)
                if contents:
                    insert_output(f" Directory not empty: {name} (contains {len(contents)} items)\n")
                    return
            except Exception as e:
                insert_output(f" Error checking directory: {e}\n")
                return
            
            try:
                os.rmdir(target)
                insert_output(f" Removed directory: {name}\n")
            except OSError as e:
                insert_output(f" Error: {e}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
            return

        elif user.startswith("rmrf "):
            if not ULTRA_MODE:
                insert_output("  Error: Permission denied. Use 'ultra on' to enable\n", "error")
                return
            
            name = user[5:].strip()
            import shutil
            try:
                shutil.rmtree(name)
                insert_output(f"  Removed: {name}\n")
            except FileNotFoundError:
                insert_output(f"  Not found: {name}\n", "error")
                return
            except Exception as e:
                insert_output(f"  Error: {e}\n", "error")
                return

        elif user.startswith("cd "):
            path = user[3:].strip()
            if path == "":
                insert_output(" Usage: cd <path>\n")
                return
            else:
                try:
                    os.chdir(path)
                    insert_output(f" Changed to: {os.getcwd()}\n")
                except FileNotFoundError:
                    insert_output(f" Folder not found: {path}\n")
                except Exception as e:
                    insert_output(f" Error: {e}\n")
                    return

        elif user == 'pslist':
            import psutil
            insert_output(f"{'PID':<8}{'Process Name':<25}{'Memory %':<10}\n")
            insert_output("-" * 45 + "\n")
            processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), 
                            key=lambda p: p.info['memory_percent'], reverse=True)[:30]
            for p in processes:
                try:
                    pid = p.info['pid']
                    name = p.info['name'][:23]
                    mem = f"{p.info['memory_percent']:.2f}%"
                    insert_output(f"{pid:<8}{name:<25}{mem:<10}\n")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return

        elif user.startswith('pkill '):
            if not ULTRA_MODE:
                insert_output("  Error: Permission denied. Use 'ultra on' to enable\n", "error")
                return
            
            import psutil
            pid_str = user[6:].strip()
            if pid_str.isdigit():
                pid = int(pid_str)
                try:
                    p = psutil.Process(pid)
                    p_name = p.name()
                    p.terminate()
                    insert_output(f"Process {pid} ({p_name}) has been terminated.\n")
                    return
                except psutil.NoSuchProcess:
                    insert_output(f"Error: PID {pid} not found.\n", "error")
                    return
                except psutil.AccessDenied:
                    insert_output(f"Error: Process {pid} is protected.\n", "error")
                    return
            else:
                insert_output("Error: Please specify a valid numeric PID (e.g., pkill 1234).\n", "error")
                return

        elif user.startswith('b64encode '): #эта команда на будущее, она работает, но другая команда, которая декодирует и вызывает ошибки, была удалена. Можете пользоваться, но декодирование будет в будущем обновлении. :)
            import base64
            text_str = user[10:]
            if text_str:
                try:
                    encoded = base64.b64encode(text_str.encode('utf-8')).decode('utf-8')
                    insert_output(f"Encoded: {encoded}\n")
                except Exception as e:
                    insert_output(f"Error: Could not encode text. {e}\n")
                    return
            else:
                insert_output("Error: Please specify text to encode (e.g., b64encode hello).\n")
                return

        elif user == 'whoami':
            import getpass
            insert_output(f"Current user: {getpass.getuser()}\n")
            return

        elif user == 'fcount':
            try:
                items = os.listdir('.')
                files = [f for f in items if os.path.isfile(f)]
                dirs = [d for d in items if os.path.isdir(d)]
                insert_output(f"Directory Stats:\n  Files: {len(files)}\n  Folders: {len(dirs)}\n")
            except Exception as e:
                insert_output(f"Error scanning directory: {e}\n")
                return

        elif user.startswith('fview '):
            filename = user[6:].strip()
            if os.path.exists(filename) and os.path.isfile(filename):
                try:
                    insert_output(f"--- Content of {filename} ---\n")
                    with open(filename, 'r', encoding='utf-8') as f:
                        for index, line in enumerate(f, 1):
                            insert_output(f"{index}: {line}")
                    insert_output("\n--- End of File ---\n")
                except Exception as e:
                    insert_output(f"Error reading file: {e}\n")
            else:
                insert_output(f"Error: File '{filename}' not found.\n")
                return

        elif user.startswith("mkdir "):
            name = user[6:].strip()
            try:
                os.mkdir(name)
                insert_output(f" Created: {name}\n")
                return
            except Exception as e:
                insert_output(f" Error: {e}\n")
                return
        elif user.startswith("writefile "):
            parts = user[10:].split(" ", 1)
            if len(parts) < 2:
                insert_output(" Usage: writefile <filename> <text>\n")
            else:
                filename = parts[0]
                text = parts[1]
                try:
                    with open(filename, "w") as f:
                        f.write(text)
                    insert_output(f" Written to {filename}\n")
                except Exception as e:
                    insert_output(f" Error: {e}\n")
                    return

        elif user == "uptime":
            diff = datetime.now() - START_TIME
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            seconds = diff.seconds % 60
            
            if days > 0:
                insert_output(f" Uptime: {days}d {hours}h {minutes}m {seconds}s\n")
            elif hours > 0:
                insert_output(f" Uptime: {hours}h {minutes}m {seconds}s\n")
            elif minutes > 0:
                insert_output(f" Uptime: {minutes}m {seconds}s\n")
            else:
                insert_output(f" Uptime: {seconds}s\n")
                return
        elif user == "systime":
            try:
                import psutil
                boot_time = psutil.boot_time()
                boot_datetime = datetime.fromtimestamp(boot_time)
                now = datetime.now()
                diff = now - boot_datetime
                
                days = diff.days
                hours = diff.seconds // 3600
                minutes = (diff.seconds % 3600) // 60
                seconds = diff.seconds % 60
                
                if days > 0:
                    insert_output(f" System uptime: {days}d {hours}h {minutes}m {seconds}s\n")
                    insert_output(f" Started: {boot_datetime.strftime('%d %B %Y %H:%M:%S')}\n")
                elif hours > 0:
                    insert_output(f" System uptime: {hours}h {minutes}m {seconds}s\n")
                    insert_output(f" Started: {boot_datetime.strftime('%H:%M:%S')}\n")
                elif minutes > 0:
                    insert_output(f" System uptime: {minutes}m {seconds}s\n")
                else:
                    insert_output(f" System uptime: {seconds}s\n")
            except Exception as e:
                insert_output(f" Error getting uptime: {e}\n")
                return

        elif user.startswith("touch "):
            name = user[6:].strip()
            try:
                with open(name, "w") as f:
                    pass
                insert_output(f" Created: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
                return
        elif user == "disk":
            import shutil
            disk = shutil.disk_usage("/")
            total = disk.total // (1024**3)
            used = disk.used // (1024**3)
            free = disk.free // (1024**3)
            insert_output(f"Disk: {used}GB / {total}GB (free: {free}GB)\n")
            return
        elif user == "cpu":
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cores = psutil.cpu_count()
            insert_output(f"CPU: {cpu_percent}% ({cores} cores)\n")
            return
        elif user == "memory":
            import psutil
            mem = psutil.virtual_memory()
            total = mem.total // (1024**3)
            used = mem.used // (1024**3)
            free = mem.free // (1024**3)
            percent = mem.percent
            insert_output(f"RAM: {used}GB / {total}GB ({percent}% used)\n")
            return
                                                                                                #     ВНИЗУ КОМАНДА CLEAR
        elif user == "clear":
            output.configure(state="normal")
            output.delete(1.0, ctk.END)
            output.configure(state="disabled")
            insert_output("Lemon Terminal v1.5s2b\n")
            insert_output("Type 'help' for categories of commands.\n")  
            insert_output("|To type, click on the input bar.\n\n", "gray_hint")
            #insert_output(show_user(), "green")
            return
        elif user.startswith("echo "):
            text = user[5:]
            insert_output(text + "\n")
            return
        elif user == "sysinfo":
            import platform
            info = f"""
            System: {platform.system()}
            Node: {platform.node()}
            Release: {platform.release()}
            Version: {platform.version()}
            Machine: {platform.machine()}
            Processor: {platform.processor()}
"""
            insert_output(info)
            return
        elif user.startswith("font size "): #ПРОШУ, не ставьте огромные значения ( 30+) в полном экарне, или маленьком окошке, у вас просто пропадёт синяя строка.( эта ошибка возможна только на старой версии)
            try:
                size = int(user[10:])
                if size < 8:
                    size = 8
                elif size > 50:
                    size = 50
                output.configure(font=("monospace", size))
                entry.configure(font=("monospace", size))
                insert_output(f"Font size set to: {size}\n")
            except:
                insert_output("Usage: font size <number> (8-50)\n")
        elif user.startswith("help "):
            category = user[5:].strip().lower()
            if category in help_users:
                data = help_users[category]
                insert_output(f" {category.upper()} - {data['desc']}:\n")
                insert_output("─" * 40 + "\n")
                for cmd in data['commands']:
                    insert_output(f"  {cmd}\n")
                insert_output("─" * 40 + "\n")
            else:
                insert_output(f" Category '{category}' not found.\n")
                insert_output("Available: system, files, themes, tools, terminal\n")
                return
    
        elif user == "exit":
            window.destroy()
            return
        elif user == "lemon": #Пасхалочка
            insert_output("Lemon Terminal was created by Mihail. :]\n")
            return
        elif user == "random 3":
            insert_output(str(random.randint(1, 3)) + "\n")
            return
        elif user == "random 10":
            insert_output(str(random.randint(1, 10)) + "\n")
            return
        elif user == "random 100":
            insert_output(str(random.randint(1, 100)) + "\n")
            return
        elif user == "theme night":
            rgb_active = False
            window.configure(fg_color="black")
            output.configure(fg_color="black", text_color="white")
            entry.configure(fg_color="white", text_color="black", border_color="white")
            insert_output("Theme set to: NIGHT\n")
            return
        elif user == "theme light":
            rgb_active = False
            window.configure(fg_color="white")
            output.configure(fg_color="white", text_color="black")
            entry.configure(fg_color="black", text_color="white", border_color="black")
            insert_output("Theme set to: LIGHT\n")
            return
        elif user == "theme normal":
            rgb_active = False
            window.configure(fg_color="#1a1a1a")  
            output.configure(fg_color="#1a1a1a", text_color="white")  
            entry.configure(
                fg_color="#FFE600",     
                text_color="black",     
                border_color="#FFE600"  
            )
            insert_output("Theme set to: NORMAL\n")
        else:
            insert_output("ERROR: such a command does not exist!\n", "error")

        #insert_output(show_user(), "green")

    def focus_entry(event):
        entry.focus()
    output.bind("<Button-1>", focus_entry)
    window.history = []
    window.history_index = -1

    def history_up(event):

        if not window.history:
            return "break"
            
        if window.history_index == -1:
            window.history_index = len(window.history) - 1
        elif window.history_index > 0:
            window.history_index -= 1
            
        entry.delete(0, "end")
        entry.insert(0, window.history[window.history_index])
        return "break"

    def history_down(event): #P.S желательно не менять код команды истории, иначе она вообще может перестать работать.
        if window.history_index == -1:
            return "break"
            
        if window.history_index < len(window.history) - 1:
            window.history_index += 1
            entry.delete(0, "end")
            entry.insert(0, window.history[window.history_index])
        else:
            window.history_index = -1
            entry.delete(0, "end")
        return "break"
    entry.bind("<Up>", history_up)
    entry.bind("<Down>", history_down)
    entry.focus()
    
    window.mainloop()

if __name__ == "__main__":
    start_gui()

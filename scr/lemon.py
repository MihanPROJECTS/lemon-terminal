import os
import random
from datetime import datetime
import platform
import psutil
import time
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")                     

def get_prompt():
    return "&\\"


font_index = -1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTOS_DIR = os.path.join(BASE_DIR, "fontos")
note_mode = False
note_content = ""
custom_image_path = ""
help_data = {
    "system": {
        "desc": "System commands",
        "commands": ["sysinfo", "memory", "cpu", "disk", "ip"]
    },
    "files": {
        "desc": "File management",
        "commands": ["ls", "cd", "mkdir", "rmdir", "touch", "rmrf", "cat", "echo", "writefile"]
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
        "commands": ["ver", "help", "clear", "exit"]
    }
}

def run_gui():
    window = ctk.CTk()
    window.title("Lemon Terminal")
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

    
    output.tag_config("green", foreground="#73d65a")
    output.tag_config("gray_hint", foreground="#757575")


    def insert_output(text, tag=None):
        output.configure(state="normal")
        if tag:
            output.insert("end", text, tag) 
        else:
            output.insert("end", text)
        output.configure(state="disabled")
        output.see("end")
    insert_output("Lemon Terminal v1.3 beta\n")
    insert_output("Type 'help' for a categories of commands.\n")
    insert_output("|To type, click on the blue bar.\n\n", "gray_hint")
    insert_output(get_prompt(), "green")

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

    def update_rgb():
        nonlocal rgb_index
        if rgb_active:
            entry.configure(fg_color=rgb_colors[rgb_index], text_color="black")
            rgb_index = (rgb_index + 1) % len(rgb_colors)
            window.after(300, update_rgb)


    entry.bind("<Return>", lambda event: handle_command(event))

    def handle_command(event):
        nonlocal rgb_active
        command = entry.get().strip().lower()
        entry.delete(0, "end")
        if not command:
            return

        insert_output(command + "\n")

        if command == "help":
            # Категории хэлп
            insert_output(" HELP - Available categories:\n")
            insert_output("─" * 40 + "\n")
            for key, value in help_data.items():
                insert_output(f"  {key}  - {value['desc']}\n")
            insert_output("─" * 40 + "\n")
            insert_output("Type 'help <category>' for detailed commands\n")
            insert_output("  Example: help system\n")                           
        elif command == "ver":
            ver_text = """
                                                            
     __                         _____               _         _ 
    |  |   ___ _____ ___ ___   |_   _|___ ___ _____|_|___ ___| |
    |  |__| -_|     | . |   |    | | | -_|  _|     | |   | .'| |
    |_____|___|_|_|_|___|_|_|    |_| |___|_| |_|_|_|_|_|_|__,|_|
        
    - made by M1hail
    - 20+ commands
    - theme support
    - run scripts
    - write 'help'
                                                            
"""
            insert_output(ver_text)

        elif command.startswith("run "):
            cmd = command[4:].strip()
            try:
                import subprocess
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                if stdout:
                    insert_output(stdout)
                if stderr:
                    insert_output("⚠️ " + stderr)
                if process.returncode != 0:
                    insert_output(f" Command failed (exit code: {process.returncode})\n")
                else:
                    insert_output(f" Command finished (exit code: {process.returncode})\n")
            except FileNotFoundError:
                insert_output(f" Command not found: {cmd}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command == "date":
            insert_output(datetime.now().strftime("%d %B %Y") + "\n")
        elif command == "theme":
            insert_output("AVAILABLE THEMES:\n")
            insert_output("─" * 40 + "\n")
            insert_output("  night      - Black background, white text\n")
            insert_output("  light      - White background, black text\n")
            insert_output("  normal     - Classic black + blue input\n")
            #insert_output("  rgbm       - Rainbow input bar\n") ргб мод слишком вырвиглазный, для серьезной программы
            insert_output("─" * 40 + "\n")
        elif command.startswith("calc "):
            expression = command[5:].strip()
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
        elif command == "fullscreen":
            state = window.attributes('-fullscreen')
            window.attributes('-fullscreen', not state)
            if state:
                insert_output("Fullscreen: OFF\n")
            else:
                insert_output("Fullscreen: ON\n")

        elif command == "extra help":
            insert_output("This is a fallback version of the help command, without the full directories.")
            insert_output("Commands: clear, exit, sysinfo, calc, date, theme < directory >")

                # Дальше идут команды файловые

        elif command == "ls":
            try:
                files = os.listdir(".")
                insert_output(" Files:\n")
                for f in files:
                    insert_output(f"  {f}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command == "ip":
            try:
                import socket
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                insert_output(f" Hostname: {hostname}\n")
                insert_output(f" IP Address: {ip}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command.startswith("cat "):
            name = command[4:].strip()
            try:
                with open(name, "r") as f:
                    content = f.read()
                    insert_output(content + "\n")
            except FileNotFoundError:
                insert_output(f" File not found: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command == "cd":
            insert_output(os.getcwd() + "\n")
        elif command.startswith("rmrf "):
            name = command[5:].strip()
            import shutil
            try:
                shutil.rmtree(name)
                insert_output(f" Removed: {name}\n")
            except FileNotFoundError:
                insert_output(f" Not found: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command.startswith("rmdir "):
            name = command[6:].strip()
            try:
                os.rmdir(name)
                insert_output(f" Directory deleted: {name}\n")
            except FileNotFoundError:
                insert_output(f" Folder not found: {name}\n")
            except OSError:
                insert_output(f" Folder not empty: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")

        elif command.startswith("cd "):
            path = command[3:].strip()
            if path == "":
                insert_output(" Usage: cd <path>\n")
            else:
                try:
                    os.chdir(path)
                    insert_output(f" Changed to: {os.getcwd()}\n")
                except FileNotFoundError:
                    insert_output(f" Folder not found: {path}\n")
                except Exception as e:
                    insert_output(f" Error: {e}\n")

        elif command.startswith("mkdir "):
            name = command[6:].strip()
            try:
                os.mkdir(name)
                insert_output(f" Created: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command.startswith("writefile "):
            parts = command[10:].split(" ", 1)
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

        elif command.startswith("touch "):
            name = command[6:].strip()
            try:
                with open(name, "w") as f:
                    pass
                insert_output(f" Created: {name}\n")
            except Exception as e:
                insert_output(f" Error: {e}\n")
        elif command == "disk":
            import shutil
            disk = shutil.disk_usage("/")
            total = disk.total // (1024**3)
            used = disk.used // (1024**3)
            free = disk.free // (1024**3)
            insert_output(f"Disk: {used}GB / {total}GB (free: {free}GB)\n")
        elif command == "cpu":
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cores = psutil.cpu_count()
            insert_output(f"CPU: {cpu_percent}% ({cores} cores)\n")
        elif command == "memory":
            import psutil
            mem = psutil.virtual_memory()
            total = mem.total // (1024**3)
            used = mem.used // (1024**3)
            free = mem.free // (1024**3)
            percent = mem.percent
            insert_output(f"RAM: {used}GB / {total}GB ({percent}% used)\n")
                                                                                                #     ВНИЗУ КОМАНДА CLEAR
        elif command == "clear":
            output.configure(state="normal")
            output.delete(1.0, ctk.END)
            output.configure(state="disabled")
            insert_output("Lemon Terminal v1.3 beta\n")
            insert_output("Type 'help' for a categories of commands.\n")  
            insert_output("|To type, click on the blue bar.\n\n", "gray_hint")
        elif command.startswith("echo "):
            text = command[5:]
            insert_output(text + "\n")
        elif command == "sysinfo":
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
        elif command.startswith("font size "): #ПРОШУ, не ставьте огромные значения ( 30+) в полном экарне, или маленьком окошке, у вас просто пропадёт синяя строка.( эта ошибка возможна только на старой версии)
            try:
                size = int(command[10:])
                if size < 8:
                    size = 8
                elif size > 50:
                    size = 50
                output.configure(font=("monospace", size))
                entry.configure(font=("monospace", size))
                insert_output(f"Font size set to: {size}\n")
            except:
                insert_output("Usage: font size <number> (8-50)\n")
        elif command.startswith("help "):
            category = command[5:].strip().lower()
            if category in help_data:
                data = help_data[category]
                insert_output(f" {category.upper()} - {data['desc']}:\n")
                insert_output("─" * 40 + "\n")
                for cmd in data['commands']:
                    insert_output(f"  {cmd}\n")
                insert_output("─" * 40 + "\n")
            else:
                insert_output(f" Category '{category}' not found.\n")
                insert_output("Available: system, files, themes, tools, terminal\n")
    
        elif command == "exit":
            window.destroy()
            return
        elif command == "lemon": #Пасхалочка
            insert_output("Lemon Terminal was created by Mihail. :]\n")
        elif command == "random 3":
            insert_output(str(random.randint(1, 3)) + "\n")
        elif command == "random 10":
            insert_output(str(random.randint(1, 10)) + "\n")
        elif command == "random 100":
            insert_output(str(random.randint(1, 100)) + "\n")
        elif command == "theme night":
            rgb_active = False
            window.configure(fg_color="black")
            output.configure(fg_color="black", text_color="white")
            entry.configure(fg_color="white", text_color="black", border_color="white")
            insert_output("Theme set to: NIGHT\n")
        elif command == "theme light":
            rgb_active = False
            window.configure(fg_color="white")
            output.configure(fg_color="white", text_color="black")
            entry.configure(fg_color="black", text_color="white", border_color="black")
            insert_output("Theme set to: LIGHT\n")
        elif command == "theme normal":
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
            insert_output("ERROR: such a command does not exist!\n")

        insert_output(get_prompt(), "green")

    def focus_entry(event):
        entry.focus()
    output.bind("<Button-1>", focus_entry)
    window.mainloop()

if __name__ == "__main__":
    run_gui()


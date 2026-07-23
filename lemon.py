import os
import random
from datetime import datetime
import platform
import tkinter as tk
import psutil
import time
#Hello developer. Привет разработчик. Оригинальный автор, M1hail.
font_index = -1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTOS_DIR = os.path.join(BASE_DIR, "fontos")
note_mode = False
note_content = ""
custom_image_path = ""
help_data = {
    "system": {
        "desc": "System commands",
        "commands": [
            "sysinfo", "memory", "cpu", "disk", "ip"
        
        ]
    },
    "files": {
        "desc": "File management (coming soon)",
        "commands": ["ls", "cd", "mkdir", "rmdir", "touch", "rmrf", "cat", "echo", "writefile"]
    },
    "themes": {
        "desc": "Themes and customization",
        "commands": [
            "theme <name>",
            "font size <number>", "fullscreen"
        ]
    },
    #"games": { Должны были быть игры, но это в будущем будет. Также я планирую добавить очень классную вещь в программу, но это пока секрет, или вы можете найти упомининия новой команды, если я недоконца зачистил код. Извиняюсь за ошибочную орфографию, если есть.
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
    window = tk.Tk()
    window.title("Lemon Terminal")
    window.geometry("800x500")
    window.configure(bg="black")
    window.minsize(400, 460)
    #window.resizable(False, False) Эта строка нужна была, чтобы запретить менять размер терминала, но это на первых днях создания проекта было нужно, уже - нет.

    def toggle_fullscreen(event=None):
        state = window.attributes('-fullscreen')
        window.attributes('-fullscreen', not state)

    window.bind("<F11>", toggle_fullscreen)

    output = tk.Text(window, bg="black", fg="white", font=("Courier", 12))
    output.pack(fill="both", expand=True, padx=5, pady=5)
    output.configure(state="disabled")

    def insert_output(text):
        output.configure(state="normal")
        output.insert(tk.END, text)
        output.configure(state="disabled")
        output.see(tk.END)

    insert_output("🍋 Lemon Terminal v1.0 Beta\n")
    insert_output("Type 'help' for a list of commands.\n")
    insert_output("To type, click on the blue bar.\n\n")
    insert_output("-> ")

    entry = tk.Entry(window, bg="#0000AA", fg="white", font=("Courier", 12))
    entry.pack(fill="x", padx=5, pady=(0, 5))

    placeholder = "Enter the command..."
    entry.insert(0, placeholder)
    entry.configure(fg="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(fg="white")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    entry.focus_set()

    rgb_active = False
    rgb_colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    rgb_index = 0

    def update_rgb():
        nonlocal rgb_index
        if rgb_active:
            entry.configure(bg=rgb_colors[rgb_index], fg="black")
            rgb_index = (rgb_index + 1) % len(rgb_colors)
            window.after(300, update_rgb)

    def handle_command(event):
        nonlocal rgb_active
        command = entry.get().strip().lower()
        entry.delete(0, tk.END)

        def handle_command(event):
            global custom_image_path
    
            command = entry.get().strip().lower()
    #За этим комментарием код для команд. Вы можете добавить новые команды, но в репозитории укажите свои команды, как новые!

        if not command or command == placeholder:
            return

        insert_output(command + "\n")


        #if command == "help":          Это старая версия команды хэлп, в ней банально много команд не поместилось бы.
         #   help_text = """
#? Available commands:
#terminal

  #help              NULL             rgbm
  #ver               NULL             calc
  #date              NULL             weather
  #clear             NULL             random 3
  #info              NULL             random 10
  #exit              NULL             random 100
  #theme             NULL             calc            
#"""
            #insert_output(help_text)

        if command == "help":
            # Категории хэлп
            insert_output("📚 HELP - Available categories:\n")
            insert_output("─" * 40 + "\n")
            for key, value in help_data.items():
                insert_output(f"  {key}  - {value['desc']}\n")
            insert_output("─" * 40 + "\n")
            insert_output("Type 'help <category>' for detailed commands\n")
            insert_output("  Example: help system\n")                           
    #    if " && " in command:
     #       commands = command.split(" && ")         
     #       for cmd in commands:
      #          cmd = cmd.strip()             У этой команды беды с выполнением. Лучше использовать run.
    #            insert_output(f"➜ {cmd}\n")
      #          try:
         #           import subprocess
             #       result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
           #         if result.stdout:
            #            insert_output(result.stdout)
           #         if result.stderr:
           #             insert_output("⚠️ " + result.stderr)
          #          if result.returncode != 0:
           #             insert_output(f"❌ Command failed: {cmd}\n")
           #             return
          #      except Exception as e:
           #         insert_output(f"❌ Error: {e}\n")
           #         return
           #insert_output("✅ All commands executed\n")
            #return

        elif command == "ver":
            ver_text = """
┌─────────────────────────────────────────────────────┐
│                                                     │
│                   Lemon Terminal                    │
│  Thanks for downlanding!                            │
│  Author:      m1hail                                │
│  License:     Open Source                           │
│  Language:    Python 3 + tkinter                    │
│                                                     │
│  ─── Features ───                                   │
│  • Custom GUI terminal                              │
│  • BIOS-style interface                             │
│  • 20+ built-in commands                            │
│  • ASCII art support                                │
│  • Many themes                                      │
│                                                     │
│  ─── Commands ───                                   │
│  Type 'help' for a categories                       │
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
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
                    insert_output(f"❌ Command failed (exit code: {process.returncode})\n")
                else:
                    insert_output(f"✅ Command finished (exit code: {process.returncode})\n")
            except FileNotFoundError:
                insert_output(f"❌ Command not found: {cmd}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command == "date":
            insert_output(datetime.now().strftime("%d %B %Y") + "\n")
        elif command == "theme":
            insert_output("AVAILABLE THEMES:\n")
            insert_output("─" * 40 + "\n")
            insert_output("  night      - Black background, white text\n")
            insert_output("  light      - White background, black text\n")
            insert_output("  classic    - Classic black + blue input\n")
            insert_output("  lemon      - Yellow accents (lemon style)\n")
            insert_output("  forest     - Green theme")
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
                # Дальше идут команды файловые

        elif command == "ls":
            try:
                files = os.listdir(".")
                insert_output("📁 Files:\n")
                for f in files:
                    insert_output(f"  {f}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command == "ip":
            try:
                import socket
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                insert_output(f" Hostname: {hostname}\n")
                insert_output(f" IP Address: {ip}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command.startswith("cat "):
            name = command[4:].strip()
            try:
                with open(name, "r") as f:
                    content = f.read()
                    insert_output(content + "\n")
            except FileNotFoundError:
                insert_output(f"❌ File not found: {name}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command == "cd":
            insert_output(os.getcwd() + "\n")
        elif command.startswith("rmrf "):
            name = command[5:].strip()
            import shutil
            try:
                shutil.rmtree(name)
                insert_output(f"🗑 Removed: {name}\n")
            except FileNotFoundError:
                insert_output(f"❌ Not found: {name}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command.startswith("rmdir "):
            name = command[6:].strip()
            try:
                os.rmdir(name)
                insert_output(f"🗑 Directory deleted: {name}\n")
            except FileNotFoundError:
                insert_output(f"❌ Folder not found: {name}\n")
            except OSError:
                insert_output(f"❌ Folder not empty: {name}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")

        elif command.startswith("cd "):
            path = command[3:].strip()
            if path == "":
                insert_output("❌ Usage: cd <path>\n")
            else:
                try:
                    os.chdir(path)
                    insert_output(f" Changed to: {os.getcwd()}\n")
                except FileNotFoundError:
                    insert_output(f"❌ Folder not found: {path}\n")
                except Exception as e:
                    insert_output(f"❌ Error: {e}\n")

        elif command.startswith("mkdir "):
            name = command[6:].strip()
            try:
                os.mkdir(name)
                insert_output(f" Created: {name}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
        elif command.startswith("writefile "):
            parts = command[10:].split(" ", 1)
            if len(parts) < 2:
                insert_output("❌ Usage: writefile <filename> <text>\n")
            else:
                filename = parts[0]
                text = parts[1]
                try:
                    with open(filename, "w") as f:
                        f.write(text)
                    insert_output(f" Written to {filename}\n")
                except Exception as e:
                    insert_output(f"❌ Error: {e}\n")

        elif command.startswith("touch "):
            name = command[6:].strip()
            try:
                with open(name, "w") as f:
                    pass
                insert_output(f" Created: {name}\n")
            except Exception as e:
                insert_output(f"❌ Error: {e}\n")
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
        elif command == "clear":
            output.configure(state="normal")
            output.delete(1.0, tk.END)
            output.configure(state="disabled")
            insert_output("🍋 Lemon Terminal v1.0\n")
            insert_output("Type 'help' for a categories of commands.\n")
            insert_output("To type, click on the blue bar.\n\n")
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
        elif command.startswith("font size "): #ПРОШУ, не ставьте огромные значения ( 30+) в полном экарне, или маленьком окошке, у вас просто пропадёт синяя строка.
            try:
                size = int(command[10:])
                if size < 8:
                    size = 8
                elif size > 50:
                    size = 50
                output.configure(font=("Courier", size))
                entry.configure(font=("Courier", size))
                insert_output(f"Font size set to: {size}\n")
            except:
                insert_output("Usage: font size <number> (8-50)\n")
        elif command.startswith("help "):
            category = command[5:].strip().lower()
    
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
        elif command.startswith("launch"):
            parts = command.split()
            if len(parts) < 1:
                insert_output("usage: launch <app>\n")
            else:
                app = parts[1]
                os.system(app + " &")
                insert_output("launching " + app + "...\n")
        #ВНИМАНИЕ Команда launch недоработана, иногда команда может крашнуть ОС, я не убираю её, ведь она работает, но почему иногда вылетает, мне неведомо. ПОЛЬЗУЙТЕСЬ НА СВОЙ СТРАХ И РИСК!
        #elif command == "theme old":
        #    rgb_active = False                        #ДАННАЯ ТЕМА ПЛОХО ОТОБРАЖАЕТСЯ
        #    window.configure(bg="#C0C0C0")
        #    output.configure(bg="#C0C0C0", fg="#000000")
        #    entry.configure(bg="#000000", fg="#000000")
        #    insert_output("Old theme activated!\n")
        elif command == "theme forest": #Мне показалось забавным, иметь в терминале визуальные темы :)
            rgb_active = False
            window.configure(bg="#1A2F1A")
            output.configure(bg="#1A2F1A", fg="#A8D5A2")
            entry.configure(bg="#2E4F2E", fg="#A8D5A2")
            insert_output("Theme set to: FOREST\n")
        elif command == "theme night":
            rgb_active = False
            window.configure(bg="black")
            output.configure(bg="black", fg="white")
            entry.configure(bg="white", fg="black")
            insert_output("Theme set to: NIGHT\n")
        elif command == "theme light":
            rgb_active = False
            window.configure(bg="white")
            output.configure(bg="white", fg="black")
            entry.configure(bg="black", fg="white")
            insert_output("Theme set to: LIGHT\n")
        elif command == "theme classic":
            rgb_active = False
            window.configure(bg="black")
            output.configure(bg="black", fg="white")
            entry.configure(bg="#0000AA", fg="white")
            insert_output("Theme set to: CLASSIC\n")
        elif command == "theme lemon":
            rgb_active = False
            window.configure(bg="black")
            output.configure(bg="black", fg="#F7DC6F")        # лимончики
            entry.configure(bg="#F7DC6F", fg="black")        # лимонный ввод
            insert_output("Theme set to: LEMON\n")
        #elif command == "rgbm":                        Это РГБ мод, где вся строка переливается цветами.
        #    if rgb_active:
        #        
        #        rgb_active = False
        #        window.configure(bg="black")
        #        output.configure(bg="black", fg="white")
        #        entry.configure(bg="#0000AA", fg="white")
        #        insert_output("RGB MODE DEACTIVATED!\n")
        #    else:
        #        
        #        rgb_active = True
        #        window.configure(bg="black")
        #        output.configure(bg="black", fg="white")
        #        update_rgb()
        #        insert_output("RGB MODE ACTIVATED!\n")
        else:
            insert_output("ERROR: such a command does not exist!\n")

        insert_output("-> ")

    entry.bind("<Return>", handle_command)

    def focus_entry(event):
        entry.focus_set()

    output.bind("<Button-1>", focus_entry)

    window.mainloop()

if __name__ == "__main__":
    run_gui()

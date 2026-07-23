
<img width="192" height="192" alt="LemonTerminaljpg" src="https://github.com/user-attachments/assets/ece1d172-4ebb-4732-b428-e3970d13a730" />

# lemon-terminal / Лимон Терминал
Lemon Terminal is a simple, straightforward terminal designed for those just starting to learn the command line. When I first started using a computer, I didn't understand how CMD and terminals worked. This project is my attempt to make the learning process easier and more engaging.

🌐 **Разные языки / Other Languages:** [English](README.md) • [Русский](README.ru.md)


![Static Badge](https://img.shields.io/badge/Language-Python%203-yellow)
   ![Static Badge](https://img.shields.io/badge/Status-Beta%20Testing-orange)   ![Static Badge](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue)   ![Static Badge](https://img.shields.io/badge/License-MIT-green)



![Lemon Terminal Demo](demo.gif)





---

##  Download

- **Windows** — `LemonTerminal.exe` 	*Unstable version*
- **Linux** — `LemonTerminal`

---


### ⚠️ This is a beta version for testing!

The program is under active development, so your Linux system may display an "Unknown file type" warning. This is normal for beta testing.

**To launch the terminal:**
1. Right-click the file -> *Properties* -> *Permissions*.
2. Check the box *"Allow executing file as program"*.


---

##  Launch

Open the file. Type `help` for a list of commands.

---


##  Available Commands

You can use the following built-in commands to manage your system, files, and terminal appearance.

###  SYSTEM
* **`sysinfo`** — Show detailed hardware characteristics of the PC.
* **`memory`** — Display current RAM status.
* **`cpu`** — Show processor model and current CPU load.
* **`disk`** — Check available disk storage space.
* **`ip`** — Display the current IP address of your device.

---

###  FILES
* **`ls`** — List all files and folders in the current directory.
* **`cd`** — Navigate to a different folder.
* **`mkdir`** — Create a new folder.
* **`rmdir`** — Delete an empty folder.
* **`touch`** — Create an empty file.
* **`cat`** — Read and display the contents of a text file.
* **`echo`** — Print the entered text on the screen.
* **`writefile`** — Write text directly into a file.

>  **WARNING! DANGEROUS COMMAND!**
> * **`rm`** / **`-rf`** — Permanent and forced deletion of files or folders along with all their contents. Use with extreme caution; deleted data cannot be recovered!

---

###  THEMES
* **`fullscreen`** — Toggle full-screen mode for the terminal window.
* **`font size`** — Change the interface font size.
* **`theme <classic>`** — Enable the standard black-and-blue theme.
* **`theme <lemon>`** — Enable the lemon-yellow theme.
* **`theme <forest>`** — Enable the green forest theme.
* **`theme <night>`** — Enable the dark night theme.
* **`theme <light>`** — Enable the clean light theme.

---

###  TOOLS
* **`date`** — Display the current date.
* **`calc`** — Launch the built-in math calculator.
* **`random 3`** — Generate a random number from 1 to 3.
* **`random 10`** — Generate a random number from 1 to 10.
* **`random 100`** — Generate a random number from 1 to 100.

---

###  TERMINAL
* **`ver`** — Show the current version of Lemon Terminal.
* **`clear`** — Wipe the console screen completely.
* **`exit`** — Close the application and exit the terminal.
* **`help`** — Display the general list of all available command categories.
* **`help <directory>`** — Show help documentation for a specific category (e.g., `help files`).


---

##  For Developers

```bash
python3 lemon.py
```

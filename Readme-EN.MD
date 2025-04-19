# ADBuster

**ADBuster** is an interactive tool written in Python that facilitates advanced control and management of Android devices via ADB (Android Debug Bridge). Designed with a menu-style CLI interface, this utility is intended for both technical users and Android enthusiasts looking to automate common tasks and perform complex operations on devices connected via USB or Wi-Fi.

"Added ADB Sideload support"

## ✨ Main Features

- 🖥 **Interactive Menu Interface**: Intuitive terminal navigation, with bilingual support (Spanish/English).
- 🔌 **Flexible Connection**: Compatible with devices connected via USB or IP over Wi-Fi.
- 🛠 **Full ADB Management**: Start/stop ADB server, list devices, run custom commands.
- 🚀 **Custom Reboots**: Reboot the device in normal, recovery, fastboot, or EDL mode.
- 📲 **APK Installation**: Graphical file selection for APKs and direct installation to the device.
- 📡 **USB to Wi-Fi Bypass**: Automatic switch from USB mode to ADB over Wi-Fi.
- 🔍 **Device Information**: Query manufacturer, model, and Android version.
- 🗂 **Integrated File Explorer**: `curses`-based interface for exploring remote device files (if module is present).
- 🎮 **scrcpy Integration**: Mirror and control the Android device screen from desktop (requires scrcpy.exe).
- 📦 **Installed Apps Listing**: View all user-installed packages.
- 🧠 **Modular Extensibility**: Supports external scripts like `adb_file_explorer.py` or `terminal.py`.
- 🌐 **English-Spanish Support**.

![Screenshot 2025-04-19 154056](https://github.com/user-attachments/assets/e1d01d14-758b-4f97-9e78-45dec42e0cd2)

![Screenshot 2025-04-19 154146](https://github.com/user-attachments/assets/ec6ecdbd-f2f3-450b-9128-f2a4c8993b44)

## 📦 Requirements

- ADB Installed
- Python 3.8+
- `pure-python-adb`
- `scrcpy` (placed in `./scrcpy/` for Windows or Linux) **VERY IMPORTANT**
- OS with console support (`cmd`, `bash`, etc.)
- Android device with USB debugging enabled

Install dependencies:
```bash
pip install pure-python-adb
```

On Windows:
```bash
pip install windows-curses
```

## 🚀 Usage

Run the main script from your terminal:

```bash
python ADBuster.py
```

![Screenshot 2025-04-19 154438](https://github.com/user-attachments/assets/cc8ef3d5-3b0c-4394-bf94-66d9648cd360)

Select your language and navigate through the various menu options to interact with connected devices.

## 📁 Recommended Structure

```
ADBuster/
│
├── ADBuster.py
├── scripts/
│   ├── adb_file_explorer.py  (optional)
│   └── terminal.py           (optional)
├── scrcpy/
│   └── scrcpy.exe            (Windows) or `scrcpy` (Linux)
```

## 🧠 Additional Notes

- Some features like the file explorer or terminal require auxiliary modules.
- For Wi-Fi connection, ensure the device is on the same network as the host and ADB TCP/IP mode is enabled.

## 📜 License

This project is open-source under the GPLv2 license. Feel free to modify, adapt, or distribute it under the same terms.
Thanks to Genymobile for releasing and maintaining scrcpy.

```
GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The licenses for most software are designed to take away your
freedom to share and change it. By contrast, the GNU General Public
License is intended to guarantee your freedom to share and change free
software--to make sure the software is free for all its users. This
General Public License applies to most of the Free Software
Foundation's software and to any other program whose authors commit to
using it. (Some other Free Software Foundation software is covered by
the GNU Library General Public License instead.) You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price. Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
this service if you wish), that you receive source code or can get it
if you want it, that you can change the software or use pieces of it
in new free programs; and that you know you can do these things.

  To protect your rights, we need to make restrictions that forbid
anyone to deny you these rights or to ask you to surrender the rights.
These restrictions translate to certain responsibilities for you if you
distribute copies of the software, or if you modify it.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must give the recipients all the rights that
you have. You must make sure that they, too, receive or can get the
source code. And you must show them these terms so they know their
rights.

  We protect your rights with two steps: (1) copyright the software, and
(2) offer you this license which gives you legal permission to copy,
distribute and/or modify the software.

  Also, for each author's protection and ours, we want to make certain
that everyone understands that there is no warranty for this free
software. If the software is modified by someone else and passed on, we
want its recipients to know that what they have is not the original, so
that any problems introduced by others will not reflect on the original
authors' reputations.

  Finally, any free program is threatened constantly by software
patents. We wish to avoid the danger that redistributors of a free
program will individually obtain patent licenses, in effect making the
program proprietary. To prevent this, we have made it clear that any
patent must be licensed for everyone's free use or not licensed at all.

  The precise terms and conditions for copying, distribution and
modification follow.
```

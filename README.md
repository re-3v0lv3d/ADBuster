# ADBuster

For Readme in English: https://github.com/re-3v0lv3d/ADBuster/blob/main/Readme-EN.MD



**ADBuster** es una herramienta interactiva escrita en Python que facilita el control y gestión avanzada de dispositivos Android mediante ADB (Android Debug Bridge). Diseñada con una interfaz CLI estilo menú, esta utilidad está pensada tanto para usuarios técnicos como para entusiastas de Android que desean automatizar tareas comunes y realizar operaciones complejas sobre dispositivos conectados por USB o Wi-Fi.


![Captura de pantalla 2025-04-19 194648](https://github.com/user-attachments/assets/705e8666-0ee7-45e8-aa85-8b1c19e884f6)



## ✨ Características principales

- 🖥 **Interfaz de Menú Interactiva**: Navegación intuitiva desde la terminal, con soporte bilingüe (Español/Inglés).
- 🔌 **Conexión Flexible**: Compatible con dispositivos conectados por USB o mediante IP a través de Wi-Fi.
- 🛠 **Gestión Completa del ADB**: Iniciar/detener servidor ADB, listar dispositivos, ejecutar comandos personalizados.
- 🚀 **Reinicios Personalizados**: Reinicio del dispositivo en modo normal, recovery, fastboot o EDL.
- 📲 **Instalación de APKs**: Selección gráfica del archivo APK desde el explorador del sistema y su instalación directa en el dispositivo.
- 📡 **Bypass de USB a Wi-Fi**: Transición automática del modo USB al modo ADB over Wi-Fi.
- 🔍 **Información del Dispositivo**: Consulta de fabricante, modelo y versión de Android.
- 🗂 **Explorador de Archivos Integrado**: Interfaz basada en `curses` para explorar archivos remotos del dispositivo (si el módulo está presente).
- 🎮 **scrcpy Integrado**: Refleja y controla la pantalla del dispositivo Android desde el escritorio (requiere scrcpy.exe).
- 📦 **Listado de Aplicaciones Instaladas**: Visualización de todos los paquetes de usuario instalados.
- 🧠 **Extensibilidad Modular**: Soporte para scripts externos como `adb_file_explorer.py` o `terminal.py`.
-      Soporte Inglés-Español.

"Añadido soporte Adb sideload ;)"



![Captura de pantalla 2025-04-19 195154](https://github.com/user-attachments/assets/428b0d3e-df36-4c35-9d51-f46651154605)



![Captura de pantalla 2025-04-19 154056](https://github.com/user-attachments/assets/e1d01d14-758b-4f97-9e78-45dec42e0cd2)



![Captura de pantalla 2025-04-19 154146](https://github.com/user-attachments/assets/ec6ecdbd-f2f3-450b-9128-f2a4c8993b44)




## 📦 Requisitos

- ADB Instalado
- Python 3.8+
- `pure-python-adb`
- `scrcpy` (colocado en `./scrcpy/` para Windows o Linux) MUY IMPORTANTE
- Sistema operativo con soporte para consola (`cmd`, `bash`, etc.)
- Dispositivo Android con depuración USB activada

Instalación de dependencias:
```bash
pip install pure-python-adb
```

(Solo windows)

```bash
pip install windows-curses
```

## 🚀 Uso

Ejecuta el script principal desde tu terminal:

```bash
python ADBuster.py
```




![Captura de pantalla 2025-04-19 154438](https://github.com/user-attachments/assets/cc8ef3d5-3b0c-4394-bf94-66d9648cd360)


Selecciona el idioma, y navega por las distintas opciones del menú para interactuar con los dispositivos conectados.

## 📁 Estructura recomendada

```
ADBuster/
│
├── ADBuster.py
├── scripts/
│   ├── adb_file_explorer.py  (opcional)
│   └── terminal.py           (opcional)
├── scrcpy/
│   └── scrcpy.exe            (Windows) o `scrcpy` (Linux)
```

## 🧠 Notas adicionales

- Algunas funciones como el explorador de archivos o terminal requieren módulos auxiliares.
- Para conexión Wi-Fi, asegúrate de que el dispositivo esté en la misma red que el host y habilitado en modo TCP/IP ADB.

## 📜 Licencia

Este proyecto es de código abierto bajo la licencia MIT. Siéntete libre de modificarlo, adaptarlo o distribuirlo bajo tus propios términos.
Gracias a Genymobile por el lanzamiento y mantenimiento de Scrcpy


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
modification follow.```

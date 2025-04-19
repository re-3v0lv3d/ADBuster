import curses
import os
import re
import subprocess
from typing import List, Dict, Optional
from ppadb.client import Client as AdbClient
from tkinter import Tk, filedialog

# Ventanita de tkinter para seleccionar archivos. La escondo porque solo quiero el diálogo.
root = Tk()
root.withdraw()

# Diccionario con los textos en español e inglés. Me costó un poco organizarlo, pero así queda claro qué mensaje va dónde.
# Lo hice con formato para poder meter nombres de archivos o errores dinámicamente.
TEXTS = {
    "es": {
        "select_language": "Seleccione idioma / Select language:",
        "language_option_1": "1. Español",
        "language_option_2": "2. English",
        "select_language_prompt": "Seleccione 1 o 2 y Enter: ",
        "invalid_language": "¡Opción no válida! Presiona Enter para intentarlo otra vez.",
        "connected_devices": "Dispositivos conectados:",
        "select_device_prompt": "Elige un número y pulsa Enter: ",
        "enter_number": "Tienes que poner un número, ¡venga!",
        "no_device_selected": "No seleccionaste ningún dispositivo. Cerrando...",
        "connected_to": "¡Conectado al dispositivo: {serial}!",
        "browsing": "Explorando: {path}",
        "actions": "Acciones: [q] Salir, [u] Subir archivo, [n] Descargar, [r] Ir a ruta, [d] Eliminar, [Enter] Entrar/Volver",
        "go_to_path": "Escribe la ruta: {buffer}",
        "delete_confirm": "¿Seguro que quieres eliminar '{name}'? (s/n)",
        "uploading": "Subiendo '{name}'... ¡Espera un momento!",
        "upload_success": "¡'{name}' subido con éxito!",
        "upload_error": "Error al subir '{name}'. Algo salió mal :(",
        "cannot_download_dotdot": "No puedes descargar '..'... ¿qué intentas hacer? :P",
        "download_dir_not_allowed": "¡No se pueden descargar carpetas! Solo archivos.",
        "downloading": "Descargando '{name}'... ¡Ya casi!",
        "download_success": "¡'{name}' descargado correctamente!",
        "download_error": "Error al descargar: {error}",
        "download_cancelled": "Descarga cancelada. No seleccionaste dónde guardarlo.",
        "cannot_delete_dotdot": "No puedes eliminar '..' ¡Eso es trampa!",
        "delete_success": "¡'{name}' eliminado sin problemas!",
        "delete_error": "Error al eliminar: {error}. Puede que no tengas permisos.",
        "delete_cancelled": "Eliminación cancelada. Todo sigue en su sitio.",
    },
    "en": {
        "select_language": "Select language / Seleccione idioma:",
        "language_option_1": "1. Spanish",
        "language_option_2": "2. English",
        "select_language_prompt": "Pick 1 or 2 and hit Enter: ",
        "invalid_language": "Invalid choice! Hit Enter to try again.",
        "connected_devices": "Connected devices:",
        "select_device_prompt": "Choose a number and press Enter: ",
        "enter_number": "You gotta enter a number, come on!",
        "no_device_selected": "No device selected. Shutting down...",
        "connected_to": "Connected to device: {serial}!",
        "browsing": "Browsing: {path}",
        "actions": "Actions: [q] Quit, [u] Upload file, [n] Download, [r] Go to path, [d] Delete, [Enter] Enter/Back",
        "go_to_path": "Enter path: {buffer}",
        "delete_confirm": "Are you sure you want to delete '{name}'? (y/n)",
        "uploading": "Uploading '{name}'... Hang on a sec!",
        "upload_success": "'{name}' uploaded successfully!",
        "upload_error": "Error uploading '{name}'. Something went wrong :(",
        "cannot_download_dotdot": "You can't download '..'... What's that about? :P",
        "download_dir_not_allowed": "Can't download folders! Files only, please.",
        "downloading": "Downloading '{name}'... Almost there!",
        "download_success": "'{name}' downloaded successfully!",
        "download_error": "Error downloading: {error}",
        "download_cancelled": "Download cancelled. You didn't pick a save location.",
        "cannot_delete_dotdot": "You can't delete '..'! That's cheating!",
        "delete_success": "'{name}' deleted without a hitch!",
        "delete_error": "Error deleting: {error}. Maybe you don't have permission.",
        "delete_cancelled": "Deletion cancelled. Everything's still there.",
    }
}

def pick_language(screen):
    """Primera pantalla para elegir idioma. Quise hacerla sencilla, solo 1 o 2."""
    curses.curs_set(0)  # Oculta el cursor para que quede más limpio
    screen.clear()
    screen.addstr(0, 0, TEXTS["es"]["select_language"])
    screen.addstr(1, 0, TEXTS["es"]["language_option_1"])
    screen.addstr(2, 0, TEXTS["es"]["language_option_2"])
    screen.addstr(4, 0, TEXTS["es"]["select_language_prompt"])
    screen.refresh()

    choice = ""
    while True:
        key = screen.getch()
        if key in (ord('1'), ord('2')):
            choice = chr(key)
            screen.addstr(4, len(TEXTS["es"]["select_language_prompt"]), choice)
            screen.refresh()
        elif key in (curses.KEY_ENTER, 10):
            if choice == "1":
                return "es"
            elif choice == "2":
                return "en"
            else:
                screen.addstr(6, 0, TEXTS["es"]["invalid_language"])
                screen.refresh()
        elif key == 27:  # Si presionan Esc, español por defecto
            return "es"
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            choice = ""
            screen.move(4, len(TEXTS["es"]["select_language_prompt"]))
            screen.delch()
            screen.refresh()

def run_adb_command(device, command):
    """Ejecuta comandos ADB en el dispositivo. A veces falla si la conexión no es estable, pero lo manejo con try/except."""
    try:
        return device.shell(command).strip().splitlines()
    except Exception as e:
        return [f"Error: {e}"]

def list_files_and_folders(device, current_path):
    """Lista archivos y carpetas en el directorio actual. Tuve que ajustar el regex porque a veces el ls -l devuelve formatos raros."""
    items = []
    for line in run_adb_command(device, f"ls -l '{current_path}'"):
        parts = re.split(r'\s+', line.strip(), maxsplit=8)
        if len(parts) >= 9 and parts[-1] not in (".", ".."):
            items.append({"type": "DIR" if parts[0].startswith("d") else "FILE", "name": parts[-1]})
        elif len(parts) >= 8 and (line.startswith("-") or line.startswith("d")) and parts[-1] not in (".", ".."):
            items.append({"type": "DIR" if parts[0].startswith("d") else "FILE", "name": parts[-1]})
    return [{"type": "DIR", "name": ".."}] + items

def upload_file(device, local_path, remote_path, screen, max_y, language):
    """Sube un archivo al dispositivo con adb push. Puse un timeout porque una vez se quedó colgado con un archivo grande."""
    cmd = ["adb", "-s", device.serial, "push", local_path, remote_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        screen.addstr(max_y - 3, 0, TEXTS[language]["upload_success"].format(name=os.path.basename(local_path)))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        screen.addstr(max_y - 3, 0, TEXTS[language]["upload_error"].format(name=os.path.basename(local_path)))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return False

def download_file(device, remote_path, local_path, screen, max_y, language):
    """Descarga un archivo con adb pull. Igual que upload_file, con timeout para evitar problemas."""
    if not local_path:
        screen.addstr(max_y - 3, 0, TEXTS[language]["download_cancelled"])
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return False

    cmd = ["adb", "-s", device.serial, "pull", remote_path, local_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)
        screen.addstr(max_y - 3, 0, TEXTS[language]["download_success"].format(name=os.path.basename(remote_path)))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        screen.addstr(max_y - 3, 0, TEXTS[language]["download_error"].format(error=str(e)))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return False

def delete_item(device, current_path, item, screen, max_y, language):
    """Elimina un archivo o carpeta. Usé rm -r para carpetas porque rm solo no funciona. Ojo con los permisos!"""
    if item["name"] == "..":
        screen.addstr(max_y - 3, 0, TEXTS[language]["cannot_delete_dotdot"])
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return False

    # Escapo el nombre por si tiene caracteres raros
    item_name = item["name"].replace("'", "'\\''")
    full_path = os.path.join(current_path, item_name).replace("'", "'\\''")
    cmd = f"rm -r '{full_path}'" if item["type"] == "DIR" else f"rm '{full_path}'"

    try:
        result = run_adb_command(device, cmd)
        if any("Error" in line for line in result):
            screen.addstr(max_y - 3, 0, TEXTS[language]["delete_error"].format(error=result[0]))
            screen.clrtoeol()
            screen.refresh()
            screen.getch()
            return False
        screen.addstr(max_y - 3, 0, TEXTS[language]["delete_success"].format(name=item["name"]))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return True
    except Exception as e:
        screen.addstr(max_y - 3, 0, TEXTS[language]["delete_error"].format(error=str(e)))
        screen.clrtoeol()
        screen.refresh()
        screen.getch()
        return False

def file_explorer(screen, device, language):
    """La función principal. Aquí pasa toda la acción: navegar, subir, descargar, eliminar... Fue un lío hacer la interfaz!"""
    current_path = "/sdcard/"  # Empiezo en sdcard porque es lo más común
    items = []
    cursor_pos = 0
    top_item = 0
    max_y, max_x = screen.getmaxyx()
    entering_path = False
    path_buffer = ""
    deleting = False

    def refresh_items():
        nonlocal items
        items = list_files_and_folders(device, current_path)

    def draw_screen():
        screen.clear()
        screen.addstr(0, 0, TEXTS[language]["browsing"].format(path=current_path), curses.A_BOLD)
        for i in range(top_item, min(top_item + max_y - 4, len(items))):
            item = items[i]
            attr = curses.A_REVERSE if i == cursor_pos else curses.A_NORMAL
            screen.addstr(i - top_item + 2, 0, f"[{item['type']}] {item['name']}", attr)
        screen.addstr(max_y - 2, 0, TEXTS[language]["actions"], curses.A_DIM)
        if entering_path:
            screen.addstr(max_y - 1, 0, TEXTS[language]["go_to_path"].format(buffer=path_buffer), curses.A_NORMAL)
            screen.clrtoeol()
        elif deleting:
            screen.addstr(max_y - 1, 0, TEXTS[language]["delete_confirm"].format(name=items[cursor_pos]["name"]), curses.A_NORMAL)
            screen.clrtoeol()
        screen.refresh()

    refresh_items()
    draw_screen()

    while True:
        key = screen.getch()

        # Modo de escribir ruta
        if entering_path:
            if key in (curses.KEY_ENTER, 10):
                current_path = path_buffer.strip()
                refresh_items()
                cursor_pos = top_item = 0
                entering_path = False
                path_buffer = ""
            elif key == 27:
                entering_path = False
                path_buffer = ""
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                path_buffer = path_buffer[:-1]
            elif 32 <= key <= 126:
                path_buffer += chr(key)
            draw_screen()
            continue

        # Modo de confirmar eliminación
        if deleting:
            confirm_key = 'y' if language == "en" else 's'
            if key == ord(confirm_key):
                deleting = False
                if delete_item(device, current_path, items[cursor_pos], screen, max_y, language):
                    refresh_items()
                    cursor_pos = min(cursor_pos, len(items) - 1)
                    top_item = min(top_item, max(0, len(items) - (max_y - 4)))
            elif key in (ord('n'), 27):
                deleting = False
                screen.addstr(max_y - 3, 0, TEXTS[language]["delete_cancelled"])
                screen.clrtoeol()
                screen.refresh()
                screen.getch()
            draw_screen()
            continue

        # Navegación con flechas
        if key == curses.KEY_DOWN:
            cursor_pos = min(cursor_pos + 1, len(items) - 1)
            if cursor_pos >= top_item + max_y - 4:
                top_item += 1
        elif key == curses.KEY_UP:
            cursor_pos = max(cursor_pos - 1, 0)
            if cursor_pos < top_item:
                top_item -= 1
        # Entrar en carpeta o volver atrás
        elif key in (curses.KEY_ENTER, 10):
            selected = items[cursor_pos]
            if selected["name"] == "..":
                current_path = os.path.dirname(current_path.rstrip('/')) + '/'
                refresh_items()
                cursor_pos = top_item = 0
            elif selected["type"] == "DIR":
                current_path = os.path.join(current_path, selected["name"]) + '/'
                refresh_items()
                cursor_pos = top_item = 0
        # Subir archivo
        elif key == ord('u'):
            file_to_upload = filedialog.askopenfilename()
            if file_to_upload:
                screen.addstr(max_y - 3, 0, TEXTS[language]["uploading"].format(name=os.path.basename(file_to_upload)))
                screen.refresh()
                destination = os.path.join(current_path, os.path.basename(file_to_upload))
                upload_file(device, file_to_upload, destination, screen, max_y, language)
                refresh_items()
                top_item = 0
                cursor_pos = 0
        # Descargar archivo
        elif key == ord('n'):
            selected = items[cursor_pos]
            if selected["name"] == "..":
                screen.addstr(max_y - 3, 0, TEXTS[language]["cannot_download_dotdot"])
                screen.clrtoeol()
                screen.refresh()
                screen.getch()
            elif selected["type"] == "DIR":
                screen.addstr(max_y - 3, 0, TEXTS[language]["download_dir_not_allowed"])
                screen.clrtoeol()
                screen.refresh()
                screen.getch()
            else:
                source_path = os.path.join(current_path, selected["name"])
                save_path = filedialog.asksaveasfilename(initialfile=selected["name"], 
                                                        title="Save file as" if language == "en" else "Guardar archivo como")
                if save_path:
                    screen.addstr(max_y - 3, 0, TEXTS[language]["downloading"].format(name=selected["name"]))
                    screen.refresh()
                    download_file(device, source_path, save_path, screen, max_y, language)
        # Entrar en modo escribir ruta
        elif key == ord('r'):
            entering_path = True
            path_buffer = ""
        # Eliminar archivo o carpeta
        elif key == ord('d'):
            deleting = True
        # Salir
        elif key == ord('q'):
            break

        draw_screen()

def main(screen, device=None):
    """Punto de entrada. Aquí empieza todo. Si me pasan un dispositivo, lo uso; si no, cierro con un mensaje."""
    curses.curs_set(0)
    
    # Elegir idioma
    language = pick_language(screen)
    
    # Usar el dispositivo pasado como argumento, si existe
    if device:
        screen.clear()
        screen.addstr(0, 0, TEXTS[language]["connected_to"].format(serial=device.serial), curses.A_BOLD)
        screen.refresh()
        curses.napms(1000)  # Pausa para que se vea el mensaje
        file_explorer(screen, device, language)
    else:
        screen.clear()
        screen.addstr(0, 0, TEXTS[language]["no_device_selected"], curses.A_BOLD)
        screen.refresh()
        curses.napms(1500)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Oops, algo falló: {e}")
        curses.endwin()
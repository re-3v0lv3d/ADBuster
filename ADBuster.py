import subprocess
import time
import os
from ppadb.client import Client as AdbClient
from tkinter import Tk
from tkinter import filedialog
import curses
try:
    from scripts.adb_file_explorer import main as file_explorer_main
    from scripts.terminal import main as terminal_main
except ImportError:
    print("[!] Warning: adb_file_explorer.py not found. File explorer functionality will be disabled.")
    file_explorer_main = None 

TEXTS = {
    "es": {
        # Language Selection
        "select_language": "Seleccione idioma / Select language:",
        "language_option_1": "Español",
        "language_option_2": "English",
        "select_language_prompt": "Seleccione 1 o 2 y Enter: ",
        "invalid_language": "¡Opción no válida! Inténtelo de nuevo.",
        # General
        "error_unexpected": "[-] Error inesperado: {error}",
        "interrupted_keyboard": "\n[-] Interrupción por teclado. Saliendo...",
        "press_enter_continue": "Presione Enter para continuar...",
        "invalid_option": "[-] Opción no válida. Intente de nuevo.",
        "exiting": "Saliendo...",
        "no_device_selected": "[-] No se seleccionó ningún dispositivo.",
        "no_wifi_device_connected": "[-] No hay dispositivo conectado por Wi-Fi.",
        # ADB Server
        "starting_adb": "[*] Iniciando servidor ADB...",
        "adb_started": "[+] Servidor ADB iniciado.\n",
        "stopping_adb": "[*] Deteniendo servidor ADB...",
        "adb_stopped": "[+] Servidor ADB detenido.\n",
        # Device Connection & Selection
        "no_usb_device": "[-] No se detectó dispositivo USB.",
        "getting_ip_error": "[-] No se pudo obtener la IP.",
        "connecting_wifi": "[*] Conectando por Wi-Fi a {ip}:{port}...",
        "connection_result": "{result}",
        "disconnecting_wifi": "[*] Desconectando dispositivos Wi-Fi...",
        "disconnected_all_wifi": "[+] Todos los dispositivos Wi-Fi desconectados.",
        "listing_devices": "[*] Dispositivos conectados:",
        "device_serial": " - {serial}",
        "no_devices_connected": "[-] No hay dispositivos conectados.",
        "available_devices": "Dispositivos disponibles:",
        "device_list_item": "{index}. {serial}",
        "select_device_prompt": "Seleccione un dispositivo: ",
        "invalid_input_number": "[-] Entrada inválida. Por favor, ingrese un número.",
        "error_selecting_device": "[-] Error al seleccionar el dispositivo: {error}",
        "no_usb_prompt_ip": "[-] No se detectaron dispositivos USB. ¿Desea conectarse por IP?",
        "prompt_yes_no": "Ingrese 'si' o 'no': ",
        "enter_ip_prompt": "Ingrese la dirección IP del dispositivo: ",
        "connecting_ip_error": "[-] Error al conectar por IP: {error}",
        "connect_ip_fail": "[-] No se pudo conectar al dispositivo con la IP proporcionada.",
        "connected_to_ip": "[+] Conectado a {serial}",
        "using_wifi_device": "[*] Usando dispositivo Wi-Fi conectado.",
        # Commands & Actions
        "executing_command_error": "[-] Error al ejecutar comando: {error}",
        "command_result": "[+] Resultado:\n{result}\n",
        "enter_command_prompt": "Escriba el comando a ejecutar: ",
        "rebooting_device": "[*] Reiniciando dispositivo...",
        "rebooted_device": "[+] Dispositivo reiniciado en modo '{mode}'.",
        "reboot_error": "[-] Error al reiniciar: {error}",
        "reboot_mode_normal": "normal",
        "checking_wifi_connection": "[*] Verificando conexión Wi-Fi...",
        "wifi_check_ok": "[+] Dispositivo conectado por Wi-Fi.",
        "wifi_check_fail": "[-] El dispositivo no está conectado por Wi-Fi.",
        "installing_apk": "[*] Instalando APK: {path}",
        "apk_install_success": "[+] APK instalado correctamente.",
        "apk_install_error": "[-] Error al instalar APK: {error}",
        "no_apk_selected": "[-] No se seleccionó ningún archivo APK.",
        "select_apk_title": "Seleccionar archivo APK",
        "scrcpy_not_found": "[-] scrcpy.exe no encontrado en la carpeta ./scrcpy/",
        "scrcpy_extract_prompt": "Asegúrese de haber extraído el archivo ZIP de scrcpy dentro del directorio del proyecto.",
        "launching_scrcpy": "[*] Lanzando scrcpy para {serial}...",
        "scrcpy_launched": "[+] scrcpy lanzado para {serial}",
        "scrcpy_error": "[-] Error al ejecutar scrcpy: {error}",
        "getting_device_info": "[*] Obteniendo información del dispositivo...",
        "device_info_model": "Modelo: {model}",
        "device_info_android_version": "Versión de Android: {version}",
        "device_info_manufacturer": "Fabricante: {manufacturer}",
        "device_info_error": "[-] Error al obtener información del dispositivo: {error}",
        "listing_apps": "[*] Listando aplicaciones instaladas...",
        "list_apps_error": "[-] Error al listar aplicaciones: {error}",
        "app_package_name": "{package}",
        "opening_file_explorer": "[*] Abriendo administrador de archivos... ¡Prepárate para explorar!",
        "file_explorer_closed": "[+] Administrador de archivos cerrado.",
        "file_explorer_error": "[-] Error al abrir el administrador de archivos: {error}",
        # Menus
        "separator_line": "===================================",
        "main_menu_title": "        ADBuster - Menú",
        "menu_1_start_adb": "1. Iniciar servidor ADB",
        "menu_2_stop_adb": "2. Detener servidor ADB",
        "menu_3_reboot": "3. Menú de reinicio",
        "menu_4_bypass": "4. Bypass USB/WIFI",
        "menu_5_disconnect": "5. Desconectar dispositivos por Wi-Fi",
        "menu_6_list_devices": "6. Listar dispositivos conectados",
        "menu_7_run_command": "7. Abrir linea de comandos",
        "menu_8_install_apk": "8. Instalar APK",
        "menu_9_open_scrcpy": "9. Abrir scrcpy",
        "menu_10_device_info": "10. Obtener información del dispositivo",
        "menu_11_list_apps": "11. Listar aplicaciones instaladas",
        "menu_12_connect_ip": "12. Conectar por IP",
        "menu_13_file_explorer": "13. Abrir administrador de archivos",
        "menu_14_exit": "14. Salir",
        "submenu_reboot_separator": "-----------------------------------",
        "select_option_prompt": "Seleccione una opción: ",
        "submenu_reboot_title": "       Submenú de Reinicio",
        "submenu_reboot_1_normal": "1. Reiniciar",
        "submenu_reboot_2_recovery": "2. Reiniciar a Recovery",
        "submenu_reboot_3_fastboot": "3. Reiniciar a Fastboot",
        "submenu_reboot_4_edl": "4. Reiniciar a EDL",
        "submenu_reboot_5_back": "5. Volver al menú principal",
        "select_reboot_option_prompt": "Seleccione una opción de reinicio: "
    },
    "en": {
        # Language Selection
        "select_language": "Select language / Seleccione idioma:",
        "language_option_1": "Spanish",
        "language_option_2": "English",
        "select_language_prompt": "Select 1 or 2 and press Enter: ",
        "invalid_language": "Invalid option! Please try again.",
        # General
        "error_unexpected": "[-] Unexpected error: {error}",
        "interrupted_keyboard": "\n[-] Keyboard interrupt. Exiting...",
        "press_enter_continue": "Press Enter to continue...",
        "invalid_option": "[-] Invalid option. Try again.",
        "exiting": "Exiting...",
        "no_device_selected": "[-] No device selected.",
        "no_wifi_device_connected": "[-] No device connected via Wi-Fi.",
        # ADB Server
        "starting_adb": "[*] Starting ADB server...",
        "adb_started": "[+] ADB server started.\n",
        "stopping_adb": "[*] Stopping ADB server...",
        "adb_stopped": "[+] ADB server stopped.\n",
        # Device Connection & Selection
        "no_usb_device": "[-] No USB device detected.",
        "getting_ip_error": "[-] Could not get IP address.",
        "connecting_wifi": "[*] Connecting via Wi-Fi to {ip}:{port}...",
        "connection_result": "{result}",
        "disconnecting_wifi": "[*] Disconnecting Wi-Fi devices...",
        "disconnected_all_wifi": "[+] All Wi-Fi devices disconnected.",
        "listing_devices": "[*] Connected devices:",
        "device_serial": " - {serial}",
        "no_devices_connected": "[-] No devices connected.",
        "available_devices": "Available devices:",
        "device_list_item": "{index}. {serial}",
        "select_device_prompt": "Select a device: ",
        "invalid_input_number": "[-] Invalid input. Please enter a number.",
        "error_selecting_device": "[-] Error selecting device: {error}",
        "no_usb_prompt_ip": "[-] No USB devices detected. Connect via IP?",
        "prompt_yes_no": "Enter 'yes' or 'no': ",
        "enter_ip_prompt": "Enter the device IP address: ",
        "connecting_ip_error": "[-] Error connecting via IP: {error}",
        "connect_ip_fail": "[-] Could not connect to the device with the provided IP.",
        "connected_to_ip": "[+] Connected to {serial}",
         "using_wifi_device": "[*] Using connected Wi-Fi device.",
       # Commands & Actions
        "executing_command_error": "[-] Error executing command: {error}",
        "command_result": "[+] Result:\n{result}\n",
        "enter_command_prompt": "Enter the command to execute: ",
        "rebooting_device": "[*] Rebooting device...",
        "rebooted_device": "[+] Device rebooted into '{mode}' mode.",
        "reboot_error": "[-] Error rebooting: {error}",
        "reboot_mode_normal": "normal",
        "checking_wifi_connection": "[*] Checking Wi-Fi connection...",
        "wifi_check_ok": "[+] Device connected via Wi-Fi.",
        "wifi_check_fail": "[-] Device is not connected via Wi-Fi.",
        "installing_apk": "[*] Installing APK: {path}",
        "apk_install_success": "[+] APK installed successfully.",
        "apk_install_error": "[-] Error installing APK: {error}",
        "no_apk_selected": "[-] No APK file selected.",
        "select_apk_title": "Select APK File",
        "scrcpy_not_found": "[-] scrcpy.exe not found in ./scrcpy/ folder.",
        "scrcpy_extract_prompt": "Make sure you have extracted the scrcpy ZIP file into the project directory.",
        "launching_scrcpy": "[*] Launching scrcpy for {serial}...",
        "scrcpy_launched": "[+] scrcpy launched for {serial}",
        "scrcpy_error": "[-] Error executing scrcpy: {error}",
        "getting_device_info": "[*] Getting device information...",
        "device_info_model": "Model: {model}",
        "device_info_android_version": "Android Version: {version}",
        "device_info_manufacturer": "Manufacturer: {manufacturer}",
        "device_info_error": "[-] Error getting device info: {error}",
        "listing_apps": "[*] Listing installed applications...",
        "list_apps_error": "[-] Error listing applications: {error}",
        "app_package_name": "{package}",
        "opening_file_explorer": "[*] Opening file explorer... Get ready to explore!",
        "file_explorer_closed": "[+] File explorer closed.",
        "file_explorer_error": "[-] Error opening file explorer: {error}",
        # Menus
        "separator_line": "===================================",
        "main_menu_title": "        ADBuster - Menu",
        "menu_1_start_adb": "1. Start ADB server",
        "menu_2_stop_adb": "2. Stop ADB server",
        "menu_3_reboot": "3. Reboot menu",
        "menu_4_bypass": "4. Bypass USB/WIFI",
        "menu_5_disconnect": "5. Disconnect Wi-Fi devices",
        "menu_6_list_devices": "6. List connected devices",
        "menu_7_run_command": "7. Open command line",
        "menu_8_install_apk": "8. Install APK",
        "menu_9_open_scrcpy": "9. Open scrcpy",
        "menu_10_device_info": "10. Get device information",
        "menu_11_list_apps": "11. List installed applications",
        "menu_12_connect_ip": "12. Connect via IP",
        "menu_13_file_explorer": "13. Open file manager",
        "menu_14_exit": "14. Exit",
        "select_option_prompt": "Select an option: ",
        "submenu_reboot_separator": "-----------------------------------",
        "submenu_reboot_title": "       Reboot Submenu",
        "submenu_reboot_1_normal": "1. Reboot",
        "submenu_reboot_2_recovery": "2. Reboot to Recovery",
        "submenu_reboot_3_fastboot": "3. Reboot to Fastboot",
        "submenu_reboot_4_edl": "4. Reboot to EDL",
        "submenu_reboot_5_back": "5. Back to main menu",
        "select_reboot_option_prompt": "Select a reboot option: "
    }
}

# --- Language Selection Function ---
def seleccionar_idioma(texts):
    """ Asks the user to select a language """
    while True:
        limpiar_pantalla()
        print(texts["es"]["select_language"]) 
        print(f"1. {texts['es']['language_option_1']}")
        print(f"2. {texts['en']['language_option_2']}")
        choice = input(texts["es"]["select_language_prompt"]).strip()
        if choice == '1':
            return 'es'
        elif choice == '2':
            return 'en'
        else:
            print(texts["es"]["invalid_language"])
            time.sleep(2)

# --- System Utility ---
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# --- ADB Functions (Modified for Language Support) ---
def iniciar_adb_server(language, texts):
    print(texts[language]["starting_adb"])
    subprocess.run(["adb", "start-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(texts[language]["adb_started"])
    time.sleep(2)
    limpiar_pantalla()

def detener_adb_server(language, texts):
    print(texts[language]["stopping_adb"])
    subprocess.run(["adb", "kill-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(texts[language]["adb_stopped"])
    time.sleep(2)
    limpiar_pantalla()

def obtener_dispositivo_usb():
    resultado = subprocess.run(["adb", "devices"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dispositivos = resultado.stdout.strip().splitlines()[1:]
    for linea in dispositivos:
        if "\tdevice" in linea:
            return linea.split("\t")[0]
    return None

def obtener_ip_dispositivo(serial):
    try:
        resultado = subprocess.run(
            ["adb", "-s", serial, "shell", "ip -f inet addr show wlan0"],
            capture_output=True,
            text=True,
            timeout=10, # Add timeout
            encoding='utf-8', errors='ignore'
        )
        for linea in resultado.stdout.strip().splitlines():
            if "inet " in linea:
                parts = linea.strip().split(" ")
                if len(parts) > 1:
                    ip_part = parts[1]
                    return ip_part.split("/")[0]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    return None

def activar_tcpip(serial, puerto=5555):
    subprocess.run(["adb", "-s", serial, "tcpip", str(puerto)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def conectar_por_wifi(ip, language, texts, puerto=5555):
    print(texts[language]["connecting_wifi"].format(ip=ip, port=puerto))
    resultado = subprocess.run(["adb", "connect", f"{ip}:{puerto}"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    output = resultado.stdout.strip()
    if not output:
        output = resultado.stderr.strip()
    print(texts[language]["connection_result"].format(result=output))
    time.sleep(3)

def desconectar_dispositivos_wifi(language, texts):
    print(texts[language]["disconnecting_wifi"])
    subprocess.run(["adb", "disconnect"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(texts[language]["disconnected_all_wifi"])
    time.sleep(3)
    limpiar_pantalla()

def conectar_con_ppadb():
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        dispositivos = client.devices()
        return dispositivos
    except RuntimeError as e:
         return []


def ejecutar_comando_en_dispositivo(dispositivo, comando, language, texts):
    try:
        resultado = dispositivo.shell(comando)
        print(texts[language]["command_result"].format(result=resultado.strip()))
    except Exception as e:
        print(texts[language]["executing_command_error"].format(error=e))
    time.sleep(3)
    # limpiar_pantalla()

def reiniciar_dispositivo(dispositivo, language, texts, modo=""):
    print(texts[language]["rebooting_device"])
    try:
        comando = f"reboot {modo}".strip()
        dispositivo.shell(comando)
        modo_display = modo if modo else texts[language]["reboot_mode_normal"]
        print(texts[language]["rebooted_device"].format(mode=modo_display))
    except Exception as e:
        print(texts[language]["reboot_error"].format(error=e))
    time.sleep(3)
    limpiar_pantalla()

def verificar_conexion_wifi(dispositivo, language, texts):
    # print(texts[language]["checking_wifi_connection"])
    try:
        resultado = dispositivo.shell("echo CONECTADO")
        is_connected = "CONECTADO" in resultado
        # if is_connected:
        #     print(texts[language]["wifi_check_ok"])
        # else:
        #      print(texts[language]["wifi_check_fail"]) # Optional
        return is_connected
    except Exception:
        # print(texts[language]["wifi_check_fail"]) # Optional
        return False

def instalar_apk(dispositivo, language, texts):
    if not dispositivo:
        print(texts[language]["no_device_selected"])
        time.sleep(3)
        limpiar_pantalla()
        return

    try:
        Tk().withdraw()
        apk_path = filedialog.askopenfilename(
            title=texts[language]["select_apk_title"],
            filetypes=[("APK Files", "*.apk")]
            )
        if not apk_path:
            print(texts[language]["no_apk_selected"])
            time.sleep(3)
            limpiar_pantalla()
            return
        print(texts[language]["installing_apk"].format(path=os.path.basename(apk_path)))
        resultado = dispositivo.install(apk_path)
        if resultado:
            print(texts[language]["apk_install_success"])
        else:
             print(texts[language]["apk_install_error"].format(error="Installation failed (check device screen for details)"))
    except Exception as e:
        print(texts[language]["apk_install_error"].format(error=e))
    time.sleep(3)
    limpiar_pantalla()

def obtener_dispositivos(language, texts):

    devices = conectar_con_ppadb()
    if not devices:
        pass
    return devices


def seleccionar_dispositivo(language, texts):
    try:
        dispositivos = obtener_dispositivos(language, texts)
        if dispositivos:
            print(texts[language]["available_devices"])
            for i, d in enumerate(dispositivos):
                print(texts[language]["device_list_item"].format(index=i + 1, serial=d.serial))
            while True:
                try:
                    indice_str = input(texts[language]["select_device_prompt"]).strip()
                    if not indice_str:
                        return None
                    indice = int(indice_str) - 1
                    if 0 <= indice < len(dispositivos):
                        return dispositivos[indice]
                    else:
                        print(texts[language]["invalid_option"])
                except ValueError:
                    print(texts[language]["invalid_input_number"])
        else:
            print(texts[language]["no_usb_prompt_ip"])
            respuesta = input(texts[language]["prompt_yes_no"]).strip().lower()
            if respuesta == "yes" or respuesta == "si" or respuesta == "s":
                ip = input(texts[language]["enter_ip_prompt"]).strip()
                if not ip: return None
                try:
                    conectar_por_wifi(ip, language, texts)
                    dispositivos_actualizados = obtener_dispositivos(language, texts)
                    for d in dispositivos_actualizados:
                        if ip in d.serial:
                            print(texts[language]["connected_to_ip"].format(serial=d.serial))
                            time.sleep(2)
                            return d
                    print(texts[language]["connect_ip_fail"])
                    time.sleep(3)
                    return None
                except Exception as e:
                    print(texts[language]["connecting_ip_error"].format(error=e))
                    time.sleep(3)
                    return None
            else:
                return None
    except Exception as e:
        print(texts[language]["error_selecting_device"].format(error=e))
        time.sleep(3)
        return None

def abrir_scrcpy(dispositivo, language, texts):
    base_path = os.path.dirname(os.path.abspath(__file__))
    ruta_scrcpy = os.path.join(base_path, "scrcpy", "scrcpy.exe") # Soporte Linux is coming xD

    if not os.path.exists(ruta_scrcpy):
        print(texts[language]["scrcpy_not_found"])
        print(texts[language]["scrcpy_extract_prompt"])
        time.sleep(4)
        return

    print(texts[language]["launching_scrcpy"].format(serial=dispositivo.serial))
    try:
        subprocess.Popen([ruta_scrcpy, "-s", dispositivo.serial])
        print(texts[language]["scrcpy_launched"].format(serial=dispositivo.serial))
        time.sleep(2)
    except Exception as e:
        print(texts[language]["scrcpy_error"].format(error=e))
        time.sleep(3)

def abrir_scrcpy_linux(dispositivo, language, texts):
    base_path = os.path.dirname(os.path.abspath(__file__))
    ruta_scrcpy = os.path.join(base_path, "scrcpy", "scrcpy")

    if not os.path.exists(ruta_scrcpy):
        print(texts[language]["scrcpy_not_found"])
        print(texts[language]["scrcpy_extract_prompt"])
        time.sleep(4)
        return

    print(texts[language]["launching_scrcpy"].format(serial=dispositivo.serial))
    try:
        subprocess.Popen([ruta_scrcpy, "-s", dispositivo.serial])
        print(texts[language]["scrcpy_launched"].format(serial=dispositivo.serial))
        time.sleep(2)
    except Exception as e:
        print(texts[language]["scrcpy_error"].format(error=e))
        time.sleep(3)

def obtener_info_dispositivo(dispositivo, language, texts):
    print(texts[language]["getting_device_info"])
    try:
        modelo = dispositivo.shell("getprop ro.product.model").strip()
        version_android = dispositivo.shell("getprop ro.build.version.release").strip()
        fabricante = dispositivo.shell("getprop ro.product.manufacturer").strip()
        print(texts[language]["device_info_model"].format(model=modelo))
        print(texts[language]["device_info_android_version"].format(version=version_android))
        print(texts[language]["device_info_manufacturer"].format(manufacturer=fabricante))
    except Exception as e:
        print(texts[language]["device_info_error"].format(error=e))
    input(texts[language]["press_enter_continue"]) # Wait for user
    limpiar_pantalla()

def listar_aplicaciones(dispositivo, language, texts):
    print(texts[language]["listing_apps"])
    try:
        aplicaciones = dispositivo.shell("pm list packages -3").splitlines()
        if not aplicaciones:
             aplicaciones = dispositivo.shell("pm list packages").splitlines()

        for app in sorted(aplicaciones):
             package_name = app.replace("package:", "").strip()
             if package_name:
                 print(texts[language]["app_package_name"].format(package=package_name))
    except Exception as e:
        print(texts[language]["list_apps_error"].format(error=e))

    input(texts[language]["press_enter_continue"])
    limpiar_pantalla()

def conectar_por_ip(language, texts):
    ip = input(texts[language]["enter_ip_prompt"]).strip()
    if not ip: return None
    try:
        conectar_por_wifi(ip, language, texts)
        dispositivos = obtener_dispositivos(language, texts)
        for d in dispositivos:
            if ip in d.serial:
                print(texts[language]["connected_to_ip"].format(serial=d.serial))
                time.sleep(2)
                limpiar_pantalla()
                return d
        print(texts[language]["connect_ip_fail"])
        time.sleep(3)
        limpiar_pantalla()
        return None
    except Exception as e:
        print(texts[language]["connecting_ip_error"].format(error=e))
        time.sleep(3)
        limpiar_pantalla()
        return None

# --- Menus (Modified for Language Support) ---
def mostrar_menu(language, texts):
    print(texts[language]["separator_line"])
    print(texts[language]["main_menu_title"])
    print(texts[language]["separator_line"])
    print(texts[language]["menu_1_start_adb"])
    print(texts[language]["menu_2_stop_adb"])
    print(texts[language]["menu_3_reboot"])
    print(texts[language]["menu_4_bypass"])
    print(texts[language]["menu_5_disconnect"])
    print(texts[language]["menu_6_list_devices"])
    print(texts[language]["menu_7_run_command"])
    print(texts[language]["menu_8_install_apk"])
    print(texts[language]["menu_9_open_scrcpy"])
    print(texts[language]["menu_10_device_info"])
    print(texts[language]["menu_11_list_apps"])
    print(texts[language]["menu_12_connect_ip"])
    if file_explorer_main:
        print(texts[language]["menu_13_file_explorer"])
    print(texts[language]["menu_14_exit"])
    print(texts[language]["separator_line"])

def mostrar_submenu_reinicio(language, texts):
    print(texts[language]["submenu_reboot_separator"])
    print(texts[language]["submenu_reboot_title"])
    print(texts[language]["submenu_reboot_separator"])
    print(texts[language]["submenu_reboot_1_normal"])
    print(texts[language]["submenu_reboot_2_recovery"])
    print(texts[language]["submenu_reboot_3_fastboot"])
    print(texts[language]["submenu_reboot_4_edl"])
    print(texts[language]["submenu_reboot_5_back"])
    print(texts[language]["submenu_reboot_separator"])

# --- Main CLI Loop (Modified for Language Support) ---
def cli_adb(language, texts):
    dispositivo_activo = None # Renamed for clarity (can be USB or Wi-Fi)

    while True:
        limpiar_pantalla()
        # Display currently active device if any
        if dispositivo_activo:
            print(f"[{texts[language]['available_devices']} {dispositivo_activo.serial}]") # Quick info
        else:
            print(f"[{texts[language]['no_devices_connected']}]")

        mostrar_menu(language, texts)
        opcion = input(texts[language]["select_option_prompt"]).strip()

        if opcion == "1":
            iniciar_adb_server(language, texts)
            # Try to auto-select a device after starting server
            devices = obtener_dispositivos(language, texts)
            if devices:
                dispositivo_activo = devices[0] # Select the first one automatically

        elif opcion == "2":
            detener_adb_server(language, texts)
            dispositivo_activo = None # Clear active device

        elif opcion == "3": # Reinicio
            if not dispositivo_activo:
                print(texts[language]["no_device_selected"]) # Use general message
                time.sleep(3)
                continue # No need for screen clear here, loop will do it

            while True:
                limpiar_pantalla()
                mostrar_submenu_reinicio(language, texts)
                subopcion = input(texts[language]["select_reboot_option_prompt"]).strip()
                if subopcion == "1":
                    reiniciar_dispositivo(dispositivo_activo, language, texts)
                    dispositivo_activo = None
                    break
                elif subopcion == "2":
                    reiniciar_dispositivo(dispositivo_activo, language, texts, "recovery")
                    dispositivo_activo = None
                    break
                elif subopcion == "3":
                    reiniciar_dispositivo(dispositivo_activo, language, texts, "bootloader")
                    dispositivo_activo = None
                    break
                elif subopcion == "4":
                    reiniciar_dispositivo(dispositivo_activo, language, texts, "edl")
                    dispositivo_activo = None
                    break
                elif subopcion == "5":
                    break # Go back to main menu
                else:
                    print(texts[language]["invalid_option"])
                    time.sleep(2)


        elif opcion == "4": # Bypass USB/WIFI
            serial_usb = obtener_dispositivo_usb()
            if not serial_usb:
                print(texts[language]["no_usb_device"])
                time.sleep(3)
                continue

            print(f"[*] USB Device Found: {serial_usb}. Attempting Wi-Fi setup...")
            ip = obtener_ip_dispositivo(serial_usb)
            if not ip:
                print(texts[language]["getting_ip_error"])
                print("[*] Make sure the device is connected to Wi-Fi and USB debugging is enabled.")
                time.sleep(4)
                continue

            print(f"[*] Device IP: {ip}")
            activar_tcpip(serial_usb)
            print("[*] TCP/IP mode activated on device.")
            time.sleep(2)
            conectar_por_wifi(ip, language, texts)
            time.sleep(2)

            dispositivos_wifi = obtener_dispositivos(language, texts)
            found = False
            for d in dispositivos_wifi:
                if ip in d.serial:
                    dispositivo_activo = d
                    print(f"[+] {texts[language]['connected_to_ip'].format(serial=d.serial)}")
                    found = True
                    break
            if not found:
                print(texts[language]["connect_ip_fail"])
            time.sleep(3)


        elif opcion == "5": # Desconectar Wi-Fi
            desconectar_dispositivos_wifi(language, texts)
            if dispositivo_activo and ":" in dispositivo_activo.serial: 
                dispositivo_activo = None


        elif opcion == "6": # Listar dispositivos
            dispositivos = obtener_dispositivos(language, texts)
            limpiar_pantalla()
            if dispositivos:
                print(texts[language]["listing_devices"])
                for i, d in enumerate(dispositivos):
                    active_marker = " (*)" if dispositivo_activo and d.serial == dispositivo_activo.serial else ""
                    print(texts[language]["device_list_item"].format(index=i + 1, serial=d.serial) + active_marker)

                try:
                    sel = input(f"{texts[language]['select_device_prompt']} (Enter=Keep current): ").strip()
                    if sel:
                        idx = int(sel) - 1
                        if 0 <= idx < len(dispositivos):
                            dispositivo_activo = dispositivos[idx]
                            print(f"[+] Active device set to: {dispositivo_activo.serial}")
                        else:
                            print(texts[language]["invalid_option"])
                except ValueError:
                    if sel:
                         print(texts[language]["invalid_input_number"])
                except Exception:
                     print(texts[language]['error_unexpected'].format(error='selection failed'))

            else:
                print(texts[language]["no_devices_connected"])
            time.sleep(1)
            input(texts[language]["press_enter_continue"])


        elif opcion == "7" and terminal_main:
            target_device = dispositivo_activo
            if not target_device:
                 print("[*] No active device. Please select one command line.")
                 target_device = seleccionar_dispositivo(language, texts)
            if target_device:
                terminal_main(target_device)


        elif opcion == "8": # Instalar APK
            target_device = dispositivo_activo
            if not target_device:
                 print("[*] No active device. Please select one.")
                 target_device = seleccionar_dispositivo(language, texts)

            if target_device:
                 instalar_apk(target_device, language, texts)
            else:
                 print(texts[language]["no_device_selected"])
                 time.sleep(3)


        elif opcion == "9":  # Abrir scrcpy
            target_device = dispositivo_activo
            if not target_device:
                print("[*] No active device. Please select one to mirror.")
                target_device = seleccionar_dispositivo(language, texts)

            if target_device:
                try:
                    abrir_scrcpy(target_device, language, texts)
                except Exception as e:
                    print(f"[!] Failed to run scrcpy for Windows: {e}")
                    print("[*] Attempting to use Linux method...")
                    try:
                        abrir_scrcpy_linux(target_device, language, texts)
                    except Exception as e_linux:
                        print(f"[X] Failed to run scrcpy for Linux as well: {e_linux}")
                        time.sleep(3)
            else:
                print(texts[language]["no_device_selected"])
                time.sleep(3)




        elif opcion == "10": # Obtener info
            target_device = dispositivo_activo
            if not target_device:
                 print("[*] No active device. Please select one.")
                 target_device = seleccionar_dispositivo(language, texts)

            if target_device:
                obtener_info_dispositivo(target_device, language, texts)
            else:
                 print(texts[language]["no_device_selected"])
                 time.sleep(3)

        elif opcion == "11": # Listar apps
            target_device = dispositivo_activo
            if not target_device:
                 print("[*] No active device. Please select one.")
                 target_device = seleccionar_dispositivo(language, texts)

            if target_device:
                 listar_aplicaciones(target_device, language, texts)
            else:
                 print(texts[language]["no_device_selected"])
                 time.sleep(3)

        elif opcion == "12": # Conectar por IP
             connected_device = conectar_por_ip(language, texts)
             if connected_device:
                 dispositivo_activo = connected_device


        elif opcion == "13" and file_explorer_main: # Abrir admin de archivos
            target_device = dispositivo_activo
            if not target_device:
                 print("[*] No active device. Please select one for file explorer.")
                 target_device = seleccionar_dispositivo(language, texts)

            if target_device:
                 print(texts[language]["opening_file_explorer"])
                 time.sleep(1) # Brief pause before curses takes over
                 limpiar_pantalla()
                 try:
                     curses.wrapper(lambda stdscr: file_explorer_main(stdscr, target_device))
                     print(f"\n{texts[language]['file_explorer_closed']}")
                 except NameError:
                      print("[!] File explorer module not loaded correctly.")
                 except Exception as e:
                     print(f"\n{texts[language]['file_explorer_error'].format(error=e)}")
                 time.sleep(3)

            else:
                 print(texts[language]["no_device_selected"])
                 time.sleep(3)

        elif opcion == "14": # Salir
            print(texts[language]["exiting"])
            time.sleep(1)
            limpiar_pantalla()
            break

        else:
            print(texts[language]["invalid_option"])
            time.sleep(2)


# --- Entry Point ---
if __name__ == "__main__":
    language = 'en'
    try:
        language = seleccionar_idioma(TEXTS)
        cli_adb(language, TEXTS)
    except KeyboardInterrupt:
        limpiar_pantalla()
        print(TEXTS[language]["interrupted_keyboard"])
    except Exception as e:
        limpiar_pantalla()
        print(TEXTS[language]["error_unexpected"].format(error=e))
        input("\nPress Enter to exit.")
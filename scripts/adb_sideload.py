import os
import sys
import subprocess
import re
import tkinter as tk
from tkinter import filedialog
from ppadb.device import Device

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def select_file_with_tkinter() -> str | None:
    """Abre un diálogo de Tkinter para seleccionar un archivo APK o ZIP."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos APK o ZIP", "*.apk *.zip"), ("Todos los archivos", "*.*")]
    )
    root.destroy()  # Limpia la instancia de Tkinter
    return file_path if file_path else None

def sideload_file(device: Device, file_path: str) -> bool:
    """Intenta hacer sideload del archivo especificado al dispositivo con visualización de progreso."""
    if not os.path.isfile(file_path):
        print(f"[Error] El archivo '{file_path}' no existe.", file=sys.stderr)
        return False

    if not file_path.lower().endswith(('.apk', '.zip')):
        print(f"[Advertencia] El archivo '{file_path}' no es un archivo .apk o .zip.", file=sys.stderr)
        proceed = input("¿Continuar con el sideload? (s/n): ").strip().lower()
        if proceed != 's':
            print("[*] Sideload cancelado.")
            return False

    print(f"[*] Iniciando sideload de '{file_path}' al dispositivo {device.serial}...")
    try:
        # Construye el comando de sideload
        cmd = ["adb", "-s", device.serial, "sideload", file_path]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Búfer de línea
            universal_newlines=True
        )

        # Expresión regular para capturar porcentajes (e.g., "~47%" o "47%")
        percentage_re = re.compile(r'~?(\d+)%')

        # Procesa la salida en tiempo real
        last_percentage = -1
        while True:
            line = process.stderr.readline()  # adb sideload suele usar stderr
            if not line and process.poll() is not None:
                break
            if line:
                # Busca el porcentaje en la línea
                match = percentage_re.search(line)
                if match:
                    percentage = int(match.group(1))
                    if percentage != last_percentage:  # Evita actualizaciones redundantes
                        print(f"\r[*] Progreso: {percentage}%", end="", flush=True)
                        last_percentage = percentage
                else:
                    # Imprime otras líneas relevantes (e.g., errores o estado final)
                    if "Total xfer" in line or "error" in line.lower() or "failed" in line.lower():
                        print(f"\r{line.strip()}")

        # Asegura un salto de línea después del progreso
        if last_percentage >= 0:
            print()

        # Verifica el código de salida del proceso
        return_code = process.wait(timeout=300)  # Timeout de 5 minutos
        if return_code == 0:
            print("[*] Sideload completado exitosamente.")
            return True
        else:
            # Captura cualquier salida de error restante
            remaining_output = process.stderr.read()
            if remaining_output:
                print(f"[Error] Fallo en el sideload: {remaining_output.strip()}", file=sys.stderr)
            else:
                print("[Error] Fallo en el sideload con error desconocido.", file=sys.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("[Error] El sideload excedió el tiempo límite de 5 minutos.", file=sys.stderr)
        process.terminate()
        return False
    except FileNotFoundError:
        print("[Error] Ejecutable ADB no encontrado. Asegúrate de que 'adb' esté en tu PATH.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[Error] Fallo en el sideload: {e}", file=sys.stderr)
        return False

def sideload_loop(device: Device):
    """Ejecuta el bucle de sideload para el dispositivo seleccionado."""
    limpiar_pantalla()
    serial = device.serial
    print(f"--- ADB Sideload para {serial} ---")
    print("Comandos: 'select' para elegir un archivo, 'exit' o 'quit' para volver al terminal principal.")
    print("O proporciona la ruta completa a un archivo .apk o .zip para sideload.")
    print("-" * (len(serial) + 30))

    while True:
        try:
            prompt = f"sideload@{serial}> "
            user_input = input(prompt).strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("Volviendo al terminal principal...")
                break

            if user_input.lower() == 'select':
                file_path = select_file_with_tkinter()
                if file_path:
                    print(f"[*] Archivo seleccionado: {file_path}")
                    sideload_file(device, file_path)
                else:
                    print("[*] No se seleccionó ningún archivo.")
                continue

            # Asume que la entrada es una ruta de archivo
            file_path = user_input.replace('"', '').replace("'", '').strip()
            sideload_file(device, file_path)

        except KeyboardInterrupt:
            print("\nCapturado Ctrl+C. Escribe 'exit' o 'quit' para volver al terminal principal.")
        except EOFError:
            print("\nEOF detectado. Volviendo al terminal principal.")
            break
        except Exception as loop_error:
            print(f"\n[Error en el Bucle de Sideload] Ocurrió un error inesperado: {loop_error}", file=sys.stderr)
            print("Volviendo al terminal principal.", file=sys.stderr)
            break

    limpiar_pantalla()

def main(device: Device):
    """Función principal del módulo de sideload, invocable desde otros scripts."""
    try:
        sideload_loop(device)
    except KeyboardInterrupt:
        print("\n[*] Sideload ADB interrumpido por el usuario.")
        limpiar_pantalla()
    except Exception as e:
        print(f"[Error] Sideload: {e}", file=sys.stderr)
        limpiar_pantalla()
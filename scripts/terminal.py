import os
import sys
import time
from ppadb.client import Client as AdbClient
from ppadb.device import Device

def limpiar_pantalla():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def conectar_y_listar_dispositivos():
    """Connects to the ADB server and returns a list of devices."""
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        return devices
    except RuntimeError as e:
        print(f"[Error] Could not connect to ADB server: {e}", file=sys.stderr)
        print("Please ensure the ADB server is running ('adb start-server').", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[Error] An unexpected error occurred connecting to ADB: {e}", file=sys.stderr)
        return None

def seleccionar_dispositivo(devices: list) -> Device | None:
    """Prompts the user to select a device from the list."""
    if not devices:
        print("[Error] No ADB devices found.", file=sys.stderr)
        print("Make sure your device is connected and USB Debugging is enabled.", file=sys.stderr)
        return None

    if len(devices) == 1:
        print(f"[*] Auto-selecting device: {devices[0].serial}")
        return devices[0]

    print("Available devices:")
    for i, device in enumerate(devices):
        try:
            model = device.shell("getprop ro.product.model").strip()
            print(f"  {i + 1}. {device.serial} ({model})")
        except Exception:
            print(f"  {i + 1}. {device.serial}")

    while True:
        try:
            choice = input("Select a device number to use: ").strip()
            if not choice:
                print("[Error] No selection made.", file=sys.stderr)
                return None

            device_index = int(choice) - 1
            if 0 <= device_index < len(devices):
                selected_device = devices[device_index]
                print(f"[*] Using device: {selected_device.serial}")
                return selected_device
            else:
                print(f"[Error] Invalid choice. Please enter a number between 1 and {len(devices)}.", file=sys.stderr)
        except ValueError:
            print("[Error] Invalid input. Please enter a number.", file=sys.stderr)
        except Exception as e:
            print(f"[Error] An error occurred during selection: {e}", file=sys.stderr)
            return None

def terminal_loop(device: Device):
    """Runs the main command loop for the selected device."""
    limpiar_pantalla()
    serial = device.serial
    print(f"--- ADB Connected to {serial} ---")
    print("Type 'exit' or 'quit' to disconnect.")
    print("-" * (len(serial) + 30))

    while True:
        try:
            prompt = f"adb@{serial}> "
            command = input(prompt).strip()

            if not command:
                continue 

            if command.lower() in ['exit', 'quit']:
                print("Disconnecting...")
                break

            try:
                result = device.shell(command, timeout=30)
                print(result) 
            except Exception as cmd_error:
                print(f"[Command Error] {cmd_error}", file=sys.stderr)

        except KeyboardInterrupt:
            print("\nCaught Ctrl+C. Type 'exit' or 'quit' to disconnect.")
        except EOFError: 
            print("\nEOF detected. Exiting.")
            break
        except Exception as loop_error:
            print(f"\n[Terminal Loop Error] An unexpected error occurred: {loop_error}", file=sys.stderr)
            print("Exiting terminal.", file=sys.stderr)
            break 

    print("\n" * (os.get_terminal_size().lines - 3))
    print("---By 3v0lv3d---")

# --- Función reutilizable para importar ---
def main(device: Device):
    """Función principal exportable para integrarla en otros scripts."""
    try:
        terminal_loop(device)
    except KeyboardInterrupt:
        print("\n[*] Terminal ADB interrumpida por el usuario.")
    except Exception as e:
        print(f"[Error] Terminal: {e}", file=sys.stderr)

# --- Ejecución directa desde terminal ---
if __name__ == "__main__":
    print("[*] Initializing ADB Terminal...")
    connected_devices = conectar_y_listar_dispositivos()

    if connected_devices is None:
        sys.exit(1)

    selected_device = seleccionar_dispositivo(connected_devices)

    if selected_device:
        main(selected_device)
    else:
        print("[*] No device selected. Exiting.")
        sys.exit(1)

#!/usr/bin/env bash

if [ "$(id -u)" != "0" ]; then
   echo "Please run $0 as root" 1>&2
   exit 1
fi

if [ $# -eq 0 ]
then
    echo "No arguments provided. Setting fans to maximum speed automatically..."
    echo "Detecting maximum fan speeds and setting to maximum..."
    
    # Leer valores min y max (para fan1 y fan2)
    fan1_min=$(cat /sys/devices/platform/applesmc.768/fan1_min)
    fan1_max=$(cat /sys/devices/platform/applesmc.768/fan1_max)
    fan2_min=$(cat /sys/devices/platform/applesmc.768/fan2_min)
    fan2_max=$(cat /sys/devices/platform/applesmc.768/fan2_max)
    
    # Determinar el máximo entre ambos ventiladores
    if [ "$fan1_max" -gt "$fan2_max" ]; then
        max_speed=$fan1_max
        echo "Fan1 has higher max speed: $fan1_max RPM"
    else
        max_speed=$fan2_max
        echo "Fan2 has higher max speed: $fan2_max RPM"
    fi
    
    echo "Setting both fans to maximum speed: $max_speed RPM"
    
    # Set fan1 manual mode if not already
    fan1_mode=$(cat /sys/devices/platform/applesmc.768/fan1_manual)
    if [ "$fan1_mode" -eq 0 ]; then
        echo 1 > /sys/devices/platform/applesmc.768/fan1_manual
        echo "Switch fan1 to manual control..."
    fi

    # Set fan2 manual mode if not already
    fan2_mode=$(cat /sys/devices/platform/applesmc.768/fan2_manual)
    if [ "$fan2_mode" -eq 0 ]; then
        echo 1 > /sys/devices/platform/applesmc.768/fan2_manual
        echo "Switch fan2 to manual control..."
    fi
    
    # Establecer ambos ventiladores al máximo
    echo "Setting fan1 speed to $max_speed"
    echo "$max_speed" > /sys/devices/platform/applesmc.768/fan1_output
    echo "Setting fan2 speed to $max_speed"
    echo "$max_speed" > /sys/devices/platform/applesmc.768/fan2_output
    
    echo "Both fans set to maximum speed successfully!"
elif [ $# -ne 1 ]
then
    echo "Usage:"
    echo "    $0                    : Set Macbook pro fans speed to maximum detected speed"
    echo "    $0 [fan speed value]  : Set Macbook pro fans speed to manual speed "
    echo "    $0 max                : Set Macbook pro fans speed to maximum detected speed"
    echo "    $0 reset              : Reset Macbook pro fans speed to kernel regulation"
else
    case $1 in
        reset)
            echo "Set to automatic fan speed scaling"
            echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
            echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
        ;;
        max)
            echo "Detecting maximum fan speeds and setting to maximum..."
            
            # Leer valores min y max (para fan1 y fan2)
            fan1_min=$(cat /sys/devices/platform/applesmc.768/fan1_min)
            fan1_max=$(cat /sys/devices/platform/applesmc.768/fan1_max)
            fan2_min=$(cat /sys/devices/platform/applesmc.768/fan2_min)
            fan2_max=$(cat /sys/devices/platform/applesmc.768/fan2_max)
            
            # Determinar el máximo entre ambos ventiladores
            if [ "$fan1_max" -gt "$fan2_max" ]; then
                max_speed=$fan1_max
                echo "Fan1 has higher max speed: $fan1_max RPM"
            else
                max_speed=$fan2_max
                echo "Fan2 has higher max speed: $fan2_max RPM"
            fi
            
            echo "Setting both fans to maximum speed: $max_speed RPM"
            
            # Set fan1 manual mode if not already
            fan1_mode=$(cat /sys/devices/platform/applesmc.768/fan1_manual)
            if [ "$fan1_mode" -eq 0 ]; then
                echo 1 > /sys/devices/platform/applesmc.768/fan1_manual
                echo "Switch fan1 to manual control..."
            fi

            # Set fan2 manual mode if not already
            fan2_mode=$(cat /sys/devices/platform/applesmc.768/fan2_manual)
            if [ "$fan2_mode" -eq 0 ]; then
                echo 1 > /sys/devices/platform/applesmc.768/fan2_manual
                echo "Switch fan2 to manual control..."
            fi
            
            # Establecer ambos ventiladores al máximo
            echo "Setting fan1 speed to $max_speed"
            echo "$max_speed" > /sys/devices/platform/applesmc.768/fan1_output
            echo "Setting fan2 speed to $max_speed"
            echo "$max_speed" > /sys/devices/platform/applesmc.768/fan2_output
            
            echo "Both fans set to maximum speed successfully!"
        ;;
        *)
            # Set fan1 manual mode if not already
            fan1_mode=$(cat /sys/devices/platform/applesmc.768/fan1_manual)
            if [ "$fan1_mode" -eq 0 ]; then
                echo 1 > /sys/devices/platform/applesmc.768/fan1_manual
                echo "Switch fan1 to manual control..."
            fi

            # Set fan2 manual mode if not already
            fan2_mode=$(cat /sys/devices/platform/applesmc.768/fan2_manual)
            if [ "$fan2_mode" -eq 0 ]; then
                echo 1 > /sys/devices/platform/applesmc.768/fan2_manual
                echo "Switch fan2 to manual control..."
            fi

            # Leer valores min y max (para fan1 y fan2)
            fan1_min=$(cat /sys/devices/platform/applesmc.768/fan1_min)
            fan1_max=$(cat /sys/devices/platform/applesmc.768/fan1_max)
            fan2_min=$(cat /sys/devices/platform/applesmc.768/fan2_min)
            fan2_max=$(cat /sys/devices/platform/applesmc.768/fan2_max)

            # Comprobar que el valor está en rango para ambos fans
            if [ "$1" -ge "$fan1_min" ] && [ "$1" -le "$fan1_max" ] && [ "$1" -ge "$fan2_min" ] && [ "$1" -le "$fan2_max" ]; then
                echo "Setting fan1 speed to $1"
                echo "$1" > /sys/devices/platform/applesmc.768/fan1_output
                echo "Setting fan2 speed to $1"
                echo "$1" > /sys/devices/platform/applesmc.768/fan2_output
            else
                echo "Fan speed not allowed. Please specify a value between:"
                echo "fan1: $fan1_min - $fan1_max"
                echo "fan2: $fan2_min - $fan2_max"
            fi
        ;;
    esac
fi

#!/bin/sh

# Configura la disposición de las pantallas
xrandr --output HDMI-A-0 --primary --auto --output eDP --auto --right-of HDMI-A-0 &

# Inicia compositor para transparencias y efectos
picom --config ~/.config/qtile/picom/picom.conf &

# Brillo
redshift -O 3700 &


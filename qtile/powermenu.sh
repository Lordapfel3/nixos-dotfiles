#!/usr/bin/env bash

options="1: Shutdown\n2: Reboot\n3: Logout"

selected=$(printf "$options" | rofi -dmenu \
    -p "Power Menu" \
    -location 0 \
    -width 20 \
    -lines 3 \
    -font "JetBrainsMono Nerd Font 12" \
    -hide-scrollbar)

case "$selected" in
    *"1:"*) systemctl poweroff ;;
    *"2:"*) systemctl reboot ;;
    *"3:"*) qtile cmd-obj -o cmd -f shutdown ;;
esac
# Fehler und Ausgaben in eine Log-Datei schreiben
LOGfile="/tmp/powermenu_debug.log"
exec 1> "$LOGfile" 2>&1

echo "--- Skript gestartet am $(date) ---"

# Pfade ausgeben #!/usr/bin/env bash

# Optionen für Rofi
options="1: Shutdown\n2: Reboot\n3: Logout"

# Rofi starten und Auswahl speichern
# Wir nutzen printf statt echo -e, das ist stabiler
selected=$(printf "$options" | rofi -dmenu \
    -p "Power Menu" \
    -location 0 \
    -width 20 \
    -lines 3 \
    -font "JetBrainsMono Nerd Font 12" \
    -hide-scrol
ptions="1: Shutdown\n2: Reboot\n3: Logout"

selected=$(printf "$options" | rofi -dmenu \
    -p "Power Menu" \
    -location 0 \
    -width 20 \
    -lines 3 \


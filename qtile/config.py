import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

# --- TASTENKÜRZEL ---
keys = [
    # Standard Navigation
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Fenster verschieben
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Fenstergröße ändern
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # System
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    # Apps
    Key([mod], "b", lazy.spawn("firefox")),
    Key([mod], "e", lazy.spawn("pcmanfm")),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod], "p", lazy.spawn("/home/leon/.config/qtile/powermenu.sh")),

    # --- LAPTOP MEDIA KEYS ---
    # Lautstärke
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Mute Volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5"), desc="Lower Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5"), desc="Raise Volume"),

    # Helligkeit
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Brightness Up"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Brightness Down"),
]

# --- GRUPPEN ---
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Move focused window to group {i.name}"),
    ])

# --- LAYOUTS ---
layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, margin=0),
    layout.Max(),
]

widget_defaults = dict(
    font="JetBrains Mono Nerd Font",
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

# --- WIDGET LISTE ---
def init_widgets_list():
    # Pfad zum Skript definieren
    home = os.path.expanduser('~')
    power_script = os.path.join(home, ".config", "qtile", "powermenu.sh")

    widgets_list = [
        widget.GroupBox(
            highlight_method='line',
            this_current_screen_border="#50fa7b",
            active="#f8f8f2",
            inactive="#6272a4",
            background="#282a36"
        ),
        
        widget.Prompt(),
        widget.WindowName(foreground="#8be9fd"),
        
        # --- RECHTE SEITE ---
        widget.Systray(),
        widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),

        # WLAN
        widget.Wlan(
            interface="wlp0s20f3", 
            format='  {essid} {percent:2.0%}',
            foreground="#ffb86c",
            mouse_callbacks={'Button1': lambda: qtile.spawn("nm-connection-editor")}
        ),
        
        
        # Helligkeit
        widget.Backlight(
            backlight_name='intel_backlight',
            format='Bri: {percent:2.0%}',
            foreground="#f1fa8c",
            step=5,
        ),
        
        widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),

        # Lautstärke
        widget.PulseVolume(
            fmt='Vol: {}',
            foreground="#bd93f9",
            limit_max_volume=True,
        ),
        
        widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),

        # Akku
        widget.Battery(
            format='{char} {percent:2.0%} {watt:.1f}W', 
            charge_char='⚡',
            discharge_char='🔋',
            empty_char='💀',
            foreground="#50fa7b",
            update_interval=5,
        ),
        
        widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),

        # Uhrzeit
        widget.Clock(format='%d.%m.%Y  %H:%M', foreground="#f1fa8c"),
        
        widget.Sep(linewidth=2, padding=10, foreground="#6272a4"),

        # --- POWER BUTTON ---
        widget.TextBox(
            text='',
            fontsize=18,
            foreground="#ff5555",
            padding=5,
            mouse_callbacks={'Button1': lambda: qtile.spawn(power_script)},
        ),
    ]
    return widgets_list

# --- SCREENS ---
screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            30,
            background="#282a36",
            opacity=0.95
        ),
        wallpaper="/home/leon/Higr/R1.jpg",
        wallpaper_mode="fill",
    ),
]

# --- MAUS ---
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
        Match(wm_class="nm-connection-editor"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="pavucontrol"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"

# --- AUTOSTART ---
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen(['nm-applet'])
    subprocess.Popen(['blueman-applet'])

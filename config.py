# ==================== IMPORTS ====================
import os
from libqtile import bar, layout, widget, qtile, hook
import subprocess
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

# ==================== VARIABLES ====================
mod = "mod4"
terminal = "alacritty"
font_color = "#ffffff"
bg_color = "#000000"

# ==================== KEY BINDINGS ====================
keys = [
    # Movimiento de foco
    Key([mod], "h", lazy.layout.left(), desc="Focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Next window"),

    # Mover ventanas
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move up"),

    # Redimensionar
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize size"),

    # Ventanas y layout
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([mod], "w", lazy.window.kill(), desc="Close window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),

    # Lanzadores
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawncmd(), desc="Run command"),
    Key([mod,"control"], "d", lazy.spawn("dmenu_run"), desc="Lanzador con dmenu"),
    Key([], "Print", lazy.spawn("flameshot gui")),


    # Qtile
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "F12", lazy.spawn("systemctl poweroff"), desc="Apagar"),
    Key([mod, "control"], "F11", lazy.spawn("systemctl suspend")),

    # System sound
    Key([mod], "F10", lazy.spawn("pavucontrol"), desc="Abrir control de volumen")


    
]

# ==================== GRUPOS ====================
screen1_groups = "12345"
screen2_groups = "6789"

groups = [Group(name) for name in screen1_groups + screen2_groups]

for i in screen1_groups:
    keys.extend([
        Key([mod], i, lazy.group[i].toscreen(0), desc=f"Switch to group {i} on screen 1"),
        Key([mod, "shift"], i, lazy.window.togroup(i), desc=f"Move window to group {i}"),
    ])

for i in screen2_groups:
    keys.extend([
        Key([mod], i, lazy.group[i].toscreen(1), desc=f"Switch to group {i} on screen 2"),
        Key([mod, "shift"], i, lazy.window.togroup(i), desc=f"Move window to group {i}"),
    ])
# ==================== LAYOUTS ====================
layouts = [
    layout.Columns(
        border_focus="#ff0000",     # borde cuando la ventana tiene foco
        border_normal="#444444",    # borde cuando NO tiene foco
        border_width=2,              # grosor del borde
        margin = 2
    ),
    layout.Max(margin=2),
]

# ==================== WIDGETS ====================
widget_defaults = dict(font="sans", fontsize=12, padding=3)
extension_defaults = widget_defaults.copy()

def primary_widgets():
    return [
        widget.TextBox("🖵 ⭢ ⓵ ", foreground=font_color),
        widget.GroupBox(highlight_method="line", this_current_screen_border=font_color),
        widget.CurrentLayout(),
        widget.WindowName(),

        # ─── ESTADÍSTICAS DEL SISTEMA ───
        widget.CPU(
            format='CPU: {load_percent:5.2f} %',
            foreground='#ff40af',
            background='#222222',
        ),
        widget.Memory(
            format='RAM: {MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}',
            update_interval=2,
            foreground='#ff0008',
            background='#333333',
            padding=10,
        ),
        widget.Battery(
            format='{char} {percent:2.0%}',
            update_interval=10,
            background='#444444'
            ),



        # ────────────────────────────────

        widget.Clock(format="%Y-%m-%d %a %I:%M %p", foreground=font_color),
        widget.Systray(),
        widget.TextBox(
            text="⏻", fontsize=16, padding=10, foreground=font_color,
            mouse_callbacks={"Button1": lazy.spawn("systemctl poweroff")},
        ),
    ]



def secondary_widgets():
    return [
        widget.TextBox(" 🖵 ⭢ ⓶ ", foreground=font_color),
        widget.GroupBox(highlight_method="line", this_current_screen_border=font_color),
        widget.CurrentLayout(),
        widget.WindowName(),
        widget.Clock(format="%H:%M"),
    ]

# ==================== SCREENS ====================
screens = [
    Screen(top=bar.Bar(primary_widgets(), 24, background=bg_color)),
    Screen(top=bar.Bar(secondary_widgets(), 24, background=bg_color)),
]

# ==================== RATÓN ====================
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ==================== CONFIG GENERAL ====================
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = False 
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),
    Match(wm_class="makebranch"),
    Match(wm_class="maketag"),
    Match(wm_class="ssh-askpass"),
    Match(title="branchdialog"),
    Match(title="pinentry"),
])

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True

# ==================== JAVA FIX ====================
wmname = "LG3D"

# ==================== MULTIPANTALLA (X11) ====================
@hook.subscribe.startup_complete
def assign_groups_to_screens():
    if len(qtile.screens) > 1:
        qtile.groups_map["1"].toscreen(0, toggle=False)  # Pantalla 1
        qtile.groups_map["2"].toscreen(1, toggle=False)  # Pantalla 2

# ======================== AUTOSTART ==========================
@hook.subscribe.startup_complete
def autostart():
    subprocess.Popen([os.path.expanduser("~/.config/qtile/autostart.sh")])


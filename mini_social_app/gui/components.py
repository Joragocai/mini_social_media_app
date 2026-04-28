from datetime import datetime

import customtkinter as ctk


BG = "#f4f6fb"
CARD = "#ffffff"
PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
TEXT = "#111827"
MUTED = "#6b7280"
FIELD = "#eef2f7"
BORDER = "#d8dee9"
DANGER = "#dc2626"
DANGER_DARK = "#b91c1c"
SUCCESS = "#16a34a"

APP_WIDTH = 430
CONTENT_PAD = 16
POST_WRAP = 350


def screen_frame(master):
    return {"fg_color": BG}


def title_label(master, text, size=24):
    return ctk.CTkLabel(
        master,
        text=text,
        font=ctk.CTkFont(size=size, weight="bold"),
        text_color=TEXT,
    )


def muted_label(master, text, size=13, anchor="center"):
    return ctk.CTkLabel(
        master,
        text=text,
        font=ctk.CTkFont(size=size),
        text_color=MUTED,
        anchor=anchor,
    )


def primary_button(master, text, command, width=None):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        height=44,
        width=width or 140,
        fg_color=PRIMARY,
        hover_color=PRIMARY_DARK,
        corner_radius=14,
        font=ctk.CTkFont(size=14, weight="bold"),
    )


def secondary_button(master, text, command, width=None):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        height=40,
        width=width or 110,
        fg_color=FIELD,
        hover_color=BORDER,
        text_color=TEXT,
        corner_radius=14,
        font=ctk.CTkFont(size=13, weight="bold"),
    )


def danger_button(master, text, command, width=None):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        height=38,
        width=width or 92,
        fg_color=DANGER,
        hover_color=DANGER_DARK,
        corner_radius=14,
        font=ctk.CTkFont(size=13, weight="bold"),
    )


def make_entry(master, placeholder="", show=None):
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        show=show,
        height=44,
        fg_color=FIELD,
        border_color=BORDER,
        corner_radius=14,
        text_color=TEXT,
    )


def format_timestamp(value):
    if not value:
        return ""
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return parsed.strftime("%b %d, %Y %I:%M %p")
    except ValueError:
        return value


class BottomNav(ctk.CTkFrame):
    def __init__(self, master, app, active):
        super().__init__(master, fg_color=CARD, corner_radius=24, height=64)
        self.app = app
        self.active = active
        self.pack_propagate(False)
        self._build()

    def _build(self):
        items = [
            ("Home", "home", self.app.show_home),
            ("Post", "post", self.app.show_create_post),
            ("Profile", "profile", self.app.show_profile),
        ]
        for label, key, command in items:
            is_active = key == self.active
            button = ctk.CTkButton(
                self,
                text=label,
                command=command,
                height=42,
                fg_color=PRIMARY if is_active else "transparent",
                hover_color=PRIMARY_DARK if is_active else FIELD,
                text_color="#ffffff" if is_active else MUTED,
                corner_radius=16,
                font=ctk.CTkFont(size=13, weight="bold"),
            )
            button.pack(side="left", expand=True, fill="x", padx=6, pady=10)

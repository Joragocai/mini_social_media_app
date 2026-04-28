from tkinter import messagebox

import customtkinter as ctk

from gui.components import (
    BG,
    CARD,
    CONTENT_PAD,
    make_entry,
    muted_label,
    primary_button,
    screen_frame,
    secondary_button,
    title_label,
)


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self._build()

    def _build(self):
        shell = ctk.CTkFrame(self, fg_color=BG)
        shell.pack(expand=True, fill="both", padx=CONTENT_PAD, pady=CONTENT_PAD)

        card = ctk.CTkFrame(shell, fg_color=CARD, corner_radius=28)
        card.pack(expand=True, fill="both", padx=4, pady=42)

        title_label(card, "Create Account", size=28).pack(pady=(30, 4))
        muted_label(card, "Join with a username and password").pack(pady=(0, 22))

        self.display_name_entry = make_entry(card, "Display name")
        self.display_name_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.username_entry = make_entry(card, "Username")
        self.username_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.password_entry = make_entry(card, "Password", show="*")
        self.password_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.confirm_entry = make_entry(card, "Confirm password", show="*")
        self.confirm_entry.pack(fill="x", padx=24, pady=(0, 20))

        primary_button(card, "Register", self.register_user, width=240).pack(pady=(0, 12))
        secondary_button(card, "Back to Login", self.app.show_login, width=240).pack(pady=(0, 28))

    def register_user(self):
        try:
            self.app.auth_manager.register(
                username=self.username_entry.get(),
                password=self.password_entry.get(),
                confirm_password=self.confirm_entry.get(),
                display_name=self.display_name_entry.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Registration failed", str(exc))
            return
        messagebox.showinfo("Account created", "Your account is ready.")
        self.app.show_home()

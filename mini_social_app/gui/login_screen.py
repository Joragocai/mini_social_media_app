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


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self._build()

    def _build(self):
        shell = ctk.CTkFrame(self, fg_color=BG)
        shell.pack(expand=True, fill="both", padx=CONTENT_PAD, pady=CONTENT_PAD)

        spacer = ctk.CTkFrame(shell, fg_color="transparent", height=72)
        spacer.pack(fill="x")

        card = ctk.CTkFrame(shell, fg_color=CARD, corner_radius=28)
        card.pack(fill="x", padx=4, pady=8)

        title_label(card, "SOCIA", size=30).pack(pady=(30, 4))
        muted_label(card, "Stay connected with your friends").pack(pady=(0, 24))

        self.username_entry = make_entry(card, "Username")
        self.username_entry.pack(fill="x", padx=24, pady=(0, 12))

        self.password_entry = make_entry(card, "Password", show="*")
        self.password_entry.pack(fill="x", padx=24, pady=(0, 18))

        primary_button(card, "Log In", self._login, width=240).pack(pady=(0, 12))
        secondary_button(card, "Create Account", self.app.show_register, width=240).pack(pady=(0, 28))

        self.username_entry.bind("<Return>", lambda _event: self._login())
        self.password_entry.bind("<Return>", lambda _event: self._login())

    def _login(self):
        try:
            self.app.auth_manager.login(
                self.username_entry.get(),
                self.password_entry.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Login failed", str(exc))
            return
        self.app.show_home()

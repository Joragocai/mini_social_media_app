from tkinter import messagebox

import customtkinter as ctk

from gui.components import (
    BG,
    CARD,
    CONTENT_PAD,
    FIELD,
    MUTED,
    PRIMARY,
    TEXT,
    BottomNav,
    make_entry,
    muted_label,
    primary_button,
    screen_frame,
    secondary_button,
    title_label,
)


class ProfileScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=BG)
        header.pack(fill="x", padx=CONTENT_PAD, pady=(18, 10))
        title_label(header, "Profile", size=28).pack(side="left")
        secondary_button(header, "Log Out", self._logout, width=92).pack(side="right")

        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=24)
        card.pack(fill="x", padx=CONTENT_PAD, pady=(0, 12))

        avatar = ctk.CTkLabel(
            card,
            text=self.app.current_user.display_name[:1].upper(),
            width=76,
            height=76,
            corner_radius=38,
            fg_color=PRIMARY,
            text_color="#ffffff",
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        avatar.pack(pady=(22, 8))

        title_label(card, self.app.current_user.display_name, size=22).pack()
        muted_label(card, f"@{self.app.current_user.username}").pack(pady=(0, 18))

        stats = self.app.post_manager.get_user_stats(self.app.current_user)
        stat_row = ctk.CTkFrame(card, fg_color=FIELD, corner_radius=18)
        stat_row.pack(fill="x", padx=18, pady=(0, 20))
        self._stat(stat_row, str(stats["post_count"]), "Posts")
        self._stat(stat_row, str(stats["likes_received"]), "Likes")
        self._stat(stat_row, str(stats["comment_count"]), "Comments")

        edit_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=24)
        edit_card.pack(fill="both", expand=True, padx=CONTENT_PAD, pady=(0, 10))

        ctk.CTkLabel(
            edit_card,
            text="Edit profile",
            text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=18, pady=(18, 8))

        self.display_entry = make_entry(edit_card, "Display name")
        self.display_entry.insert(0, self.app.current_user.display_name)
        self.display_entry.pack(fill="x", padx=18, pady=(0, 12))

        self.bio_text = ctk.CTkTextbox(
            edit_card,
            height=116,
            fg_color=FIELD,
            text_color=TEXT,
            corner_radius=18,
            wrap="word",
            font=ctk.CTkFont(size=14),
        )
        self.bio_text.insert("1.0", self.app.current_user.bio)
        self.bio_text.pack(fill="both", expand=True, padx=18, pady=(0, 8))
        muted_label(edit_card, "Bio limit: 160 characters", size=12, anchor="w").pack(
            fill="x",
            padx=20,
            pady=(0, 10),
        )
        primary_button(edit_card, "Save Profile", self._save_profile, width=160).pack(pady=(0, 18))

        BottomNav(self, self.app, "profile").pack(fill="x", padx=CONTENT_PAD, pady=(0, 14))

    def _stat(self, master, value, label):
        item = ctk.CTkFrame(master, fg_color="transparent")
        item.pack(side="left", expand=True, fill="x", padx=8, pady=12)
        ctk.CTkLabel(
            item,
            text=value,
            text_color=TEXT,
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack()
        ctk.CTkLabel(
            item,
            text=label,
            text_color=MUTED,
            font=ctk.CTkFont(size=12),
        ).pack()

    def _save_profile(self):
        try:
            self.app.auth_manager.update_profile(
                self.display_entry.get(),
                self.bio_text.get("1.0", "end-1c"),
            )
        except ValueError as exc:
            messagebox.showerror("Profile update failed", str(exc))
            return
        self.app.current_user = self.app.auth_manager.current_user
        messagebox.showinfo("Profile saved", "Your profile has been updated.")
        self.app.show_profile()

    def _logout(self):
        self.app.auth_manager.logout()
        self.app.show_login()

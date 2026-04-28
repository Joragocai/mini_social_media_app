from tkinter import messagebox

import customtkinter as ctk

from gui.components import (
    BG,
    CARD,
    CONTENT_PAD,
    FIELD,
    MUTED,
    TEXT,
    BottomNav,
    muted_label,
    primary_button,
    screen_frame,
    title_label,
)


class CreatePostScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=BG)
        header.pack(fill="x", padx=CONTENT_PAD, pady=(18, 10))
        title_label(header, "Create Post", size=28).pack(anchor="w")
        muted_label(header, "Share a short text update with everyone.", anchor="w").pack(anchor="w")

        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=24)
        card.pack(fill="both", expand=True, padx=CONTENT_PAD, pady=(0, 10))

        ctk.CTkLabel(
            card,
            text="What is on your mind?",
            text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=18, pady=(20, 8))

        self.post_text = ctk.CTkTextbox(
            card,
            height=220,
            fg_color=FIELD,
            border_color=FIELD,
            text_color=TEXT,
            corner_radius=18,
            wrap="word",
            font=ctk.CTkFont(size=15),
        )
        self.post_text.pack(fill="both", expand=True, padx=18, pady=(0, 8))
        self.post_text.bind("<KeyRelease>", lambda _event: self._update_count())

        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=18, pady=(0, 18))
        self.count_label = ctk.CTkLabel(
            footer,
            text="0 / 500",
            text_color=MUTED,
            font=ctk.CTkFont(size=12),
        )
        self.count_label.pack(side="left")
        primary_button(footer, "Publish", self._publish, width=128).pack(side="right")

        BottomNav(self, self.app, "post").pack(fill="x", padx=CONTENT_PAD, pady=(0, 14))

    def _update_count(self):
        length = len(self.post_text.get("1.0", "end-1c").strip())
        self.count_label.configure(text=f"{length} / 500")

    def _publish(self):
        content = self.post_text.get("1.0", "end-1c")
        try:
            self.app.post_manager.create_post(self.app.current_user, content)
        except ValueError as exc:
            messagebox.showerror("Post failed", str(exc))
            return
        messagebox.showinfo("Post created", "Your post is now in the feed.")
        self.app.show_home()

from tkinter import messagebox

import customtkinter as ctk

from gui.components import (
    BG,
    CARD,
    CONTENT_PAD,
    DANGER,
    FIELD,
    MUTED,
    POST_WRAP,
    PRIMARY,
    TEXT,
    BottomNav,
    danger_button,
    format_timestamp,
    muted_label,
    screen_frame,
    secondary_button,
    title_label,
)


class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self._build()
        self.load_feed()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=BG)
        header.pack(fill="x", padx=CONTENT_PAD, pady=(18, 8))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        title_label(left, "Feed", size=28).pack(anchor="w")
        muted_label(left, f"Welcome, {self.app.current_user.display_name}", anchor="w").pack(anchor="w")

        secondary_button(header, "Log Out", self._logout, width=92).pack(side="right", padx=(8, 0))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG, scrollbar_button_color=FIELD)
        self.scroll.pack(fill="both", expand=True, padx=CONTENT_PAD, pady=(0, 8))

        BottomNav(self, self.app, "home").pack(fill="x", padx=CONTENT_PAD, pady=(0, 14))

    def load_feed(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        posts = self.app.post_manager.get_feed(self.app.current_user)
        if not posts:
            empty = ctk.CTkFrame(self.scroll, fg_color=CARD, corner_radius=22)
            empty.pack(fill="x", pady=12)
            title_label(empty, "No posts yet", size=20).pack(pady=(26, 6))
            muted_label(empty, "Create the first post from the Post tab.").pack(pady=(0, 26))
            return

        for post in posts:
            self._add_post_card(post)

    def _add_post_card(self, post):
        card = ctk.CTkFrame(self.scroll, fg_color=CARD, corner_radius=22)
        card.pack(fill="x", pady=(0, 12))

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))

        avatar = ctk.CTkLabel(
            header,
            text=post.display_name[:1].upper(),
            width=42,
            height=42,
            corner_radius=21,
            fg_color=PRIMARY,
            text_color="#ffffff",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        avatar.pack(side="left", padx=(0, 10))

        name_block = ctk.CTkFrame(header, fg_color="transparent")
        name_block.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            name_block,
            text=post.display_name,
            text_color=TEXT,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        ).pack(anchor="w")
        muted_label(
            name_block,
            f"@{post.username} - {format_timestamp(post.created_at)}",
            size=12,
            anchor="w",
        ).pack(anchor="w")

        content = ctk.CTkLabel(
            card,
            text=post.content,
            text_color=TEXT,
            font=ctk.CTkFont(size=15),
            wraplength=POST_WRAP,
            justify="left",
            anchor="w",
        )
        content.pack(fill="x", padx=16, pady=(4, 12))

        stats = ctk.CTkFrame(card, fg_color="transparent")
        stats.pack(fill="x", padx=16, pady=(0, 10))
        muted_label(stats, f"{post.like_count} likes", size=12, anchor="w").pack(side="left")
        muted_label(stats, f"{post.comment_count} comments", size=12, anchor="e").pack(side="right")

        actions = ctk.CTkFrame(card, fg_color=FIELD, corner_radius=16)
        actions.pack(fill="x", padx=16, pady=(0, 16))

        like_text = "Unlike" if post.liked_by_current_user else "Like"
        like_color = DANGER if post.liked_by_current_user else PRIMARY
        ctk.CTkButton(
            actions,
            text=like_text,
            command=lambda post_id=post.id: self._toggle_like(post_id),
            height=36,
            fg_color=like_color,
            hover_color=like_color,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left", expand=True, fill="x", padx=6, pady=6)

        secondary_button(
            actions,
            "Comment",
            lambda post_id=post.id: self.app.show_comments(post_id),
            width=98,
        ).pack(side="left", expand=True, fill="x", padx=6, pady=6)

        if post.user_id == self.app.current_user.id:
            danger_button(
                actions,
                "Delete",
                lambda post_id=post.id: self._delete_post(post_id),
                width=86,
            ).pack(side="left", expand=True, fill="x", padx=6, pady=6)

    def _toggle_like(self, post_id):
        try:
            self.app.post_manager.toggle_like(self.app.current_user, post_id)
        except ValueError as exc:
            messagebox.showerror("Like failed", str(exc))
            return
        self.load_feed()

    def _delete_post(self, post_id):
        if not messagebox.askyesno("Delete post", "Delete this post and its comments?"):
            return
        try:
            self.app.post_manager.delete_post(self.app.current_user, post_id)
        except ValueError as exc:
            messagebox.showerror("Delete failed", str(exc))
            return
        self.load_feed()

    def _logout(self):
        self.app.auth_manager.logout()
        self.app.show_login()

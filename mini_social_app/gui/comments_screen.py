from tkinter import messagebox

import customtkinter as ctk

from gui.components import (
    BG,
    CARD,
    CONTENT_PAD,
    FIELD,
    MUTED,
    POST_WRAP,
    PRIMARY,
    TEXT,
    format_timestamp,
    muted_label,
    primary_button,
    screen_frame,
    secondary_button,
    title_label,
)


class CommentsScreen(ctk.CTkFrame):
    def __init__(self, master, app, post_id):
        super().__init__(master, **screen_frame(master))
        self.app = app
        self.post_id = post_id
        self.post = self.app.post_manager.get_post(post_id, self.app.current_user)
        self._build()
        self.load_comments()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=BG)
        header.pack(fill="x", padx=CONTENT_PAD, pady=(18, 10))
        secondary_button(header, "Back", self.app.show_home, width=80).pack(side="left")
        title_label(header, "Comments", size=24).pack(side="left", padx=12)

        if self.post is None:
            missing = ctk.CTkFrame(self, fg_color=CARD, corner_radius=24)
            missing.pack(fill="both", expand=True, padx=CONTENT_PAD, pady=CONTENT_PAD)
            title_label(missing, "Post not found", size=20).pack(pady=(40, 8))
            muted_label(missing, "It may have been deleted.").pack()
            return

        post_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=22)
        post_card.pack(fill="x", padx=CONTENT_PAD, pady=(0, 10))
        ctk.CTkLabel(
            post_card,
            text=self.post.display_name,
            text_color=TEXT,
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 0))
        muted_label(
            post_card,
            f"@{self.post.username} - {format_timestamp(self.post.created_at)}",
            size=12,
            anchor="w",
        ).pack(fill="x", padx=16)
        ctk.CTkLabel(
            post_card,
            text=self.post.content,
            text_color=TEXT,
            font=ctk.CTkFont(size=14),
            wraplength=POST_WRAP,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=16, pady=(10, 14))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=BG, scrollbar_button_color=FIELD)
        self.scroll.pack(fill="both", expand=True, padx=CONTENT_PAD, pady=(0, 10))

        composer = ctk.CTkFrame(self, fg_color=CARD, corner_radius=22)
        composer.pack(fill="x", padx=CONTENT_PAD, pady=(0, 14))
        self.comment_text = ctk.CTkTextbox(
            composer,
            height=76,
            fg_color=FIELD,
            text_color=TEXT,
            corner_radius=16,
            wrap="word",
            font=ctk.CTkFont(size=14),
        )
        self.comment_text.pack(side="left", fill="both", expand=True, padx=(12, 8), pady=12)
        primary_button(composer, "Send", self._send_comment, width=80).pack(side="right", padx=(0, 12), pady=12)

    def load_comments(self):
        if self.post is None:
            return
        for child in self.scroll.winfo_children():
            child.destroy()

        comments = self.app.post_manager.get_comments(self.post_id)
        if not comments:
            empty = ctk.CTkFrame(self.scroll, fg_color=CARD, corner_radius=18)
            empty.pack(fill="x", pady=8)
            muted_label(empty, "No comments yet. Start the conversation.").pack(pady=20)
            return

        for comment in comments:
            self._add_comment(comment)

    def _add_comment(self, comment):
        card = ctk.CTkFrame(self.scroll, fg_color=CARD, corner_radius=18)
        card.pack(fill="x", pady=(0, 10))

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 2))

        badge = ctk.CTkLabel(
            header,
            text=comment.display_name[:1].upper(),
            width=30,
            height=30,
            corner_radius=15,
            fg_color=PRIMARY,
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        badge.pack(side="left", padx=(0, 8))

        name = ctk.CTkFrame(header, fg_color="transparent")
        name.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            name,
            text=comment.display_name,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).pack(anchor="w")
        muted_label(name, format_timestamp(comment.created_at), size=11, anchor="w").pack(anchor="w")

        ctk.CTkLabel(
            card,
            text=comment.content,
            text_color=TEXT,
            font=ctk.CTkFont(size=14),
            wraplength=POST_WRAP,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(6, 14))

    def _send_comment(self):
        try:
            self.app.post_manager.add_comment(
                self.app.current_user,
                self.post_id,
                self.comment_text.get("1.0", "end-1c"),
            )
        except ValueError as exc:
            messagebox.showerror("Comment failed", str(exc))
            return
        self.comment_text.delete("1.0", "end")
        self.load_comments()

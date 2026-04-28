import customtkinter as ctk

from auth import AuthManager
from database import StorageManager
from gui.comments_screen import CommentsScreen
from gui.create_post_screen import CreatePostScreen
from gui.home_screen import HomeScreen
from gui.login_screen import LoginScreen
from gui.profile_screen import ProfileScreen
from gui.register_screen import RegisterScreen
from posts import PostManager


class MiniSocialApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Socia")
        self.geometry("430x760")
        self.minsize(390, 680)

        self.storage = StorageManager()
        self.auth_manager = AuthManager(self.storage)
        self.post_manager = PostManager(self.storage)
        self.current_frame = None

        self.show_login()

    @property
    def current_user(self):
        return self.auth_manager.current_user

    @current_user.setter
    def current_user(self, user):
        self.auth_manager.current_user = user

    def _show_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self._show_frame(LoginScreen)

    def show_register(self):
        self._show_frame(RegisterScreen)

    def show_home(self):
        if self.current_user is None:
            self.show_login()
            return
        self._show_frame(HomeScreen)

    def show_create_post(self):
        if self.current_user is None:
            self.show_login()
            return
        self._show_frame(CreatePostScreen)

    def show_profile(self):
        if self.current_user is None:
            self.show_login()
            return
        self._show_frame(ProfileScreen)

    def show_comments(self, post_id):
        if self.current_user is None:
            self.show_login()
            return
        self._show_frame(CommentsScreen, post_id)


if __name__ == "__main__":
    app = MiniSocialApp()
    app.mainloop()

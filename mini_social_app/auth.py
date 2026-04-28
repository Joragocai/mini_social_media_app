import hashlib
import os
import re
import hmac
from models import User


USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,20}$")


class AuthManager:
    """Application logic for registration, login, logout, and profile edits."""

    def __init__(self, storage):
        self.storage = storage
        self.current_user = None

    def register(self, username, password, confirm_password, display_name):
        username = username.strip()
        display_name = display_name.strip() or username

        if not USERNAME_PATTERN.match(username):
            raise ValueError("Username must be 3-20 letters, numbers, or underscores.")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if password != confirm_password:
            raise ValueError("Passwords do not match.")
        if len(display_name) > 50:
            raise ValueError("Display name must be 50 characters or fewer.")

        row = self.storage.create_user(
            username=username,
            password_hash=self._hash_password(password),
            display_name=display_name,
        )
        self.current_user = User.from_row(row)
        return self.current_user

    def login(self, username, password):
        username = username.strip()
        if not username or not password:
            raise ValueError("Enter your username and password.")

        row = self.storage.get_user_by_username(username)
        if row is None or not self._verify_password(password, row["password_hash"]):
            raise ValueError("Invalid username or password.")

        self.current_user = User.from_row(row)
        return self.current_user

    def logout(self):
        self.current_user = None

    def update_profile(self, display_name, bio):
        if self.current_user is None:
            raise ValueError("You must be logged in to edit your profile.")

        display_name = display_name.strip()
        bio = bio.strip()
        if not display_name:
            raise ValueError("Display name is required.")
        if len(display_name) > 50:
            raise ValueError("Display name must be 50 characters or fewer.")
        if len(bio) > 160:
            raise ValueError("Bio must be 160 characters or fewer.")

        row = self.storage.update_user_profile(self.current_user.id, display_name, bio)
        self.current_user = User.from_row(row)
        return self.current_user

    def _hash_password(self, password):
        salt = os.urandom(16).hex()
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            120000,
        ).hex()
        return f"pbkdf2_sha256${salt}${digest}"

    def _verify_password(self, password, stored_hash):
        try:
            algorithm, salt, expected_digest = stored_hash.split("$", 2)
        except ValueError:
            return False

        if algorithm != "pbkdf2_sha256":
            return False

        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            120000,
        ).hex()
        return hmac.compare_digest(actual_digest, expected_digest)

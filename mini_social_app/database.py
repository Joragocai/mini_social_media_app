import sqlite3
from contextlib import contextmanager
from pathlib import Path


class StorageManager:
    """SQLite data access layer for users, posts, likes, and comments."""

    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("social_app.db")
        self.initialize_database()

    @contextmanager
    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize_database(self):
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    bio TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS likes (
                    user_id INTEGER NOT NULL,
                    post_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, post_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
                CREATE INDEX IF NOT EXISTS idx_likes_post_id ON likes(post_id);
                """
            )

    def create_user(self, username, password_hash, display_name, bio=""):
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (username, password_hash, display_name, bio)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, password_hash, display_name, bio),
                )
                user_id = cursor.lastrowid
            return self.get_user_by_id(user_id)
        except sqlite3.IntegrityError as exc:
            raise ValueError("That username is already taken.") from exc

    def get_user_by_username(self, username):
        with self._connect() as connection:
            return connection.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,),
            ).fetchone()

    def get_user_by_id(self, user_id):
        with self._connect() as connection:
            return connection.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()

    def update_user_profile(self, user_id, display_name, bio):
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE users
                SET display_name = ?, bio = ?
                WHERE id = ?
                """,
                (display_name, bio, user_id),
            )
        return self.get_user_by_id(user_id)

    def create_post(self, user_id, content):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO posts (user_id, content)
                VALUES (?, ?)
                """,
                (user_id, content),
            )
            return cursor.lastrowid

    def get_post(self, post_id, current_user_id=None):
        with self._connect() as connection:
            return connection.execute(
                self._post_select_sql("WHERE p.id = ?"),
                (current_user_id or 0, post_id),
            ).fetchone()

    def get_all_posts(self, current_user_id=None):
        with self._connect() as connection:
            return connection.execute(
                self._post_select_sql(""),
                (current_user_id or 0,),
            ).fetchall()

    def delete_post(self, post_id, user_id):
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM posts WHERE id = ? AND user_id = ?",
                (post_id, user_id),
            )
            return cursor.rowcount > 0

    def add_like(self, user_id, post_id):
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO likes (user_id, post_id)
                VALUES (?, ?)
                """,
                (user_id, post_id),
            )

    def remove_like(self, user_id, post_id):
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM likes WHERE user_id = ? AND post_id = ?",
                (user_id, post_id),
            )

    def has_like(self, user_id, post_id):
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?",
                (user_id, post_id),
            ).fetchone()
            return row is not None

    def add_comment(self, user_id, post_id, content):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO comments (post_id, user_id, content)
                VALUES (?, ?, ?)
                """,
                (post_id, user_id, content),
            )
            return cursor.lastrowid

    def get_comments_for_post(self, post_id):
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT
                    c.id,
                    c.post_id,
                    c.user_id,
                    c.content,
                    c.created_at,
                    u.username,
                    u.display_name
                FROM comments c
                JOIN users u ON u.id = c.user_id
                WHERE c.post_id = ?
                ORDER BY c.created_at ASC, c.id ASC
                """,
                (post_id,),
            ).fetchall()

    def get_user_stats(self, user_id):
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM posts WHERE user_id = ?) AS post_count,
                    (
                        SELECT COUNT(*)
                        FROM likes l
                        JOIN posts p ON p.id = l.post_id
                        WHERE p.user_id = ?
                    ) AS likes_received,
                    (SELECT COUNT(*) FROM comments WHERE user_id = ?) AS comment_count
                """,
                (user_id, user_id, user_id),
            ).fetchone()

    def _post_select_sql(self, where_clause):
        return f"""
            SELECT
                p.id,
                p.user_id,
                p.content,
                p.created_at,
                u.username,
                u.display_name,
                COUNT(DISTINCT l.user_id) AS like_count,
                COUNT(DISTINCT c.id) AS comment_count,
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM likes current_like
                        WHERE current_like.user_id = ?
                        AND current_like.post_id = p.id
                    )
                    THEN 1
                    ELSE 0
                END AS liked_by_current_user
            FROM posts p
            JOIN users u ON u.id = p.user_id
            LEFT JOIN likes l ON l.post_id = p.id
            LEFT JOIN comments c ON c.post_id = p.id
            {where_clause}
            GROUP BY p.id
            ORDER BY p.created_at DESC, p.id DESC
        """

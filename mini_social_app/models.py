from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    display_name: str
    bio: str
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            display_name=row["display_name"],
            bio=row["bio"] or "",
            created_at=row["created_at"],
        )


@dataclass
class Post:
    id: int
    user_id: int
    content: str
    created_at: str
    username: str
    display_name: str
    like_count: int = 0
    comment_count: int = 0
    liked_by_current_user: bool = False

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            content=row["content"],
            created_at=row["created_at"],
            username=row["username"],
            display_name=row["display_name"],
            like_count=row["like_count"],
            comment_count=row["comment_count"],
            liked_by_current_user=bool(row["liked_by_current_user"]),
        )


@dataclass
class Comment:
    id: int
    post_id: int
    user_id: int
    content: str
    created_at: str
    username: str
    display_name: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            post_id=row["post_id"],
            user_id=row["user_id"],
            content=row["content"],
            created_at=row["created_at"],
            username=row["username"],
            display_name=row["display_name"],
        )

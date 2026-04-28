from models import Comment, Post


class PostManager:
    """Application logic for posts, likes, comments, and feed retrieval."""

    def __init__(self, storage):
        self.storage = storage

    def create_post(self, user, content):
        self._require_user(user)
        content = content.strip()
        if not content:
            raise ValueError("Post content cannot be empty.")
        if len(content) > 500:
            raise ValueError("Posts must be 500 characters or fewer.")
        return self.storage.create_post(user.id, content)

    def get_feed(self, current_user):
        current_user_id = current_user.id if current_user else None
        return [Post.from_row(row) for row in self.storage.get_all_posts(current_user_id)]

    def get_post(self, post_id, current_user):
        current_user_id = current_user.id if current_user else None
        row = self.storage.get_post(post_id, current_user_id)
        return Post.from_row(row) if row else None

    def delete_post(self, user, post_id):
        self._require_user(user)
        deleted = self.storage.delete_post(post_id, user.id)
        if not deleted:
            raise ValueError("You can delete only your own posts.")
        return True

    def toggle_like(self, user, post_id):
        self._require_user(user)
        if self.storage.has_like(user.id, post_id):
            self.storage.remove_like(user.id, post_id)
            return False
        self.storage.add_like(user.id, post_id)
        return True

    def add_comment(self, user, post_id, content):
        self._require_user(user)
        content = content.strip()
        if not content:
            raise ValueError("Comment cannot be empty.")
        if len(content) > 240:
            raise ValueError("Comments must be 240 characters or fewer.")
        return self.storage.add_comment(user.id, post_id, content)

    def get_comments(self, post_id):
        return [Comment.from_row(row) for row in self.storage.get_comments_for_post(post_id)]

    def get_user_stats(self, user):
        self._require_user(user)
        row = self.storage.get_user_stats(user.id)
        return {
            "post_count": row["post_count"],
            "likes_received": row["likes_received"],
            "comment_count": row["comment_count"],
        }

    def _require_user(self, user):
        if user is None:
            raise ValueError("You must be logged in for this action.")

# Mini Social App

A lightweight desktop social media application built with Python, CustomTkinter, SQLite, and a layered architecture.

## Features

- Register and log in
- View a scrollable feed
- Create text posts
- Delete your own posts
- Like and unlike posts
- Add and view comments
- View and edit your profile
- Persist data in SQLite

## Project Structure

```text
mini_social_app/
|-- main.py
|-- database.py
|-- models.py
|-- auth.py
|-- posts.py
|-- requirements.txt
|-- gui/
|   |-- login_screen.py
|   |-- register_screen.py
|   |-- home_screen.py
|   |-- create_post_screen.py
|   |-- profile_screen.py
|   |-- comments_screen.py
|   `-- components.py
`-- assets/
```

## Run Steps

1. Open a terminal in the project folder:

   ```bash
   cd mini_social_app
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python main.py
   ```

The database file `social_app.db` is created automatically beside `main.py` the first time the app starts.

## Database Tables

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    bio TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE likes (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

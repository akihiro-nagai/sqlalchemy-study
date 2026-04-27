#!/usr/bin/env python
"""SQLAlchemy study console — Rails console 風の対話環境"""
from sqlalchemy import select, text

from blog.database import AUTOBEGIN, Session, engine
from blog.dto import BlogWithTags, TagData
from blog.mapping import setup_mappers, posts_table, tags_table, post_tags_table
from blog.models import Base, Comment, Post, Tag, User

# テーブルが存在しない場合は自動作成
Base.metadata.create_all(engine)

# Data Mapper パターンのマッピングを有効化
setup_mappers()

session = Session()

print("=" * 60)
print("SQLAlchemy Study Console")
print(f"  autobegin = {AUTOBEGIN}  (blog/database.py の AUTOBEGIN で切替)")
print("=" * 60)
print("利用可能なオブジェクト:")
print("  session          - SQLAlchemy セッション")
print("  select, text     - sqlalchemy の select / text")
print("  User, Post, Comment, Tag - Declarative モデル")
print("  BlogWithTags, TagData    - Data Mapper DTO")
print("  posts_table, tags_table, post_tags_table - Table オブジェクト")
print("  engine           - DB エンジン (echo=True でSQL出力済み)")
print("=" * 60)
print()

import IPython
IPython.start_ipython(argv=[], user_ns={
    "Session": Session,
    "session": session,
    "select": select,
    "text": text,
    "engine": engine,
    "User": User,
    "Post": Post,
    "Comment": Comment,
    "Tag": Tag,
    "Base": Base,
    "BlogWithTags": BlogWithTags,
    "TagData": TagData,
    "posts_table": posts_table,
    "tags_table": tags_table,
    "post_tags_table": post_tags_table,
})

session.close()

#!/usr/bin/env python
"""サンプルデータ投入スクリプト"""
from datetime import datetime, timedelta

from blog.database import Session, engine
from blog.models import Base, Comment, Post, Tag, User

Base.metadata.create_all(engine)

session = Session()

# 既存データをクリア
for model in [Comment, Post, User, Tag]:
    session.query(model).delete()
session.commit()

# タグ
tags = {name: Tag(name=name) for name in ["Python", "SQLAlchemy", "MySQL", "Web"]}
session.add_all(tags.values())

# ユーザー
alice = User(name="Alice", email="alice@example.com")
bob = User(name="Bob", email="bob@example.com")
carol = User(name="Carol", email="carol@example.com")
session.add_all([alice, bob, carol])
session.flush()

# 投稿
post1 = Post(
    user_id=alice.id,
    title="SQLAlchemy 2.0 入門",
    body="SQLAlchemy 2.0 では mapped_column と Mapped を使った型安全なモデル定義が推奨されています。",
    published_at=datetime.now() - timedelta(days=5),
    tags=[tags["Python"], tags["SQLAlchemy"]],
)
post2 = Post(
    user_id=alice.id,
    title="MySQL と SQLAlchemy の接続設定",
    body="PyMySQL を使うと純 Python で MySQL に接続できます。",
    published_at=datetime.now() - timedelta(days=3),
    tags=[tags["MySQL"], tags["SQLAlchemy"]],
)
post3 = Post(
    user_id=bob.id,
    title="ORM と生 SQL の使い分け",
    body="複雑な集計クエリは text() や Core API が便利です。",
    tags=[tags["Python"], tags["Web"]],
)
session.add_all([post1, post2, post3])
session.flush()

# コメント
session.add_all([
    Comment(post_id=post1.id, user_id=bob.id, body="わかりやすい解説ありがとうございます！"),
    Comment(post_id=post1.id, user_id=carol.id, body="relationship の設定が参考になりました。"),
    Comment(post_id=post2.id, user_id=carol.id, body="cryptography パッケージも必要ですよね。"),
    Comment(post_id=post3.id, user_id=alice.id, body="select() の使い方も知りたいです。"),
])

session.commit()
session.close()
print("シードデータを投入しました。")

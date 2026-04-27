"""
SQLAlchemy Data Mapper パターンのデモ

Declarative (Active Record 的) との違い:
  - ドメインオブジェクト (BlogWithTags, TagData) は ORM を一切知らない
  - テーブル定義 → ドメインクラス → マッピング の 3 層が分離されている
  - ドメインクラスは普通の dataclass なのでテストやシリアライズが容易

注意: 既存の Declarative モデル (Post, Tag) と同じテーブルを使うため、
      このスクリプトは Declarative モデルを import せずに単独で動かす。
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, registry, relationship

from blog.dto import BlogWithTags, TagData

# =========================================================
# 1. テーブル定義 (スキーマ層 — ドメインから独立)
# =========================================================
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(255), unique=True, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

posts_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("title", String(255), nullable=False),
    Column("body", Text, nullable=False),
    Column("published_at", DateTime, nullable=True),
    Column("created_at", DateTime, nullable=False),
)

tags_table = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True, nullable=False),
)

post_tags_table = Table(
    "post_tags",
    metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

# =========================================================
# 2. マッピング (ドメインオブジェクト ↔ テーブルの橋渡し)
# =========================================================
mapper_registry = registry()


def setup_mappers() -> None:
    """ドメインクラスをテーブルに紐付ける (一度だけ呼ぶ)"""
    mapper_registry.map_imperatively(TagData, tags_table)
    mapper_registry.map_imperatively(
        BlogWithTags,
        posts_table,
        properties={
            "tags": relationship(TagData, secondary=post_tags_table),
        },
    )


# =========================================================
# 3. デモ
# =========================================================
def main() -> None:
    engine = create_engine(
        "mysql+pymysql://blog:blog@127.0.0.1:3306/blog",
        echo=True,
    )
    setup_mappers()

    with Session(engine) as session:
        # --- 全件取得 ---
        print("\n" + "=" * 60)
        print("全件取得")
        print("=" * 60)
        blogs = session.scalars(select(BlogWithTags)).all()
        for blog in blogs:
            print(f"  {blog}")
            print(f"    published={blog.is_published}, tag_names={blog.tag_names}")

        # --- タグで絞り込み ---
        print("\n" + "=" * 60)
        print("'Python' タグが付いた記事")
        print("=" * 60)
        stmt = (
            select(BlogWithTags)
            .join(post_tags_table)
            .join(tags_table)
            .where(tags_table.c.name == "Python")
        )
        for blog in session.scalars(stmt):
            print(f"  {blog}")

        # --- 新規作成 ---
        print("\n" + "=" * 60)
        print("新規作成")
        print("=" * 60)
        python_tag = session.scalars(
            select(TagData).where(TagData.name == "Python")
        ).first()

        new_blog = BlogWithTags(
            title="Data Mapper Pattern in SQLAlchemy",
            body="Imperative mapping で純粋なデータクラスを DB にマッピングする例",
            user_id=1,
            created_at=datetime.now(),
            tags=[python_tag] if python_tag else [],
        )
        session.add(new_blog)
        session.flush()
        print(f"  Created: {new_blog}")
        print(f"  is_published={new_blog.is_published}")
        print(f"  tag_names={new_blog.tag_names}")

        # デモなのでロールバック
        session.rollback()
        print("  (rollback)")


if __name__ == "__main__":
    main()

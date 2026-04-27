"""
ドメインオブジェクト定義 (Data Mapper パターン)

ここで定義するクラスは SQLAlchemy に一切依存しない純粋な Python データクラス。
テストやシリアライズが容易で、ORM なしでも単体で使える。
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TagData:
    id: int | None = None
    name: str = ""

    def __repr__(self) -> str:
        return f"TagData(id={self.id}, name={self.name!r})"


@dataclass
class BlogWithTags:
    id: int | None = None
    title: str = ""
    body: str = ""
    user_id: int | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    tags: list[TagData] = field(default_factory=list)

    def __repr__(self) -> str:
        tag_names = [t.name for t in self.tags]
        return f"BlogWithTags(id={self.id}, title={self.title!r}, tags={tag_names})"

    @property
    def tag_names(self) -> list[str]:
        return [t.name for t in self.tags]

    @property
    def is_published(self) -> bool:
        return self.published_at is not None

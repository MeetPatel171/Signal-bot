"""Reader-layer dataclasses. See plan §4.1."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Attachment:
    url: str
    local_path: str | None
    mime_type: str | None
    size_bytes: int | None


@dataclass
class Embed:
    url: str
    title: str | None
    description: str | None
    image_url: str | None
    provider: str | None


@dataclass
class Message:
    id: str
    channel_id: str
    channel_name: str
    author: str
    timestamp: datetime
    content: str
    reply_to_id: str | None
    attachments: list[Attachment]
    embeds: list[Embed]
    raw_html: str

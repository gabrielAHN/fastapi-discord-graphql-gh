import strawberry

from typing import Optional, List
from datetime import datetime

@strawberry.type
class ChannelMessageType:
    message_id: str
    author: str
    content: str
    timestamp: datetime
    channel_id: str
    channel_name: str
    thread_name: Optional[str]
    thread_id: Optional[str]
    thread_status: Optional[str]
    message_type: str


@strawberry.input
class MessageFilterInput:
    category_channel: str
    thread_id : Optional[str] = None
    channel_id : Optional[str] = None
    authors: Optional[List[str]] = None
    message_types: Optional[List[str]] = None
    channel_names: Optional[List[str]] = None
    content: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    thread_exist: Optional[bool] = None


@strawberry.type
class AuthorMessageType:
    author: str

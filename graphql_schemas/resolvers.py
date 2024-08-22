import asyncio
import discord

from typing import List, Optional
from graphql_schemas.object_types import (
    ChannelMessageType,
    MessageFilterInput,
)


async def LatestChannelsMessagesResolver(category, filters: Optional[MessageFilterInput] = None) -> List[ChannelMessageType]:
    all_messages = []

    def message_matches_filters(message: ChannelMessageType) -> bool:
        if message.content == "":
            return False

        if filters:
            if filters.thread_id and message.thread_id != filters.thread_id:
                return False
            if filters.channel_id and message.channel_id != filters.channel_id:
                return False
            if filters.message_types and message.message_type not in filters.message_types:
                return False
            if filters.authors and message.author not in filters.authors:
                return False
            if filters.channel_names and message.channel_name not in filters.channel_names:
                return False
            if filters.content and filters.content not in message.content:
                return False
            if filters.start_time and filters.end_time:
                if not (filters.start_time <= message.timestamp <= filters.end_time):
                    return False
            if filters.thread_exist is not None:
                if filters.thread_exist and not message.thread_id:
                    return False
                if not filters.thread_exist and message.thread_id:
                    return False
        return True

    async def fetch_channel_messages(channel):
        messages = []
        append_message = messages.append

        async for message in channel.history(limit=None):
            thread_name = str(message.thread.name) if message.thread else None
            thread_id = str(message.thread.id) if message.thread else None

            if message.type == discord.MessageType.thread_created:
                message_type = 'threadstarters'
                thread_status = '✅'
            if message.type == discord.MessageType.reply:
                message_type = 'message'
            else:
                if message.reference:
                    thread_status = '✅'
                    message_type = 'thread'
                else:
                    message_type = 'message'
                    thread_status = '❌'

            new_message = ChannelMessageType(
                message_id=str(message.id),
                author=message.author.name,
                content=message.content,
                timestamp=message.created_at,
                channel_id=str(channel.id),
                channel_name=channel.name,
                thread_name=thread_name,
                thread_id=thread_id,
                thread_status=thread_status,
                message_type=message_type
            )

            if message_matches_filters(new_message):
                append_message(new_message)

            if message.thread:
                print(f"Processing thread: {message.thread.name}")
                async for thread_message in message.thread.history(limit=None):
                    thread_message_instance = ChannelMessageType(
                        message_id=str(thread_message.id),
                        author=thread_message.author.name,
                        content=thread_message.content,
                        timestamp=thread_message.created_at,
                        channel_id=str(channel.id),
                        channel_name=channel.name,
                        thread_name=thread_name,
                        thread_id=thread_id,
                        thread_status=None,
                        message_type='thread'
                    )

                    if message_matches_filters(thread_message_instance):
                        append_message(thread_message_instance)

        return messages

    tasks = [fetch_channel_messages(channel)
             for channel in category.text_channels]
    results = await asyncio.gather(*tasks)

    all_messages = [message for result in results for message in result]

    all_messages.sort(key=lambda m: m.timestamp, reverse=True)

    return all_messages


async def MessageInfoResolver(category: discord.CategoryChannel, message_id: int) -> Optional[ChannelMessageType]:
    for channel in category.text_channels:
        try:
            # Initialize message_type with a default value
            message_type = 'message'

            message = await channel.fetch_message(message_id)

            if message.thread:
                thread_status = '✅'
            elif message.reference:
                thread_status = '✅'
                message_type = 'thread'
            else:
                thread_status = '❌'

            return ChannelMessageType(
                message_id=str(message.id),
                author=message.author.name,
                content=message.content,
                timestamp=message.created_at,
                channel_id=str(message.channel.id),
                channel_name=message.channel.name,
                thread_name=str(
                    message.thread.name) if message.thread else None,
                thread_id=str(message.thread.id) if message.thread else None,
                thread_status=thread_status,
                message_type=message_type
            )
        except discord.NotFound:
            pass

        for thread in channel.threads:
            try:
                message = await thread.fetch_message(message_id)
                return ChannelMessageType(
                    message_id=str(message.id),
                    author=message.author.name,
                    content=message.content,
                    timestamp=message.created_at,
                    channel_id=str(message.channel.id),
                    channel_name=message.channel.name,
                    thread_name=thread.name,
                    thread_id=str(thread.id),
                    thread_status=None,
                    message_type='thread'
                )
            except discord.NotFound:
                continue
    raise ValueError("Message not found in the category channels or threads.")

import asyncio
import discord
import strawberry

from typing import List, Optional
from discord_bot.bot import bot
from .object_types import (
    ChannelMessageType
)
from .resolvers import (
    LatestChannelsMessagesResolver,
    MessageInfoResolver,
    MessageFilterInput
)


@strawberry.type
class Query:

    @strawberry.field
    async def getAllCategoryMessages(
        self,
        filters: Optional[MessageFilterInput] = None
    ) -> List[ChannelMessageType]:
        await bot.wait_until_ready()

        category = bot.get_channel(int(filters.category_channel))
        if category is None or not isinstance(category, discord.CategoryChannel):
            raise ValueError("Category channel not found or invalid.")
        future = asyncio.run_coroutine_threadsafe(
            LatestChannelsMessagesResolver(category, filters=filters), bot.loop)

        return future.result()

    @strawberry.field
    async def getMessageInfo(
        self,
        CategoryId: str,
        MessageId: str
    ) -> ChannelMessageType:
        await bot.wait_until_ready()

        category = bot.get_channel(int(CategoryId))

        future = asyncio.run_coroutine_threadsafe(
            MessageInfoResolver(category, MessageId), bot.loop)
        return future.result()

    @strawberry.field
    async def GetAuthorsOfChannel(
        self,
        category_id: str
    ) -> List[str]:
        await bot.wait_until_ready()

        async def fetch_unique_authors():
            category = bot.get_channel(int(category_id))
            if category is None or not isinstance(category, discord.CategoryChannel):
                return "Category not found or is not a category channel."

            unique_authors = set()

            for channel in category.text_channels:
                async for message in channel.history(limit=None):
                    unique_authors.add(message.author.name)

            return list(unique_authors)

        result = await asyncio.wrap_future(
            asyncio.run_coroutine_threadsafe(
                fetch_unique_authors(), bot.loop)
        )

        return result

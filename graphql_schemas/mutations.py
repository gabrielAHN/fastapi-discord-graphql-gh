import discord
import asyncio
import strawberry

from discord_bot.bot import bot


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def SendMessage(self, channel_id: str, content: str) -> str:
        await bot.wait_until_ready()

        channel = bot.get_channel(int(channel_id))
        if channel is None:
            return "Channel not found."

        try:
            future = asyncio.run_coroutine_threadsafe(
                channel.send(content), bot.loop)
            future.result()
            return "Message sent!"
        except Exception as e:
            return f"Failed to send message: {str(e)}"

    @strawberry.mutation
    async def CreateThread(
        self,
        channel_id: str,
        message_id: str,
        thread_name: str,
        thread_message: str
    ) -> str:
        await bot.wait_until_ready()

        async def create_thread_task():
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                return "Channel not found."

            try:
                message = await channel.fetch_message(int(message_id))
                if message.type != discord.MessageType.default:
                    return "The message type does not support thread creation."

            except discord.NotFound:
                return "Message not found."
            except Exception as e:
                return f"Failed to fetch message: {str(e)}"

            try:
                thread = await message.create_thread(name=thread_name)
            except Exception as e:
                return f"Failed to create thread or send message: {str(e)}"

            try:
                message = await thread.send(thread_message)
                return f"Thread '{thread_name}' created and message sent in the thread!"
            except Exception as e:
                return f"Failed to send message in the thread: {str(e)}"

        return await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(create_thread_task(), bot.loop))

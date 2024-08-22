import os
import threading
import asyncio
import hypercorn.asyncio
import strawberry

from hypercorn.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from discord_bot.bot import bot, DISCORD_TOKEN
from graphql_schemas.queries import Query
from graphql_schemas.mutations import Mutation
from dotenv import load_dotenv

load_dotenv()

WEBSITE_URL = os.getenv("WEBSITE_URL")


def start_discord_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot.run(DISCORD_TOKEN)

discord_thread = threading.Thread(target=start_discord_bot, daemon=True)
discord_thread.start()

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()

origins = ['https://{WEBSITE_URL}']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"Hello": "World railway 🚂"}


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
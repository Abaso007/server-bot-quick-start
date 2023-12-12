from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from modal import Image, Stub, asgi_app


class LangchainOpenAIChatBot(fp.PoeBot):
    def __init__(self, OPENAI_API_KEY: str):
        self.chat_model = ChatOpenAI(api_key=OPENAI_API_KEY)

    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        messages = []
        for message in request.query:
            if message.role == "bot":
                messages.append(AIMessage(content=message.content))
            elif message.role == "system":
                messages.append(SystemMessage(content=message.content))
            elif message.role == "user":
                messages.append(HumanMessage(content=message.content))

        response = self.chat_model.predict_messages(messages).content
        if isinstance(response, str):
            yield fp.PartialResponse(text=response)
        else:
            yield fp.PartialResponse(text="There was an issue processing your query.")


REQUIREMENTS = ["fastapi-poe==0.0.24", "langchain==0.0.330", "openai==0.28.1"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("langchain-openai-poe")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    OPENAI_API_KEY = "<your key>"
    bot = LangchainOpenAIChatBot(OPENAI_API_KEY=OPENAI_API_KEY)
    return fp.make_app(bot, allow_without_key=True)

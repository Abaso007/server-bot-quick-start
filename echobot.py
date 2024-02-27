"""

Sample bot that echoes back messages.

This is the simplest possible bot and a great place to start if you want to build your own bot.

"""

from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app


class EchoBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        last_message = request.query[-1].content
        yield fp.PartialResponse(text=last_message)


REQUIREMENTS = ["fastapi-poe==0.0.25"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("echobot-poe")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = EchoBot()
    return fp.make_app(bot, allow_without_key=True)

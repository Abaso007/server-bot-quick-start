"""

Sample bot that wraps GPT-3.5-Turbo but makes responses use all-caps.

"""

from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app


class GPT35TurboAllCapsBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        async for msg in fp.stream_request(
            request, "GPT-3.5-Turbo", request.access_key
        ):
            yield msg.model_copy(update={"text": msg.text.upper()})

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        return fp.SettingsResponse(server_bot_dependencies={"GPT-3.5-Turbo": 1})


REQUIREMENTS = ["fastapi-poe==0.0.24"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("turbo-allcaps-poe")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = GPT35TurboAllCapsBot()
    return fp.make_app(bot, allow_without_key=True)

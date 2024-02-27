from __future__ import annotations

from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, asgi_app

IMAGE_URL = (
    "https://images.pexels.com/photos/46254/leopard-wildcat-big-cat-botswana-46254.jpeg"
)


class SampleImageResponseBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        yield fp.PartialResponse(text=f"This is a test image. ![leopard]({IMAGE_URL})")


REQUIREMENTS = ["fastapi-poe==0.0.25"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("image-response-poe")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = SampleImageResponseBot()
    return fp.make_app(bot, allow_without_key=True)

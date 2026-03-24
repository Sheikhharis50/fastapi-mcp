import time

from fastapi import Request


async def request_timer_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)

    return response

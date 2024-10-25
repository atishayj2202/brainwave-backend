import os
import time

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.client.whatsapp import WhatsAppClient
from src.router.game import game_router
from src.router.message import message_router
from src.router.user import user_router
from src.service.whatsapp import handle_message
from src.utils.client import getDBClient, getFirebaseClient

app = FastAPI(title="BrainWave Backend", version="0.2.0-dev1")

origins = os.environ["CORS_ORIGINS"].split(",")
ENDPOINT_GET_WHATSAPP_MESSAGES = "/whatsapp"

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()

        try:
            response = await call_next(request)
        except HTTPException as exc:
            response = exc

        end_time = time.time()
        process_time = end_time - start_time
        print(
            f"Request {request.method} {request.url} processed in {process_time:.5f} seconds"
        )

        return response


app.add_middleware(TimingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def startup_event() -> None:
    getDBClient()
    getFirebaseClient()


"""@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exception:
        return http_exception
    except Exception as e:
        return Response(
            content="Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )"""


app.add_event_handler("startup", startup_event)
app.include_router(user_router)
app.include_router(message_router)
app.include_router(game_router)

@app.get(ENDPOINT_GET_WHATSAPP_MESSAGES)
async def verify_webhook(request: Request):
    VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if verify_token == VERIFY_TOKEN:
        return Response(content=challenge, status_code=200)
    else:
        return Response(status_code=403)


@app.post(ENDPOINT_GET_WHATSAPP_MESSAGES)
async def get_whatsapp_messages(
    request: dict,
    wb_client: WhatsAppClient = Depends(WhatsAppClient),
):
    return handle_message(request, wb_client)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=80, reload=True)

from whats_app_browser import WhatsAppBrowser
from starlette.responses import JSONResponse
from starlette import status
from fastapi import FastAPI
from asyncio.locks import Lock

wp = WhatsAppBrowser()
wp_lock = Lock()

app = FastAPI()


@app.get("/get_profile_picture_url/")
async def get_profile_picture_url(phone: str):
    await wp_lock.acquire()
    url = wp.get_profile_picture_url(phone)
    wp_lock.release()
    return JSONResponse({"phone": phone, "url": url}, status_code=status.HTTP_200_OK)

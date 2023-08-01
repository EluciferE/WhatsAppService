from whats_app_browser import WhatsAppBrowser
from starlette.responses import JSONResponse
from starlette import status
from fastapi import FastAPI
from backend import catch_server_error
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
whats_app = WhatsAppBrowser()


@app.on_event('startup')
async def init_browser():
    async with whats_app as browser:
        browser.sing_to_wp()
        browser._wait_unit_page_loaded()
        browser.inject_api()


@app.get("/get_profile_picture_url")
@catch_server_error
async def get_profile_picture_url(phone: str):
    async with whats_app as browser:
        url = browser.get_profile_picture_url(phone)
    return JSONResponse({"phone": phone, "url": url}, status_code=status.HTTP_200_OK)


@app.get("/is_authenticated")
@catch_server_error
async def is_authenticated():
    async with whats_app as browser:
        login_status = browser.is_authenticated()
    return JSONResponse({"status": login_status}, status_code=status.HTTP_200_OK)


@app.get("/login")
@catch_server_error
async def login():
    async with whats_app as browser:
        qr_code = browser.get_login_qr_code_as_base64()
    return JSONResponse({"qr_code": qr_code}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app, host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
    )

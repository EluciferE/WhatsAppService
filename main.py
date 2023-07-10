from whats_app_browser import WhatsAppBrowser
from starlette.responses import JSONResponse
from starlette import status
from fastapi import FastAPI

app = FastAPI()
whats_app = WhatsAppBrowser()


async def init_wp():
    async with whats_app as browser:
        browser.sing_to_wp()


@app.on_event('startup')
async def init_browser():
    async with whats_app as browser:
        browser.sing_to_wp()


@app.get("/get_profile_picture_url/")
async def get_profile_picture_url(phone: str):
    try:
        async with whats_app as browser:
            url = browser.get_profile_picture_url(phone)
        return JSONResponse({"phone": phone, "url": url}, status_code=status.HTTP_200_OK)
    except Exception as error:
        return JSONResponse(
            {"message": str(error)},
            status_code=getattr(error, '_STATUS_CODE', status.HTTP_500_INTERNAL_SERVER_ERROR)
        )

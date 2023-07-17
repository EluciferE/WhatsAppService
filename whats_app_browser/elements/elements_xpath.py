class ELEMENT_XPATH:
    # PROFILE_SIDEBAR = "/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section"
    # PROFILE_SMALL_PIC = "/html/body/div[1]/div/div/div[5]/div/header/div[1]/div"
    PROFILE_SIDEBAR = "//div[@data-testid='chat-info-drawer']"
    PROFILE_HEADER = "//div[@data-testid='conversation-info-header']"
    PROFILE_BIG_PIC = "//div[@data-testid='chat-info-drawer']//img"

    CHAT_POPUP = "//*[@data-testid='popup-contents' or @data-testid='popup-title']"
    LOADING_SCREEN = "//div[@data-testid='wa-web-loading-screen']"

    QR_PRELOAD = "//div[@class='landing-main']/div/div/div[2]//span"
    QR_CODE = "//div[@data-testid='qrcode']"

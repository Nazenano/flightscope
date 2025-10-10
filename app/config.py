class WindowConfig:
    ## Basics ##
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768
    WINDOW_TITLE = "flightscope"
    FULLSCREEN = False

    ## Background color ##
    BG_COLOR = (100 / 255, 100 / 255, 100 / 255, 1.0)

    ## Frames ##
    FPS = 60

    ## Perspectives ##
    FOV = 45
    NEAR_PLANE = 0.1
    FAR_PLANE = 100.0
    ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT

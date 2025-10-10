import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL import GL as gl
from OpenGL import GLU as glu
from app.config import WindowConfig as c


def main():
    pygame.init()

    flags = DOUBLEBUF | OPENGL
    if c.FULLSCREEN:
        flags |= pygame.FULLSCREEN

    ## Create the screen ##
    pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT), flags)
    pygame.display.set_caption(c.WINDOW_TITLE)

    ## OpenGL basic setup ##
    gl.glViewport(0, 0, c.WINDOW_WIDTH, c.WINDOW_HEIGHT)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(c.FOV, c.ASPECT_RATIO, c.NEAR_PLANE, c.FAR_PLANE)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glClearColor(*c.BG_COLOR)

    clock = pygame.time.Clock()

    ## Main loop ##
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        pygame.display.flip()
        clock.tick(c.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

from ursina import Ursina, Entity, DirectionalLight, AmbientLight, Slider, Text, Vec2, color, time, camera, window, mouse

app = Ursina(
    title='flightscope',
    borderless=True
)

window.color = color.rgb(5 / 255, 51 / 255, 255 / 255)
window.size = Vec2(1280, 720)
window.position = Vec2(0, 40)

earth = Entity(
    model='sphere',
    texture='textures/earth_texture.jpg',
    scale=3,
    color=color.white
)

DirectionalLight().look_at(earth)
AmbientLight(color=(0.2, 0.2, 0.2, 1))

camera.position = (0, 0, -10)
camera.look_at(earth)

rotation_speed = 2.0

dragging = False
last_mouse = Vec2(0, 0)
last_drag_time = 0

speed_slider = Slider(min=0, max=50, default=rotation_speed, step=1)
speed_slider.position = Vec2(0.5, -0.4)
speed_slider.scale = 1

speed_text = Text(text=f'Speed:', position=(0.36, -0.387), scale=1)

def update():
    global rotation_speed, dragging, last_mouse, auto_rotation_enabled

    rotation_speed = speed_slider.value
    speed_text.text = f'Speed: {rotation_speed:.1f}'

    earth.rotation_y += rotation_speed * time.dt

    if mouse.left:
        if not getattr(earth, 'dragging', False):
            earth.dragging = True
            earth.last_mouse = Vec2(mouse.x, mouse.y)
        else:
            dx = mouse.x - earth.last_mouse.x
            dy = mouse.y - earth.last_mouse.y
            earth.rotation_y -= dx * 100
            earth.rotation_x -= dy * 100
            earth.last_mouse = Vec2(mouse.x, mouse.y)
    else:
        earth.dragging = False

earth.update = update

app.run()

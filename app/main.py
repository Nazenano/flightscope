from ursina import Ursina, Entity, DirectionalLight, AmbientLight, Slider, Text,  Vec3, Vec2, color, time, camera, window, mouse , WindowPanel, InputField, Button , ButtonGroup


app = Ursina(
    title='flightscope',
    borderless=True
)

app = Ursina(title="flightscope", borderless=True)

window.color = color.rgb(5 / 255, 51 / 255, 255 / 255)
window.size = Vec2(1280, 720)
window.position = Vec2(0, 40)

earth = Entity(
    name='globe',
    model='sphere',
    texture='textures/earth_texture.jpg',
    scale=3, # type: ignore
    collider='sphere'
)

DirectionalLight().look_at(earth)
AmbientLight(color=(0.2, 0.2, 0.2, 1))



rotation_speed = 2
rotation_lock = False
dragging = False
last_mouse = 0
last_drag_time = 0
last_pivot_position = 0
max_zoom_distance = -12
min_zoom_distance = -3
zoom_distance = -10
resume_time = time.time()
rotation_timeout = 2
valid_rotation = False

camera.position = (0, 0, zoom_distance)
camera.look_at(earth)

 
def mode_check () : 
    earth.wireframe =  True if modes.value == 'Simulation' else False


modes= ButtonGroup(('Real Time', 'Simulation'), origin= (0,0))
modes.on_value_changed = mode_check


settings = WindowPanel(
    title='Settings',
    content=(
        Text('Rotation speed:'),
        Slider(min=0, max=50, default=rotation_speed, step=1 ),
        Text('Mode:'),
        modes
        ),
    popup=False
    )
settings.y = settings.panel.scale_y / 2 * settings.scale_y    
settings.layout()



pivot = Entity(position=earth.position)
camera.parent = pivot

   

def input(key) : 
    global dragging , resume_time , rotation_lock , valid_rotation
    if key == 'scroll up':
        if camera.position[2]+1<=min_zoom_distance:
            camera.position= (0,0,camera.position[2]+1)
    if key == 'scroll down':
        if camera.position[2]-1>=max_zoom_distance:
            camera.position= (0,0,camera.position[2]-1)
    if key == "left mouse down" and mouse.hovered_entity == earth:
        dragging=True
        valid_rotation=True
    if key == "right mouse down":
        rotation_lock=True
    if key == "right mouse up":
        rotation_lock=False
    if key == "left mouse up" and valid_rotation:
        dragging=False
        resume_time = time.time()+rotation_timeout
        valid_rotation=False
    # if key == "w":
    #     earth.wireframe = True
    # if key == "w up":
    #     earth.wireframe = False
    print(key)


def update():
    global rotation_speed, dragging, last_mouse , last_pivot_position , resume_time ,rotation_lock

    rotation_speed = settings.content[1].value
    
    if not dragging and time.time()>= resume_time and not rotation_lock:
        earth.rotation_y += rotation_speed * time.dt

                    
    camera.look_at(earth)   
    if mouse.left and mouse.hovered_entity == earth:
        if not getattr(earth, 'dragging', False):
            earth.dragging = True
            earth.last_mouse = mouse.x
            last_pivot_position = mouse.y
        else:
            dx = mouse.x - earth.last_mouse
            dy = mouse.y - last_pivot_position
            
            earth.rotation_y -= dx * 100
            pivot.rotation_x -= dy * 100

            if pivot.rotation_x < -80:
                pivot.rotation_x = -80
            elif pivot.rotation_x > 80:
                pivot.rotation_x = 80
            

            earth.last_mouse = mouse.x
            last_pivot_position = mouse.y
    else:
        earth.dragging = False

app.run()
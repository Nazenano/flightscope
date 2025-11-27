from ursina import Ursina, Entity, DirectionalLight, AmbientLight, Slider, Text,  Vec3, Vec2, color, time, camera, window, mouse , WindowPanel, InputField, Button , ButtonGroup , Mesh
from math import sin , cos , radians, acos 
import api.requests as req
from functools import partial


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



rotation_speed = 0
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

arc_points = 30   
arc_thickness = 0.01

camera.position = (0, 0, zoom_distance)
camera.look_at(earth)

 
def mode_check () :
    if modes.value == 'Simulation' :
        earth.wireframe= True
        earth.texture = None
    else:
        earth.wireframe = False
        earth.texture =  'textures/earth_texture.jpg'

modes= ButtonGroup(('Real Time', 'Simulation'), origin= (0,0), spacing=(1,0))
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
settings.position = Vec2(.85, -.15)  
settings.layout()

pivot = Entity(position=earth.position)
camera.parent = pivot




def latlon_to_unitvec(lat_deg: float, lon_deg: float ,  radius=1.5, height=0, east_offset=0):
    lat_r = radians(lat_deg)
    lon_r = radians(lon_deg+90)
    x = radius * cos(lat_r) * cos(lon_r)
    y = radius * sin(lat_r)
    z = radius * cos(lat_r) * sin(lon_r)

    surface = Vec3(x, y, z)
    normal = surface.normalized()

    east = Vec3(-sin(lon_r), 0, cos(lon_r)).normalized()
    final_pos = surface + normal * height + east * east_offset
    return final_pos

# def great_circle_points(unit_a: Vec3, unit_b: Vec3, steps: int):
#     dot = max(-1.0, min(1.0, unit_a.dot(unit_b)))
#     angle = acos(dot)
#     pts = []
#     if abs(angle) < 1e-6:
#         pts.append(unit_a)
#         return pts

#     for i in range(steps + 1):
#         t = i / steps
#         s1 = sin((1 - t) * angle)
#         s2 = sin(t * angle)
#         denom = sin(angle)
#         v = (unit_a * s1 + unit_b * s2) / denom
#         pts.append(v.normalized())
#     return pts



def create_arc_mesh(unit_pts, radius=3, thickness=0.05, color_=color.cyan):
    vertices = []
    triangles = []
    for u in unit_pts:
        pos = u * radius
        vertices.append(pos)
    line = Entity(model=Mesh(vertices=vertices, mode='line'), color=color_)
    return line


airplanes = req.get_all_aircraft( 40.75 , 50.6 , 10.10 , 26.9)
# print(airplanes)
a = latlon_to_unitvec(0, 0)

Entity(model='sphere',
scale=.01,
collider='sphere',
color= color.orange,
position= a)


def globe_clicked (data ) : 
    print(data)
    print( int(time.time()-3600*5))
    print( int(time.time()))
    print(req.get_aircraft_flights(data[0], int(time.time()-3600) , int(time.time())  ))

for airplane in airplanes['states']:
    if airplane[7] is not None:
        normalized_value = (airplane[7] - 0) / (15000 - 0)
        new_value = 0.005 + (.05 - 0.005) * normalized_value
    else :
        new_value=0.005

    
    a = latlon_to_unitvec(airplane[6], airplane[5] , height=new_value)
    # print(airplane[6], airplane[5], airplane[7])
    Entity(model='sphere',
    scale=.01,
    collider='sphere',
    color= color.cyan,
    on_click=partial( globe_clicked, airplane ) ,
    position= a
)



# pts = great_circle_points(a, b, arc_points)
# arc_entity = create_arc_mesh(pts, 1.6)


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
    # print(key)


def update():
    global rotation_speed, dragging, last_mouse , last_pivot_position , resume_time ,rotation_lock

    rotation_speed = settings.content[1].value
    
    if not dragging and time.time()>= resume_time and not rotation_lock:
        pivot.rotation_y += rotation_speed * time.dt

                    
    camera.look_at(earth)   
    if mouse.left and mouse.hovered_entity == earth:
        if not getattr(earth, 'dragging', False):
            earth.dragging = True
            earth.last_mouse = mouse.x
            last_pivot_position = mouse.y
        else:
            dx = mouse.x - earth.last_mouse
            dy = mouse.y - last_pivot_position
            
            pivot.rotation_y += dx * 100
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
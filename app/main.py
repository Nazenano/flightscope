from ursina import (
    Ursina,
    Entity,
    DirectionalLight,
    AmbientLight,
    Vec3,
    Vec2,
    color,
    time,
    camera,
    window,
    mouse,
    Mesh,
)
from math import sin, cos, radians, acos
import api.requests as req
from components.settings_window import SettingsWindow

app = Ursina(title="flightscope", borderless=True)

window.color = color.rgb(5 / 255, 51 / 255, 255 / 255)
window.size = Vec2(1280, 720)
window.position = Vec2(0, 40)

earth = Entity(
    name="globe",
    model="sphere",
    texture="textures/earth_texture.jpg",
    scale=3,  # type: ignore
    collider="sphere",
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


def mode_check():
    if settings_window.modes.value == "Simulation":
        earth.wireframe = True
        earth.texture = None
    else:
        earth.wireframe = False
        earth.texture = "textures/earth_texture.jpg"


# Render settings window
settings_window = SettingsWindow(rotation_speed, mode_check)


pivot = Entity(position=earth.position)
camera.parent = pivot


def latlon_to_unitvec(lat_deg: float, lon_deg: float):
    lat = radians(lat_deg)
    lon = radians(lon_deg)
    x = cos(lat) * sin(lon)
    y = sin(lat)
    z = cos(lat) * cos(lon)
    return Vec3(x, y, z).normalized()


def great_circle_points(unit_a: Vec3, unit_b: Vec3, steps: int):
    dot = max(-1.0, min(1.0, unit_a.dot(unit_b)))
    angle = acos(dot)
    pts = []
    if abs(angle) < 1e-6:
        pts.append(unit_a)
        return pts

    for i in range(steps + 1):
        t = i / steps
        s1 = sin((1 - t) * angle)
        s2 = sin(t * angle)
        denom = sin(angle)
        v = (unit_a * s1 + unit_b * s2) / denom  # type: ignore
        pts.append(v.normalized())
    return pts


def create_arc_mesh(unit_pts, radius=1.5, thickness=0.05, color_=color.red):
    vertices = []
    triangles = []
    for u in unit_pts:
        pos = u * radius
        vertices.append(pos)

    # LineList: minden 2 pont egy vonal
    # Ursina: egyszerűen Line modell (Line segédfüggvény)
    line = Entity(model=Mesh(vertices=vertices, mode="line"), color=color_)
    return line


a = latlon_to_unitvec(0, 0)  # Budapest
b = latlon_to_unitvec(48.15, 0)  # Bratislava
pts = great_circle_points(a, b, arc_points)
arc_entity = create_arc_mesh(pts, 1.6)


def input(key):
    global dragging, resume_time, rotation_lock, valid_rotation
    if key == "scroll up":
        if camera.position[2] + 1 <= min_zoom_distance:
            camera.position = (0, 0, camera.position[2] + 1)
    if key == "scroll down":
        if camera.position[2] - 1 >= max_zoom_distance:
            camera.position = (0, 0, camera.position[2] - 1)
    if key == "left mouse down" and mouse.hovered_entity == earth:
        dragging = True
        valid_rotation = True
    if key == "right mouse down":
        rotation_lock = True
    if key == "right mouse up":
        rotation_lock = False
    if key == "left mouse up" and valid_rotation:
        dragging = False
        resume_time = time.time() + rotation_timeout
        valid_rotation = False
    # print(key)


def update():
    global rotation_speed, dragging, last_mouse, last_pivot_position, resume_time, rotation_lock

    rotation_speed = settings_window.value

    if not dragging and time.time() >= resume_time and not rotation_lock:
        pivot.rotation_y += rotation_speed * 5 * time.dt

    camera.look_at(earth)
    if mouse.left and mouse.hovered_entity == earth:
        if not getattr(earth, "dragging", False):
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


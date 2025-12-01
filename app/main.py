import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    destroy
)
from api.requests import get_aircraft_metadata
from functools import partial
from components.details_window import DetailsWindow
from core.airplane import fetch_airplanes
from components.settings_window import SettingsWindow
from components.generator_window import generator_window


app = Ursina(title="flightscope", borderless=True)

window.color = color.rgb(5 / 255, 51 / 255, 255 / 255)
window.size = Vec2(1280, 720)
window.position = Vec2(0, 40)

earth = Entity(
    name="globe",
    model="sphere",
    texture="textures/earth_texture.jpg",
    scale=Vec3(3),
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
        for airplane in airplane_entities:
            destroy(airplane_entities[airplane])
        settings_window.window.content[4].enabled = False
        settings_window.window.content[5].enabled = True
        generator_window.clear()
        
    else:
        earth.wireframe = False
        earth.texture = "textures/earth_texture.jpg"
        settings_window.window.content[4].enabled = True
        settings_window.window.content[5].enabled = False
        generator_window.clear()


# Render settings window
settings_window = SettingsWindow(rotation_speed, mode_check)


pivot = Entity(position=earth.position)
camera.parent = pivot


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

# def create_arc_mesh(unit_pts, radius=3, thickness=0.05, color_=color.cyan):
#     vertices = []
#     triangles = []
#     for u in unit_pts:
#         pos = u * radius
#         vertices.append(pos)
#     line = Entity(model=Mesh(vertices=vertices, mode="line"), color=color_)
#     return line

# Entity(
#     model="sphere",
#     scale=Vec3(0.01),
#     collider="sphere",
#     color=color.orange,
#     position=latlon_to_unitvec(0, 0),
# )
# pts = great_circle_points(a, b, arc_points)
# arc_entity = create_arc_mesh(pts, 1.6)


# Render airplanes
planes = fetch_airplanes()


details_window = None


def globe_clicked(plane_data):
    global details_window

    if details_window:
        details_window.destroy()

    icao = plane_data["icao24"]

    meta = get_aircraft_metadata(icao)

    combined = {**plane_data, **meta}

    details_window = DetailsWindow(icao, combined)


airplane_entities = {}
for plane in planes:
    e = Entity(
        model="sphere",
        scale=Vec3(0.01),
        collider="sphere",
        color=color.cyan,
        on_click=partial(globe_clicked, plane["data"]),
        position=plane["pos"],
    )
    airplane_entities[plane["id"]] = e


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


last_fetch_time = 0


def update_airplanes():
    planes = fetch_airplanes()
    for plane in planes:
        plane_id = plane["id"]
        if plane["pos"] is None:
            continue
        if plane_id in airplane_entities:
            airplane_entities[plane_id].position = plane["pos"]
        else:
            e = Entity(
                model="sphere",
                scale=Vec3(0.01),
                collider="sphere",
                color=color.cyan,
                on_click=partial(globe_clicked, plane["data"]),
                position=plane["pos"],
            )
            airplane_entities[plane_id] = e


def update():
    global rotation_speed, dragging, last_mouse, last_pivot_position, resume_time, rotation_lock, last_fetch_time

    rotation_speed = settings_window.value

    if not dragging and time.time() >= resume_time and not rotation_lock:
        pivot.rotation_y += rotation_speed * -5 * time.dt

    camera.look_at(earth)

    # Update airplane positions
    if time.time() - last_fetch_time > 5.0 and settings_window.value == "Real Time":
        update_airplanes()
        last_fetch_time = time.time()

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

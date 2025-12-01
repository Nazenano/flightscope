from ursina import (
    Text,
    Vec2,
    WindowPanel,
    destroy,
    Button,
    InputField,
    Entity,
    Vec3,
    color
)
import random
from core.utils import random_point , latlon_to_unitvec


class generator_window :    
    instance = None 
    simulated_plains= []
    def __init__(self):
        if generator_window.instance:
            generator_window.instance.gen_window.enabled = True
            return
        generator_window.instance = self
        generate = Button('Generate')
        
        self.low = InputField(limit_content_to='0123456789' ,default_value='0')
        self.med = InputField(limit_content_to='0123456789', default_value='0')
        self.high = InputField(limit_content_to='0123456789', default_value='0')
        generate.on_click = self.create_planes
        self.gen_window = WindowPanel(
                title="Plane Generator",
                content=(
                    Text("Low Range Plane:"),
                    self.low,
                    Text("Medium Range Plane:"),
                    self.med,
                    Text("High Range Plane:"),
                    self.high,
                    generate
                ),
                popup=False,
                collider="box",
            )
        self.gen_window.position = Vec2(-0.65, 0)
        self.gen_window.layout()

    
    
    @classmethod
    def clear(cls):
        for plain in cls.simulated_plains:
            destroy(plain)
        cls.simulated_plains.clear()

    def create_planes (self ):
       
        for plain in generator_window.simulated_plains:
           destroy(plain)
        generator_window.simulated_plains.clear()
        
        for low_plane in range(int(self.gen_window.content[1].text)):
            base_lat, base_lon = random_point()
            start_vec = latlon_to_unitvec(base_lat, base_lon)

            offset_lat = base_lat + random.uniform(-5, 5)
            offset_lon = base_lon + random.uniform(-5, 5)
            plane_start = latlon_to_unitvec(offset_lat, offset_lon)

            delta_lat = offset_lat - base_lat
            delta_lon = offset_lon - base_lon
            distance_factor = random.uniform(0.5, 1.5)  
            end_lat = offset_lat + delta_lat * distance_factor
            end_lon = offset_lon + delta_lon * distance_factor
            end_vec = latlon_to_unitvec(end_lat, end_lon)

            plane = Entity(
                model='sphere',
                scale=Vec3(0.05),
                collider='sphere',
                color=color.red,
                position=start_vec
            )
            plane.end_point = end_vec
            plane.start_point = plane_start
            self.simulated_plains.append(plane)
        for medium_plane in range(int(self.gen_window.content[3].text)):
            base_lat, base_lon = random_point()
            start_vec = latlon_to_unitvec(base_lat, base_lon)

            offset_lat = base_lat + random.uniform(-30, 30)
            offset_lon = base_lon + random.uniform(-30, 30)
            plane_start = latlon_to_unitvec(offset_lat, offset_lon)

            delta_lat = offset_lat - base_lat
            delta_lon = offset_lon - base_lon
            distance_factor = random.uniform(0.5, 1.5)  
            end_lat = offset_lat + delta_lat * distance_factor
            end_lon = offset_lon + delta_lon * distance_factor
            end_vec = latlon_to_unitvec(end_lat, end_lon)

            plane = Entity(
                model='sphere',
                scale=Vec3(0.05),
                collider='sphere',
                color=color.red,
                position=start_vec
            )
            plane.end_point = end_vec
            plane.start_point = plane_start
            self.simulated_plains.append(plane)
        for high_plane in range(int(self.gen_window.content[5].text)):
            base_lat, base_lon = random_point()
            start_vec = latlon_to_unitvec(base_lat, base_lon)

            offset_lat = base_lat + random.uniform(-60, 60)
            offset_lon = base_lon + random.uniform(-60, 60)
            plane_start = latlon_to_unitvec(offset_lat, offset_lon)

            delta_lat = offset_lat - base_lat
            delta_lon = offset_lon - base_lon
            distance_factor = random.uniform(0.5, 1.5)  
            end_lat = offset_lat + delta_lat * distance_factor
            end_lon = offset_lon + delta_lon * distance_factor
            end_vec = latlon_to_unitvec(end_lat, end_lon)

            plane = Entity(
                model='sphere',
                scale=Vec3(0.05),
                collider='sphere',
                color=color.red,
                position=start_vec
            )
            plane.end_point = end_vec
            plane.start_point = plane_start
            self.simulated_plains.append(plane)
            

           


        self.close()
    
    
    def close(self):
        if self.gen_window:
            destroy(self.gen_window)
            self.gen_window = None
            generator_window.instance = None
            
   
from ursina import Text, Vec2, Vec3, WindowPanel, destroy, color, Button


class DetailsWindow:
    """Window that displays details about a selected aircraft"""

    def __init__(self, plane_id: str, plane_data: dict):
        self.plane_id = plane_id
        self.plane_data = plane_data
        self.window = WindowPanel(
            title=f"Aircraft {plane_id.upper()}",
            name="details_window",
            content=self._build_content(),
            collider="box",
            popup=False,
        )
        close_button = Button(
            parent=self.window,
            text="x",
            color=color.red,  # type: ignore
            position=Vec3(-0.45, -0.5, -0.01),
        )
        close_button.scale_x = 0.08
        close_button.scale_y = 0.8
        close_button.on_click = self.destroy
        self.close_button = close_button

        self.window.position = Vec2(0.5, 0.5)
        self.window.layout()
        self.window.panel.scale_y = 10

    def _build_content(self):
        full_text = (
            f"Callsign:      {self.plane_data.get('callsign', 'N/A')}\n"
            f"Country:       {self.plane_data.get('origin_country', 'N/A')}\n"
            f"Latitude:      {self._fmt(self.plane_data.get('latitude'))}\n"
            f"Longitude:     {self._fmt(self.plane_data.get('longitude'))}\n"
            f"Altitude:      {self._fmt(self.plane_data.get('baro_altitude'))} m\n"
            f"Velocity:      {self._fmt(self.plane_data.get('velocity'))} m/s\n"
            f"Heading:       {self._fmt(self.plane_data.get('heading'))}°\n"
            f"Vertical rate: {self._fmt(self.plane_data.get('vertical_rate'))} m/s\n"
            f"On ground:     {self.plane_data.get('on_ground', False)}\n"
            "\n"
            f"Model:         {self.plane_data.get('model', 'N/A')}\n"
            f"Type code:     {self.plane_data.get('type', 'N/A')}\n"
            f"Manufacturer:  {self.plane_data.get('manufacturer', 'N/A')}\n"
            f"Built:         {self.plane_data.get('built', 'N/A')}\n"
            f"Registration:  {self.plane_data.get('registered', 'N/A')}\n"
            f"Owner:         {self.plane_data.get('owner', 'N/A')}\n"
            f"Category:      {self.plane_data.get('category', 'N/A')}"
        )

        return (
            Text(
                full_text,
                size=0.022,
                origin=(0, 0.5),
                line_height=1.05,
                wordwrap=35,
            ),
        )

    def _fmt(self, value):
        return "N/A" if value is None else round(value, 2)

    def destroy(self):
        if self.window:
            self.window.enabled = False
            destroy(self.window)

    def update_data(self, new_data: dict):
        self.plane_data = new_data
        self.window.content = self._build_content()
        self.window.layout()

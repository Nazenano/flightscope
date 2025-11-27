from ursina import (
    Text,
    Vec2,
    WindowPanel,
    destroy,
)


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

        self.window.position = Vec2(0.5, 0.5)
        self.window.layout()

    def _build_content(self):
        return (
            Text(f"Callsign: {self.plane_data.get('callsign', 'N/A')}"),
            Text(f"Country: {self.plane_data.get('origin_country', 'N/A')}"),
            Text(f"Latitude: {self._fmt(self.plane_data.get('latitude'))}"),
            Text(f"Longitude: {self._fmt(self.plane_data.get('longitude'))}"),
            Text(f"Altitude: {self._fmt(self.plane_data.get('altitude'))} m"),
            Text(f"Velocity: {self._fmt(self.plane_data.get('velocity'))} m/s"),
            Text(f"Heading: {self._fmt(self.plane_data.get('heading'))}°"),
            Text(
                f"Vertical rate: {self._fmt(self.plane_data.get('vertical_rate'))} m/s"
            ),
            Text(f"On ground: {self.plane_data.get('on_ground', False)}"),
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

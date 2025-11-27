from ursina import (
    Slider,
    Text,
    Vec2,
    WindowPanel,
    ButtonGroup,
    destroy,
)


class SettingsWindow:
    """Window that displays app settings"""

    def __init__(self, rotation_speed: float = 0, mode_callback=None):
        self.rotation_speed = rotation_speed
        self.mode_callback = mode_callback

        self.modes = ButtonGroup(
            ("Real Time", "Simulation"), origin=(0, 0), spacing=(1, 0)
        )
        if self.mode_callback:
            self.modes.on_value_changed = self.mode_callback

        self.speed_slider = Slider(min=0, max=10, default=self.rotation_speed, step=1)

        self.window = WindowPanel(
            title="Settings",
            name="settings_window",
            content=self._build_content(),
            collider="box",
            popup=False,
        )

        self.window.position = Vec2(0.85, -0.15)
        self.window.layout()

    def _build_content(self):
        return (
            Text("Rotation speed:"),
            self.speed_slider,
            Text("Mode:"),
            self.modes,
        )

    @property
    def value(self):
        """Return the current rotation speed"""
        return self.speed_slider.value

    def destroy(self):
        if self.window:
            self.window.enabled = False
            destroy(self.window)

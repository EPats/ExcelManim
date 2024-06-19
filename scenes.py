from manim import *


def create_narration_circle(scene: Scene) -> None:
    c = Circle(radius=0.9, color=YELLOW_E, fill_color=YELLOW_E, fill_opacity=1).to_corner(UR, buff=0.2)
    c.z_index = 100
    scene.add(c)


class NarratedScene(Scene):
    def __init__(self):
        super().__init__()
        create_narration_circle(self)

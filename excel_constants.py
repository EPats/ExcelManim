#type: ignore
from manim import *

EP_BLUE: ManimColor = XKCD.BLURPLE
EP_GREEN: ManimColor = XKCD.APPLEGREEN
EP_YELLOW: ManimColor = YELLOW
EP_EXCEL_GREEN: ManimColor = XKCD.DARKFORESTGREEN
RANGE_COLORS: list[ManimColor] = [XKCD.BLUISH, RED, PURPLE, GREEN, XKCD.BLUSHPINK, ORANGE, TEAL, YELLOW_E]


def create_tick() -> Union:
    r1 = RoundedRectangle(corner_radius=0.5, width=3, height=1)
    r2 = (RoundedRectangle(corner_radius=0.5, width=1, height=7)
          .align_to(r1, RIGHT + DOWN))
    tick = Union(r1, r2, color=EP_GREEN, fill_opacity=1).rotate(-45 * DEGREES).scale(0.5)
    return tick


def create_cross() -> Union:
    r1 = RoundedRectangle(corner_radius=0.5, width=7, height=1)
    r2 = RoundedRectangle(corner_radius=0.5, width=1, height=7)
    cross = Union(r1, r2, color=RED, fill_opacity=1).rotate(45 * DEGREES).scale(0.5)
    return cross


TICK = create_tick()
CROSS = create_cross()
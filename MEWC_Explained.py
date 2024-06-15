import math

from manim import *
import random
import numpy as np
import re


import excel_character
from excel_helpers import *
from excel_tables import *
from excel_formula import *
from scenes import NarratedScene


def trace_bracket(bracket_corners: list[Vector3D], dot: Dot) -> Callable[[VMobject], None]:
    def update_bracket(x: VMobject):
        if dot.get_center()[0] >= bracket_corners[1][0]:
            new_corners = bracket_corners[:2]
            new_corners.append(dot.get_center())
        else:
            new_corners = bracket_corners[:1]
            new_corners.append(dot.get_center())
        x.become(VMobject().set_points_as_corners(new_corners))

    return update_bracket


def create_bracket_arm(dot_color: ManimColor, start_location: Vector3D, depth: int = 1, up: bool = False,
                       reverse: bool = False) -> tuple[Dot, list[Vector3D]]:
    arm_length = 2
    arm_height = 0.25 * depth

    dot = Dot(color=dot_color, fill_color=dot_color, fill_opacity=1).move_to(start_location)
    c1 = start_location + arm_length * (LEFT if reverse else RIGHT)
    c2 = c1 + arm_height * (UP if up else DOWN)
    bracket_corners = [start_location, c1, c2]
    # bracket_shape = VMobject().set_points_as_corners(bracket_corners)
    # updater = trace_bracket(bracket_corners, dot)
    return dot, bracket_corners


class Brackets(NarratedScene):
    def construct(self):
        # dot = Dot(color=RED, fill_color=RED, fill_opacity=1)
        # bracket_corners = [ORIGIN, np.array([2, 0, 0]), np.array([2, 0.25, 0])]
        # bracket_shape = VMobject().set_points_as_corners([np.array([0, 0, 0]), np.array([2, 0, 0]), np.array([2, 0.25, 0])])
        # # self.play(Create(bracket_shape), run_time=2)
        # b = VMobject()
        # b.add_updater(trace_bracket(bracket_corners, dot))
        # self.add(b)
        # self.play(Create(dot))
        # self.play(MoveAlongPath(dot, bracket_shape), rate_func=linear)
        # self.wait(2)
        # self.play(dot.animate.move_to(np.array([2, 0.5, 0])))


        # 16 manim colors in a list
        colors = [WHITE, BLACK, BLUE, GREEN, RED, YELLOW, PURPLE, TEAL, ORANGE, MAROON, PINK,
                  XKCD.LIME, XKCD.BROWN, XKCD.OLIVE, XKCD.NAVY, XKCD.ARMYGREEN]
        start_locations = [LEFT + UP * i/2.0 for i in range(-8, 8)]
        ups = [True, False] * 8
        brackets = [create_bracket_arm(color, start_location, up=up) for color, start_location, up in zip(colors, start_locations, ups)]
        creates = []
        moves = []
        for dot, bracket_corners in brackets:
            bracket_path = VMobject().set_points_as_corners(bracket_corners)
            b = VMobject()
            b.add_updater(trace_bracket(bracket_corners, dot))
            self.add(b)
            creates.append(Create(dot))
            moves.append(MoveAlongPath(dot, bracket_path, rate_func=linear))

        self.play(*creates)
        self.play(*moves)
        self.wait(2)
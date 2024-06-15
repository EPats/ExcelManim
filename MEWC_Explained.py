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


class Brackets(NarratedScene):
    ARM_LENGTH = 1
    ARM_BASE_HEIGHT = 0.2
    HIGHLIGHT_SCALE = 3
    HIGHLIGHT_SHRINK = 0.001
    HIGHLIGHT_RUN_TIME = 0.4
    MOVE_RUN_TIME = 3
    GAMMA: float = 0.01
    # COLORS = [WHITE, XKCD.ADOBE, BLUE, GREEN, RED, YELLOW, PURPLE, TEAL, ORANGE, MAROON, PINK,
    #               XKCD.LIME, XKCD.BROWN, XKCD.OLIVE, XKCD.NAVY, XKCD.ARMYGREEN]
    START_X = 5 * LEFT
    COLORS = [
        XKCD.WHITE,
        XKCD.PINK,
        XKCD.RED,
        XKCD.ORANGE,
        XKCD.YELLOW,
        XKCD.CHARTREUSE,
        XKCD.GREEN,
        XKCD.TEAL,
        XKCD.CYAN,
        XKCD.AZURE,
        XKCD.BLUE,
        XKCD.INDIGO,
        XKCD.VIOLET,
        XKCD.PURPLE,
        XKCD.MAGENTA,
        XKCD.LAVENDER
    ]

    def construct(self):
        start_locations = [self.START_X + UP * (3 + i * -2 / 5.0) for i in range(len(self.COLORS))]
        dots = [self.create_dot(color, start_location) for color, start_location in zip(self.COLORS, start_locations)]
        self.play(*[Create(dot) for dot in dots])
        first_bracket = VGroup(*self.animate_bracket(dots), *dots)
        self.wait(2)

        all_brackets = [first_bracket.copy()]
        for i in range(7):
            dots = [self.create_dot(color, start_location) for color, start_location in zip(self.COLORS, start_locations)]
            new_bracket = VGroup(*self.create_unanimated_bracket(dots))
            all_brackets.append(new_bracket)

        all_brackets_mob = VGroup(*all_brackets)
        all_brackets_mob.arrange_in_grid(2, buff=(0.5, 1.2))
        all_brackets_mob.scale(0.4)
        all_brackets_mob.align_to(first_bracket, LEFT + UP)
        self.play(first_bracket.animate.scale(0.4, about_point=first_bracket.get_corner(UL)), FadeIn(all_brackets_mob[1:]))
        # self.wait(1)
        # static_version.scale([-1, 1, 1])
        # self.add(static_version)
        self.wait(3)

    def animate_bracket(self, dots: list[Dot]):
        for dot in dots:
            dot.z_index = 1

        objects = []
        for i in range(4):
            dots, brackets = self.run_bracket(dots, i)
            objects.extend(brackets)

        winning_dot = dots[0]
        win_line = Line(winning_dot.get_center(), winning_dot.get_center() + RIGHT * self.ARM_LENGTH)
        win_trace = VMobject()
        win_updater = lambda x: x.become(Line(win_line.get_left(), winning_dot.get_center()))
        win_trace.add_updater(win_updater)
        self.add(win_trace)
        self.play(MoveAlongPath(winning_dot, win_line, rate_func=rate_functions.ease_out_quad),
                  run_time=self.MOVE_RUN_TIME)
        win_trace.remove_updater(win_updater)
        crown = (SVGMobject('svg/crown.svg', fill_color=winning_dot.color)
                 .scale(0.25).move_to(winning_dot.get_center()).shift(UP*0.1))
        objects.append(crown)
        objects.append(win_trace)
        # objects.remove(winning_dot)
        self.play(Transform(winning_dot, crown))
        return objects

    def run_bracket(self, dots: List[Dot], depth: int):
        ups = [False, True] * (len(dots) // 2)
        brackets = [self.create_bracket_arm(dot.get_center(), depth=depth, up=up)
                    for dot, up in zip(dots, ups)]
        anims = []
        tracing_objects = []
        for dot, bracket_corners in zip(dots, brackets):
            bracket_path = VMobject().set_points_as_corners(bracket_corners)
            tracing_object = VMobject()
            updater = self.trace_bracket(bracket_corners, dot)
            tracing_object.add_updater(updater)
            tracing_objects.append((tracing_object, updater))
            anims.append(
                MoveAlongPath(dot, bracket_path, rate_func=rate_functions.ease_out_sine)
                .set_run_time(self.MOVE_RUN_TIME)
            )

        self.add(*[tracing_object for tracing_object, updater in tracing_objects])
        dots = [random.choice(dots[i:i + 2]) for i in range(0, len(dots), 2)]
        for dot in dots:
            dot.z_index += 1
        self.play(*anims)
        for tracing_object, updater in tracing_objects:
            tracing_object.remove_updater(updater)

        highlight_circles = [Circle(dot.radius * self.HIGHLIGHT_SCALE, color=dot.color).move_to(dot)
                             for dot in dots]
        self.add(*highlight_circles)
        self.play(*[highlight_circle.animate.scale(self.HIGHLIGHT_SHRINK)
                    for highlight_circle in highlight_circles], run_time=self.HIGHLIGHT_RUN_TIME)
        self.remove(*highlight_circles)
        return dots, [tracing_object for tracing_object, updater in tracing_objects]

    def trace_bracket(self, bracket_corners: list[Vector3D], dot: Dot) -> Callable[[VMobject], None]:
        def update_bracket(x: VMobject):
            if abs(dot.get_center()[0] - bracket_corners[1][0]) <= self.GAMMA:
                new_corners = bracket_corners[:2]
                new_corners.append(dot.get_center())
            else:
                new_corners = bracket_corners[:1]
                new_corners.append(dot.get_center())
                new_corners.append(dot.get_center())
            x.become(VMobject().set_points_as_corners(new_corners))

        return update_bracket

    def create_dot(self, dot_color: ManimColor, start_location: Vector3D) -> Dot:
        return Dot(color=dot_color, fill_color=dot_color, fill_opacity=1).move_to(start_location)

    def create_bracket_arm(self, start_location: Vector3D, depth: int, up: bool = False) -> list[Vector3D]:
        arm_length = self.ARM_LENGTH
        arm_height = self.ARM_BASE_HEIGHT * (2 ** depth)

        c1 = start_location + arm_length * RIGHT
        c2 = c1 + arm_height * (UP if up else DOWN)
        bracket_corners = [start_location, c1, c2]
        return bracket_corners

    def create_unanimated_bracket(self, dots: list[Dot]):
        starting_positions = [dot.get_center() for dot in dots]
        for i, dot in enumerate(dots):
            dot.z_index = 1
            dot.shift(self.ARM_LENGTH * RIGHT + self.ARM_BASE_HEIGHT * (-1 if i % 2 == 0 else 1) * UP)

        winning_indices = [i for i in range(len(dots))]
        objects = []
        for i in range(4):
            ups = [False, True] * (len(starting_positions) // 2)
            brackets = [self.create_bracket_arm(starting_position, depth=i, up=up) for starting_position, up
                        in zip(starting_positions, ups)]
            starting_positions = [bracket[2] for bracket in brackets[::2]]
            objects.extend([VMobject().set_points_as_corners(bracket) for bracket in brackets])
            winning_indices = [random.choice(winning_indices[i:i + 2]) for i in range(0, len(winning_indices), 2)]
            for k, j in enumerate(winning_indices):
                if i == 3:
                    continue
                dots[j].shift(self.ARM_LENGTH * RIGHT +
                              self.ARM_BASE_HEIGHT * UP * (-1 if k % 2 == 0 else 1) * UP * (2 ** (i + 1)))

        winning_dot = dots[winning_indices[0]]
        winning_line = Line(winning_dot.get_center(), winning_dot.get_center() + RIGHT * self.ARM_LENGTH)
        winning_dot.shift(self.ARM_LENGTH * RIGHT)
        crown = (SVGMobject('svg/crown.svg', fill_color=winning_dot.color)
                 .scale(0.25).move_to(winning_dot.get_center()).shift(UP*0.1))
        objects.extend(dots)
        objects.remove(winning_dot)
        objects.extend([winning_line, crown])
        return objects


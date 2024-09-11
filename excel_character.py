import math
from enum import Enum
from functools import partial

from manim.mobject.mobject import _AnimationBuilder
from typing_extensions import Self

from manim import *
from manim.typing import Vector3D
import re
import excel_constants
from custom_animations import CreateWithMovement, FadeInWithMovementAndScale
from excel_tables import ExcelTable
import numpy as np


class Eye(VGroup):
    def __init__(self, is_left: bool = True, **kwargs):
        self.is_left = is_left
        self.eye_background = Circle(radius=0.2, color=BLACK, fill_color=WHITE, fill_opacity=1)
        outer_pupil = Circle(radius=0.1, color=excel_constants.EP_GREEN, fill_color=BLACK, fill_opacity=1)
        pupil_highlight = (AnnularSector(outer_radius=0.08, inner_radius=0.04, angle=75 * DEGREES, fill_color=WHITE,
                                         fill_opacity=1, stroke_opacity=0)
                           .flip(Y_AXIS).move_to(outer_pupil.get_center()).shift(LEFT * 0.02 + UP * 0.02))
        self.eye_background.set_z_index(4 if is_left else 1)
        self.pupil = VGroup(outer_pupil, pupil_highlight).set_z_index(5 if is_left else 2)
        self.eye_cover = self.eye_background.copy().set_fill(opacity=0).set_z_index(6 if is_left else 3)
        self.eyebrow_expressions: dict[str, VMobject] = {
            'angry': self._create_angry_eyebrow().set_z_index(7),
            'intrigued': self._create_intrigued_eyebrow().set_z_index(7),
            'surprised': self._create_surprised_eyebrow().set_z_index(7)
        }
        super().__init__(self.eye_background, self.pupil, self.eye_cover,
                         *self.eyebrow_expressions.values(), **kwargs)
        self.shift((LEFT if is_left else RIGHT) * 0.18 + UP * 0.2)

    def _create_angry_eyebrow(self):
        start_pos = (
                (self.eye_background.get_left() if self.is_left else self.eye_background.get_right())
                + UP * self.eye_background.height * 1 / 2
                + (RIGHT if self.is_left else LEFT) * self.eye_background.width * 1 / 10
        )
        end_pos = (
                (self.eye_background.get_right() if self.is_left else self.eye_background.get_left())
                + UP * self.eye_background.height * 3 / 10
        )
        return Line(start_pos, end_pos, color=GREY_BROWN, stroke_width=7)

    def _create_intrigued_eyebrow(self):
        arc = Arc(radius=0.2, color=GREY_BROWN, angle=120 * DEGREES, start_angle=30 * DEGREES,
                  fill_opacity=0)
        arc.stretch(0.4, dim=1)
        arc.next_to(self.eye_background, UP, buff=0.05)
        if not self.is_left:
            arc.points = arc.points[::-1]
        return arc

    def _create_surprised_eyebrow(self):
        arc = Arc(radius=0.2, color=GREY_BROWN, angle=120 * DEGREES, start_angle=30 * DEGREES)
        arc.next_to(self.eye_background, UP, buff=0.15)
        arc.rotate(10 * DEGREES * (1 if self.is_left else -1), about_point=self.eye_background.get_center())
        if not self.is_left:
            arc.points = arc.points[::-1]
        return arc

    def animate_create(self) -> Animation:
        for eyebrow_type in self.eyebrow_expressions:
            self.eyebrow_expressions[eyebrow_type].set_stroke(opacity=0)

        return LaggedStart(
            Create(self.eye_background, run_time=1.3),
            FadeIn(self.pupil),
            FadeIn(self.eye_cover, run_time=0.1),
            lag_ratio=0.2
        )

    def animate_close(self, **kwargs) -> Animation:
        return self.eye_cover.animate(**kwargs).set_fill(opacity=1)

    def animate_open(self, **kwargs) -> Animation:
        return self.eye_cover.animate(**kwargs).set_fill(opacity=0)

    def animate_blink(self, **kwargs) -> Animation:
        return self.animate_close(rate_func=there_and_back_with_pause, **kwargs)

    def animate_look(self, direction: Vector3D, **kwargs):
        return self.pupil.animate(**kwargs).shift(direction * 0.01)

    def animate_triangle_eye(self, additional_scale: float = 1, **kwargs) -> Animation:
        triangle_shape = Polygon(ORIGIN + LEFT * 1, ORIGIN + RIGHT * 1 + DOWN * 0.1,
                                 ORIGIN + UP * 2.25 + LEFT * 0.4,
                                 color=BLACK, fill_color=WHITE, fill_opacity=1).scale(0.25 * additional_scale)
        triangle_shape.move_to(self.eye_background.get_center() +
                               UP * additional_scale * 0.1 + RIGHT * additional_scale * 0.05)
        # if not self.is_left:
        #     triangle_shape.rotate(10 * DEGREES).shift(LEFT * 0.025 + UP * 0.025)
        triangle_cover = triangle_shape.copy().set_fill(opacity=0)
        return AnimationGroup(
            Transform(self.eye_background, triangle_shape, **kwargs),
            Transform(self.eye_cover, triangle_cover, **kwargs)
        )

    def animate_square_eye(self, additional_scale: float = 1, **kwargs) -> Animation:
        square_shape = Polygon(ORIGIN + LEFT * 0.9 + DOWN * 0.3, ORIGIN + RIGHT * 0.8 + DOWN * 0.5,
                               ORIGIN + UP * 1.5 + RIGHT * 1.1, ORIGIN + UP * 1.2 + LEFT * 1,
                               color=BLACK, fill_color=WHITE, fill_opacity=1).scale(0.21 * additional_scale)
        square_shape.move_to(self.eye_background)
        square_cover = square_shape.copy().set_fill(opacity=0)
        return AnimationGroup(
            Transform(self.eye_background, square_shape, **kwargs),
            Transform(self.eye_cover, square_cover, **kwargs)
        )

    def animate_angry_eye(self, **kwargs) -> Animation:
        eyebrow: VMobject = self.eyebrow_expressions['angry']
        eyebrow.set_stroke(opacity=1)
        return Create(eyebrow, **kwargs)

    def animate_intrigued_eye(self, **kwargs) -> Animation:
        eyebrow: VMobject = self.eyebrow_expressions['intrigued']
        eyebrow.set_stroke(opacity=1)
        return CreateWithMovement(eyebrow, eyebrow.height * 2 * DOWN, **kwargs)

    def animate_move_eyebrow(self, relative_movement: Vector3D, eyebrow: str = 'intrigued', **kwargs) -> (
            _AnimationBuilder | Self):
        eyebrow: VMobject = self.eyebrow_expressions.get(eyebrow, self.eyebrow_expressions['intrigued'])
        eyebrow.set_stroke(opacity=1)
        movement: Vector3D = relative_movement * eyebrow.height
        return eyebrow.animate(**kwargs).shift(movement)

    def animate_surprised_eye(self, rate_func=linear, **kwargs) -> Animation:
        eyebrow: VMobject = self.eyebrow_expressions['surprised']
        eyebrow.set_stroke(opacity=1)
        # eyebrow.set_opacity(1)
        return LaggedStart(
            FadeInWithMovementAndScale(
                eyebrow.height * 2 * DOWN, 0.2,
                eyebrow, rate_func=rate_func, **kwargs
            ),
            self.animate_eye_flex(run_time=1.3),
            lag_ratio=0.2
        )

    def animate_eye_flex(self, run_time: float = 0.6, scale: float = 1.1):
        return AnimationGroup(
            self.eye_background.animate(run_time=run_time, rate_func=there_and_back).scale(scale),
            self.eye_cover.animate(run_time=run_time, rate_func=there_and_back).scale(scale)
        )

    def get_shown_eyebrows(self) -> list[str]:
        eyebrows_shown: list[str] = []
        for key in self.eyebrow_expressions:
            if self.eyebrow_expressions.get(key).stroke_opacity > 0:
                eyebrows_shown.append(key)
        return eyebrows_shown

    def animate_hide_eyebrow(self, eyebrow_type: str, **kwargs) -> Animation:
        eyebrow = self.eyebrow_expressions.get(eyebrow_type, self.eyebrow_expressions['intrigued'])
        return FadeOut(eyebrow, **kwargs)


class XCharacter(VGroup):
    def __init__(self, **kwargs):
        self.straight_arm = self._create_arm('straight_arm')
        self.curved_arm = self._create_arm('curved_arm').scale(1.25).align_to(self.straight_arm, DOWN)
        self.wave_arm = self._create_arm('curved_arm_wave').scale(1.25).align_to(self.straight_arm, DOWN)
        self.left_eye = Eye()
        self.right_eye = Eye(is_left=False)
        self.eyes = [self.left_eye, self.right_eye]

        super().__init__(self.straight_arm, self.curved_arm, self.left_eye, self.right_eye, **kwargs)
        self.scale_factor = 1

    def _create_arm(self, arm_name: str) -> SVGMobject:
        return SVGMobject(
            file_name=f'svg/x_char_{arm_name}.svg',
            fill_color=excel_constants.EP_GREEN, fill_opacity=1,
            stroke_color=excel_constants.EP_EXCEL_GREEN, stroke_width=2
        )

    def scale(self, scale_factor: float, **kwargs) -> Self:
        self.scale_factor = scale_factor
        return super().scale(scale_factor, **kwargs)

    def animate_blink(self, blink_time: float = 0.4):
        return AnimationGroup(
            self.left_eye.animate_blink(run_time=blink_time),
            self.right_eye.animate_blink(run_time=blink_time)
        )

    def animate_triangle_eyes(self, **kwargs):
        return AnimationGroup(
            *[eye.animate_triangle_eye(additional_scale=self.scale_factor, **kwargs) for eye in self.eyes]
        )

    def animate_square_eyes(self, **kwargs):
        return AnimationGroup(
            *[eye.animate_square_eye(additional_scale=self.scale_factor, **kwargs) for eye in self.eyes]
        )

    def animate_angry_eyes(self, **kwargs):
        return AnimationGroup(
            *[eye.animate_angry_eye(**kwargs) for eye in self.eyes]
        )

    def animate_intrigued_eyes(self, **kwargs):
        return AnimationGroup(
            *[eye.animate_intrigued_eye(**kwargs) for eye in self.eyes]
        )

    def animate_think_eye(self, **kwargs):
        return self.left_eye.animate_move_eyebrow(relative_movement=UP * 2,
                                                  rate_func=there_and_back_with_pause,
                                                  run_time=1.5, **kwargs)

    def animate_hide_eyebrow(self, eyebrow_type: str, **kwargs) -> Animation:
        return AnimationGroup(
            *[eye.animate_hide_eyebrow(eyebrow_type, **kwargs) for eye in self.eyes]
        )

    def true_hide_eyebrow(self, eyebrow_type: str):
        for eye in self.eyes:
            eyebrow = eye.eyebrow_expressions.get(eyebrow_type)
            if eyebrow:
                eyebrow.set_stroke(opacity=0)

    def animate_surprised_eyes(self, **kwargs):
        return AnimationGroup(
            *[eye.animate_surprised_eye(**kwargs) for eye in self.eyes]
        )

    def animate_look(self, direction: Vector3D, **kwargs):
        return AnimationGroup(*[eye.animate_look(direction, **kwargs) for eye in self.eyes])

    def animate_create(self):
        straight_arm_animation = DrawBorderThenFill(self.straight_arm, run_time=2)
        curved_arm_animation = DrawBorderThenFill(self.curved_arm, run_time=2)
        arm_animations = LaggedStart(straight_arm_animation, curved_arm_animation, lag_ratio=0.2)

        eye_animations = LaggedStart(
            *[eye.animate_create() for eye in self.eyes[::-1]],
            lag_ratio=0.2
        )

        return Succession(LaggedStart(arm_animations, eye_animations, lag_ratio=0.3))

    def animate_wave_transform(self):
        tmp_points = self.wave_arm[0].points
        new_arm = self.curved_arm[0].copy()
        for i in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
            new_arm.points[i] = tmp_points[i]
        return Transform(self.curved_arm[0], new_arm, rate_func=there_and_back, run_time=2)

    def animate_lean_eyes(self,
                          angle: float = PI / 8,
                          axis: Vector3D = OUT,
                          rate_func=there_and_back_with_pause,
                          **kwargs):
        return AnimationGroup(
            *[eye.animate(rate_func=rate_func, **kwargs).rotate(angle=angle, axis=axis, about_point=self.get_center())
              for eye in self.eyes]
        )

    def animate_twist_and_shout(self,
                                angle: float = PI / 5,
                                rate_func=there_and_back_with_pause,
                                **kwargs) -> Animation:
        center = self.get_center()
        top_y = self.get_top()[1]
        longest_distance = top_y - center[1]
        self.save_state()

        def apply_rotation_to_points(points):
            rotated_points = points.copy()
            for i in range(len(points)):
                y_distance = points[i][1] - center[1]
                if y_distance > 0:
                    rotation_factor = y_distance / longest_distance
                    point_angle = angle * rotation_factor
                    rot_matrix = rotation_matrix(point_angle, UP)
                    rotated_points[i] = np.dot(rot_matrix, points[i])
            return rotated_points

        # rot_matrix = rotation_matrix(angle, UP)
        return self.animate(rate_func=rate_func, **kwargs).apply_points_function_about_point(
            apply_rotation_to_points, center, **kwargs
        )


        # def offset_rotation
        # # def rotation_calculation(theta: float) -> Vector3D:
        # #     rot_matrix = rotation_matrix(theta, UP)
        #
        # rotation_centre = self.get_center()
        # farthest_point = self.get_top()
        # longest_distance = farthest_point[1] - rotation_centre[1]
        #
        # # self.apply_points_function_about_point(
        # #     lambda points: np.dot(points, rotation_matrix(angle * alpha, UP).T), about_point, **kwargs
        # # )
        # return UpdateFromAlphaFunc(
        #     self,
        #     lambda mob, alpha: mob.become(
        #         self.copy().apply_points_function_about_point(
        #             lambda p: np.dot(p, rotation_matrix(angle * alpha, UP).T),
        #             about_point=rotation_centre
        #         )
        #     ),
        #     **kwargs
        # )

        # return self.animate(rate_func=rate_func, **kwargs).rotate(angle=angle, axis=axis, about_point=self.get_center())

        # animations: list[Animation] = []
        # start_pos: Vector3D = (config.frame_width / 2 + max(
        #     [pokemon.width for pokemon in pokemon_group])) * RIGHT + DOWN * 1.5
        # for pokemon in pokemon_group:
        #     pokemon_start_width: float = pokemon.width
        #     pokemon.prev_rotation = 0
        #
        #     pokemon_updater = partial(pokemon_carousel,
        #                               start_width=pokemon_start_width,
        #                               start_loc=start_pos
        #                               )
        #
        #     animations.append(UpdateFromAlphaFunc(
        #         pokemon,
        #         pokemon_updater,
        #         run_time=10,
        #         rate_func=rate_functions.ease_out_sine)
        #     )
        # return UpdateFromAlphaFunc(
        #     self,
        #     lambda mob, alpha: mob.become(
        #         self.copy().apply_function(
        #             lambda p: p + wave_function(alpha)
        #             if (p[0] > tmp_arm.get_center()[0]
        #                 and p[1] > tmp_arm.get_center()[1])
        #             else p
        #         )
        #     )
        # ).set_run_time(2)

    def animate_wave_shift(self):
        def wave_function(t: float):
            t_adjustment: float = 0.5
            adj_t: float = t - t_adjustment

            b: float = 0.18
            c: float = 0.15
            angle: float = -30 * np.pi / 180

            def x_calc(a: float):
                return b * np.sin(2 * np.pi * a)

            def y_calc(a: float):
                return c * np.cos(2 * np.pi * a)

            # Calculate point on the ellipse
            x = x_calc(adj_t) - x_calc(-t_adjustment)
            y = y_calc(adj_t) - y_calc(-t_adjustment)

            x_rotated = x * np.cos(angle) - y * np.sin(angle)
            y_rotated = x * np.sin(angle) + y * np.cos(angle)

            return np.array([x_rotated, y_rotated, 0])

        tmp_arm = self.curved_arm[0].copy()

        return UpdateFromAlphaFunc(
            self.curved_arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(
                    lambda p: p + wave_function(alpha)
                    if (p[0] > tmp_arm.get_center()[0]
                        and p[1] > tmp_arm.get_center()[1])
                    else p
                )
            )
        ).set_run_time(2)

    def animate_wave_half_circle(self):
        def wave_function(t: float):
            t_adjustment: float = 0.5

            # Adjust t to create a back-and-forth motion
            if t < 0.5:
                adj_t = 2 * t - t_adjustment
            else:
                adj_t = 2 * (1 - t) - t_adjustment

            # Ellipse parameters
            b: float = 0.18  # semi-major axis (height)
            c: float = 0.15  # semi-minor axis (width)
            angle: float = -30 * np.pi / 180  # tilt angle in radians

            def x_calc(a: float):
                return b * np.sin(np.pi * a)  # Changed to np.pi to limit the motion

            def y_calc(a: float):
                return c * np.cos(np.pi * a)  # Changed to np.pi to limit the motion

            # Calculate point on the ellipse
            x = x_calc(adj_t) - x_calc(-t_adjustment)
            y = y_calc(adj_t) - y_calc(-t_adjustment)

            # Rotate the point
            x_rotated = x * np.cos(angle) - y * np.sin(angle)
            y_rotated = x * np.sin(angle) + y * np.cos(angle)

            return np.array([x_rotated, y_rotated, 0])

        tmp_arm = self.curved_arm[0].copy()
        # Animate the waving motion
        return UpdateFromAlphaFunc(
            self.curved_arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(
                    lambda p: p + wave_function(alpha)
                    if (p[0] > tmp_arm.get_center()[0]
                        and p[1] > tmp_arm.get_center()[1])
                    else p
                )
            )
        ).set_run_time(2)

    def animate_jump(self):
        jump_height = 0.5
        jump_time = 1.5
        squat_scale_y = 0.9  # Vertical scale for squatting
        squat_scale_x = 1.1  # Horizontal scale for squatting
        stretch_scale_y = 1.1  # Vertical scale for stretching
        stretch_scale_x = 0.95  # Horizontal scale for stretching

        def jump_function(t):
            if t < 0.2:  # Initial squat
                progress = t / 0.2
                scale_y = 1 + (squat_scale_y - 1) * progress
                scale_x = 1 + (squat_scale_x - 1) * progress
                return -0.05 * np.sin(np.pi * progress), scale_x, scale_y
            elif t < 0.8:  # Main jump
                t_adjusted = (t - 0.2) / 0.6
                if t_adjusted < 0.5:
                    scale_y = 1 + (stretch_scale_y - 1) * (t_adjusted * 2)
                    scale_x = 1 + (stretch_scale_x - 1) * (t_adjusted * 2)
                else:
                    scale_y = stretch_scale_y + (1 - stretch_scale_y) * ((t_adjusted - 0.5) * 2)
                    scale_x = stretch_scale_x + (1 - stretch_scale_x) * ((t_adjusted - 0.5) * 2)
                return jump_height * np.sin(np.pi * t_adjusted), scale_x, scale_y
            else:  # Landing and recovery
                t_adjusted = (t - 0.8) / 0.2
                y = max(0, jump_height * np.sin(np.pi * 0.8 + np.pi * t_adjusted * 0.2))
                if t_adjusted < 0.5:
                    scale_y = 1 + (squat_scale_y - 1) * (1 - t_adjusted * 2)
                    scale_x = 1 + (squat_scale_x - 1) * (1 - t_adjusted * 2)
                else:
                    scale_y = squat_scale_y + (1 - squat_scale_y) * ((t_adjusted - 0.5) * 2)
                    scale_x = squat_scale_x + (1 - squat_scale_x) * ((t_adjusted - 0.5) * 2)
                return y, scale_x, scale_y

        char_mobs = [self, self.straight_arm, self.curved_arm, self.left_eye, self.right_eye]

        def create_update_func(mob):
            initial_center = mob.get_center()
            initial_height = mob.get_height()
            initial_width = mob.get_width()

            def update_func(m, alpha):
                y_offset, scale_x, scale_y = jump_function(alpha)
                m.move_to(initial_center + np.array([0, y_offset, 0]))
                new_height = initial_height * scale_y
                new_width = initial_width * scale_x
                m.stretch_to_fit_height(new_height)
                m.stretch_to_fit_width(new_width)
                return m

            return update_func

        animations = [
            UpdateFromAlphaFunc(
                mob,
                create_update_func(mob),
                run_time=jump_time
            ) for mob in char_mobs
        ]

        return AnimationGroup(*animations)

    def animate_spin(self, clockwise: bool = True):
        return Rotate(self, angle=PI * (-2 if clockwise else 2), about_point=self.get_center(), run_time=2)

    def animate_wave_bouncing(self):
        def wave_function(t: float):
            x = 0.2 * np.sin(2 * np.pi * t)
            y = 0.1 * np.abs(np.sin(4 * np.pi * t))
            return np.array([x, y, 0])

        tmp_arm = self.curved_arm[0].copy()
        return UpdateFromAlphaFunc(
            self.curved_arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(
                    lambda p: p + wave_function(alpha)
                    if (p[0] > tmp_arm.get_center()[0] and p[1] > tmp_arm.get_center()[1])
                    else p
                )
            )
        ).set_run_time(2)

    def rotate_arms(self, clockwise_curved: bool = True, clockwise_straight: bool = False, angle_rad: float = PI * 0.1):
        return AnimationGroup(
            Rotate(self.curved_arm, angle=angle_rad * (-1 if clockwise_curved else 1), about_point=self.get_center(),
                   run_time=2),
            Rotate(self.straight_arm, angle=angle_rad * (-1 if clockwise_straight else 1),
                   about_point=self.get_center(), run_time=2)
        )

    def rotate_arms_there_and_back(self, clockwise_curved: bool = True, clockwise_straight: bool = False,
                                   angle_rad: float = PI * 0.1):
        return (self.rotate_arms(clockwise_curved, clockwise_straight, angle_rad)
                .set_rate_func(there_and_back))

    def get_arm_flex_animation(self, use_straight_arm: bool = True, bend_multiplier: float = 0.15):
        arm = self.straight_arm if use_straight_arm else self.curved_arm

        def flex_function(t: float):
            bend_amount = bend_multiplier * np.sin(np.pi * t)

            def apply_flex(p):
                x, y, z = p
                x_min, x_max = arm[0].get_left()[0], arm[0].get_right()[0]
                x_range = x_max - x_min
                x_progress = (x - x_min) / x_range
                return np.array([x, y + bend_amount * np.sin(x_progress * np.pi), z])

            return apply_flex

        tmp_arm = arm[0].copy()

        return UpdateFromAlphaFunc(
            arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(flex_function(alpha))
            )
        ).set_run_time(1.5)

    def get_flatten_wave_animation(self):
        def waving_rate_func(t: float, inflection: float = 10.0) -> float:
            new_t = np.interp(t, [0, 0.25, 0.5, 0.75, 1], [0, 0.5, 0.1, 0.5, 1])
            return smooth(new_t, inflection)

        return self.get_arm_flatten_animation().set_run_time(2.5).set_rate_func(waving_rate_func)

    def get_arm_flatten_animation(self, flatten_multiplier: float = 0.5):
        arm = self.curved_arm

        def flex_function(t: float):
            bend_amount = flatten_multiplier * np.sin(np.pi * t) * 0.8

            def apply_flex(p):
                x, y, z = p
                x_min, x_max = arm[0].get_left()[0], arm[0].get_right()[0]
                x_range = x_max - x_min
                x_progress = (x - x_min) / x_range
                x_progress = x_progress ** 10

                return np.array([x, y + bend_amount * x_progress, z])

            return apply_flex

        tmp_arm = arm[0].copy()

        return UpdateFromAlphaFunc(
            arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(flex_function(alpha))
            )
        ).set_run_time(1.5)

    def get_puff_animation(self):

        def get_alpha_adj(alpha: float) -> float:
            return (-math.cos(alpha * PI * 2) + 1) * 0.05

        def get_new_positition(start_pos: Vector3D, v_mov: float, multiplier: float = 1.0) -> Vector3D:
            return start_pos + v_mov * UP * multiplier

        def move_eye(eye: Eye, alpha: float, start_pos: Vector3D):
            alpha_adj = get_alpha_adj(alpha)
            eye.eye_background.move_to(get_new_positition(start_pos, alpha_adj))
            eye.pupil.move_to(get_new_positition(start_pos, alpha_adj, 1.5))

        def move_eye_cover(cover: Mobject, alpha: float, start_pos: Vector3D):
            alpha_adj = get_alpha_adj(alpha)
            cover.move_to(get_new_positition(start_pos, alpha_adj))

        return AnimationGroup(
            self.get_arm_flex_animation(),
            self.get_arm_flatten_animation(),
            UpdateFromAlphaFunc(
                self.left_eye,
                partial(move_eye, start_pos=self.left_eye.get_center()),
                run_time=1.5
            ),
            UpdateFromAlphaFunc(
                self.right_eye,
                partial(move_eye, start_pos=self.right_eye.get_center()),
                run_time=1.5
            ),
            UpdateFromAlphaFunc(
                self.left_eye_cover,
                partial(move_eye_cover, start_pos=self.left_eye_cover.get_center()),
                run_time=1.5
            ),
            UpdateFromAlphaFunc(
                self.right_eye_cover,
                partial(move_eye_cover, start_pos=self.right_eye_cover.get_center()),
                run_time=1.5
            )
        )

    def get_arm_rotation_animation(self, angle=PI / 16):
        # Get all points of the straight arm
        arm_points = self.straight_arm[0].get_points()

        rotation_point = arm_points[25] + np.array([0.15, 0.1, 0])

        def rotation_function(t: float):
            current_angle = angle * np.sin(np.pi * t)

            def apply_rotation(p):
                x, y, z = p - rotation_point
                rotated_x = x * np.cos(current_angle) - y * np.sin(current_angle)
                rotated_y = x * np.sin(current_angle) + y * np.cos(current_angle)
                return np.array([rotated_x, rotated_y, z]) + rotation_point

            return apply_rotation

        tmp_arm = self.straight_arm[0].copy()
        return Rotate(self.straight_arm, angle=angle, about_point=rotation_point,
                      run_time=2, rate_func=there_and_back)
        # return UpdateFromAlphaFunc(
        #     self.straight_arm[0],
        #     lambda mob, alpha: mob.become(
        #         tmp_arm.copy().apply_function(rotation_function(alpha))
        #     )
        # ).set_run_time(run_time)

    def get_arm_extend_animation(self):
        # Get all points of the straight arm
        original_points = self.straight_arm[0].get_points()

        # Find the bottom-most and top-most points
        bottom_point = original_points[np.argmin(original_points[:, 1])]
        top_point = original_points[np.argmax(original_points[:, 1])]

        # Calculate the midpoint
        midpoint_y = (bottom_point[1] + top_point[1]) / 2

        # Calculate the original height of the upper half
        original_upper_height = top_point[1] - midpoint_y

        def extend_function(t: float):
            extend_factor = 1 + 0.2 * np.sin(np.pi * t)  # Extend up to 20% longer

            def apply_extend(p):
                if p[1] <= midpoint_y:
                    # If the point is in the lower half, don't change it
                    return p
                else:
                    # If the point is in the upper half, scale its y-coordinate
                    relative_y = (p[1] - midpoint_y) / original_upper_height
                    new_y = midpoint_y + relative_y * original_upper_height * extend_factor
                    return np.array([p[0], new_y, p[2]])

            return apply_extend

        tmp_arm = self.straight_arm[0].copy()

        return UpdateFromAlphaFunc(
            self.straight_arm[0],
            lambda mob, alpha: mob.become(
                tmp_arm.copy().apply_function(extend_function(alpha))
            )
        ).set_run_time(2)

    def get_arm_wave_animation(self):
        wave_time = 2
        wave_amplitude = 0.1  # Maximum wave amplitude
        wave_frequency = 1  # Number of complete waves in the animation

        def wave_function(t):
            # Create a wave that's stronger at the top of the arm
            def apply_wave(y_progress):
                wave = wave_amplitude * y_progress * np.sin(2 * np.pi * (wave_frequency * t + y_progress))
                return wave, 0, 1, 1  # x_offset, y_offset, scale_x, scale_y

            return apply_wave

        char_mobs = [self.straight_arm[0]]  # We only want to animate the straight arm

        def create_update_func(mob):
            initial_points = mob.get_points()
            y_min, y_max = initial_points[:, 1].min(), initial_points[:, 1].max()
            y_range = y_max - y_min

            def update_func(m, alpha):
                new_points = initial_points.copy()
                for i, point in enumerate(new_points):
                    y_progress = (point[1] - y_min) / y_range
                    x_offset, y_offset, scale_x, scale_y = wave_function(alpha)(y_progress)
                    new_points[i, 0] += x_offset
                m.set_points(new_points)
                return m

            return update_func

        animations = [
            UpdateFromAlphaFunc(
                mob,
                create_update_func(mob),
                run_time=wave_time
            ) for mob in char_mobs
        ]

        return AnimationGroup(*animations)

    def get_body_shake_animation(self):
        shake_time = 1
        shake_amplitude_x = 0.05
        shake_amplitude_y = 0.03
        shake_frequency = 4  # Number of complete shakes per second

        def shake_function(t):
            shake_x = shake_amplitude_x * np.sin(2 * np.pi * shake_frequency * t)
            shake_y = shake_amplitude_y * np.cos(2 * np.pi * shake_frequency * t)
            return shake_x, shake_y, 1, 1  # x_offset, y_offset, scale_x, scale_y

        char_mobs = [self, self.straight_arm, self.curved_arm, self.left_eye, self.right_eye, self.left_eye_cover,
                     self.right_eye_cover]

        def create_update_func(mob):
            initial_center = mob.get_center()
            initial_height = mob.get_height()
            initial_width = mob.get_width()

            def update_func(m, alpha):
                x_offset, y_offset, scale_x, scale_y = shake_function(alpha)
                m.move_to(initial_center + np.array([x_offset, y_offset, 0]))
                new_height = initial_height * scale_y
                new_width = initial_width * scale_x
                m.stretch_to_fit_height(new_height)
                m.stretch_to_fit_width(new_width)
                return m

            return update_func

        animations = [
            UpdateFromAlphaFunc(
                mob,
                create_update_func(mob),
                run_time=shake_time
            ) for mob in char_mobs
        ]

        return AnimationGroup(*animations)


class WaveGoodbye(Scene):
    def construct(self):
        char = XCharacter().scale(1.3)
        self.wait()
        self.play(char.animate_create())
        self.wait(0.5)
        self.play(char.animate_jump())
        self.play(char.get_flatten_wave_animation())
        self.wait()


class Test(Scene):
    def construct(self):
        char = XCharacter()
        char.scale(1.5)
        char.to_corner(DL)

        self.play(char.animate_create())

        # self.play(char.animate_intrigued_eyes())
        # self.wait()
        # self.play(char.animate_think_eye())
        # self.wait()
        # self.play(char.animate_hide_eyebrow('intrigued'))
        # char.true_hide_eyebrow('intrigued')
        # self.wait()
        # self.play(char.animate_angry_eyes())
        # self.wait()
        # self.play(char.animate_hide_eyebrow('angry'))
        # char.true_hide_eyebrow('angry')
        # self.wait()
        # self.play(char.animate_surprised_eyes())
        # self.wait()
        # self.play(char.animate_hide_eyebrow('surprised'))
        # char.true_hide_eyebrow('surprised')
        # self.wait()
        #
        # self.play(char.animate_square_eyes())
        # self.play(char.animate_blink())
        # self.play(char.animate_look(UP * 3))
        # self.play(char.animate_look(DOWN * 6 + RIGHT * 7))
        # self.play(char.animate_lean_eyes())
        # self.wait(2)

        self.play(char.animate_twist_and_shout())
        self.wait(2)
        # self.play(char.animate_wave_shift())
        # self.play(char.animate_wave_half_circle())

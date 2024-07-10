from manim import *
from manim.typing import Vector3D
import re
import excel_constants


class Eye(VGroup):
    def __init__(self, **kwargs):
        self.eye_background = Circle(radius=0.2, color=BLACK, fill_color=WHITE, fill_opacity=1)
        outer_pupil = Circle(radius=0.1, color=excel_constants.EP_GREEN, fill_color=BLACK, fill_opacity=1)
        pupil_highlight = (AnnularSector(outer_radius=0.08, inner_radius=0.04, angle=75 * DEGREES, fill_color=WHITE,
                                         fill_opacity=1, stroke_opacity=0)
                           .flip(Y_AXIS).move_to(outer_pupil.get_center()).shift(LEFT * 0.02 + UP * 0.02))
        self.pupil = VGroup(outer_pupil, pupil_highlight)
        super().__init__(self.eye_background, self.pupil, **kwargs)

    def get_animation_for_look(self, direction: Vector3D):
        return self.pupil.animate.shift(direction * 0.01)


class XCharacter(VGroup):
    def __init__(self, **kwargs):
        self.straight_arm = SVGMobject(
            file_name='svg/x_char_straight_arm.svg',
            fill_color=excel_constants.EP_GREEN, fill_opacity=1,
            stroke_color=excel_constants.EP_EXCEL_GREEN
        )
        self.curved_arm = (SVGMobject(
            file_name='svg/x_char_curved_arm.svg',
            fill_color=excel_constants.EP_GREEN, fill_opacity=1,
            stroke_color=excel_constants.EP_EXCEL_GREEN
        ).scale(1.25).align_to(self.straight_arm, DOWN))

        self.wave_arm = (SVGMobject(
            file_name='svg/x_char_curved_arm_wave.svg',
            fill_color=excel_constants.EP_GREEN, fill_opacity=1,
            stroke_color=excel_constants.EP_EXCEL_GREEN
        ).scale(1.25).align_to(self.straight_arm, DOWN))

        self.left_eye = Eye().shift(LEFT * 0.18 + UP * 0.2)
        self.right_eye = Eye().shift(RIGHT * 0.18 + UP * 0.2).set_z_index(2)
        self.left_eye_cover = self.left_eye.eye_background.copy().set_fill(opacity=0).set_z_index(1)
        self.right_eye_cover = self.right_eye.eye_background.copy().set_fill(opacity=0).set_z_index(3)

        super().__init__(self.straight_arm, self.curved_arm, self.left_eye, self.right_eye,
                         self.left_eye_cover, self.right_eye_cover, **kwargs)
        # self.left_eye.z_index = 2
        # self.right_eye_cover.z_index = 1

    def get_animation_for_look(self, direction: Vector3D, run_time: float = 1):
        return AnimationGroup(self.left_eye.get_animation_for_look(direction),
                              self.right_eye.get_animation_for_look(direction), run_time=run_time)

    def get_animation_draw_then_fill(self):
        straight_arm_animation = DrawBorderThenFill(self.straight_arm, run_time=2)
        curved_arm_animation = DrawBorderThenFill(self.curved_arm, run_time=2)
        arm_animations = LaggedStart(straight_arm_animation, curved_arm_animation, lag_ratio=0.2)

        left_eye_background_animations = Create(self.left_eye.eye_background, run_time=1.3)
        right_eye_background_animations = Create(self.right_eye.eye_background, run_time=1.3)
        eye_background_animations = LaggedStart(left_eye_background_animations,
                                                right_eye_background_animations, lag_ratio=0.2)

        left_pupil_animation = FadeIn(self.left_eye.pupil, run_time=1)
        right_pupil_animation = FadeIn(self.right_eye.pupil, run_time=1)
        pupil_animations = LaggedStart(left_pupil_animation, right_pupil_animation, lag_ratio=0.2)

        eye_cover_animations = FadeIn(self.left_eye_cover, self.right_eye_cover, run_time=0.1)

        return Succession(LaggedStart(arm_animations, eye_background_animations,
                                      pupil_animations, lag_ratio=0.3), eye_cover_animations)

    def get_wave_by_transform_animation(self):
        tmp_points = self.wave_arm[0].points
        new_arm = self.curved_arm[0].copy()
        for i in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
            new_arm.points[i] = tmp_points[i]
        return Transform(self.curved_arm[0], new_arm, rate_func=there_and_back, run_time=2)

    def get_wave_by_shift_animation(self):
        def wave_function(t: float):
            t_adjustment: float = 0.5
            adj_t: float = t - t_adjustment

            # Ellipse parameters
            b: float = 0.18  # semi-major axis (height)
            c: float = 0.15  # semi-minor axis (width)
            angle: float = -30 * np.pi / 180  # tilt angle in radians

            def x_calc(a: float):
                return b * np.sin(2 * np.pi * a)

            def y_calc(a: float):
                return c * np.cos(2 * np.pi * a)

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

    def get_half_circle_wave_animation(self):
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

    def get_jump_animation(self):
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

        char_mobs = [self, self.straight_arm, self.curved_arm, self.left_eye, self.right_eye, self.left_eye_cover,
                     self.right_eye_cover]

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

    def get_spin_animation(self, clockwise: bool = True):
        return Rotate(self, angle=PI * (-2 if clockwise else 2), about_point=self.get_center(), run_time=2)

    def get_bouncing_wave_animation(self):
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

    def get_blink_animation(self, blink_time: float = 0.4):
        return Succession(
            self.get_close_eyes_animation(blink_time / 2),
            self.get_open_eyes_animation(blink_time / 2)
        )

    def get_close_eyes_animation(self, close_time: float = 0.2):
        return AnimationGroup(
            Transform(self.left_eye_cover, self.left_eye.eye_background.copy().set_fill(opacity=1)),
            Transform(self.right_eye_cover, self.right_eye.eye_background.copy().set_fill(opacity=1)),
            run_time=close_time
        )

    def get_open_eyes_animation(self, open_time: float = 0.2):
        return AnimationGroup(
            Transform(self.left_eye_cover, self.left_eye.eye_background.copy().set_fill(opacity=0)),
            Transform(self.right_eye_cover, self.right_eye.eye_background.copy().set_fill(opacity=0)),
            run_time=open_time
        )

    def rotate_arms(self, clockwise_curved: bool = True, clockwise_straight: bool = False, angle_rad: float = PI * 0.1):
        return AnimationGroup(
            Rotate(self.curved_arm, angle=angle_rad * (-1 if clockwise_curved else 1), about_point=self.get_center(), run_time=2),
            Rotate(self.straight_arm, angle=angle_rad * (-1 if clockwise_straight else 1), about_point=self.get_center(), run_time=2)
        )

    def rotate_arms_there_and_back(self, clockwise_curved: bool = True, clockwise_straight: bool = False, angle_rad: float = PI * 0.1):
        return (self.rotate_arms(clockwise_curved, clockwise_straight, angle_rad)
                .set_rate_func(there_and_back))

    def get_arm_flex_animation(self, use_straight_arm: bool = True):
        arm = self.straight_arm if use_straight_arm else self.curved_arm
        def flex_function(t: float):
            bend_amount = 0.1 * np.sin(np.pi * t)

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


class CharacterAnimation(Scene):
    def construct(self):
        character = XCharacter()
        self.add(character)

        original_arm = character.curved_arm[0]
        new_arm = original_arm.copy()

        tmp_points = character.wave_arm[0].points
        for i in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]:
            new_arm.points[i] = tmp_points[i]
        # self.play(Transform(original_arm, new_arm), rate_func=there_and_back, run_time=2)

        anims_fn = [
            character.rotate_arms_there_and_back,
            character.get_arm_flex_animation,
            character.get_arm_rotation_animation,
            character.get_arm_extend_animation,
            character.get_arm_wave_animation,
            character.get_body_shake_animation,

            character.get_wave_by_transform_animation,
            character.get_wave_by_shift_animation,
            character.get_half_circle_wave_animation,
            character.get_bouncing_wave_animation,
            character.get_jump_animation,
            character.get_spin_animation,
            character.get_blink_animation
        ]

        animation_name = Text(anims_fn[0].__name__)
        animation_name.to_edge(UP)
        self.add(animation_name)
        for anim_fn in anims_fn:
            new_name = Text(anim_fn.__name__)
            new_name.to_edge(UP)
            self.play(Transform(animation_name, new_name))
            self.play(anim_fn())
            self.wait(2)

        self.wait(2)


class TestScene(Scene):
    def construct(self):
        x = XCharacter()
        self.play(x.get_animation_draw_then_fill())
        self.wait(3)
        self.play(x.get_animation_for_look(RIGHT * 9 + UP * 4))
        self.wait(3)

        curves = [
            {
                'type': 'relative',
                'control_points': [
                    np.array([-0.435581, -0.59554, 1]),
                    np.array([-0.238699, -3.55239, 1]),
                    np.array([0.487741, -2.9019, 1])
                ]
            },
            {
                'type': 'absolute',
                'control_points': [
                    np.array([14.155645, 38.744005, 1]),
                    np.array([27.39746, 7.2208952, 1]),
                    np.array([32.6175, 4.2771552, 1])
                ]
            },
            {
                'type': 'relative',
                'control_points': [
                    np.array([2.0789, -1.17235, 1]),
                    np.array([4.81788, -0.80107, 1]),
                    np.array([4.8127, -0.77611, 1])
                ]
            },
            {
                'type': 'absolute',
                'control_points': [
                    np.array([32.11547, -3.1751248, 1]),
                    np.array([15.466713, 40.605565, 1]),
                    np.array([6.3567567, 35.099565, 1])
                ]
            }
        ]

        self.remove(x)
        for curve in curves:
            bez = bezier(curve['control_points'])
            CubicBezier

            pc = ParametricFunction(bez, t_range=np.array([0, 1, 0.001]))
            self.play(Create(pc))
            self.wait(3)
            # self.remove(pc)


class SVGBezierPath(Scene):
    def construct(self):
        # Scaling factor and translation to fit within [-7, 7] x [-4, 4]
        scale_factor = -0.1  # Adjust the scale factor as needed
        x_offset = -3  # Offset to place the start point near the origin
        y_offset = 2.5  # Offset to place the start point near the origin

        def point3D(point):
            return np.array([point[0], point[1], 0])

        p0 = ORIGIN
        p1 = point3D([-0.435581, -0.59554])
        p2 = point3D([-0.238699, -3.55239])
        p3 = point3D([0.487741, -2.9019])

        p4 = point3D([14.155645 - 6, 38.744005 - 35])
        p5 = point3D([27.39746 - 6, 7.22089525])
        p6 = point3D([32.6175 - 6, 4.2771552])

        # p7 = point3D([32.6175 - 6 + 2.0789, 4.2771552 - 1.17235 + 35])
        # p8 = point3D([32.6175 - 6 + 4.81788, 4.2771552 - 0.80107 + 35])
        # p9 = point3D([32.6175 - 6 + 4.8127, 4.2771552 - 0.77611 + 35])
        #
        # p10 = point3D([32.6175 - 6 + 4.8127 - 0.71674, 4.2771552 - 0.77611 + 3.45397 + 35])
        # p11 = point3D([32.6175 - 6 + 4.8127 - 0.71674 - 0.91805, 4.2771552 - 0.77611 + 3.45397 + 0.005 + 35])

        # Create the beziers
        bezier1 = CubicBezier(p0, p1, p2, p3)
        bezier2 = CubicBezier(p3, p4, p5, p6)
        # bezier3 = CubicBezier(p6, p7, p8, p9)
        # line1 = Line(p9, p10)
        # line2 = Line(p10, p11)
        # closing_line = Line(p11, p0)

        # Create the path
        path = VGroup(bezier1, bezier2)  #, bezier3, line1, line2, closing_line)
        self.add(path)
        self.play(Create(path), run_time=4)


class test(Scene):
    def construct(self):
        m = [[0, 0],
             [-0.435581, -0.59554],
             [-0.238699, -3.55239],
             [0.487741, -2.9019]]
        l = [np.array([p] + [0]) for p in m]
        bez = bezier(l)
        pc = ParametricFunction(bez, t_range=np.array([0, 1, 0.001]))
        self.play(Create(pc))
        self.wait(3)
        self.remove(pc)


def draw_curves(start, lines, colors):
    group = VGroup()
    for i, line in enumerate(lines):
        start_point = start if i == 0 else lines[i - 1]['end_point']
        points_simple = [start_point] + (line['control_points'] + [line['end_point']] \
                                             if line['type'] == 'cubic_bezier' else [line['end_point']])
        points = [np.array([point[0], point[1] * -1, 0]) for point in points_simple]

        line['points'] = points
        line_mob = CubicBezier(*points) if line['type'] == 'cubic_bezier' else Line(*points)
        line_mob.set_color(colors[i % len(colors)])
        group.add(line_mob)

    return group


class bez2(Scene):
    def construct(self):
        start = (6, 35)
        lines = [
            # Cubic Bezier curve to (6.487741, 32.0981)
            {
                'type': 'cubic_bezier',
                'control_points': [(5.564419, 34.40446), (5.761301, 31.44761)],
                'end_point': (6.487741, 32.0981)
            },
            # Cubic Bezier curve to (32.6175, 4.2771552)
            {
                'type': 'cubic_bezier',
                'control_points': [(14.155645, 38.744005), (27.39746, 7.2208952)],
                'end_point': (32.6175, 4.2771552)
            },
            # Cubic Bezier curve to (37.4302, 3.5010452)
            {
                'type': 'cubic_bezier',
                'control_points': [(34.6964, 3.1048052), (37.43538, 3.4760852)],
                'end_point': (37.4302, 3.5010452)
            },
            # Line to (36.71346, 6.9550152)
            {
                'type': 'line',
                'end_point': (36.71346, 6.9550152)
            },
            # Line to (35.79541, 6.9600152)
            {
                'type': 'line',
                'end_point': (35.79541, 6.9600152)
            },
            # Cubic Bezier curve to (6.3567567, 35.099565)
            {
                'type': 'cubic_bezier',
                'control_points': [(32.11547, -3.1751248), (15.466713, 40.605565)],
                'end_point': (6.3567567, 35.099565)
            },
            # Close path to (6, 35)
            {
                'type': 'close_path',
                'end_point': (6, 35)
            }
        ]

        group = VGroup()
        colors = [RED, GREEN, BLUE]

        curve_arm = draw_curves(start, lines, colors)
        curve_arm.scale(0.1).move_to(ORIGIN)
        for line in curve_arm:
            self.play(Create(line), run_time=5)
            self.wait(3)
        self.wait(3)

        start = (6, 12)
        lines = [
            # Cubic Bezier curve to (6, 12) (since control points are relative and result in no movement)
            {
                'type': 'cubic_bezier',
                'control_points': [(6, 12), (6, 12)],
                'end_point': (6, 12)
            },
            # Line to (6, 12) with relative horizontal move to
            {
                'type': 'line',
                'end_point': (6, 12)
            },
            # Line to (35.66023, 12)
            {
                'type': 'line',
                'end_point': (35.66023, 12)
            },
            # Cubic Bezier curve to (112.241014, 124.78013)
            {
                'type': 'cubic_bezier',
                'control_points': [(35.918061, 26.156343), (67.621281, 117.59919)],
                'end_point': (112.241014, 124.78013)
            },
            # Line to (112.241014, 124.78013)
            {
                'type': 'line',
                'end_point': (112.241014, 124.78013)
            },
            # Line to (108.358324, 135.34509)
            {
                'type': 'line',
                'end_point': (108.358324, 135.34509)
            },
            # Line to (71.732517, 135.29809)
            {
                'type': 'line',
                'end_point': (71.732517, 135.29809)
            },
            # Cubic Bezier curve to (71.742717, 128.01547)
            {
                'type': 'cubic_bezier',
                'control_points': [(71.737517, 128.04297), (71.742717, 128.01547)],
                'end_point': (71.742717, 128.01547)
            },
            # Line to (71.742717, 128.01547)
            {
                'type': 'line',
                'end_point': (71.742717, 128.01547)
            },
            # Cubic Bezier curve to (71.742717, 122.54903)
            {
                'type': 'cubic_bezier',
                'control_points': [(71.742717, 123.24882), (72.695417, 122.6639)],
                'end_point': (71.742717, 122.54903)
            },
            # Cubic Bezier curve to (15.051116, 12.96748)
            {
                'type': 'cubic_bezier',
                'control_points': [(45.900769, 20.408447), (20.438669, 12.725405)],
                'end_point': (6, 25)
            },
            # Close path to (6, 12)
            {
                'type': 'close_path',
                'end_point': (6, 12)
            }
        ]

        straight_arm = draw_curves(start, lines, colors)
        straight_arm.scale(0.03).move_to(ORIGIN)
        line = ParametricFunction
        for line in straight_arm:
            self.play(Create(line), run_time=5)
            self.wait(3)
        self.wait(3)

from manim import *
from manim.typing import Vector3D

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

        self.curved_down = (SVGMobject(
            file_name='svg/x_char_curved_arm_down.svg',
            fill_color=excel_constants.EP_GREEN, fill_opacity=1,
            stroke_color=excel_constants.EP_EXCEL_GREEN
        ).align_to(self.straight_arm, DOWN))

        self.curved_up = (SVGMobject(
            file_name='svg/x_char_curved_arm_up.svg',
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


class TestScene(Scene):
    def construct(self):
        x = XCharacter()
        self.play(x.get_animation_draw_then_fill())
        self.wait(3)
        self.play(x.get_animation_for_look(RIGHT*9+UP*4))
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
        path = VGroup(bezier1, bezier2)#, bezier3, line1, line2, closing_line)
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
        points = [np.array([point[0], point[1]*-1, 0]) for point in points_simple]

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

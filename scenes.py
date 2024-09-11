from functools import partial

from manim import *

from excel_character import XCharacter
from excel_tables import ExcelTable


class BackgroundScene(Scene):
    def __init__(self):
        super().__init__()
        n_circles = 1000
        concentric = VGroup(*[Circle(radius=0.005 * n, fill_opacity=1) for n in range(n_circles)][::-1])
        concentric.set_z(-250)
        color_1 = ManimColor("#0F0026")
        color_2 = ManimColor("#030008")

        colors = [interpolate_color(color_2,
                                    color_1,
                                    rate_functions.linear(n / (n_circles - 1)))
                  for n in range(n_circles)]
        concentric.set_color_by_gradient(*colors)
        concentric.shift(LEFT * 3.5 + UP * 2)
        self.background = concentric
        self.add(self.background)

    def get_mobjects_except_background(self):
        return [mob for mob in self.mobjects if mob is not self.background]


class BackgroundSceneThreeD(ThreeDScene):
    def __init__(self):
        super().__init__()
        n_circles = 1000
        concentric = VGroup(*[Circle(radius=0.07 * n, fill_opacity=1) for n in range(n_circles)][::-1])
        concentric.set_z(-250)
        color_1 = ManimColor("#0F0026")
        color_2 = ManimColor("#030008")

        colors = [interpolate_color(color_2,
                                    color_1,
                                    rate_functions.linear(n / (n_circles - 1)))
                  for n in range(n_circles)]
        concentric.set_color_by_gradient(*colors)
        scale_up = 13.5
        concentric.shift(LEFT * 3.5 * scale_up + UP * 2 * scale_up)
        self.background = concentric
        self.add(self.background)

        def get_mobjects_except_background(self):
            return [mob for mob in self.mobjects if mob is not self.background]


def create_narration_circle(scene: Scene) -> None:
    c = Circle(radius=0.9, color=YELLOW_E, fill_color=YELLOW_E, fill_opacity=1).to_corner(UR, buff=0.2)
    c.z_index = 100
    scene.add(c)


class NarratedScene(Scene):
    def __init__(self):
        super().__init__()
        create_narration_circle(self)


class IntroScene(Scene):
    def __init__(self, title: str, below_name_line: str = 'Excel Tutorials', title_line_2: str = ''):
        super().__init__()
        self.title = title
        self.below_name_line = below_name_line
        self.title_line_2 = title_line_2

    def construct(self):

        def subscribe_click(mob, alpha, original_width):
            if alpha < 0.5:
                scale = 1 - 0.2 * alpha
            else:
                scale = 0.9 + 0.1 * (alpha - 0.5)
                if mob[0].color == red_color:
                    mob[0].set_color(XKCD.DEEPGREEN)

            mob.scale_to_fit_width(original_width * scale)

        char = XCharacter()
        table_data = [
            ['\\underline{\\textbf{Elliott Paterson}}'],
            [self.below_name_line],
            [f'\\textbf{{{self.title}}}']
        ]
        if self.title_line_2:
            table_data.append([f'\\textbf{{{self.title_line_2}}}'])

        blank_row = [''] * 3
        table_data = [blank_row.copy(), *[['']  + row + [''] for row in table_data], blank_row.copy()]
        print(table_data)
        table = ExcelTable(table_data).scale(0.5)
        table.get_rows()[0].z_index = 10
        table.get_columns()[0].z_index = 10

        red_color = XKCD.TOMATORED
        subscribe_rectangle = RoundedRectangle(corner_radius=0.2,  width=5, height=1,
                                            color=red_color, fill_color=red_color, fill_opacity=1)
        subscribe_tex = Text('Subscribe', font='sans-serif').scale(1.3)
        subscribed_tex = Text('Subscribed', font='sans-serif').scale(1.3)
        play_button = (Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1)
                       .rotate(-90*DEGREES)
                       .stretch(1.3, dim=0)
                       .scale(0.4))

        play_button.corner_radius = 0.05
        play_button.round_corners(play_button.corner_radius)

        play_button.next_to(subscribe_rectangle, LEFT, buff=-(play_button.width + 0.2))
        subscribe_tex.next_to(subscribe_rectangle, RIGHT, buff=-(subscribe_tex.width + 0.2))

        play_button.next_to(subscribe_rectangle, ORIGIN, coor_mask=np.array([0, 1, 0]))
        subscribe_tex.next_to(subscribe_rectangle, ORIGIN, coor_mask=np.array([0, 1, 0]))
        subscribe_tex.shift(UP * 0.02)
        subscribed_tex.move_to(subscribe_tex)

        subscribe_button = VGroup(subscribe_rectangle, play_button, subscribe_tex)#

        subscribe_button.shift(DOWN * 2)
        char.shift(UP * 1)
        table.shift(UP * 1)

        char_transform = AnimationGroup(
                Transform(VGroup(char.straight_arm, char.curved_arm), table.get_background_rectangles()),
                Transform(char.left_eye.eye_background, table.get_columns()[0]),
                Transform(char.right_eye.eye_background, table.get_rows()[0]),
                Transform(char.right_eye_cover, table.get_vertical_lines()),
                Transform(char.left_eye_cover, table.get_horizontal_lines()),
                Transform(VGroup(char.left_eye.pupil, char.right_eye.pupil), table.get_rows()[1:])
            )

        subscribe_button.set_opacity(0)
        sub_anims = [
            Wait(1.3),
            subscribe_button.animate(run_time=0.01).set_opacity(1),
            LaggedStart(DrawBorderThenFill(subscribe_rectangle), DrawBorderThenFill(play_button), Write(subscribe_tex, run_time=1), lag_ratio=0.3),
            UpdateFromAlphaFunc(
                subscribe_button,
                partial(subscribe_click, original_width=subscribe_button.width)
            )
        ]

        self.wait(0.5)
        self.play(Succession(char.animate_create(),
                             char.get_puff_animation(),
                             char_transform.set_run_time(0.5)),
                  Succession(*sub_anims))

        self.wait(0.7)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

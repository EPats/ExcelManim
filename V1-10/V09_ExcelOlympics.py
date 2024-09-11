from functools import partial

from manim import *
from excel_tables import ExcelTable
from excel_character import XCharacter


class OlympicLogo(Scene):

    def construct(self):
        olympic_colours = [
            XKCD.AZURE,
            XKCD.AMBER,
            XKCD.ALMOSTBLACK,
            XKCD.ALGAEGREEN,
            XKCD.LIPSTICK
        ]
        circles = [Circle(radius=1, stroke_color=colour, stroke_width=18) for colour in olympic_colours]

        for i, circle in enumerate(circles, start=-2):
            circle.shift(RIGHT * i * 1.2 + UP)
            circle.shift(UP * 0.5 * (1 if i % 2 == 0 else -1))
            circle.z_index = 4

        red_color = XKCD.TOMATORED
        subscribe_rectangle = RoundedRectangle(corner_radius=0.2, width=5, height=1,
                                               color=red_color, fill_color=red_color, fill_opacity=1)
        subscribe_tex = Text('Subscribe', font='sans-serif').scale(1.3)
        subscribed_tex = Text('Subscribed', font='sans-serif').scale(1.3)
        play_button = (Triangle(color=WHITE, fill_color=WHITE, fill_opacity=1)
                       .rotate(-90 * DEGREES)
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

        subscribe_button = VGroup(subscribe_rectangle, play_button, subscribe_tex)  #

        subscribe_button.shift(DOWN * 2)
        def subscribe_click(mob, alpha, original_width):
            if alpha < 0.5:
                scale = 1 - 0.2 * alpha
            else:
                scale = 0.9 + 0.1 * (alpha - 0.5)
                if mob[0].color == red_color:
                    mob[0].set_color(XKCD.DEEPGREEN)

            mob.scale_to_fit_width(original_width * scale)
        sub_anims = [
            Wait(1),
            subscribe_button.animate(run_time=0.01).set_opacity(1),
            LaggedStart(DrawBorderThenFill(subscribe_rectangle), DrawBorderThenFill(play_button),
                        Write(subscribe_tex, run_time=1), lag_ratio=0.3),
            UpdateFromAlphaFunc(
                subscribe_button,
                partial(subscribe_click, original_width=subscribe_button.width)
            )
        ]

        xchar = XCharacter()
        xchar.scale(0.6).move_to(circles[0].get_center())
        #
        # # char.right_eye.scale(1.2)

        # char.left_eye.eye_background.z_index = 4
        # char.left_eye.pupil.z_index = 10
        #
        xchar.left_eye_cover.set_stroke(width=0)
        xchar.right_eye_cover.set_stroke(width=0)
        xchar.left_eye.eye_background.set_stroke(width=1.1)
        xchar.right_eye.eye_background.set_stroke(width=1.1)
        #
        # char.left_eye.eye_background.z_index = 1
        # char.right_eye.eye_background.z_index = 1
        xchar.left_eye.eye_background.set_z_index(3)
        xchar.left_eye.pupil.set_z_index(4)
        # char.right_eye.pupil.z_index = 4
        # char.straight_arm.z_index = -1

        # char.right_eye.pupil.scale(0.7)
        # char.left_eye.pupil.scale(0.7)

        subscribe_button.set_opacity(0)
        self.play(LaggedStart(
            LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.3),
            Succession(
                xchar.animate_create(),
                xchar.get_puff_animation()
            ),
            lag_ratio=0.1),
            Succession(*sub_anims))
        self.wait(2)


sports: list[str] = [
            'Data Retrieval\n\rSprint\n\r',
            'Dynamic\n\rDiscus\n\r',
            'Error\n\rHurdles\n\r',
            'Mixed\n\rDoubles\n\r',
            'Text\n\rTennis\n\r',
            'Most Valuable\n\rNon Function\n\r',
            'Most\n\rObscure\n\r',
            'Synchronised\n\rData Dive'
        ]


competitors: list[list[str]] = [
    ['Choose', 'Index/Match', 'VLookup', 'XLookup'],
    ['TextSplit', 'XLookup', 'ByRow', 'Sequence', 'Filter', 'SortBy', 'Unique'],
    ['IfError', 'IfNa', 'Filter', 'XLookup'],
    ['Offset/CountA', 'DateDif/EOMonth', 'If/And', 'Index/Match', 'Lambda/Let'],
    ['Left', 'Mid', 'Concatenate', 'TextJoin', 'TextSplit', 'RegExExtract'],
    ['Formatting', 'Conditional\n\rFormatting', 'Checkboxes', 'Charts', 'Pivot Tables'],
    ['FormulaText', 'Cell', 'DateDif', 'IsOmitted', 'CubeValue', 'CubeMember', 'CubeSetCount'],
    ['GroupBy', 'SortBy', 'XLookup', 'Unique', 'Filter']
]

winners: list[list[int]] = [
    [0, 1, 3],
    [-2, -1, -3],
    [1, 2, 3],
    [-3, -2, -1],
    [-3, -2, -1],
    [-2, 1, 2],
    [0, 2, 3],
    [1, 2, 0]
]

category_titles = Tex(*[sport for sport in sports])

class SportingCategories(Scene):
    def construct(self):

        local_category_titles = category_titles.copy()
        local_category_titles.arrange_in_grid(2)
        local_category_titles[:4].shift(UP*1)

        for i, title in enumerate(local_category_titles):
            title.shift(RIGHT * 0.2 * ((i % 4) - 2 if (i & 2) == 0 else (i % 4) -1))
            self.play(Write(title), run_time=0.8)
            self.wait(0.5)

class SportingCategories2(Scene):
    def construct(self):

        local_category_titles = category_titles.copy()
        local_category_titles.arrange_in_grid(3, buff=0.5)
        local_category_titles[:3].shift(UP*1)
        local_category_titles[-2:].shift(DOWN * 1 + RIGHT * 1.5)
        self.wait(0.5)

        for i, title in enumerate(local_category_titles):
            # title.shift(RIGHT * 0.2 * ((i % 4) - 2 if (i & 2) == 0 else (i % 4) -1))
            self.play(Write(title), run_time=0.8)
            self.wait(0.5)

        self.wait(5)


class Competitors(Scene):
    def construct(self):
        for i, sport in enumerate(sports):
            title = Title(sport, match_underline_width_to_text=True).scale(0.8)

            sport_competitors = competitors[i]
            competitors_mobs = VGroup(*[Tex(competitor).scale(0.8) for competitor in sport_competitors])

            competitors_mobs.arrange(DOWN)
            competitors_mobs.next_to(title, DOWN, buff=0.3)
            if len(sport_competitors) % 2 == 1:
                competitors_mobs[-1].set_x(0)

            self.wait(3)
            self.play(Write(title))
            self.wait()
            for mob in competitors_mobs:
                self.play(Write(mob))
                self.wait(0.2)

            self.wait(3)
            self.remove(*self.mobjects)
            self.wait(3)

class Sports(ThreeDScene):
    def construct(self):
        bronze_podium = Prism(dimensions=[2, 2.5, 2], fill_color=XKCD.BRONZE, fill_opacity=0.6)
        silver_podium = Prism(dimensions=[2, 3, 2], fill_color=XKCD.SILVER, fill_opacity=0.6)
        gold_podium = Prism(dimensions=[2, 3.5, 2], fill_color=XKCD.GOLD, fill_opacity=0.6)
        bronze_podium.shift(RIGHT * bronze_podium.width)
        silver_podium.shift(LEFT * bronze_podium.width)
        bronze_podium.align_to(gold_podium, DOWN)
        silver_podium.align_to(gold_podium, DOWN)

        podiums = VGroup(bronze_podium, silver_podium, gold_podium)
        start_loc = (config.frame_height + podiums.height) / 2 * DOWN
        podiums.move_to(start_loc)
        podiums.rotate(5 * PI / 6, axis=Y_AXIS)
        podiums.current_rot = 0

        def spin_to_position(mob, alpha: float):
            additional_rot = PI * alpha - mob.current_rot
            mob.current_rot += additional_rot
            mob.rotate(additional_rot, axis=-Y_AXIS)
            mob.move_to(start_loc + alpha * mob.height * 0.6 * UP)

        for i, sport in enumerate(sports):
            title = Title(sport, match_underline_width_to_text=True)

            sport_competitors = competitors[i]
            sport_winners = winners[i]
            competitors_mobs = VGroup(*[Tex(competitor).scale(0.8) for competitor in sport_competitors])
            bronze_winner = competitors_mobs[sport_winners[0]]
            silver_winner = competitors_mobs[sport_winners[1]]
            gold_winner = competitors_mobs[sport_winners[2]]

            competitors_mobs.arrange_in_grid(cols=2, buff=(0.8, MED_SMALL_BUFF))
            competitors_mobs.next_to(title, DOWN, buff=0.7)
            if len(sport_competitors) % 2 == 1:
                competitors_mobs[-1].set_x(0)

            self.wait(3)
            self.play(Write(title))
            self.wait()
            for mob in competitors_mobs:
                self.play(Write(mob))
                self.wait(0.2)

            self.wait(3)

            self.play(UpdateFromAlphaFunc(
                    podiums,
                    spin_to_position,
                    run_time=3,
                    rate_func=rate_functions.ease_out_sine)
                )

            bronze_winner_copy = bronze_winner.copy()
            silver_winner_copy = silver_winner.copy()
            gold_winner_copy = gold_winner.copy()
            winner_offset = LEFT * 0.08 + UP * 0.25
            bronze_position = podiums[0].get_top() + winner_offset
            silver_position = podiums[1].get_top() + winner_offset + DOWN * 0.05
            if i == 5:
                silver_position += DOWN * 0.25
            gold_position = podiums[2].get_top() + winner_offset

            self.wait(3)
            self.play(bronze_winner_copy.animate.move_to(bronze_position).scale(1.25), bronze_winner.animate.set_color(XKCD.SEPIA))
            self.wait()
            self.play(silver_winner_copy.animate.move_to(silver_position).scale(1.25), silver_winner.animate.set_color(XKCD.SLATEGREY))
            self.wait()
            self.play(gold_winner_copy.animate.move_to(gold_position).scale(1.25), gold_winner.animate.set_color(XKCD.GOLD))
            self.wait()

            self.wait(3)
            self.remove(*self.mobjects)
            self.wait(3)
            podiums.current_rot = 0
            podiums.rotate(PI, axis=Y_AXIS)
            podiums.move_to(start_loc)


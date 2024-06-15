from manim import *
from excel_helpers import *


class SearchArray(VGroup):
    def __init__(self, n: int, **kwargs):
        r = Rectangle(color=BLUE, fill_color=BLUE, fill_opacity=1, height=0.01, width=0.6)
        rectangles = [r.copy for _ in range(n)]
        super().__init__(*rectangles, **kwargs)


class Searches(Scene):
    def construct(self):
        num_elements = 50
        rect_height = 0.01
        rect_width = 0.6

        r = Rectangle(color=BLUE, fill_color=BLUE, fill_opacity=1, height=rect_height, width=rect_width)
        r.move_to((-4, 3, 0))
        rectangles = [r.copy()]

        for i in range(1, num_elements):
            rect = always_redraw(lambda i=i: r.copy().next_to(rectangles[i - 1], DOWN, buff=0.1))
            rectangles.append(rect)

        rectangles_group = VGroup(*rectangles)
        self.play(Create(rectangles_group), run_time=1)
        self.wait(2)

        new_height = rect_height * 2
        new_width = rect_width * 1.3
        run_time = 0.3

        def linear_search(target: int, start: int = 0):
            anims = []
            for i in range(start, target - 1, 1 if start < target else -1):
                rectangle = rectangles[i]
                anim = rectangle.animate(run_time=run_time, rate_func=there_and_back).set_color(YELLOW).set_height(
                    new_height).set_width(new_width).shift(DOWN * (new_height - rect_height) / 2)
                anims.append(anim)

            final_rect = rectangles[target - 1]
            final_check = final_rect.animate(run_time=run_time / 2.0).set_color(YELLOW).set_height(
                new_height).set_width(new_width).shift(DOWN * (new_height - rect_height) / 2)
            anims.append(final_check)
            anims.append(Wait(1.5))
            self.play(AnimationGroup(*anims, lag_ratio=0.15))
            final_rect.set_color(PURE_GREEN).set_height(new_height).set_width(new_width).shift(
                DOWN * (new_height - rect_height) / 2)
            self.wait(4)
            self.play(final_rect.animate(run_time=run_time / 2.0).set_color(BLUE).set_height(rect_height).set_width(
                rect_width).shift(
                UP * (new_height - rect_height) / 2))
            final_rect.set_color(BLUE).set_height(rect_height).set_width(rect_width).shift(
                UP * (new_height - rect_height) / 2)

        def linear_search2(target: int, start: int = 0):
            for i in range(start, target - 1, 1 if start < target else -1):
                rectangle = rectangles[i]
                self.play(rectangle.animate.set_color(YELLOW).set_height(new_height).set_width(new_width).shift(
                    DOWN * (new_height - rect_height) / 2), run_time=run_time)
                self.play(rectangle.set_color(YELLOW).set_height(new_height).set_width(new_width).shift(
                    DOWN * (new_height - rect_height) / 2).animate.set_color(RED), run_time=run_time)
                self.play(rectangle.set_color(RED).set_height(new_height).set_width(new_width).shift(
                    DOWN * (new_height - rect_height) / 2).animate.set_height(rect_height).set_width(rect_width).shift(
                    UP * (new_height - rect_height) / 2), run_time=run_time)
                rectangle.set_color(RED)

        def binary_search(target: int):
            n = math.ceil(num_elements / 2)
            # while n != target:

            # anims = []
            # for i in range(start, target - 1, 1 if start < target else -1):
            #     anim = rectangles[i].animate(run_time=run_time, rate_func=there_and_back).set_color(
            #         YELLOW).set_height(
            #         new_height).set_width(new_width).shift(DOWN * (new_height - rect_height) / 2)
            #     anims.append(anim)
            #
            # final_rect = rectangles[target - 1]
            # final_check = final_rect.animate(run_time=run_time / 2.0).set_color(YELLOW).set_height(
            #     new_height).set_width(new_width).shift(DOWN * (new_height - rect_height) / 2)
            # anims.append(final_check)
            # anims.append(Wait(1.5))
            # self.play(AnimationGroup(*anims, lag_ratio=0.15))
            # final_rect.set_color(PURE_GREEN).set_height(new_height).set_width(new_width).shift(
            #     DOWN * (new_height - rect_height) / 2)
            # self.wait(4)
            # self.play(final_rect.animate(run_time=run_time / 2.0).set_color(BLUE).set_height(rect_height).set_width(
            #     rect_width).shift(
            #     UP * (new_height - rect_height) / 2))
            # final_rect.set_color(BLUE).set_height(rect_height).set_width(rect_width).shift(
            #     UP * (new_height - rect_height) / 2)

        target = 32  # Change this to your desired target index
        linear_search2(target)
        # binary_search(target)
        self.wait(2)


class SearchesGPT(Scene):
    def construct(self):
        num_elements = 50
        rect_height = 0.01
        rect_width = 0.6

        r = Rectangle(color=BLUE, fill_color=BLUE, fill_opacity=1, height=rect_height, width=rect_width)
        r.move_to((-4, 3, 0))
        rectangles = [r.copy()]

        for i in range(1, num_elements):
            rect = r.copy().next_to(rectangles[i - 1], DOWN, buff=0.1)
            rectangles.append(rect)

        rectangles_group = VGroup(*rectangles)
        self.play(Create(rectangles_group), run_time=1)
        self.wait(2)

        new_height = rect_height * 2
        new_width = rect_width * 1.3
        run_time = 0.3

        def linear_search2(target: int, start: int = 0):
            for i in range(start, target - 1, 1 if start < target else -1):
                rectangle = rectangles[i]
                # Animate to yellow and grow
                self.play(rectangle.animate.set_color(YELLOW).set_height(new_height).set_width(new_width).shift(
                    DOWN * (new_height - rect_height) / 2), run_time=run_time)

                # Change to red while keeping the size
                self.play(rectangle.animate.set_color(RED), run_time=run_time)

                # Shrink back to original size while keeping red
                self.play(rectangle.animate.set_height(rect_height).set_width(rect_width).shift(
                    UP * (new_height - rect_height) / 2), run_time=run_time)
                rectangle.set_color(RED)  # Ensure it stays red after shrinking

                # Update positions of all rectangles below the current one
                for j in range(i + 1, num_elements):
                    new_position = rectangles[j - 1].get_bottom() + np.array([0, -rect_height - 0.1, 0])
                    rectangles[j].move_to(new_position)

        target = 32  # Change this to your desired target index
        linear_search2(target)
        self.wait(2)
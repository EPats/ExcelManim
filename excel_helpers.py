
from math import ceil
from manim import * 
import numpy as np
import random
from manim.typing import Vector3D


def change_path_to_top_left_clockwise(polygon: Polygon) -> Polygon:
    path = polygon.get_points()
    top_left = polygon.get_corner(UL)
    i = [i for i, point in enumerate(path) if (point == top_left).all()][0]

    if i:
        i += 1
        new_path = np.concatenate((path[i:], path[:i]), axis=0)
        polygon.set_points(new_path)

    return polygon


class Test(Scene):
    def construct(self):
        tex = Tex('Dissolving Text').scale(4).shift(UP)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex, right_to_left=True))
        self.wait(2)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex))
        config.disable_caching = False


class Test2(Scene):
    def construct(self):
        tex = Tex('\\verb|[|not\\verb|_|found\\verb|]|', color=BLUE).scale(2).shift(UP)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex))
        self.wait(2)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex, right_to_left=False))
        config.disable_caching = False


class Test3(Scene):
    def construct(self):
        tex = Tex('This is', ' a test', color=GREEN, fill_color=BLUE).scale(2)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex))
        self.wait(2)
        self.play(FadeIn(tex))
        self.wait(1)
        self.play(dissolve_tex(self, tex, right_to_left=False))
        config.disable_caching = False


def dissolve_tex(scene: Scene, tex: Tex, pixel_size: float = -1, pixel_lag: float = 0.0001, fade_lag: float = 0.05,
                 right_to_left: bool = True):
    config.disable_caching = True
    tex_string: str = tex.tex_string
    if pixel_size <= 0:
        quality = config['quality']
        if quality == 'low_quality':
            pixel_size = 0.5
        elif quality == 'medium_quality':
            pixel_size = 0.1
        else:
            pixel_size = 0.01
    
    chars = []
    i = 0
    char: str
    while i < len(tex_string):
        char = tex_string[i]
        if char != '\\':
            chars.append(char)
            i += 1
            continue
        j = tex_string.find('|', i + 1 + 5)
        char = tex_string[i:j + 1]
        chars.append(char)
        i = j + 1

    tex_chars = Tex(*[char for char in chars]).match_width(tex).match_height(tex).match_style(tex).align_to(tex, UP+LEFT)
    scene.remove(tex)
    scene.add(tex_chars)

    step = -1 if right_to_left else 1
    animations = []

    char_tex: Tex
    for i, char_tex in enumerate(tex_chars[::step], start=1):
        print(f'Processing character {i}/{len(tex_chars)}')
        if not char_tex.tex_string.strip():
            continue

        vectorized_char = VMobject().set_points_as_corners([*char_tex.get_all_points()])
        vectorized_char.set_fill(color=tex.color, opacity=1)
        vectorized_char.set_stroke(width=0)

        char_centre = vectorized_char.get_center()
        pixel_grid = VGroup()

        char_width = vectorized_char.width
        width_step = pixel_size
        if right_to_left:
            char_width *= -1
            width_step *= -1

        char_height = vectorized_char.height

        x_pos = np.arange(-char_width / 2, char_width / 2, width_step)
        y_pos = np.arange(-char_height / 2, char_height / 2, pixel_size)
        # Create pixels within the bounding box
        for k, x in enumerate(x_pos):
            for j, y in enumerate(y_pos, start=1):
                pixel_n = k * len(y_pos) + j
                total_pixels = len(y_pos) * len(x_pos)
                if pixel_n % ceil(total_pixels / 5) == 0:
                    print(f'Processing pixel {pixel_n}/{total_pixels}'\
                          f' for character {i}/{len(tex_chars)} ({char_tex.tex_string})')
                pixel = Square(side_length=pixel_size, stroke_width=0, stroke_color=tex_chars.color,
                               fill_color=tex_chars.color, fill_opacity=1)
                pixel.move_to(char_centre + np.array([x, y, 0]))
                pixel = Intersection(vectorized_char, pixel).set_stroke(width=0).set_fill(color=tex_chars.color, opacity=1)
                pixel_grid.add(pixel)

        pixel_movements = []
        for pixel in pixel_grid:
            left_or_right = RIGHT if right_to_left else LEFT
            direction = UP * random.uniform(-0.05, 1) + left_or_right * random.uniform(-0.05, 1)
            pixel_movements.append(pixel.animate.shift(direction).set_opacity(0))
        animations.append(AnimationGroup(FadeOut(char_tex).set_run_time(0.5),
                                         LaggedStart(*pixel_movements, lag_ratio=pixel_lag)
                                         )
                          )

    return LaggedStart(*animations, lag_ratio=fade_lag)



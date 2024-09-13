import math
from typing import Callable

from manim import *
from manim.mobject.opengl.opengl_surface import OpenGLSurface
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
from manim.typing import Vector3D
from manim.utils.rate_functions import unit_interval

import excel_constants


@unit_interval
def slow_tip_then_bounce(t: float) -> float:
    if t <= 0.5:
        return rate_functions.ease_in_sine(t * 2) * 0.5
    else:
        return rate_functions.ease_out_bounce((t - 0.5) * 2) * 0.5 + 0.5


@unit_interval
def custom_ease(t: float) -> float:
    if t < 0.5:
        # Ease-in quad for the first half
        u: float = t / 0.5
        return u * u
    else:
        # Overshoot and bounce for the second half
        t = (t - 0.5) * 2  # Normalize t to 0-1 range for the second half
        bounce: float = math.exp(-t * 6) * math.cos(t * 20)
        overshoot_amount: float = 0.2
        return 1 + bounce * overshoot_amount


@unit_interval
def less_bouncy_ease_out_elastic(t: float) -> float:
    # c4 is a constant used to control the period of the sine wave
    # It's approximately 2.0943951023931953, which is 2π/3
    # This value gives a nice aesthetic "bounce" to the elastic effect
    c4 = (2 * np.pi) / 3

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        # Slower initial move
        t = t * t  # Apply some easing to slow down the initial movement
        oscillations = 4.5  # Number of "springs"
        amplitude = 0.8  # Higher = more elastic, lower = less elastic
        frequency = 4  # Decay of springs - higher is faster decay

        return 1 + amplitude * pow(2, -frequency * t) * np.sin((t * oscillations - 0.75) * c4)


@unit_interval
def custom_ease_out_elastic(t: float,
                            c4: float = (2 * np.pi) / 3,
                            oscillations: float = 4.5,
                            amplitude: float = 0.8,
                            frequency: float = 4) -> float:
    # c4 is a constant used to control the period of the sine wave
    # It's approximately 2.0943951023931953, which is 2π/3
    # This value gives a nice aesthetic "bounce" to the elastic effect
    # Oscilations - Number of "springs"
    # Amplitude - Higher = more elastic, lower = less elastic
    # Frequency - Decay of springs - higher is faster decay

    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        t = t * t  # Apply some easing to slow down the initial movement


        return 1 + amplitude * pow(2, -frequency * t) * np.sin((t * oscillations - 0.75) * c4)


@unit_interval
def there_and_back_sin(t: float) -> float:
    return -(np.cos(np.pi * t * 2) - 1) / 2


class ColorChangeAndRotate(Animation):
    def __init__(
            self,
            mobject: Mobject,
            color: ManimColor | str = excel_constants.EP_GREEN,
            angle: float = PI / 2,
            about_point: Vector3D | None = None,
            **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.color: ManimColor | str = color
        self.color_alpha: float = 0
        self.angle: float = angle
        self.prev_angle: float = 0
        self.about_point: Vector3D = mobject.get_corner(DL) if about_point is None else about_point

    def interpolate_mobject(self, alpha):
        true_alpha: float = self.rate_func(alpha)
        self.color_alpha = max(0.0, min(1.0, true_alpha))
        original_color = self.starting_mobject.get_color()
        current_color = interpolate_color(original_color, self.color, self.color_alpha)
        self.mobject.set_color(current_color)

        # Interpolate rotation
        current_angle = interpolate(0, self.angle, true_alpha)
        self.mobject.rotate(-self.prev_angle, about_point=self.about_point)
        self.mobject.rotate(current_angle, about_point=self.about_point)
        self.prev_angle = current_angle


class ColorChangeRotateAndScale(ColorChangeAndRotate):
    def __init__(
            self,
            mobject: Mobject,
            scale: float,
            color: ManimColor | str = excel_constants.EP_GREEN,
            angle: float = PI / 2,
            about_point: Vector3D | None = None,
            **kwargs
    ):
        super().__init__(mobject, color=color, angle=angle, about_point=about_point, **kwargs)
        self.scale: float = scale

    def interpolate_mobject(self, alpha):
        pass


class ZoomThrough(Transform):
    def __init__(
            self,
            mobject: Mobject,
            indexes: list[int] | None = None,
            scale: float = 150,
            **kwargs
    ):

        end_mob: Mobject = mobject.copy().scale(scale)
        zoom_mob: Mobject
        if indexes is None:
            zoom_mob = end_mob
        else:
            zoom_mob = self.get_zoom_mob(indexes, end_mob)
        end_mob.shift(-(zoom_mob.get_center()))
        super().__init__(mobject, end_mob, **kwargs)

    def get_zoom_mob(self, indexes: list[int], end_mob: Mobject) -> Mobject:
        mob: Mobject = end_mob
        for i in indexes:
            mob = mob[i]
        return mob


class ShrinkIn(Animation):
    def __init__(
            self,
            mobject: Mobject,
            start_scale: float = 1.2,
            rate_func: Callable[[float], float] = less_bouncy_ease_out_elastic,
            opacity: float | tuple[float, float] = (0, 1),
            **kwargs
    ):

        super().__init__(mobject, rate_func=rate_func, **kwargs)
        self.start_scale: float = start_scale
        self.mobject.save_state()
        if isinstance(opacity, float):
            self.start_opacity: float = opacity
            self.end_opacity: float = opacity
        else:
            self.start_opacity: float = opacity[0]
            self.end_opacity: float = opacity[1]

    def interpolate_mobject(self, alpha):
        true_alpha: float = self.rate_func(alpha)
        scale: float = interpolate(self.start_scale, 1, true_alpha)
        opacity: float = interpolate(self.start_opacity, self.end_opacity, alpha)
        self.mobject.restore()
        self.mobject.scale(scale)
        self.mobject.set_opacity(opacity)


class FadeInWithMovementAndScale(FadeIn):

    def __init__(
            self,
            offset: Vector3D,
            scale: float = 1.0,
            *mobjects: Mobject,
            **kwargs
    ):
        super().__init__(*mobjects, **kwargs)
        self.offset = offset
        self.end_pos = self.mobject.get_center()
        self.start_scale = scale

    def interpolate_mobject(self, alpha):
        super().interpolate_mobject(alpha)
        true_alpha: float = self.rate_func(alpha)
        current_pos = self.end_pos + self.offset * (1 - true_alpha)
        scale = interpolate(self.start_scale, 1, true_alpha)
        self.mobject.scale(scale)
        self.mobject.move_to(current_pos)


class CreateWithMovement(Create):
    def __init__(
            self,
            mobject: VMobject | OpenGLVMobject | OpenGLSurface,
            offset: Vector3D,
            **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.offset = offset
        self.end_pos = mobject.get_center()

    def interpolate_mobject(self, alpha):
        super().interpolate_mobject(alpha)
        true_alpha: float = self.rate_func(alpha)
        current_pos = self.end_pos + self.offset * (1 - true_alpha)
        self.mobject.move_to(current_pos)


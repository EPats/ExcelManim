from manim import *
from manim.typing import Vector3D
import random

import tex_objs


class Test(Scene):
    def construct(self):
        bubble_1 = DefaultThoughtBubble('This is\n\ra test\n\rstring awawawaw!')
        self.play(bubble_1.animate_draw_bubble())
        self.wait(2)

        # circ = Circle()
        # a = [-0.5, 0, 0]
        # b = [2, 1, 0]
        # c = [0, 2, 0]
        # t = ArcPolygon(a, b, c, arc_config=[
        #     {'radius': -3},
        #     {'radius': 2},
        #     {'radius': -5}
        # ]).move_to(circ.get_corner(DR))
        # # t = Triangle().move_to(c.get_corner(DR))
        # u = Union(circ, t)
        # u.to_corner(UL)
        # self.play(DrawBorderThenFill(u))
        # self.wait(2)


class SpeechSpikeOrientation:
    def __init__(
            self,
            direction: Vector3D = DR,
            flip: bool = True,
            rotation: float = 0,
            shift: Vector3D = ORIGIN
    ):
        self.direction: Vector3D = direction
        self.flip: bool = flip
        self.rotation: float = rotation
        self.shift: Vector3D = shift


class TextBubble(VGroup):
    def __init__(
            self,
            bubble_background: VMobject,
            text_mob: Tex,
            **kwargs
    ):
        self.bubble_background: VMobject = bubble_background
        self.text_mob: Tex = text_mob
        super().__init__(self.bubble_background, self.text_mob, **kwargs)

    def animate_draw_bubble(self, lag_ratio: float = 0.2, **kwargs):
        return LaggedStart(
            DrawBorderThenFill(self.bubble_background),
            Write(self.text),
            lag_ratio=lag_ratio,
            **kwargs
        )


class SpeechBubble(TextBubble):
    def __init__(
            self,
            bubble_shape: VMobject,
            speech_text: str,
            speech_spike_orientations: SpeechSpikeOrientation | list[SpeechSpikeOrientation],
            text_template: TexTemplate = tex_objs.GENTLE_SANS_SERIF,
            buff: float = 0.3,
            **kwargs
    ):
        self.speech_bubble_base: VMobject = bubble_shape

        self.text_str: str = speech_text
        self.text: Tex = Tex(speech_text, tex_template=text_template).move_to(self.speech_bubble_base)
        self.speech_bubble_base.stretch((1 + buff * 2) * self.text.width / self.speech_bubble_base.width, dim=0)
        self.speech_bubble_base.stretch((1 + buff * 2) * self.text.height / self.speech_bubble_base.height, dim=1)

        self.speech_spikes: list[VMobject] = self._create_speech_spikes(speech_spike_orientations)
        self.bubble_background: VMobject = self.speech_bubble_base
        for speech_spike in self.speech_spikes:
            self.bubble_background = Union(self.bubble_background, speech_spike)

        super().__init__(self.bubble_background, self.text, **kwargs)

    def _create_speech_spikes(
            self,
            speech_spike_orientations: SpeechSpikeOrientation | list[SpeechSpikeOrientation]
    ) -> list[VMobject]:
        return_list: list[VMobject] = []
        a = [-0.5, 0, 0]
        b = [2, 1, 0]
        c = [0, 2, 0]

        spike = ArcPolygon(a, b, c, arc_config=[
            {'radius': -3},
            {'radius': 2},
            {'radius': -5}
        ]).scale(0.4)

        a = [0.5, 0, 0]
        b = [-2, 1, 0]
        c = [0, 2, 0]

        flipped_spike = ArcPolygon(c, b, a, arc_config=[
            {'radius': 3},
            {'radius': 5},
            {'radius': -2}
        ]).scale(0.4)

        # spike = Triangle().stretch(1.2, dim=1)
        if not isinstance(speech_spike_orientations, list):
            speech_spike_orientations = [speech_spike_orientations]

        orientation: SpeechSpikeOrientation
        for orientation in speech_spike_orientations:
            new_spike = flipped_spike.copy() if orientation.flip else spike.copy()
            if orientation.direction[0] != 0 and orientation.direction[1] != 0:
                new_spike.move_to(self.speech_bubble_base.get_corner(orientation.direction))
            else:
                new_spike.move_to(self.speech_bubble_base.get_edge_center(orientation.direction))
            new_spike.shift((0 / 5) * np.array(
                (
                    orientation.direction[0] * new_spike.width,
                    orientation.direction[1] * new_spike.height,
                    0
                )
            ))
            new_spike.rotate(orientation.rotation)
            new_spike.shift(orientation.shift)
            return_list.append(new_spike)

        return return_list


class SpeechBubbleEllipse(SpeechBubble):
    def __init__(self,
                 speech_text: str,
                 speech_spike_orientations: SpeechSpikeOrientation | list[SpeechSpikeOrientation] | None = None,
                 text_template: TexTemplate = tex_objs.GENTLE_SANS_SERIF,
                 **kwargs
                 ):
        if speech_spike_orientations is None:
            # speech_spike_orientations = SpeechSpikeOrientation(flip=False, direction=DL, shift=UP * 0.2 + RIGHT * 0.55)
            speech_spike_orientations = SpeechSpikeOrientation(shift=UP * 0.2 + LEFT * 0.55)

        bubble_shape = Circle()
        super().__init__(bubble_shape, speech_text, speech_spike_orientations, text_template, **kwargs)


class SpeechBubbleRoundedRectangle(SpeechBubble):
    def __init__(self,
                 speech_text: str,
                 speech_spike_orientations: SpeechSpikeOrientation | list[SpeechSpikeOrientation] | None = None,
                 text_template: TexTemplate = tex_objs.GENTLE_SANS_SERIF,
                 **kwargs
                 ):
        if speech_spike_orientations is None:
            # speech_spike_orientations = SpeechSpikeOrientation(flip=False, direction=DL, shift=RIGHT * 0.4)
            speech_spike_orientations = SpeechSpikeOrientation(shift=LEFT * 0.4)

        bubble_shape = RoundedRectangle()
        super().__init__(bubble_shape, speech_text, speech_spike_orientations, text_template, **kwargs)


class ThoughtBubbleOrientation:
    def __init__(
            self,
            size_bounds: tuple[int, int],
            direction: Vector3D = DR,
            shift: Vector3D = ORIGIN,
            scale: float = 0.5
    ):
        self.size_bounds: tuple[int, int] = size_bounds
        self.direction: Vector3D = direction
        self.shift: Vector3D = shift
        self.scale: float = scale


def random_point_on_ellipse(ellipse):
    # Get the width and height of the ellipse
    width = ellipse.width
    height = ellipse.height

    # Generate a random angle
    theta = np.random.uniform(0, 2 * PI)

    # Calculate the point on the ellipse
    x = (width / 2) * np.cos(theta)
    y = (height / 2) * np.sin(theta)

    # The point is relative to the ellipse's center, so add the ellipse's center coordinates
    point = ellipse.get_center() + np.array([x, y, 0])

    return point, theta


def new_point_clockwise(ellipse, start_point, start_theta, distance):
    # Get the width and height of the ellipse
    width = ellipse.width
    height = ellipse.height

    # Calculate the approximate arc length of the ellipse
    a = width / 2
    b = height / 2
    circumference = PI * (3*(a+b) - np.sqrt((3*a + b) * (a + 3*b)))

    # Calculate the angle to move based on the distance
    angle_to_move = (distance / circumference) * 2 * PI

    # Calculate the new angle
    new_theta = (start_theta + angle_to_move) % (2 * PI)

    # Calculate the new point on the ellipse
    x = (width / 2) * np.cos(new_theta)
    y = (height / 2) * np.sin(new_theta)

    # The point is relative to the ellipse's center, so add the ellipse's center coordinates
    new_point = ellipse.get_center() + np.array([x, y, 0])

    return new_point, new_theta


def _create_thought_bubble(size_bounds: tuple[int, int]) -> VMobject:
    debug = VGroup()
    bubble = Ellipse(width=2, height=1.5, color=GREEN)
    union_mob = bubble.copy()
    inner_ellipse = bubble.copy().scale(1.2).set_color(BLUE)
    debug.add(bubble, inner_ellipse)
    pt, theta = random_point_on_ellipse(inner_ellipse)
    total_distance = 0.0
    buffer = PI / 5
    while total_distance - buffer < 2 * PI:
        r = random.randint(*size_bounds) / 100
        c = Circle(radius=r)
        pt: Vector3D
        distance = r * 1.1
        if total_distance > 0:
            pt, theta = new_point_clockwise(inner_ellipse, pt, theta, distance)
        total_distance += distance
        c.move_to(pt)
        union_mob = Union(union_mob, c)
        debug.add(c)
    return union_mob
    # return debug


class ThoughtBubble(TextBubble):
    def __init__(self,
                 speech_text: str,
                 thought_bubble_orientations: ThoughtBubbleOrientation | list[ThoughtBubbleOrientation] | None = None,
                 text_template: TexTemplate = tex_objs.GENTLE_SANS_SERIF,
                 buff: float = 0.3,
                 **kwargs
                 ):

        if thought_bubble_orientations is None:
            self.thought_bubble_orientations = []
        else:
            self.thought_bubble_orientations: (ThoughtBubbleOrientation
                                               | list[ThoughtBubbleOrientation]) = thought_bubble_orientations
        self.buff: float = buff
        self.text_str: str = speech_text

        self.text: Tex = Tex(speech_text, tex_template=text_template)
        self.bubbles: VMobject = self._create_thought_bubbles()
        self.text.move_to(self.bubbles[0])

        super().__init__(self.bubbles, self.text, **kwargs)

    def animate_draw_bubble(self, lag_ratio: float = 0.2, **kwargs):
        return LaggedStart(
            *[DrawBorderThenFill(mob) for mob in self.bubbles[::-1]],
            Write(self.text),
            lag_ratio=lag_ratio,
            **kwargs
        )

    def _create_thought_bubbles(self) -> VGroup:
        bubbles = VGroup()

        first_bubble = _create_thought_bubble(size_bounds=(20, 50))
        first_bubble.stretch((1 + self.buff * 2) * self.text.width / first_bubble.width, dim=0)
        first_bubble.stretch((1 + self.buff * 2) * self.text.height / first_bubble.height, dim=1)
        bubbles.add(first_bubble)

        for i, thought_bubble_details in enumerate(self.thought_bubble_orientations):
            new_bubble = _create_thought_bubble(thought_bubble_details.size_bounds)
            new_bubble.scale(thought_bubble_details.scale)

            next_to_mob = bubbles[i]
            new_bubble.next_to(next_to_mob, thought_bubble_details.direction, buff=0)
            new_bubble.shift(thought_bubble_details.shift)

            bubbles.add(new_bubble)
        return bubbles


class DefaultThoughtBubble(ThoughtBubble):
    def __init__(self,
                 speech_text: str,
                 text_template: TexTemplate = tex_objs.GENTLE_SANS_SERIF,
                 buff: float = 0.3,
                 **kwargs
                 ):
        thought_bubble_orientations = [
            ThoughtBubbleOrientation((30, 60), shift=LEFT * 1.5 + UP * 0.3),
            ThoughtBubbleOrientation((50, 80), scale=0.3, shift=UP * 0.5),
            ThoughtBubbleOrientation((70, 120), scale=0.1)
        ]
        super().__init__(speech_text, thought_bubble_orientations, text_template, buff, **kwargs)


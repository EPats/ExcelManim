from functools import partial

from manim import *
import re

from manim.typing import Vector3D

import custom_animations

GENTLE_SANS_SERIF: TexTemplate = TexFontTemplates.comfortaa
HANDWRITTEN: TexTemplate = TexFontTemplates.ecf_jd
ROBOTO: TexTemplate = TexFontTemplates.electrum_adf
ITALIC: TexTemplate = TexFontTemplates.urw_zapf_chancery

class BlockTex(Tex):
    def __init__(self, main_text: str, pre_text: str = '', post_text: str = '',
                 tex_template: TexTemplate = GENTLE_SANS_SERIF, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, **kwargs):
        self.current_scale: int = 1
        text_strs: list[str] = [text for text in main_text.split('\n') if text]
        pre_vertical_strs: list[str] = [text for text in pre_text.split('\n') if text]
        post_vertical_strs: list[str] = [text for text in post_text.split('\n') if text]

        all_strs: list[str] = pre_vertical_strs + text_strs + post_vertical_strs
        super().__init__(*[text for text in all_strs], tex_template=tex_template, **kwargs)

        main_block_start = len(pre_vertical_strs)
        main_block_end = main_block_start + len(text_strs)
        max_width: float = max([mob.width for mob in self[main_block_start:main_block_end]])

        self[main_block_start].scale_to_fit_width(max_width)
        sub_mob: Mobject
        for i, sub_mob in enumerate(self[main_block_start + 1: main_block_end], start=main_block_start + 1):
            sub_mob.scale_to_fit_width(max_width)
            sub_mob.next_to(self[i - 1], DOWN, buff=buff)
            sub_mob.align_to(self[i - 1], LEFT)

        self.main_mob = self[main_block_start:main_block_end]
        if main_block_start > 0:
            self.start_mob = self[:main_block_start]
        else:
            self.start_mob = None
        if main_block_end < len(self) - 1:
            self.end_mob = self[main_block_end:]
        else:
            self.end_mob = None

        height: float = self.main_mob.height

        for i, sub_mob in enumerate(self[:main_block_start][::-1]):
            sub_mob.scale_to_fit_width(height)
            sub_mob.rotate(PI / 2)
            sub_mob.next_to(self.main_mob if i == 0 else self[main_block_start - i], LEFT, buff=buff)

        for i, sub_mob in enumerate(self[main_block_end:][::-1]):
            sub_mob.scale_to_fit_width(height)
            sub_mob.rotate(-PI / 2)
            sub_mob.next_to(self.main_mob if i == 0 else self[-i], RIGHT, buff=buff)

    def get_add_word_by_word_anim(self, gap_between: int = 1, lag_ratio: float = 0.25,
                                  custom_gaps: dict[int, int | float] | None = None) -> Animation:
        custom_gaps = custom_gaps or {}
        current_word: int = 1
        anims: list[Animation] = []
        for mob in self:
            text: str = mob.tex_string
            if '{' in text:
                text = re.sub('\\\\.*?{', '', text)
                text = text.replace('}', '')

            curr_pos: int = 0
            words: list[str] = text.split(' ')
            for i, word in enumerate(words):
                anims.append(custom_animations.ShrinkIn(mob[curr_pos:curr_pos + len(word)], run_time=0.7))
                gap = custom_gaps[current_word] if current_word in custom_gaps else gap_between
                gaps = [Wait() for _ in range(gap)]
                if gaps and i < len(words) - 1:
                    anims.extend(gaps)
                curr_pos += len(word)
                current_word += 1
        return LaggedStart(*anims, lag_ratio=lag_ratio)

import json

from manim import *

import custom_animations
import tex_objs


class Parallax(ThreeDScene):
    def construct(self):
        c = Circle(radius=1, fill_color=RED, fill_opacity=0.7)
        s = Square(side_length=1, fill_color=WHITE, fill_opacity=0.7)
        t = Triangle(fill_color=BLUE, fill_opacity=0.7)

        shapes = [c, s, t]
        for i, shape in enumerate(shapes):
            shape.shift(i * OUT * 3)
            self.play(Create(shape))

        self.play(*[shape.animate.shift(LEFT * 2) for shape in shapes], run_time=5)
        self.play(*[shape.animate.shift(RIGHT * 2) for shape in shapes], run_time=5)
        self.move_camera(frame_center=np.array([2, 0, 0]), run_time=7, rate_func=rate_functions.ease_in_out_sine)
        self.wait()
        self.move_camera(frame_center=ORIGIN)
        self.wait()


class Test(Scene):
    def construct(self):
        text: str = '\\textbf{time}\n\\textbf{of year}\n\\textbf{to say}'
        v_text: str = 'Hello,\nWorld'
        v_text_l: str = 'This is my\nfavourite'
        tex: tex_objs.BlockTex = tex_objs.BlockTex(text, post_text=v_text, pre_text=v_text_l)
        self.play(tex.get_add_word_by_word_anim(custom_gaps={4: 1, 10: 5}), run_time=2)
        self.wait(2)
        self.play(tex.get_zoom_through_anim(-1, 1), run_time=3)

        test_tex: Tex = tex_objs.BlockTex('This is\na test')
        self.play(Write(test_tex))
        self.wait(2)
        self.play(custom_animations.ColorChangeAndRotate(test_tex),
                  run_time=1.5,
                  rate_func=custom_animations.custom_ease)
        self.wait(2)

class Fonts(Scene):
    def construct(self):
        text: str = 'Hello, world.'
        pairs: list[tuple[TexTemplate, str]] = [
            (TexFontTemplates.antykwa, 'Antykwa Półtawskiego (TX Fonts for Greek and math symbols)'), # Greek style
            (TexFontTemplates.american_typewriter, 'American Typewriter'), # Missing
            (TexFontTemplates.apple_chancery, 'Apple Chancery'), # Missing
            (TexFontTemplates.auriocus_kalligraphicus, 'Auriocus Kalligraphicus (Symbol Greek)'), #V ery curly
            (TexFontTemplates.baskervald_adf_fourier, 'Baskervald ADF with Fourier'), # Smooth serif
            (TexFontTemplates.baskerville_it, 'Baskerville (Italic)'), # Missing
            (TexFontTemplates.biolinum, 'Biolinum'), #SANS SERIF VERSION
            (TexFontTemplates.brushscriptx, 'BrushScriptX-Italic (PX math and Greek)'), # Missing
            (TexFontTemplates.chalkboard_se, 'Chalkboard SE'), # Missing
            (TexFontTemplates.chalkduster, 'Chalkduster'), # Missing
            (TexFontTemplates.comfortaa, 'Comfortaa'), # Gentle sans serif
            (TexFontTemplates.comic_sans, 'Comic Sans MS'), # Ew
            (TexFontTemplates.droid_sans, 'Droid Sans'), # Fine
            (TexFontTemplates.droid_sans_it, 'Droid Sans (Italic)'), # Fine
            (TexFontTemplates.droid_serif, 'Droid Serif'), # Fine
            (TexFontTemplates.droid_serif_px_it, 'Droid Serif (PX math symbols) (Italic)'), # Fine
            (TexFontTemplates.ecf_augie, 'ECF Augie (Euler Greek)'), # Handwriting Gentle
            (TexFontTemplates.ecf_jd, 'ECF JD (with TX fonts)'), # Handwriting soft but rough
            (TexFontTemplates.ecf_skeetch, 'ECF Skeetch (CM Greek)'), # Handwriting too sketchy
            (TexFontTemplates.ecf_tall_paul, 'ECF Tall Paul (with Symbol font)'), #Small
            (TexFontTemplates.ecf_webster, 'ECF Webster (with TX fonts)'), # Not handwriting
            (TexFontTemplates.electrum_adf, 'Electrum ADF (CM Greek)'), # Roboto
            (TexFontTemplates.epigrafica, ' Epigrafica '), # Gentle
            (TexFontTemplates.fourier_utopia, 'Fourier Utopia (Fourier upright Greek)'), # Blah
            (TexFontTemplates.french_cursive, 'French Cursive (Euler Greek)'), # Cursive
            (TexFontTemplates.gfs_bodoni, 'GFS Bodoni'), # Missing
            (TexFontTemplates.gfs_didot, 'GFS Didot (Italic)'), # Meh
            (TexFontTemplates.gfs_neoHellenic, 'GFS NeoHellenic'), # Meh
            (TexFontTemplates.gnu_freesans_tx, 'GNU FreeSerif (and TX fonts symbols)'), # Meh
            (TexFontTemplates.gnu_freeserif_freesans, 'GNU FreeSerif and FreeSans'), # Meh
            (TexFontTemplates.helvetica_fourier_it, 'Helvetica with Fourier (Italic)'), # Meh
            (TexFontTemplates.latin_modern_tw_it, 'Latin Modern Typewriter Proportional (CM Greek) (Italic)'), # Serif nice
            (TexFontTemplates.latin_modern_tw, 'Latin Modern Typewriter Proportional'), #Serif nice
            (TexFontTemplates.libertine, 'Libertine'), # Condensed
            (TexFontTemplates.libris_adf_fourier, 'Libris ADF with Fourier'), # Interesting
            (TexFontTemplates.minion_pro_myriad_pro, 'Minion Pro and Myriad Pro (and TX fonts symbols)'), # Missing
            (TexFontTemplates.minion_pro_tx, 'Minion Pro (and TX fonts symbols)'), # Missing
            (TexFontTemplates.new_century_schoolbook, 'New Century Schoolbook (Symbol Greek)'), # No
            (TexFontTemplates.new_century_schoolbook_px, 'New Century Schoolbook (Symbol Greek, PX math symbols)'), # No
            (TexFontTemplates.noteworthy_light, 'Noteworthy Light'), # Missing
            (TexFontTemplates.palatino, 'Palatino (Symbol Greek)'), # No
            (TexFontTemplates.papyrus, 'Papyrus'), # Hah
            (TexFontTemplates.romande_adf_fourier_it, 'Romande ADF with Fourier (Italic)'), # No
            (TexFontTemplates.slitex, 'SliTeX (Euler Greek)'), # Missing
            (TexFontTemplates.times_fourier_it, 'Times with Fourier (Italic)'), # Typical
            (TexFontTemplates.urw_avant_garde, 'URW Avant Garde (Symbol Greek)'), # Smooth nice
            (TexFontTemplates.urw_zapf_chancery, 'URW Zapf Chancery (CM Greek)'), # OOH ITALIC
            (TexFontTemplates.venturis_adf_fourier_it, 'Venturis ADF with Fourier (Italic)'), # No
            (TexFontTemplates.verdana_it, 'Verdana (Italic)'), # Hm
            (TexFontTemplates.vollkorn_fourier_it, 'Vollkorn with Fourier (Italic)'), # Missing
            (TexFontTemplates.vollkorn, 'Vollkorn (TX fonts for Greek and math symbols)'), # Missing
            (TexFontTemplates.zapf_chancery, 'Zapf Chancery') # Nice
        ]

        font: TexTemplate
        name: str
        font, name = pairs.pop(0)

        tex_mob: Tex = Tex(text, tex_template=font)
        name_mob: Tex = Tex(name, tex_template=font)
        name_mob.next_to(tex_mob, UP, buff=1)

        self.play(Write(name_mob))
        self.play(Write(tex_mob))
        self.wait(2)

        failed_fonts: list[str] = []
        for font, name in pairs:
            try:
                new_tex_mob: Tex = Tex(text, tex_template=font)
                new_name_mob: Tex = Tex(name, tex_template=font)
                new_name_mob.next_to(new_tex_mob, UP, buff=1)

                self.play(LaggedStart(
                    Transform(name_mob, new_name_mob),
                    Transform(tex_mob, new_tex_mob),
                    lag_ratio=0.4)
                )
                self.wait(2)
            except Exception:
                failed_fonts.append(name)


        if failed_fonts:
            print(f'Failed for {len(failed_fonts)} fonts:')
            print(json.dumps(failed_fonts, indent=4))


import manim
import XLookup_E01
import scenes
import MEWC_Explained
import XLookup_E02


if __name__ == '__main__':
    with manim.tempconfig({'quality': 'low_quality', 'disable_caching': False, 'preview': True}):
        scene = XLookup_E02.MatchMode()
        scene.render()
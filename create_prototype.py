import manim
import XLookup_E01
import scenes
import MEWC_Explained

if __name__ == '__main__':
    with manim.tempconfig({'quality': 'low_quality', 'disable_caching': True, 'preview': True}):
        scene = MEWC_Explained.Brackets()
        scene.render()
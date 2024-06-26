import subprocess
import inspect
import manim
import XLookup_E01
import XLookup_E03
import scenes
import MEWC_Explained
import XLookup_E02


def prototype(proto_scene, quality: str = 'low') -> None:
    with manim.tempconfig({'quality': f'{quality}_quality', 'disable_caching': True}):
        proto_scene().render()


def create_multiple_scenes(scene_classes: list) -> None:
    for new_scene in scene_classes:
        new_scene().render()


def create_all_scenes_in_module(module: object) -> None:
    scene_classes = [cls for name, cls in inspect.getmembers(module, inspect.isclass)
                     if issubclass(cls, manim.Scene) and cls.__module__ == module.__name__]
    create_multiple_scenes(scene_classes)


if __name__ == '__main__':
    current_scene = XLookup_E03.WildCardSearch

    prototype(current_scene)
    # create_multiple_scenes([current_scene])
    # create_multiple_scenes([XLookup_E02.SearchModesExample, XLookup_E02.NotFoundExample2])
    # create_all_scenes_in_module(XLookup_E02)


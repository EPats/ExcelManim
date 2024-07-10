import inspect
import manim
import os
import subprocess

import XLookup_E01
import XLookup_E03
import excel_character
import scenes
import MEWC_Explained
import XLookup_E02


PYTHON_VENV = './venv/Scripts/python.exe'


def create_scene(module_name: str, scene_name: str, quality: str = 'low', preview: bool = True) -> None:
    quality_argument: str
    match quality:
        case 'low':
            quality_argument = 'ql'
        case 'medium':
            quality_argument = 'qm'
        case 'high':
            quality_argument = 'qh'
        case _:
            quality_argument = 'ql'

    if preview:
        quality_argument = f'p{quality_argument}'

    # Define the command and its arguments as a list
    command = [
        PYTHON_VENV, '-m', 'manim',
        f'-{quality_argument}',  # Quality of the video
        f'{module_name}.py',  # Python script containing the scene
        scene_name  # Name of the scene to render
    ]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful and print the output
    if result.returncode == 0:
        print(f'{module_name}/{scene_name} created successfully!')
        print(result.stdout)
        print(result.stderr)
    else:
        print('Error:')
        print(result.stderr)


def create_multiple_scenes(module_name: str, scene_names: list[str], quality: str = 'low') -> None:
    for scene_name in scene_names:
        create_scene(module_name, scene_name, quality)


def get_all_scenes_in_module(module: object) -> list[str]:
    return [name for name, cls in inspect.getmembers(module, inspect.isclass)
            if issubclass(cls, manim.Scene) and cls.__module__ == module.__name__]


def create_all_scenes_in_module(module: object, quality: str = 'low') -> None:
    create_multiple_scenes(module.__name__, get_all_scenes_in_module(module), quality)


if __name__ == '__main__':
    current_module = excel_character
    current_module_name = current_module.__name__
    current_scene = 'CharacterAnimation'
    current_scenes = ['HelperLookups', 'NamedRangeTableExample']

    # Prototypes
    # create_scene(current_module_name, current_scene)
    # create_multiple_scenes(current_module_name, current_scenes)
    # create_all_scenes_in_module(XLookup_E03)

    # High Quality
    create_scene(current_module_name, current_scene, quality='low')
    # create_multiple_scenes(current_module_name, current_scenes, quality='high')
    # create_all_scenes_in_module(XLookup_E03, quality='high')

import json
import math
import os

import requests
from PIL import Image
from manim import *
from manim.typing import Vector3D

from scenes import IntroScene
from excel_formula import ExcelFormula
from excel_tables import ExcelTable
from scenes import NarratedScene

from functools import partial
import random

pokemon_ids = {
    'Bulbasaur': 1,
    'Charmander': 4,
    'Squirtle': 7,
    'Pikachu': 25,
    'Jigglypuff': 39,
    'Meowth': 52,
    'Psyduck': 54,
    'Magikarp': 129,
    'Magneton': 82,
    'Krabby': 98,
    'Exeggcute': 102,
    'Rhyhorn': 111,
    'Electabuzz': 125,
    'Magmar': 126,
    'Eevee': 133,
    'Vaporeon': 134,
    'Jolteon': 135,
    'Flareon': 136,
    'Porygon': 137,
    'Snorlax': 143,
    'Articuno': 144,
    'Zapdos': 145,
    'Moltres': 146,
    'Dragonite': 149,
    'Gastly': 92,
    'Slowpoke': 79,
    'Rattata': 19,
    'Machop': 66,
    'Hitmonchan': 107,
    'Metapod': 11
}

pokemon_table_data: list[list[str]] = [
    ['\\textbf{Pokemon}', '\\textbf{Type}', '\\textbf{HP}', '\\textbf{Attack}', '\\textbf{Defense}', '\\textbf{Speed}',
     '\\textbf{Excels Vs}', '\\textbf{Vigor}', '\\textbf{Battle Form}'],
    ['Bulbasaur', 'Grass', '45', '36', '62', '27', 'Water', 'Vulnerable', 'Metapod'],
    ['Charmander', 'Fire', '49', '39', '33', '73', 'Grass', 'Vulnerable', 'Rattata'],
    ['Squirtle', 'Water', '48', '49', '48', '32', 'Fire', 'Vulnerable', 'Slowpoke'],
    ['Pikachu', 'Electric', '32', '46', '42', '48', 'Water', 'Fragile', 'Slowpoke'],
    ['Jigglypuff', 'Normal', '89', '17', '24', '22', 'None', 'Resilient', 'Magikarp'],
    ['Meowth', 'Normal', '41', '35', '39', '92', 'None', 'Fragile', 'Rattata'],
    ['Psyduck', 'Water', '52', '38', '53', '26', 'Fire', 'Vulnerable', 'Metapod'],
    ['Magikarp', 'Water', '17', '12', '47', '49', 'Fire', 'Fragile', 'Magikarp'],
    ['Magneton', 'Electric', '93', '61', '93', '37', 'Water', 'Resilient', 'Snorlax'],
    ['Krabby', 'Water', '29', '33', '51', '73', 'Fire', 'Fragile', 'Exeggcute'],
    ['Exeggcute', 'Grass', '63', '32', '58', '64', 'Water', 'Average', 'Exeggcute'],
    ['Rhyhorn', 'Ground', '87', '52', '67', '34', 'Electric', 'Resilient', 'Snorlax'],
    ['Electabuzz', 'Electric', '93', '53', '46', '73', 'Water', 'Resilient', 'Hitmonchan'],
    ['Magmar', 'Fire', '64', '56', '49', '72', 'Grass', 'Average', 'Hitmonchan'],
    ['Eevee', 'Normal', '54', '44', '43', '63', 'None', 'Vulnerable', 'Rattata'],
    ['Vaporeon', 'Water', '61', '32', '57', '70', 'Fire', 'Average', 'Exeggcute'],
    ['Jolteon', 'Electric', '61', '54', '49', '69', 'Water', 'Average', 'Hitmonchan'],
    ['Flareon', 'Fire', '61', '59', '60', '50', 'Grass', 'Average', 'Snorlax'],
    ['Porygon', 'Normal', '62', '37', '64', '61', 'None', 'Average', 'Exeggcute'],
    ['Snorlax', 'Normal', '160', '52', '69', '29', 'None', 'Unbreakable', 'Snorlax'],
    ['Articuno', 'Ice', '94', '57', '68', '57', 'Dragon', 'Resilient', 'Dragonite'],
    ['Zapdos', 'Electric', '106', '58', '67', '58', 'Water', 'Sturdy', 'Dragonite'],
    ['Moltres', 'Fire', '91', '57', '74', '60', 'Grass', 'Resilient', 'Dragonite'],
    ['Dragonite', 'Dragon', '112', '73', '73', '56', 'Dragon', 'Sturdy', 'Dragonite'],
    ['Gastly', 'Ghost', '47', '26', '29', '32', 'Ghost', 'Vulnerable', 'Magikarp'],
    ['Slowpoke', 'Water', '103', '49', '46', '34', 'Fire', 'Sturdy', 'Slowpoke'],
    ['Rattata', 'Normal', '29', '32', '32', '84', 'None', 'Fragile', 'Rattata'],
    ['Machop', 'Fighting', '70', '37', '58', '29', 'Normal', 'Average', 'Metapod'],
    ['Hitmonchan', 'Fighting', '73', '55', '47', '74', 'Normal', 'Average', 'Hitmonchan'],
    ['Metapod', 'Bug', '48', '22', '54', '31', 'Grass', 'Vulnerable', 'Metapod']
]
pokemon_table_data = sorted(pokemon_table_data, key=lambda row: pokemon_ids.get(row[0], -1))

excels_vs: list[list[str]] = [
    ['Bug', 'Grass'],
    ['Dragon', 'Dragon'],
    ['Electric', 'Water'],
    ['Fighting', 'Normal'],
    ['Fire', 'Grass'],
    ['Ghost', 'Ghost'],
    ['Grass', 'Water'],
    ['Ground', 'Electric'],
    ['Ice', 'Dragon'],
    ['Normal', 'None'],
    ['Water', 'Fire']
]

vigor: list[list[str]] = [
    ['0', 'Fragile'],
    ['45', 'Vulnerable'],
    ['60', 'Average'],
    ['85', 'Resilient'],
    ['100', 'Sturdy'],
    ['130', 'Unbreakable']
]

battle_form: list[list[str]] = [
    ['L/L/L', 'Magikarp'],
    ['L/L/H', 'Metapod'],
    ['L/H/L', 'Slowpoke'],
    ['L/H/H', 'Snorlax'],
    ['H/L/L', 'Rattata'],
    ['H/L/H', 'Exeggcute'],
    ['H/H/L', 'Hitmonchan'],
    ['H/H/H', 'Dragonite']
]

field_details = [
    ['\\textbf{Excels Vs}', ''],
    *excels_vs,
    ['', ''],
    ['\\textbf{Vigor Bound}', '\\textbf{Group}'],
    *vigor,
    ['', ''],
    ['\\textbf{Sp/Att/De}', '\\textbf{Battle Form}'],
    *battle_form
]
if len(field_details) < len(pokemon_table_data):
    field_details.extend([['', ''] for _ in range(len(pokemon_table_data) - len(field_details))])

pokemon_table_data = [pokemon_table_data[i] + [''] + field_details[i] for i in range(len(pokemon_table_data))]


class HighlightRules(Scene):
    def construct(self):
        pokemon_table: ExcelTable = ExcelTable(pokemon_table_data).scale(0.17).to_edge(LEFT, buff=0.3)
        self.add(pokemon_table)
        self.remove(*[pokemon_table.get_rows()[i][j] for j in [7, 8, 9] for i in range(2, len(pokemon_table_data) + 1)])

        self.wait()
        self.play(pokemon_table.get_passing_flash('K1:L12'))

        self.wait()
        self.play(pokemon_table.get_passing_flash('K14:L20'))

        self.wait()
        self.play(pokemon_table.get_passing_flash('K22:L30'))

        self.wait()


class NestedIfIntroText(Scene):
    def construct(self):
        if_sequence_text = ('=IF(ExcelUser,\nIF(UsesIf,\nIF(MessyNesting,\n"This is for you"'
                            ',\n"Inconceivable!"),\n"Avoid my mistakes"),\n"You don\'t even go here!")')
        if_sequence = ExcelFormula(if_sequence_text, start_location=UP*2, start_align=LEFT+UP, scale=0.9)
        self.wait(2)
        self.play(if_sequence.write_to_scene())
        self.wait(5)


class ComparisonIfs(Scene):
    def construct(self):
        names = Tex('\\textbf{Switch}', '\\textbf{XLookup}', '\\textbf{Ifs}').scale(1.1)
        for i, name in enumerate(names, start=-1):
            name.set_x(0)
            name.shift(UP * 1.5 + RIGHT * i * (2 + (name.width + names[1].width) / 2))
            if i == 0:
                name.shift(LEFT * 0.24)
        self.play(Write(names))
        self.wait(2)
        use_cases = Tex('Comparing a\n\rsingle cell\n\ragainst\n\rmultiple options\n\r',
                        'Comparing with\n\rranges or\n\rboundaries\n\r',
                        'Comparing with\n\rmultiple\n\rconditions, even\n\rasymmetrically')

        for i, use_case in enumerate(use_cases):
            name = names[i]
            use_case.scale(0.8)
            use_case.shift(RIGHT * name.get_x() + DOWN * 0.2)
            # use_case.next_to(use_cases[1], RIGHT, coor_mask=np.array([0,1,0]))
            use_case.align_to(use_cases[1], UP)
            if i == 0:
                use_case.shift(DOWN * 0.34)
            self.play(Write(use_case))
            self.wait()
        self.wait(4)


class PokemonData(NarratedScene):

    def __init__(self):
        super().__init__()
        self.pokemon_table: ExcelTable = ExcelTable(pokemon_table_data).scale(0.17).to_edge(LEFT, buff=0.3)

    def pokemon_formula(self, formula_text: str, target_cell: str):
        return ExcelFormula(formula_text, tables_list=[self.pokemon_table], target_cell=target_cell,
                            split_lines='\n' not in formula_text, nested_indent=0.15, scale=0.44,
                            start_location=self.pokemon_table.get_right() + RIGHT * 0.3, start_align=LEFT)

    def show_alternatives(self, formula_1: ExcelFormula, formula_2: ExcelFormula, column_to_reveal: int,
                          remove: bool = True):
        formula_1.next_to(self.pokemon_table, RIGHT, coor_mask=np.array([0, 1, 0]))
        formula_2.next_to(self.pokemon_table, RIGHT, coor_mask=np.array([0, 1, 0]))
        formula_1.formula_box[1].move_to(formula_1).shift(UP * 0.02)
        formula_2.formula_box[1].move_to(formula_2).shift(UP * 0.02)

        self.play(formula_1.formula_box_anim())
        self.play(formula_1.write_line_by_line(line_run_time=0.4))
        self.play(LaggedStart(
            *[Write(result) for result in self.pokemon_table.get_columns()[column_to_reveal][2:]],
            lag_ratio=0.1
        ))
        self.wait(3)

        self.play(Unwrite(formula_1),
                  Uncreate(formula_1.highlight_objs)
                  )
        self.play(Transform(formula_1.formula_box[0], formula_2.formula_box[1]))
        self.play(formula_2.write_line_by_line(line_run_time=0.4))
        self.wait(5)
        if remove:
            self.play(Uncreate(formula_1.formula_box[0]),
                      Unwrite(formula_2),
                      Uncreate(formula_2.highlight_objs))
            self.wait()

    def construct(self):
        hidden_data_cells: list[tuple[int, int]] = [(i, j) for j in [7, 8, 9] for i in
                                                    range(2, len(pokemon_table_data) + 1)]

        self.play(self.pokemon_table.animate_draw(hidden_data=hidden_data_cells), run_time=5)
        self.wait(3)

        if_switch_nested_txt: str = ''
        for type1, type2 in excels_vs:
            if_switch_nested_txt = f'{if_switch_nested_txt}\n' if if_switch_nested_txt else '='
            if_switch_nested_txt = f'{if_switch_nested_txt}IF(B2="{type1}", "{type2}",'
        if_switch_nested_txt = f'{if_switch_nested_txt}\n"Unknown"\n{")" * len(excels_vs)}'

        switch_txt: str = ''
        for type1, type2 in excels_vs:
            switch_txt = f'{switch_txt}\n' if switch_txt else '=SWITCH(B2,\n'
            switch_txt = f'{switch_txt}"{type1}", "{type2}",'
        switch_txt = f'{switch_txt}\n"Unknown")'

        if_switch_nested = self.pokemon_formula(formula_text=if_switch_nested_txt, target_cell='G2')
        switch = self.pokemon_formula(formula_text=switch_txt, target_cell='G2')

        self.show_alternatives(if_switch_nested, switch, 7, False)
        self.play(Unwrite(switch),
                  Uncreate(switch.highlight_objs))

        xlookup_2_txt = '=XLOOKUP(B2, $K$2:$K$12, $L$2:$L$12, "Unknown")'
        xlookup_2 = self.pokemon_formula(formula_text=xlookup_2_txt, target_cell='G2')
        xlookup_2.next_to(self.pokemon_table, RIGHT, coor_mask=np.array([0, 1, 0]))
        xlookup_2.formula_box[1].move_to(xlookup_2).shift(UP * 0.02)

        self.play(Transform(if_switch_nested.formula_box[0], xlookup_2.formula_box[1]))
        self.play(xlookup_2.write_line_by_line(line_run_time=0.8))
        self.wait(2)
        self.play(Unwrite(xlookup_2),
                  Uncreate(if_switch_nested.formula_box[0]),
                  *[Uncreate(mob) for mob in xlookup_2.highlight_objs])
        self.wait(2)

        if_xlookup_nested_txt: str = ''
        for i in range(len(vigor) - 1):
            if_xlookup_nested_txt = f'{if_xlookup_nested_txt}\n' if if_xlookup_nested_txt else '='
            if_xlookup_nested_txt = f'{if_xlookup_nested_txt}IF(C2 < {vigor[i + 1][0]}, "{vigor[i][1]}",'
        if_xlookup_nested_txt = f'{if_xlookup_nested_txt}\n"Unbreakable"\n)))))'

        xlookup_txt: str = '=XLOOKUP(C2, $K$15:$K$20, $L$15:$L$20, , -1)'

        if_xlookup_nested = self.pokemon_formula(formula_text=if_xlookup_nested_txt, target_cell='H2')
        xlookup = self.pokemon_formula(formula_text=xlookup_txt, target_cell='H2')

        self.show_alternatives(if_xlookup_nested, xlookup, 8)

        translations = {
            'SL': 'F2 <= 55',
            'SH': 'F2 > 55',
            'AL': 'D2 <= 45',
            'AH': 'D2 > 45',
            'DL': 'E2 <= 50',
            'DH': 'E2 > 50'
        }

        if_ifs_nested_txt: str = ''
        for form, type in battle_form[:-1]:
            if_ifs_nested_txt = f'{if_ifs_nested_txt}\n' if if_ifs_nested_txt else '='
            if_ifs_nested_txt = (f'{if_ifs_nested_txt}IF(AND({translations["S" + form[0]]}, '
                                 f'{translations["A" + form[2]]}, {translations["D" + form[4]]}), "{type}",')
        if_ifs_nested_txt = f'{if_ifs_nested_txt}\n"{battle_form[-1][1]}"\n{")" * (len(battle_form) - 1)}'

        ifs_txt: str = ''
        for form, type in battle_form:
            ifs_txt = f'{ifs_txt}\n' if ifs_txt else '=IFS('
            ifs_txt = (f'{ifs_txt}AND({translations["S" + form[0]]}, {translations["A" + form[2]]}, '
                       f'{translations["D" + form[4]]}), "{type}",')
        ifs_txt = f'{ifs_txt}\n)'

        if_ifs_nested = self.pokemon_formula(formula_text=if_ifs_nested_txt, target_cell='I2')
        ifs = self.pokemon_formula(formula_text=ifs_txt, target_cell='I2')

        self.show_alternatives(if_ifs_nested, ifs, 9)

        self.wait(2)


def image_to_pixel_squares(pokemon_name: str) -> VGroup:
    download_pokemon_image(pokemon_name)
    image_path = f'pokemon_images/{pokemon_name.lower()}.png'
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)

    # Create a VGroup to hold all squares
    pixel_squares = VGroup()

    # Get image dimensions
    height, width = img_array.shape[:2]
    # Create squares for each pixel
    for i, y in enumerate(range(height)):
        for j, x in enumerate(range(width)):
            color = img_array[y, x]

            # Skip transparent pixels
            if color[3] == 0:
                continue

            # Create square for this pixel
            square = Square(
                side_length=1 / max(width, height),
                fill_color=rgb_to_color(color[:3] / 255),
                fill_opacity=color[3] / 255,
                stroke_width=1.5,
                stroke_color=rgb_to_color(color[:3] / 255)
            )

            # Position the square
            square.move_to([x / width - 0.5, -y / height + 0.5, 0])

            pixel_squares.add(square)

            # if config['quality'] == 'low_quality' and len(pixel_squares) == 10:
            #     return pixel_squares

    return pixel_squares


class SortingPokemon(NarratedScene):
    def construct(self):
        pokemon_names: list[str] = [row[0] for row in pokemon_table_data[1:]]
        pokemon_mobs: list[VGroup] = [image_to_pixel_squares(pokemon_name).scale(4) for pokemon_name in pokemon_names]
        pokemon_group: VGroup = VGroup(*pokemon_mobs)

        def pokemon_carousel(mob: VGroup, alpha: float, start_width: float, start_loc: Vector3D):
            center_scale: float = 3 / 4.0
            x_pos: Vector3D = (start_loc * math.cos(alpha * PI))
            y_pos: Vector3D = (start_loc * (1 + math.cos(alpha * 2 * PI)) / 2 + UP * 2)
            scale: float = (math.cos(alpha * 2 * PI) + 1) / 2 * (1 - center_scale) + center_scale
            rot: float = (-80 * math.cos(alpha * PI)) * DEGREES
            opacity: float = math.sin(alpha * PI) ** 5

            mob.move_to(np.array([x_pos[0], y_pos[1], 0]))
            mob.rotate(angle=mob.prev_rotation, axis=DOWN)
            mob.scale_to_fit_width(scale * start_width)
            mob.prev_rotation = rot
            mob.rotate(angle=rot, axis=UP)
            mob.set_opacity(opacity)

        animations: list[Animation] = []
        start_pos: Vector3D = (config.frame_width / 2 + max(
            [pokemon.width for pokemon in pokemon_group])) * RIGHT + DOWN * 1.5
        for pokemon in pokemon_group:
            pokemon_start_width: float = pokemon.width
            pokemon.prev_rotation = 0

            pokemon_updater = partial(pokemon_carousel,
                                      start_width=pokemon_start_width,
                                      start_loc=start_pos
                                      )

            animations.append(UpdateFromAlphaFunc(
                pokemon,
                pokemon_updater,
                run_time=10,
                rate_func=rate_functions.ease_out_sine)
            )

        carousel_animation = LaggedStart(*animations, lag_ratio=0.05)
        known_characteristics = VGroup(*[Tex(el) for el in ['Name', 'Type', 'HP', 'Attack', 'Defense', 'Speed']])
        calculated_characteristics = VGroup(*[Tex(el) for el in ['Excels Vs', 'Vigor', 'Battle Form']])

        known_characteristics.arrange(DOWN)
        calculated_characteristics.arrange(DOWN)
        known_characteristics.shift(LEFT * 2.2 + DOWN * 2)
        calculated_characteristics.shift(RIGHT * 2.2).align_to(known_characteristics, UP)

        write_chars = Succession(*[Write(char) for char in known_characteristics],
                                 Wait(1.5),
                                 *[Write(char) for char in calculated_characteristics],
                                 lag_ratio=1.25)

        self.play(LaggedStart(carousel_animation, write_chars, lag_ratio=0.2))
        self.play(FadeOut(known_characteristics), FadeOut(calculated_characteristics))
        self.wait()


def get_pokemon_image(pokemon_name: str) -> ImageMobject | None:
    img_path = f'pokemon_images/{pokemon_name.lower()}.png'
    return ImageMobject(img_path)


def download_pokemon_image(pokemon_name: str) -> None:
    # Checks if image exists in the pokemon_images folder:
    img_path = f'pokemon_images/{pokemon_name.lower()}.png'
    os.makedirs('../pokemon_images', exist_ok=True)

    # If the image does not exist, download from pokemon api and save it to the folder
    if not os.path.exists(img_path):
        url: str = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'pokemon_images/{pokemon_name.lower()}.png', 'wb') as file:
                file.write(requests.get(response.json()['sprites']['front_default']).content)
        else:
            print(f'Error for {pokemon_name}: {response.status_code}')


class IfIntro(IntroScene):
    def __init__(self):
        super().__init__('Better If Statements')

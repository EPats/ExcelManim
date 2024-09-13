from manim import *

import excel_tables

table_data: list[list[str]] = [
    ['\\textbf{Name}', '\\textbf{Field}', '\\textbf{Known For}', '\\textbf{Birth Year}', '\\textbf{IQ}', '\\textbf{Impact}'],
    ['Ifsaac Newton', 'Physics', 'Laws of Motion', '1643', '186', '8.1'],
    ['Sumarie Curie', 'Physics and Chemistry', 'Radioactivity', '1867', '192', '8.4'],
    ['Albert EinSign', 'Physics', 'Theory of Relativity', '1879', '164', '9.8'],
    ['Charles Dec2Bin', 'Biology', 'Theory of Evolution', '1809', '166', '9.2'],
    ['V. Lookup Asteur', 'Microbiology', 'Pasteurization', '1822', '175', '7.7'],
    ['Min Planck', 'Physics', 'Quantum Theory', '1858', '181', '8.2'],
    ['Harmean Minkowski', 'Mathematics', 'Minkowski Space', '1864', '176', '8.3'],
    ['Linest Rutherford', 'Physics', 'Nuclear Model', '1871', '184', '9.5'],
    ['Absdus Salam', 'Physics', 'Electroweak Theory', '1926', '188', '6.3'],
    ['Rowsalind Franklin', 'Chemistry', 'DNA Structure', '1920', '168', '7.1'],
    ['Leon Ordo Da Vinci', 'Polymath', 'Vitruvian Man', '1452', '195', '8.8'],
    ['Ada Replace', 'Mathematics', 'First Computer Program', '1815', '178', '8.1'],
    ['Stdeven Hawking', 'Physics', 'Black Hole Radiation', '1942', '160', '9.7'],
    ['ANDers Celsius', 'Physics', 'Temperature Scale', '1701', '162', '7.1'],
    ['Alexander Ceiling', 'Bacteriology', 'Discovery of Penicillin', '1881', '157', '6.2'],
    ['Alexander ByRow', 'Engineering', 'Telephone', '1847', '159', '8.1'],
    # ['Dmitri Mendeleev', 'Chemistry', 'Periodic Table of Elements', '1834', '182', '7.6'],
    ['ByColas Tesla', 'Electrical Engineering', 'Alternating Current', '1856', '167', '8.3']
]

table_data = [row[0:1] + row[2:] for row in table_data]


class Test(Scene):
    def construct(self):
        table = excel_tables.ExcelTable(table_data).scale(0.3)
        self.wait()
        self.play(table.animate_draw())
        self.wait(5)
        self.play(table.animate.scale(0.7).to_corner(DL))
        self.wait(2)

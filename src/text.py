"""Copyright 2026 Pierre Halipré

This file is part of Chasse à l'ogre.

Chasse à l'ogre is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Chasse à l'ogre is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Chasse à l'ogre. If not, see <https://www.gnu.org/licenses/>.
"""

from tool import Math, Path, File, Array
from design import Design


class Text:
    def __init__(self) -> None:
        self.numerals = Array()
        self.home = Array()
        self.pause = Array()
        self.end = Array()
        self.custom = Array()

        i = 0

        while i < 8:
            self.custom.add(None)
            i += 1

    def fill(self, name: str, design: Design) -> None:
        path_mode = design.get_path_mode_current()
        path_texts = Path.join(path_mode, "texts")
        path_file = Path.join(path_texts, name)
        path = Path.text(path_file)
        file = File(path)
        self.numerals.add(Sentence(file, 13))
        self.home.add(Paragraph(file, 3))
        self.pause.add(Paragraph(file, 2))
        self.end.add(Paragraph(file, 2))

    def set_custom_numeral(self, i: int, numeral: int, design: Design) -> None:
        numerals = self.numerals.get(design.mode)
        unicode = numerals.get(numeral)
        self.custom.set(i, unicode)

    def set_custom_pause(self, milliseconds: int, design: Design) -> None:
        minutes = Math.floor(milliseconds / 60000)
        minutes_ten = Math.floor(minutes / 10)
        minutes_unit = minutes % 10
        minutes_separator = 10
        seconds = Math.floor((milliseconds % 60000) / 1000)
        seconds_ten = Math.floor(seconds / 10)
        seconds_unit = seconds % 10
        seconds_separator = 11
        centiseconds = Math.floor((milliseconds % 1000) / 10)
        centiseconds_ten = Math.floor(centiseconds / 10)
        centiseconds_unit = centiseconds % 10

        self.set_custom_numeral(0, minutes_ten, design)
        self.set_custom_numeral(1, minutes_unit, design)
        self.set_custom_numeral(2, minutes_separator, design)
        self.set_custom_numeral(3, seconds_ten, design)
        self.set_custom_numeral(4, seconds_unit, design)
        self.set_custom_numeral(5, seconds_separator, design)
        self.set_custom_numeral(6, centiseconds_ten, design)
        self.set_custom_numeral(7, centiseconds_unit, design)

    def set_custom_end(self, score: int, design: Design) -> None:
        thousand = Math.floor(score / 1000)
        hundred = Math.floor((score % 1000) / 100)
        ten = Math.floor((score % 100) / 10)
        unit = score % 10
        space = 12

        self.set_custom_numeral(0, space, design)
        self.set_custom_numeral(1, space, design)
        self.set_custom_numeral(2, thousand, design)
        self.set_custom_numeral(3, hundred, design)
        self.set_custom_numeral(4, ten, design)
        self.set_custom_numeral(5, unit, design)
        self.set_custom_numeral(6, space, design)
        self.set_custom_numeral(7, space, design)


class Sentence(Array):
    def __init__(self, file: File, n_characters: int) -> None:
        super().__init__()

        i = 0

        while i < n_characters:
            character = file.read()
            self.add(Math.unicode(character))
            i += 1


class Paragraph(Array):
    def __init__(self, file: File, n_sentences: int) -> None:
        super().__init__()

        i = 0

        while i < n_sentences:
            self.add(Sentence(file, 8))
            i += 1

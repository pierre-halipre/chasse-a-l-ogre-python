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

import os
import shutil
import PyInstaller.__main__

PATH_MAIN = os.path.join(".", "main.py")
PATH_DATA = os.path.join("..", "res")
PATH_ICON = os.path.join(PATH_DATA, "icon.ico")
PATH_EXE = os.path.join(".", "main")
PATH_EXE_FINAL = os.path.join("..", "..", "chasse_a_l_ogre.exe")
PATH_BUILD = os.path.join(".", "build")

PyInstaller.__main__.run(
    (
        PATH_MAIN,
        "--clean",
        "--onefile",
        "--noconsole",
        "--disable-windowed-traceback",
        "--add-data=" + PATH_DATA + ";" + ".",
        "--name=" + PATH_EXE,
        "--icon=" + PATH_ICON,
        "--distpath=.",
    )
)

os.remove(PATH_EXE + ".spec")
shutil.rmtree(PATH_BUILD)
os.rename(PATH_EXE + ".exe", PATH_EXE_FINAL)

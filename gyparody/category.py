# Brandon Edens
# 2010-03-20
# Copyright (C) 2010 Brandon Edens <brandon@as220.org>
#
# This file is part of gyparody.
#
# gyparody is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gyparody is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gyparody. If not, see <http://www.gnu.org/licenses/>.
"""
"""

###############################################################################
## Imports
###############################################################################

import clutter
import logging

from answer import Answer
from config import config
from text import Text


###############################################################################
## Constants
###############################################################################

BACKGROUND_COLOR = clutter.Color(6, 11, 121)


###############################################################################
## Classes
###############################################################################

class Category(clutter.Box):
    """
    """

    def __init__(self):
        """
        """
        super(Category, self).__init__(clutter.BoxLayout())

        layout = self.get_layout_manager()
        layout.set_spacing(10)
        layout.set_vertical(True)

        self.name = CategoryName('hello world')
        self.add(self.name)

        for i in xrange(5):
            answer = Answer()
            self.add(answer)

    def set_size(self, width, height):
        """
        """
        super(Category, self).set_size(width, height)
        spacing = int(height * 0.01)
        layout = self.get_layout_manager()
        layout.set_spacing(spacing)
        children = self.get_children()
        for child in children:
            child.set_size(width, (height / len(children)) - spacing)

class CategoryName(clutter.Box):

    def __init__(self, text):
        """
        """
        super(CategoryName, self).__init__(
            clutter.BinLayout(clutter.BIN_ALIGNMENT_CENTER,
                              clutter.BIN_ALIGNMENT_CENTER))

        self.set_color(config.square_background_color)

        self.text = Text(config.category_font, text)
        self.add(self.text)

# Paolo DePetrillo
# 2010-04-13
# Copyright (C) 2010 Paolo DePetrillo <paolod@gmail.com>
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

from category import Category

###############################################################################
## Classes
###############################################################################

class GameBoard(clutter.Box):
    def __init__(self, model):
        super(GameBoard, self).__init__(clutter.BoxLayout())

        self.model = model

        layout = self.get_layout_manager()
        layout.set_vertical(False)
        spacing = int(self.get_width() * 0.01)
        layout.set_spacing(spacing)

        self.categories = []
        category_number = 0
        round = self.model.get_round()
        for category in round:
            category = Category(model, category, category_number)
            self.add(category)
            category.set_size(self.get_width() / len(round) - spacing,
                              self.get_height())
            self.categories.append(category)
            category_number += 1

    def set_click_handler(self, click_handler):
        """
        """
        for category in self.categories:
            category.set_click_handler(click_handler)

    def set_size(self, width, height):
        """
        """
        try:
            super(GameBoard, self).set_size(width, height)
            layout = self.get_layout_manager()
            spacing = int(self.get_width() * 0.01)
            layout.set_spacing(spacing)
            children = self.get_children()
            for child in children:
                child.set_size(self.get_width() / len(children) - spacing,
                               self.get_height())
        except AttributeError:
            # If there is an attribute error then its most likely because
            # self.game_board did not exist because the stage is first
            # loading. Therefore we simply pass on this exception as during
            # loading correctly size of internals will be set.
            pass

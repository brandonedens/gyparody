# Brandon Edens
# 2010-04-16
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

from config import config
from game import game

###############################################################################
## Classes
###############################################################################

class Admin(clutter.Stage):
    """
    """

    def __init__(self):
        super(Admin, self).__init__()

        self.set_fullscreen(False)
        self.set_size(400, 300)
        self.set_user_resizable(False)

        box = clutter.Box(clutter.BoxLayout())
        box.get_layout_manager().set_vertical(True)
        self.add(box)

        box.add(clutter.Text(config.admin_font, 'Enter value:'))

        self.value = clutter.Text(config.admin_font, '0')
        self.value.set_reactive(True)
        self.value.set_editable(True)
        self.value.connect('button-release-event',
            lambda actor, event: self.set_key_focus(self.value))
        box.add(self.value)

        self.add_buttons = []
        self.sub_buttons = []
        for i in range(3):
            add = clutter.Text(config.admin_font, 'Add to player %d' % (i+1))
            add.set_reactive(True)
            add.connect('button-release-event',
                lambda actor, event: game.adjust_score(i, self.get_value()))
            self.add_buttons.append(add)
            box.add(add)
            sub = clutter.Text(config.admin_font, 'Subtract from player %d' % (i+1))
            sub.set_reactive(True)
            sub.connect('button-release-event',
                lambda actor, event: game.adjust_score(i, -self.get_value()))
            self.sub_buttons.append(sub)
            box.add(sub)

        self.show()

    def get_value(self):
        return int(self.value.get_text())


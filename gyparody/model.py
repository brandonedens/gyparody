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

import gobject

###############################################################################
## Classes
###############################################################################

class Model(gobject.GObject):
    """
    """

    def __init__(self):
        """
        """
        super(Model, self).__init__()

        self.selected_answers = {}

    def get_round(self):
        return self.round

    def is_answer_selected(self, answer_numbers):
        """
        """
        return self.selected_answers.has_key(answer_numbers)

    def select_answer(self, answer_numbers):
        self.selected_answers[answer_numbers] = None
        self.emit('update-model')

gobject.type_register(Model)
gobject.signal_new('update-model',
                   Model,
                   gobject.SIGNAL_RUN_FIRST,
                   gobject.TYPE_NONE,
                   ())


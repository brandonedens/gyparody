# Brandon Edens
# 2010-03-21
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

import os

import clutter
import yaml


###############################################################################
## Constants
###############################################################################

# User's home directory
USER_HOME_DIR = os.getenv('HOME')

# Locations to search for configuration file.
CONFIG_LOCATIONS = (USER_HOME_DIR+'./.gyparody.rc',
                    '/etc/gyparody/config',
                    '.gyparody.rc',
                    )


###############################################################################
## Classes
###############################################################################

class Config(object):
    def __init__(self):

        # Logging settings
        self.log_filename = '/var/tmp/gyparody.log'
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Screen setup options
        self.fullscreen = False
        self.screen_width = 800
        self.screen_height = 600

        # Background color
        self.background_color = clutter.Color(6, 11, 121)

        # Category settings
        self.category_font = "Haettenschweiler 24"

        # Answer settings
        self.answer_font = "ScaKorinna 24"
        self.answer_value_font = "ScaKorinna 26"

        # Answer value font
        self.value_color = clutter.Color(217, 161, 71)
        self.answer_font = "ScaKorinna 64"

        # Spacing between categories
        self.category_spacing = 20

        self.round_1_data = '/home/brandon/src/gyparody/docs/round1.yaml'

    def load(self):
        config_filename = self._find_config_file()
        if config_filename:
            config_file = open(config_filename, 'r')
            options = yaml.load(config_file)
            self.players = options['players']

    def _find_config_file(self):
        absolute_path = None
        for location in CONFIG_LOCATIONS:
            if os.path.isfile(location):
                absolute_path = path
        return absolute_path


###############################################################################
## Statements
###############################################################################

config = Config()
config.load()


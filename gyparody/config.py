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

        # Save file location
        self.save_filename = '/tmp/gyparody_save.yaml'

        # Screen setup options
        self.fullscreen = False
        self.screen_width = 800
        self.screen_height = 600
        self.fullscreen_width = 1366
        self.fullscreen_height = 768

        # Background color
        self.background_color = clutter.Color(6, 11, 121)

        # Square background color
        self.square_background_color = clutter.Color(6, 11, 121)

        # Category settings
        self.category_font = "Haettenschweiler 18"

        # Clue settings
        self.clue_font = "ScaKorinna 10"
        self.clue_value_font = "ScaKorinna 20"
        self.clue_value_color = clutter.Color(217, 161, 71)

        # Clue overlay font
        self.clue_overlay_font = "ScaKorinna 48"
        self.category_overlay_font = "ScaKorinna 48"

        # Spacing between categories
        self.category_spacing = 10

        self.round_1_data = './docs/round1.yaml'

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
                absolute_path = location
        return absolute_path


###############################################################################
## Statements
###############################################################################

config = Config()
config.load()


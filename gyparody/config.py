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

        # Audio filenames
        self.sound_daily_double = 'sounds/daily_double.wav'
        self.sound_final_music = 'sounds/final_music.wav'
        self.sound_timeout = 'sounds/timeout.wav'

        # baud rate
        self.serial_port = '/dev/ttyUSB0'
        self.serial_baud_rate = 57600

        # Timeouts
        # After a player buzzes in the number of seconds alotted for them to
        # answer.
        self.await_answer_timeout = 10
        # After question is read, the number of seconds to await an incoming
        # player buzz.
        self.await_buzz_timeout = 15
        self.buzzer_lockout_time = 1

        # Screen setup options
        self.fullscreen = False
        self.screen_width = 800
        self.screen_height = 600
        self.fullscreen_width = 1366
        self.fullscreen_height = 768
        self.admin_screen_width = 800
        self.admin_screen_height = 600

        # Number of rounds in game
        self.game_rounds = 1

        # Player scores on the main screen
        self.display_player_scores = True
        # Player scores position
        self.player_scores_position = 'east'
        self.player_name_font = "ScaKorinna 10"
        self.player_score_font = "ScaKorinna 18"

        # Stage background color
        self.stage_background_color = clutter.Color(2, 2, 2)
        # Background color
        self.background_color = clutter.Color(6, 11, 121)

        # Square background color
        self.square_background_color = clutter.Color(6, 11, 121)

        # Increasing score color
        self.increase_score_color = clutter.Color(0, 255, 0)
        # Decreasing score color
        self.decrease_score_color = clutter.Color(255, 0, 0)

        # Category settings
        self.category_font = "Haettenschweiler 18"

        # Clue settings
        self.clue_font = "ScaKorinna 10"
        self.clue_value_font = "ScaKorinna 20"
        self.clue_value_color = clutter.Color(217, 161, 71)

        # Clue overlay font
        self.clue_overlay_font = "ScaKorinna 48"
        self.category_overlay_font = "ScaKorinna 48"
        self.player_overlay_font = "ScaKorinna 48"
        self.all_player_overlay_font = "ScaKorinna 36"

        # Spacing between categories
        self.category_spacing = 10

        # Admin font
        self.admin_font_header = "Sans 26"
        self.admin_font = "Sans 22"

        # Daily double font
        self.daily_double_font = 'Gyparody 96'
        # Final round font
        self.final_round_font = 'Gyparody 96'

        self.round_1_data = './etc/round1.yaml'
        self.round_2_data = './etc/round2.yaml'
        self.final_round = './etc/final_round1.yaml'

        self.player_a_name = 'Team 1'
        self.player_b_name = 'Team 2'
        self.player_c_name = 'Team 3'

        self.drink_value = 100

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


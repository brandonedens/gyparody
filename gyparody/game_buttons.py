# Brandon Edens
# 2010-04-19
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

import logging
import serial

from config import config


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################

class GameButtons(object):

    def __init__(self):
        """
        Setup the serial system.
        """
        super(GameButtons, self).__init__()

        self.serial = None

        # Buttons
        self.button_1 = False
        self.button_2 = False
        self.button_3 = False

        # Player lights
        self.player_1 = False
        self.player_2 = False
        self.player_3 = False

        # Boolean representing whether or not send player serial
        self.send_player_state = False

        # Setup the serial connection.
        try:
            self.serial = serial.Serial(config.serial_port,
                                        config.serial_baud_rate,
                                        timeout=1)
            self.serial.xonxoff = False
            self.serial_rtscts = False
            self.serial.flushInput()
        except serial.serialutil.SerialException:
            print 'No serial port is available.'
            print 'Are the game buttons connected?'

        self.ring = 'XXABC'

    def close(self):
        """
        Cleanup the serial system.
        """
        if self.serial:
            self.serial.close()
        else:
            logging.warning('Attempting to close serial that was not opened.')

    def player_set(self, player_index, value):
        """
        Set the player led specified by index:
        player 1 = 0,
        player 2 = 1,
        player 3 = 2
        to the given value.
        """
        if player_index == 0 and value != self.player_1:
            self.player_1 = value
            self.send_player_state = True
        elif player_index == 1 and value != self.player_2:
            self.player_2 = value
            self.send_player_state = True
        elif player_index == 2 and value != self.player_3:
            self.player_3 = value
            self.send_player_state = True

    def read(self):
        """
        Read the buttons.
        """
        if self.serial:
            while self.serial.inWaiting() > 0:
                c = self.serial.read(1)
                if len(c) != 1:
                    continue
                self.ring = self.ring[1:] + c
                if self.ring[:2] == 'GY':
                    if self.ring[2] == '1':
                        self.button_1 = True
                    if self.ring[3] == '1':
                        self.button_2 = True
                    if self.ring[4] == '1':
                        self.button_3 = True
                    if not self.button_1 and not self.button_2 and not self.button_3:
                        continue
                    logging.debug("buttons player1 = %s player2 = %s player3 = %s" % (self.button_1,
                                                                                      self.button_2,
                                                                                      self.button_3))
                    return (self.button_1, self.button_2, self.button_3)

        return (0, 0, 0)

    def reset_buttons(self):
        """
        Reset the buttons
        """
        self.button_1 = False
        self.button_2 = False
        self.button_3 = False
        if self.serial:
            self.serial.flushInput()

    def reset_player_lights(self):
        """
        Reset the buttons.
        """
        self.player_1 = False
        self.player_2 = False
        self.player_3 = False
        self.send_player_state = True
        self.send_players()

    def send_players(self):
        """
        Send the player lights.
        """
        if self.serial and self.send_player_state:
            text = "GY%d%d%d" % (self.player_1,
                                 self.player_2,
                                 self.player_3)
            self.serial.write(text)
            self.send_player_state = False


###############################################################################
## Statements
###############################################################################

game_buttons = GameButtons()


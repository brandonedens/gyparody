.. -*- mode: rst; -*-

========================
Gyparody Software README
========================

:author: Brandon Edens
:date: 2009-04-21

.. contents:: Table of Contents
.. sectnum::
.. footer:: Gyparody Software README


Authors
=======

This software would not be possible if it were not for the work of:

* Brandon Edens <brandon@as220.org>
* Paolo DePetrillo <paolod@gmail.com>


Copying
=======

This source code for this software is licensed as the GNU Public License
version 3. A complete listing of this license is available in the COPYING file
found in the software as well as at:
http://www.gnu.org/licenses/gpl.html


Installing
==========

Some basic competency in Unix is required. Knowing how to operating the command
line and install software via your package manager is necessary. This software
has only been tested on GNU/Linux machines. Please do not email the authors
with software installation problems if those problems involve installing 3rd
party software such as clutter OR issues with operating your OSes package
manager.


Software Requirements
---------------------

* pyyaml - aka python-yaml
* libclutter >= 1.2
* libclutter-gst >= 1.0
* pyclutter > 1.0
* pyclutter-gst > 1.0


Installing Needed Libraries
---------------------------

Copies of gyparody software can be retrieved by::

  git clone https://github.com/brandonedens/gyparody.git

To execute the software you will need clutter >= 1.2 and pyclutter > 1.0. This
software is relatively new (as of 2010-04-21) with libclutter 1.2 version not
available in Ubuntu Karmic Koala.

Therefore we must install the software from what is available on Clutter's
website at: http://clutter-project.org/download.html

The latest (possibly unstable versions can be obtained by executing)::

  git clone git://git.clutter-project.org/clutter
  git clone git://git.clutter-project.org/clutter-gst
  git clone git://git.clutter-project.org/bindings/pyclutter
  git clone git://git.clutter-project.org/bindings/pyclutter-gst

See clutter's git web interface at: http://git.clutter-project.org/

Building Git versions of Clutter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build the git versions of clutter, enter the directory containing the
downloaded software and execute::

  ./autogen.sh
  make
  sudo make install


Building Gyparody
-----------------

Gyparody can be executed from the directory in which it was
downloaded. However, it can also be installed into Python or build as a
Ubuntu/Debian .deb file for installation via dpkg/apt-get. We cover each method
in turn.

Executing Gyparody (in place)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To execute gyparody from a git checked out version first set your Python path
to the current working directory via::

  export PYTHONPATH=".:$PYTHONPATH"

Then run gyparody via::

  ./bin/gyparody

Installing into Python Path library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure that you have python setuptools installed. Then execute::

  python setup.py build
  sudo python setup.py install

Copy the ./bin/gyparody file to somewhere in your path aka::

  sudo cp bin/gyparody /usr/local/bin/

Installing via Ubuntu/Debian
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enter the directory containing the gyparody

Ubuntu users may elect to utilize Gyparody's build system for creating a .deb
file that can be installed by apt-get. To do this execute the following::

  dpkg-buildpackage -rfakeroot
  sudo dpkg -i ../gyparody_*_i386.deb



General Rules
=============

Game Board
----------

* 6 categories.
* 5 questions in each category.

* first round
    - $200
    - $400
    - $600
    - $800
    - $1000

* second round
    - $400
    - $800
    - $1200
    - $1600
    - $2000

* daily double hidden on board each round

* may wager no less than $5 on daily double
* if contestant has score less than highest dollar value in round then he/she
  can wager up to that top value. alternatively contestant can make it a true
  daily double and wager all of his/her score.

* must wait before host finishes reading the clue before ringing in

* ringing in before that point locks contestant out for two tenths of a second

* 5 seconds to offer a response

* first round allowed to not form in question
* second round much more strict

* player with lowest amount of money in first round chooses first question in
  second round.

* double gyparody has 2 daily doubles

* if contestant has less than $0 they cannot participate in final gyparody



Administering Gyparody Game
===========================

General Notes
-------------

Pressing 'f' on the keyboard will fullscreen the game board screen. Pressing
'f' again will unfullscreen the game board.

The host can press the 's' button on the keyboard at any time to display the
contestant scores. Pressing 's' again will remove the scores.

At the start of the round the host can press the 'l' key to begin displaying
category information full-screen. Pressing 'l' again will scroll the category
information leftwards displaying more category information. The idea is that
the host reads each category verbally to the audience in turn until all
categories have been read.


Gameplay of the round
---------------------

* During a round the host responds to contestants choosing a category and value
  of question by clicking on the appropriate square on the gameboard.

* After clicking a square the host reads the clue then presses the space bar.

* The contestants then have 10 seconds to buzz in their answer (via the arduino
  attached buzzers or by pressing the 'a', 'b', or 'c' buttons on the keyboard.

* If a contestant buzzes in to respond to the clue then they have 5 seconds to
* begin answering their clue. If a contestant begins answering the host presses
* the space bar.
  - If a contestant is correct the host presses 'y'.
  - If a contestant  is wrong the host presses 'n'.

* If a contestant answers the clue correctly then the new value of their score
  is displayed with the value of the clue added to their score. The game then
  displays the answer to the clue for the audience. Finally the game reverts
  back to the game board display so that the contestant that answered correctly
  can choose their next clue.

* If a contestant answers the clue wrong then the value of the clue is
  decremented from their score which is displayed on the screen. The game
  reverts back to a display of the clue and other contestants can buzz in to
  answer the clue (they have 10 seconds to do so). If no-one elects to buzz
  their buzzer then the game automatically displays the correct answer and
  reverts to the game board.


End of the round
----------------

* The round ends when all questions have been answered. If the ending round is
  round 1 then the game board immediately cycles over to displaying round 2. If
  this is the end of round 2 then the game cycles over to displaying final
  gyparody.



Credits / Attribution
=====================

./tests/test.jpg taken from:
http://www.flickr.com/photos/humboldthead/4536402090/

./tests/test.avi courtesy of 20th Century Fox:
http://www.google.com/search?q=20th+centruy+fox+intro&tbo=p&tbs=vid%3A1&source=vgc&hl=en&aq=f

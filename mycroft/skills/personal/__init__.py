# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'eward'

logger = getLogger(__name__)


class PersonalSkill(MycroftSkill):

    def __init__(self):
        super(PersonalSkill, self).__init__(name="PersonalSkill")

    def initialize(self):
        self.register_intent('personal.born.when.intent',
                             self.handle_when_were_you_born_intent)

        self.register_intent('personal.born.where.intent',
                             self.handle_where_were_you_born_intent)

        self.register_intent('personal.who.made.you.intent',
                             self.handle_who_made_you_intent)

        self.register_intent('personal.who.are.you.intent',
                             self.handle_who_are_you_intent)

        self.register_intent('personal.what.are.you.intent',
                             self.handle_what_are_you_intent)

    def handle_when_were_you_born_intent(self, message):
        self.speak_dialog("when.was.i.born")

    def handle_where_were_you_born_intent(self, message):
        self.speak_dialog("where.was.i.born")

    def handle_who_made_you_intent(self, message):
        self.speak_dialog("who.made.me")

    def handle_who_are_you_intent(self, message):
        self.speak_dialog("who.am.i")

    def handle_what_are_you_intent(self, message):
        self.speak_dialog("what.am.i")

    def stop(self):
        pass


def create_skill():
    return PersonalSkill()

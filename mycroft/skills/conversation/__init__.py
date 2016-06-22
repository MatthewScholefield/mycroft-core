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


import datetime
import glob
import json
import random
from random import Random, randint

import os
import time
from os.path import dirname, join

import tzlocal
from astral import Astral
from pytz import timezone

from adapt.intent import IntentBuilder

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'ryanleesipes'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# TODO - Localization
class ConversationSkill(MycroftSkill):
    def __init__(self):
        super(ConversationSkill, self).__init__(name="ConversationSkill")
    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', 'en-us'))

        commence_intent = IntentBuilder("ConversationCommenceIntent").require(
            "ConversationCommenceKeyword").build()
        ask_intent = IntentBuilder("ConversationAskIntent").require(
            "ConversationAskKeyword").build()

        self.register_intent(commence_intent, self.handle_commence_intent)
        self.register_intent(ask_intent, self.handle_ask_intent)
        self.tests = self.discover_tests()

    @staticmethod
    def discover_tests():
        tsts = {}
        skills = [
            skill for skill
            in glob.glob(os.path.join(PROJECT_ROOT, 'mycroft/skills/*'))
            if os.path.isdir(skill)
            ]

        for skill in skills:
            test_intent_files = [
                f for f
                in
                glob.glob(os.path.join(skill, 'test/intent/*.intent.json'))
                ]
            if len(test_intent_files) > 0:
                tsts[skill] = test_intent_files

        return tsts

    def get_rand_utterance(self):
        skill = self.tests.keys()[randint(0, len(self.tests.keys()) - 1)]
        test = self.tests[skill][randint(0, len(self.tests[skill]) - 1)]

        ex_json = json.load(open(test, 'r'))
        return ex_json.get('utterance')

    def respond(self):
        utt = self.get_rand_utterance()
        self.speak('hey my croft')
        self.speak(utt)
        self.emitter.emit(Message('ConversationSkill:ModeEnabled'))
        self.emitter.once('skill:complete', self.respond)

    def testing(self):
        getLogger().debug("AHFISAJK")

    def handle_commence_intent(self, message):
        self.speak('hey my croft')
        # self.speak('would you like to have a conversation with me')
        self.emitter.on('ConversationSkill:ModeEnabled', self.testing)
        self.emitter.emit(Message('ConversationSkill:ModeEnabled'))
        self.emitter.once('skill:complete', self.respond)

    def handle_ask_intent(self, message):
        self.speak('sure')
        self.respond()

    def stop(self):
        pass


def create_skill():
    return ConversationSkill()

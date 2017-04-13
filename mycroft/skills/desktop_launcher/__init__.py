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


import sys
import urllib2
import webbrowser

from adapt.intent import IntentBuilder
from adapt.tools.text.tokenizer import EnglishTokenizer
from os.path import dirname, join

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

logger = getLogger(__name__)
__author__ = 'seanfitz'

IFL_TEMPLATE = "http://www.google.com/search?&sourceid=navclient&btnI=I&q=%s"


class DesktopLauncherSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self, "DesktopLauncherSkill")
        self.apps = {}

    def initialize(self):
        try:
            import gio
        except:
            sys.path.append("/usr/lib/python2.7/dist-packages")
            try:
                import gio
            except:
                logger.error("Could not import gio")
                return

        tokenizer = EnglishTokenizer()

        app_names = []

        for app in gio.app_info_get_all():
            name = app.get_name().lower()

            self.apps[name] = app
            app_names.append(name)

            tokenized_name = tokenizer.tokenize(name)[0]
            if name != tokenized_name:
                app_names.append(tokenized_name)

        # TODO: self.add_capture(app_names)

        import os.path
        with open(os.path.join('intents','application.capture'), 'w') as file:
            for name in app_names:
                file.write(name + '\n')

        self.register_intent('launcher.launch.intent', self.handle_launch_desktop_app)
        self.register_intent('launcher.website.intent', self.handle_launch_website)
        self.register_intent('launcher.search.intent', self.handle_search_website)

    def handle_launch_desktop_app(self, message):
        app_name = message.data.get('application')
        apps = self.apps.get(app_name)
        if apps and len(apps) > 0:
            apps[0].launch()

    def handle_launch_website(self, message):
        site = message.data.get('website')
        webbrowser.open(IFL_TEMPLATE % (urllib2.quote(site)))

    def handle_search_website(self, message):
        site = message.data.get('website')
        search_terms = message.data.get('query')
        search_str = site + " " + search_terms
        webbrowser.open(IFL_TEMPLATE % (urllib2.quote(search_str)))

    def stop(self):
        pass


def create_skill():
    return DesktopLauncherSkill()

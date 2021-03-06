'''
PreseMT - A presentation software
================================
'''

import kivy
kivy.require('1.0.6')

from sys import argv
from os.path import join, expanduser, dirname
from shutil import rmtree
from kivy.utils import QueryDict
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

# even if it's not used in this current files
# behaviours are used into kv
import behaviours
import fbocapture


class PresemtApp(App):
    def __init__(self):
        super(PresemtApp, self).__init__()
        self.screens = {}

    def build_config(self, config):
        config.add_section('paths')
        try:
            import android
            user_dir = '/sdcard'
        except ImportError:
            user_dir = expanduser('~')
        config.set('paths', 'workspace', join(user_dir, 'Documents', 'PreseMT'))

    def show(self, name):
        '''Create and show a screen widget
        '''
        screens = self.screens
        modulename, clsname = name.split('.')
        if not name in screens:
            m = __import__('screens.%s' % modulename, fromlist=[modulename])
            cls = getattr(m, clsname)
            screens[name] = cls(app=self)
        screen = screens[name]
        self.root.clear_widgets()
        self.root.add_widget(screen)
        return screen

    def unload(self, name):
        if name in self.screens:
            del self.screens[name]

    def show_start(self):
        self.show('project.SelectorScreen')

    def delete_project(self, filename):
        if not filename.startswith(self.config.get('paths', 'workspace')):
            return False
        directory = dirname(filename)
        try:
            rmtree(directory, True)
        except OSError:
            return False
        return True

    def create_empty_project(self):
        '''Create and start an empty project
        '''
        self.unload('presentation.MainScreen')
        return self.show('presentation.MainScreen')

    def play_project(self, filename):
        project = self.create_empty_project()
        project.return_action = 'menu'
        project.filename = filename
        project.do_publish()

    def edit_project(self, filename=None):
        project = self.create_empty_project()
        if filename:
            project.filename = filename
        project.return_action = 'edit'
        project.do_edit()

    def build(self):
        self.root = FloatLayout()
        self.show('loading.LoadingScreen')
        Clock.schedule_once(self._async_load, .5)

    def _async_load(self, dt):
        # ... do loading here ^^
        if len(argv) > 1:
            self.edit_project(argv[1])
        else:
            self.show('project.SelectorScreen')

if __name__ in ('__main__', '__android__'):
    PresemtApp().run()

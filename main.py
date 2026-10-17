import sys

sys.dont_write_bytecode = True

import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv('API_URL'):
    print('[error] Env wajib belum diisi: API_URL')
    sys.exit(1)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivy.utils import platform
from libs.storage import get_token
from screens.home import HomeScreen
from screens.register import RegisterScreen
from screens.sign_in import SignInScreen
from screens.users import UsersScreen


class SkeletonApp(App):
    title = 'Kivy Skeleton'

    def build(self):
        if platform in ("win", "macosx", "linux"):
            Window.size = (400, 720)

        manager = ScreenManager(transition=NoTransition())
        manager.add_widget(SignInScreen(name='sign_in'))
        manager.add_widget(RegisterScreen(name='register'))
        manager.add_widget(HomeScreen(name='home'))
        manager.add_widget(UsersScreen(name='users'))
        return manager

    def on_start(self):
        self.root.current = 'home' if get_token() else 'sign_in'


if __name__ == '__main__':
    SkeletonApp().run()

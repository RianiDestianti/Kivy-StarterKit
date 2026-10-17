from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from components.loading import Loading
from components.ui import AppButton, AppInput  # daftarkan widget untuk KV
from libs.storage import remove_token
from libs.theme import colors
from store.controllers.auth_controller import get_profile
from store.slices.auth_slice import actions as auth_actions
from store.store import store

Builder.load_string('''
#:import colors libs.theme.colors

<HomeScreen>:
    canvas.before:
        Color:
            rgba: colors['background']
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: dp(24)
            spacing: dp(6)
            canvas.before:
                Color:
                    rgba: colors['card']
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(12)]
            Label:
                id: name
                text: '-'
                bold: True
                font_size: sp(20)
                color: colors['text']
                size_hint_y: None
                height: dp(30)
            Label:
                id: email
                text: '-'
                color: colors['muted']
                size_hint_y: None
                height: dp(22)
            Label:
                id: role
                text: '-'
                color: colors['text']
                size_hint_y: None
                height: dp(22)
            Label:
                id: verified
                text: '-'
                size_hint_y: None
                height: dp(22)
        AppButton:
            id: manage_users
            text: 'Manage Users'
            opacity: 0
            disabled: True
            on_release: root.manager.current = 'users'
        AppButton:
            text: 'Logout'
            variant: 'outline'
            on_release: root.logout()
        Widget:
''')


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading        = Loading()
        self.unsubscribe    = None

    def on_enter(self):
        self.unsubscribe = store.select(lambda state: state['auth'], self.render)
        store.dispatch(get_profile())

    def on_leave(self):
        if self.unsubscribe:
            self.unsubscribe()
        self.loading.set_visible(False)

    def logout(self):
        remove_token()
        store.dispatch(auth_actions['handle_logout']())
        self.manager.current = 'sign_in'

    def render(self, state_auth):
        self.loading.set_visible(state_auth['loading'])

        if state_auth['error_code'] in (401, 403):
            self.logout()
            return

        profile = state_auth['profile'] or {}
        is_admin = profile.get('role') == 'admin'

        self.ids.name.text      = profile.get('name') or '-'
        self.ids.email.text     = profile.get('email') or '-'
        self.ids.role.text      = profile.get('role') or '-'
        self.ids.verified.text  = 'verified' if profile.get('verified') else 'not verified'
        self.ids.verified.color = colors["success"] if profile.get("verified") else colors["danger"]

        self.ids.manage_users.opacity   = 1 if is_admin else 0
        self.ids.manage_users.disabled  = not is_admin

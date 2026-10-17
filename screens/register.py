from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from components.loading import Loading
from components.ui import AppButton, AppInput  # daftarkan widget untuk KV
from libs.general import first_error, handle_change_input
from libs.storage import set_token
from store.controllers.auth_controller import handle_action_register
from store.slices.auth_slice import actions as auth_actions
from store.store import store

Builder.load_string('''
#:import colors libs.theme.colors

<RegisterScreen>:
    canvas.before:
        Color:
            rgba: colors['background']
        Rectangle:
            pos: self.pos
            size: self.size
    AnchorLayout:
        padding: dp(16)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: dp(24)
            spacing: dp(12)
            canvas.before:
                Color:
                    rgba: colors['card']
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(12)]
            Label:
                text: 'Create Account'
                bold: True
                font_size: sp(20)
                color: colors['text']
                size_hint_y: None
                height: dp(40)
            Label:
                id: alert
                text: ''
                color: colors['danger']
                size_hint_y: None
                height: dp(24) if self.text else 0
            AppInput:
                id: name
                label: 'Name'
                required: True
                hint_text: 'Enter name'
                on_text: root.on_change('name', self.text)
            AppInput:
                id: email
                label: 'Email'
                required: True
                hint_text: 'Enter email'
                on_text: root.on_change('email', self.text)
            AppInput:
                id: password
                label: 'Password'
                required: True
                password: True
                hint_text: 'Minimum 6 characters'
                on_text: root.on_change('password', self.text)
                on_submit: root.handle_register()
            AppButton:
                text: 'REGISTER'
                on_release: root.handle_register()
            AppButton:
                text: 'Back to sign in'
                variant: 'outline'
                on_release: root.manager.current = 'sign_in'
''')


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading        = Loading()
        self.request        = { 'name': '', 'email': '', 'password': '' }
        self.unsubscribe    = None

    def on_change(self, name, value):
        handle_change_input(name, value, self.request)

    def on_enter(self):
        store.dispatch(auth_actions['handle_clean_response']())
        self.unsubscribe = store.select(lambda state: state['auth'], self.render)

    def on_leave(self):
        if self.unsubscribe:
            self.unsubscribe()
        self.loading.set_visible(False)

    def handle_register(self):
        store.dispatch(handle_action_register(dict(self.request)))

    def render(self, state_register):
        self.loading.set_visible(state_register['loading'])
        self.ids.alert.text     = state_register['error'] or ''

        for field in ('name', 'email', 'password'):
            self.ids[field].error = first_error(state_register['error_fields'], field)

        if state_register['response_register']:
            set_token(state_register['response_register']['key'])
            store.dispatch(auth_actions['handle_clean_response']())
            self.manager.current = 'home'

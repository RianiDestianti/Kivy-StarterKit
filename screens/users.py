from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from components.loading import Loading
from components.ui import AppButton, AppInput  # daftarkan widget untuk KV
from store.controllers.user_controller import delete_user, get_list_user
from store.slices.user_slice import actions as user_actions
from store.store import store

Builder.load_string('''
#:import colors libs.theme.colors

<UserRow>:
    size_hint_y: None
    height: dp(64)
    padding: dp(12)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: colors['card']
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.user.get('name', '')
            bold: True
            color: colors['text']
            text_size: self.size
            halign: 'left'
        Label:
            text: '{}  |  {}'.format(root.user.get('email', ''), root.user.get('role', ''))
            color: colors['muted']
            font_size: sp(12)
            text_size: self.size
            halign: 'left'
    AppButton:
        text: 'Delete'
        variant: 'danger'
        size_hint_x: None
        width: dp(80)
        on_release: root.screen.handle_delete_data(root.user)

<UsersScreen>:
    canvas.before:
        Color:
            rgba: colors['background']
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(12)
            AppButton:
                text: 'Back'
                variant: 'outline'
                size_hint_x: None
                width: dp(80)
                on_release: root.manager.current = 'home'
            Label:
                id: title
                text: 'Users (0)'
                bold: True
                font_size: sp(18)
                color: colors['text']
                text_size: self.size
                halign: 'left'
                valign: 'middle'
        AppInput:
            id: keyword
            hint_text: 'Search name, email, phone (Enter)'
            on_submit: root.handle_search()
        Label:
            id: error
            text: ''
            color: colors['danger']
            size_hint_y: None
            height: dp(20) if self.text else 0
        ScrollView:
            GridLayout:
                id: list
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(12)
            AppButton:
                id: previous
                text: 'Previous'
                variant: 'outline'
                on_release: root.handle_change_page(root.page - 1)
            Label:
                id: page_text
                text: '1 / 1'
                color: colors['text']
            AppButton:
                id: next
                text: 'Next'
                variant: 'outline'
                on_release: root.handle_change_page(root.page + 1)
''')


class UserRow(BoxLayout):
    user = DictProperty({})

    def __init__(self, screen, **kwargs):
        self.screen = screen
        super().__init__(**kwargs)


class UsersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading        = Loading()
        self.page           = 1
        self.unsubscribe    = None

    def on_enter(self):
        self.unsubscribe = store.select(lambda state: state['user'], self.render)
        self.load_data(1)

    def on_leave(self):
        if self.unsubscribe:
            self.unsubscribe()
        self.loading.set_visible(False)

    def load_data(self, target_page):
        store.dispatch(get_list_user({ 'keyword': self.ids.keyword.text, 'page': target_page }))

    def handle_search(self):
        self.page = 1
        self.load_data(1)

    def handle_change_page(self, target_page):
        self.page = target_page
        self.load_data(target_page)

    def handle_delete_data(self, user):
        store.dispatch(delete_user(user['id']))

    def render(self, state_user):
        self.loading.set_visible(state_user['loading'])

        total_pages             = max(state_user['total']['pages'], 1)
        self.ids.title.text     = f"Users ({state_user['total']['data']})"
        self.ids.error.text     = state_user['error'] or ''
        self.ids.page_text.text = f"{self.page} / {total_pages}"
        self.ids.previous.disabled  = self.page <= 1
        self.ids.next.disabled      = self.page >= state_user['total']['pages']

        self.ids.list.clear_widgets()
        for user in state_user['users']:
            self.ids.list.add_widget(UserRow(screen=self, user=user))

        if state_user['response']['delete']:
            store.dispatch(user_actions['reset_response']())

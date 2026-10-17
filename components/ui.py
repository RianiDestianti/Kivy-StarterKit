from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string('''
#:import colors libs.theme.colors

<AppButton>:
    size_hint_y: None
    height: dp(44)
    background_normal: ''
    background_down: ''
    background_color: colors['danger'] if self.variant == 'danger' else (colors['card'] if self.variant == 'outline' else colors['primary'])
    color: colors['primary'] if self.variant == 'outline' else colors['primary_text']
    bold: True
    opacity: 0.5 if self.disabled else 1
    canvas.after:
        Color:
            rgba: colors['primary'] if self.variant == 'outline' else (0, 0, 0, 0)
        Line:
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(8)

<AppInput>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    spacing: dp(4)
    Label:
        text: root.label + ('[color=e53e3e]*[/color]' if root.required else '')
        markup: True
        bold: True
        color: colors['text']
        size_hint_y: None
        height: dp(20) if root.label else 0
        opacity: 1 if root.label else 0
        text_size: self.size
        halign: 'left'
    TextInput:
        id: field
        text: root.text
        hint_text: root.hint_text
        password: root.password
        multiline: False
        write_tab: False
        size_hint_y: None
        height: dp(42)
        padding: dp(10), dp(11)
        on_text: root.text = self.text
        on_text_validate: root.dispatch('on_submit')
    Label:
        text: root.error
        color: colors['danger']
        font_size: sp(12)
        size_hint_y: None
        height: dp(16) if root.error else 0
        text_size: self.size
        halign: 'left'
''')


class AppButton(Button):
    variant = StringProperty('primary')


class AppInput(BoxLayout):
    label       = StringProperty('')
    text        = StringProperty('')
    hint_text   = StringProperty('')
    error       = StringProperty('')
    password    = BooleanProperty(False)
    required    = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_submit')
        super().__init__(**kwargs)

    def on_submit(self):
        pass

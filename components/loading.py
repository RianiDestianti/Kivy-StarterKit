from kivy.lang import Builder
from kivy.uix.modalview import ModalView

Builder.load_string('''
#:import colors libs.theme.colors

<Loading>:
    auto_dismiss: False
    size_hint: None, None
    size: dp(160), dp(80)
    background_color: 0, 0, 0, 0.25
    Label:
        text: 'Loading...'
        color: colors['primary']
        canvas.before:
            Color:
                rgba: colors['card']
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(12)]
''')


class Loading(ModalView):
    def set_visible(self, visible):
        if visible and not self._window:
            self.open(animation=False)
        elif not visible and self._window:
            self.dismiss(animation=False)

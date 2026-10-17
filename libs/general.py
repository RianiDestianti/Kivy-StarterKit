def handle_change_input(name, value, request):
    """Versi Kivy dari handleChangeInput: simpan nilai TextInput ke dict request."""
    request[name] = value


def first_error(error_fields, field):
    if not error_fields:
        return ''
    return (error_fields.get(field) or [''])[0]

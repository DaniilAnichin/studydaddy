from flask_wtf import Form, form
from wtforms import fields


__all__ = (
    'DataForm',
    'OpenTestForm',
    'SimpleTestForm',
    'ComplexTestForm',
)


class DataForm(Form):
    pass


class OpenTestForm(Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def __init__(self, formdata=form._Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, answer=None, *args, **kwargs):
        super().__init__(
            formdata=formdata,
            obj=obj,
            prefix=prefix,
            csrf_context=csrf_context,
            secret_key=secret_key,
            csrf_enabled=csrf_enabled,
            *args,
            **kwargs,
        )


class SimpleTestForm(Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def __init__(self, formdata=form._Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, answer=None, *args, **kwargs):
        super().__init__(
            formdata=formdata,
            obj=obj,
            prefix=prefix,
            csrf_context=csrf_context,
            secret_key=secret_key,
            csrf_enabled=csrf_enabled,
            *args,
            **kwargs,
        )


class ComplexTestForm(Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def __init__(self, formdata=form._Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, answer=None, *args, **kwargs):
        super().__init__(
            formdata=formdata,
            obj=obj,
            prefix=prefix,
            csrf_context=csrf_context,
            secret_key=secret_key,
            csrf_enabled=csrf_enabled,
            *args,
            **kwargs,
        )

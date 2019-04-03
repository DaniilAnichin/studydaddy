from flask_wtf import Form, form
from wtforms import fields
from werkzeug.datastructures import OrderedMultiDict

__all__ = (
    'DataForm',
    'OpenTestForm',
    'SimpleTestForm',
    'ComplexTestForm',
)


class DataForm(Form):
    pass


class BaseTestFormMixing:
    def __init__(self, formdata=form._Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, answer=None, *args, **kwargs):
        if answer and isinstance(formdata, dict) and not formdata:
            formdata = OrderedMultiDict(formdata)
            formdata.update(self.from_answer(answer))
        print(formdata)
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

    def from_answer(self, answer):
        raise NotImplementedError

    def get_answer(self):
        raise NotImplementedError


class OpenTestForm(BaseTestFormMixing, Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def from_answer(self, answer):
        return {'answer': answer.answer}

    def get_answer(self):
        return self.answer.data


class SimpleTestForm(BaseTestFormMixing, Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def from_answer(self, answer):
        raise NotImplementedError

    def get_answer(self):
        raise NotImplementedError


class ComplexTestForm(BaseTestFormMixing, Form):
    answer = fields.TextAreaField(label='Відповідь: ')
    confirm = fields.SubmitField(label='Зберігти')

    def from_answer(self, answer):
        raise NotImplementedError

    def get_answer(self):
        raise NotImplementedError


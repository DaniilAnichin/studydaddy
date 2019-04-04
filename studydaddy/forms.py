from random import shuffle

from flask_wtf import Form, form
from wtforms import fields, widgets
from studydaddy.models import SEPARATOR


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
                 secret_key=None, csrf_enabled=None, item=None, answer=None, *args, **kwargs):
        self._item = item
        self._answer = answer
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
        if item:
            self.from_item(item)
        if answer and isinstance(formdata, dict) and not formdata:
            self.from_answer(answer)

    def from_item(self, item):
        raise NotImplementedError

    def from_answer(self, answer):
        raise NotImplementedError

    def get_answer(self):
        raise NotImplementedError


class OpenTestForm(BaseTestFormMixing, Form):
    answer = fields.TextAreaField(label='Ответ: ')
    confirm = fields.SubmitField(label='Сохранить')

    def from_item(self, item):
        pass

    def from_answer(self, answer):
        self.answer.data = answer.answer

    def get_answer(self):
        return self.answer.data


class SimpleTestForm(BaseTestFormMixing, Form):
    answers = fields.RadioField(label='Ответ: ')
    confirm = fields.SubmitField(label='Сохранить')

    def from_item(self, item):
        self.answers.choices = item.content.get_options
        shuffle(self.answers.choices)

    def from_answer(self, answer):
        for i, title in self._item.content.get_options:
            if answer.answer == title:
                self.answers.data = str(i)
                self.answers.raw_data = [str(i)]
                return

    def get_answer(self):
        for i, title, selected in self.answers.iter_choices():
            if selected:
                return title


class MultiCheckboxField(fields.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ComplexTestForm(BaseTestFormMixing, Form):
    answers = MultiCheckboxField(label='Ответы (выберите несколько): ')
    confirm = fields.SubmitField(label='Сохранить')

    def from_item(self, item):
        self.answers.choices = item.content.get_options
        shuffle(self.answers.choices)

    def from_answer(self, answer):
        results = [str(i) for i, title in self._item.content.get_options if title in answer.answer.split(SEPARATOR)]
        self.answers.data = results
        self.answers.raw_data = results

    def get_answer(self):
        results = [title for i, title, selected in self.answers.iter_choices() if selected]
        return SEPARATOR.join(results)

from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_nav.elements import Navbar, View

from .admin_views import SUCCESS
from .forms import *
from .setup import app, db, nav, admin
from .models import *

studydaddy = Blueprint('studydaddy', __name__)

nav.register_element(
    'frontend_top',
    Navbar(
        View('StudyDaddy', '.index'),
        View('Старт', '.index'),
        View('Тести', '.tests'),
        View('Оцінки', '.marks'),
    )
)

TEMPLATES = {
    'data': 'data.html',
    'open_test': 'open_test.html',
    'simple_test': 'simple_test.html',
    'complex_test': 'complex_test.html',
}
FORMS = {
    'data': DataForm,
    'open_test': OpenTestForm,
    'simple_test': SimpleTestForm,
    'complex_test': ComplexTestForm,
}


@app.route('/')
def index():
    root_item = Item.query.filter_by(root=True).first()
    return redirect(url_for('get_item', item_id=root_item.id))


@app.route('/item/<item_id>/', methods=['GET', 'POST'])
def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()

    if item.item_type == 'marks':
        # NOTICE Collecting marks
        template = TEMPLATES['data']
        form = FORMS['data']()
        content = item.data or Data(item=item)
        content.topic = 'Оцінки'
        content.content = get_marks()
        db.session.add(content)
        db.session.commit()

        return render_template(
            template,
            item=item,
            content=content,
            form=form,
        )

    content = item.content
    if not content:
        raise ValueError

    template = TEMPLATES[item.item_type]
    form = FORMS[item.item_type](request.form, item=item, answer=item.answer)
    if request.method == 'POST':
        # NOTICE Submitting answer
        answer = item.answer or Answer(item=item)
        answer.answer = form.get_answer()
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('get_item', item_id=item.next_item_id))

    return render_template(
        template,
        item=item,
        content=content,
        form=form,
    )


@app.route('/tests/')
def tests():
    test_item = Item.query.filter_by(item_type='simple_test').first()
    return redirect(url_for('get_item', item_id=test_item.id))


@app.route('/marks/')
def marks():
    finish_item = Item.query.filter_by(item_type='marks').first()
    return redirect(url_for('get_item', item_id=finish_item.id))


if __name__ == '__main__':
    # FLASK_DEBUG=1 FLASK_APP=studydaddy.app flask run
    app.run()

from datetime import datetime

from flask import Blueprint, render_template, request, redirect
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
        View('Оцінки', '.marks'),
    )
)

TEMPLATES = {
    Data: 'data.html',
    OpenTest: 'open_test.html',
    SimpleTest: 'simple_test.html',
    ComplexTest: 'complex_test.html',
}
FORMS = {
    Data: DataForm,
    OpenTest: OpenTestForm,
    SimpleTest: SimpleTestForm,
    ComplexTest: ComplexTestForm,
}


@app.route('/')
def index():
    root_item = Item.query.filter_by(root=True).first()
    return redirect(f'/item/{root_item.id}/')


@app.route('/marks/')
def marks():
    finish_item = Item.query.filter_by(next_item_id=None).first()
    return redirect(f'/item/{finish_item.id}/')


@app.route('/item/<item_id>/', methods=['GET', 'POST'])
def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()

    content = item.content
    if not content:
        raise ValueError

    content_type = type(content)
    template = TEMPLATES[content_type]
    form = FORMS[content_type](request.form, answer=item.answer)

    return render_template(
        template,
        item=item,
        content=content,
        form=form,
    )


@app.route('/mark-names/', methods=['GET', 'POST'])
def mark_names():
    """mark_name for marks for students by name for semester by date start < now < end"""
    form = StudentForm(request.form)
    context = {'form': form}
    if request.method == 'POST':
        now = datetime.now()
        items = SMark.query.join(
            StudentMarks,
            Student,
            TeachPlan,
            Semester
        ).filter(
            Semester.teach_begin_date < now,
            Semester.teach_end_date > now,
            Student.book_no.ilike(f'%{form.student_book_no.data}%')
        ).all()
        context['table'] = MarkTable(items, classes=['darkTable'])
    return render_template('mark_names.html', **context)


@app.route('/cafedras/', methods=['GET', 'POST'])
def cafedras():
    """cafedra by student group / speciality"""
    form = GroupSpecialityForm(request.form)
    context = {'form': form}
    if request.method == 'POST':
        query = Cafedra.query.outerjoin(
            Speciality,
            Group,
            StudentGroup,
            Student,
        )
        if form.student_book_no.data:
            query = query.filter(Student.book_no.ilike(f'%{form.student_book_no.data}%'))
        if form.group_code.data:
            query = query.filter(Group.group_code.ilike(f'%{form.group_code.data}%'))
        if form.speciality_name.data:
            query = query.filter(Speciality.speciality_name.ilike(f'%{form.speciality_name.data}%'))
        if form.speciality_shifr.data:
            query = query.filter(Speciality.speciality_shifr.ilike(f'%{form.speciality_shifr.data}%'))

        items = query.all()

        context['table'] = CafedraTable(items, classes=['darkTable'])

    return render_template('cafedras.html', **context)


@app.route('/violations/', methods=['GET', 'POST'])
def violations():
    """violation type, punish_kind by student"""
    form = PersonForm(request.form)
    context = {'form': form}
    if request.method == 'POST':
        query = Violation.query.join(
            Person,
        )
        if form.student_name.data:
            query = query.filter(Person.name.ilike(f'%{form.student_name.data}%'))
        if form.student_surname.data:
            query = query.filter(Person.surname.ilike(f'%{form.student_surname.data}%'))
        if form.student_patronymic.data:
            query = query.filter(Person.patronymic.ilike(f'%{form.student_patronymic.data}%'))

        items = query.all()
        context['table'] = ViolationTable(items, classes=['darkTable'])
    return render_template('violations.html', **context)


@app.route('/orders/', methods=['GET', 'POST'])
def orders():
    """order by order type, student"""
    form = OrderForm(request.form)
    context = {'form': form}
    if request.method == 'POST':
        query = Order.query.join(
            Violation,
            Person,
            SOrderKind
        ).filter(
            SOrderKind.order_kind_name.ilike(f'%{form.order_kind.data}%')
        )
        if form.student_name.data:
            query = query.filter(Person.name.ilike(f'%{form.student_name.data}%'))
        if form.student_surname.data:
            query = query.filter(Person.surname.ilike(f'%{form.student_surname.data}%'))
        if form.student_patronymic.data:
            query = query.filter(Person.patronymic.ilike(f'%{form.student_patronymic.data}%'))

        items = query.all()
        context['table'] = OrderTable(items, classes=['darkTable'])
    return render_template('orders.html', **context)


if __name__ == '__main__':
    # FLASK_DEBUG=1 FLASK_APP=studydaddy.app flask run
    app.run()

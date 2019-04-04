from werkzeug.utils import cached_property

from .setup import db


__all__ = (
    'Item',
    'Answer',
    'Data',
    'OpenTest',
    'SimpleTest',
    'ComplexTest',

    'SEPARATOR',
    'get_marks',
)


SEPARATOR = ';|;'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    next_item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True, unique=True)

    next_item = db.relationship(
        'Item',
        remote_side=[id],
        foreign_keys=[next_item_id],
        backref=db.backref('prev_item', uselist=False)
    )

    root = db.Column(db.Boolean(), default=False)
    item_type = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'Item #{self.id} ({self.item_type})'

    @property
    def content(self):
        return getattr(self, self.item_type, None)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, unique=True)
    item = db.relationship('Item', backref=db.backref('data', uselist=False))

    topic = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'Data "{self.topic}"'


class SimpleTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, unique=True)
    item = db.relationship('Item', backref=db.backref('simple_test', uselist=False))

    topic = db.Column(db.String(250), nullable=False)
    options = db.Column(db.Text(), nullable=False)
    correct = db.Column(db.Text(), nullable=False)

    translate = 'Тест первого уровня'

    def __repr__(self):
        return f'SimpleTest "{self.topic}"'

    @cached_property
    def get_options(self):
        return list(enumerate(self.options.split(SEPARATOR)))

    @cached_property
    def get_correct(self):
        return self.correct.split(SEPARATOR)[0]

    def get_mark(self) -> float:
        return float(bool(self.item.answer and self.item.answer.answer == self.correct))


class ComplexTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, unique=True)
    item = db.relationship('Item', backref=db.backref('complex_test', uselist=False))

    topic = db.Column(db.String(250), nullable=False)
    options = db.Column(db.Text(), nullable=False)
    correct = db.Column(db.Text(), nullable=False)

    translate = 'Тест второго уровня'

    def __repr__(self):
        return f'ComplexTest "{self.topic}"'

    @cached_property
    def get_options(self):
        return list(enumerate(self.options.split(SEPARATOR)))

    @cached_property
    def get_correct(self):
        return set(self.correct.split(SEPARATOR))

    def get_mark(self) -> float:
        if not self.item.answer:
            return 0

        options = set(self.item.answer.answer.split(SEPARATOR))
        if options == self.get_correct:
            return 1
        elif options & self.get_correct:
            return len(options & self.get_correct) / len(self.get_correct)
        return 0


class OpenTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, unique=True)
    item = db.relationship('Item', backref=db.backref('open_test', uselist=False))

    topic = db.Column(db.String(250), nullable=False)
    correct = db.Column(db.Text(), nullable=False)

    translate = 'Открытый вопрос'

    def __repr__(self):
        return f'OpenTest "{self.topic}"'

    @cached_property
    def get_correct(self):
        return set(self.correct.split(SEPARATOR))

    def get_mark(self) -> float:
        if not self.item.answer:
            return 0
        options = set(self.item.answer.answer.split(SEPARATOR))
        if options == self.get_correct:
            return 1
        elif options & self.get_correct:
            return len(options & self.get_correct) / len(self.get_correct)
        return 0


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False, unique=True)
    item = db.relationship('Item', backref=db.backref('answer', uselist=False))
    # user_id = ...
    # user = ...

    answer = db.Column(db.Text(), nullable=False)


def get_marks():
    results = []
    points = 0
    total = 0
    open_tests_1 = OpenTest.query.filter(OpenTest.id.in_(range(1, 20)))
    open_tests_2 = OpenTest.query.filter(OpenTest.id.in_(range(20, 38)))
    simple_tests = SimpleTest.query
    complex_tests = ComplexTest.query
    for test in open_tests_1:
        mul = 5
        mark = int(test.get_mark() * mul)
        points += mark
        total += mul
        results.append(
            f'{test.translate} первого уровня ({test.topic[:30]}...): {mark} / {mul}'
        )
    results.append('')
    for test in open_tests_2:
        mul = 10
        mark = int(test.get_mark() * mul)
        points += mark
        total += mul
        results.append(
            f'{test.translate} второго уровня ({test.topic[:30]}...): {mark} / {mul}'
        )
    results.append('')
    for test in simple_tests:
        mul = 5
        mark = int(test.get_mark() * mul)
        points += mark
        total += mul
        results.append(
            f'{test.translate} ({test.topic[:30]}...): {mark} / {mul}'
        )
    results.append('')
    for test in complex_tests:
        mul = 10
        mark = int(test.get_mark() * mul)
        points += mark
        total += mul
        results.append(
            f'{test.translate} ({test.topic[:30]}...): {mark} / {mul}'
        )

    results.append(
        f'Всего: {points} / {total} ({int(points * 100 / total)}%)'
    )

    return '<br>'.join(results)

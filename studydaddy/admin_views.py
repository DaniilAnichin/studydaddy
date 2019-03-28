from flask_admin.contrib.sqla import ModelView

from .setup import admin, db
from .models import *


admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Data, db.session))
admin.add_view(ModelView(SimpleTest, db.session))
admin.add_view(ModelView(ComplexTest, db.session))
admin.add_view(ModelView(OpenTest, db.session))


SUCCESS = True

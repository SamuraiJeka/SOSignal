from sqladmin import ModelView

from models import (
    Admin,
    User,
    Stuff,
    Order,
    Group
)


class AdminView(ModelView, model=Admin):
    form_include_pk = True
    form_excluded_columns = [Admin.id]

    column_list = [Admin.id, Admin.name]
    column_searchable_list = [Admin.id, Admin.name]


class UserView(ModelView, model=User):
    form_include_pk = True
    form_excluded_columns = [User.id]

    column_list = [User.id, User.email, User.full_name, User.problem_type]
    column_searchable_list = [User.id, User.full_name, User.email]


class StuffView(ModelView, model=Stuff):
    form_include_pk = True
    form_excluded_columns = [Stuff.id]

    column_list = [Stuff.id, Stuff.email, Stuff.full_name,]
    column_searchable_list = [Stuff.id, Stuff.full_name, Stuff.email]


class OrderView(ModelView, model=Order):
    form_include_pk = True
    form_excluded_columns = [Order.id]

    column_list = [Order.id, Order.baggage, Order.order_date, Order.start_time, Order.finish_time]
    column_searchable_list = [Order.id, Order.baggage, Order.order_date]


class GroupView(ModelView, model=Group):
    form_include_pk = True
    form_excluded_columns = [Group.id]

    column_list = [Group.id, Group.order_id, Group.stuff_id]
    column_searchable_list = [Group.id, Group.order_id, Group.stuff_id]

# -*- coding: utf-8 -*-
from . import views
from flask import Blueprint, current_app
from sqlalchemy.engine.reflection import Inspector

blueprint = Blueprint(
    'pdfhook', __name__,
)

@blueprint.before_app_first_request
def make_sure_there_is_a_working_database(*args, **kwargs):
    if current_app.config.get('ENV') != 'dev':
        return
    inspector = Inspector.from_engine(db.engine)
    tables = inspector.get_table_names()
    required_tables = [models.PDFForm.__tablename__]
    if not (set(required_tables) < set(tables)):
        current_app.logger.warning(
            "database tables {} not found. Creating tables".format(required_tables))
        db.create_all()

# -*- coding: utf-8 -*-
from . import views
from .views import PDFFormAPI
from flask import Blueprint

blueprint = Blueprint(
    'pdfhook', __name__,
)

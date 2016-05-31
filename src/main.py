import os
from flask import Flask
from src.extensions import db, ma
from src.context_processors import inject_static_url
from src.logs import register_logging
from src.pdfhook import blueprint
from src.pdfhook import PDFFormAPI
from flask import jsonify, make_response
from flask import render_template
from flask import request
from flask import url_for

def create_app():
    config = os.environ.get('CONFIG', 'src.settings.DevConfig')
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_api(app)
    register_blueprints(app)
    register_context_processors(app)
    register_logging(app, config)
    # If the app is running on Heroku, use SSLify
    if 'DYNO' in os.environ:
        from flask_sslify import SSLify
        SSLify(app)
    return app

def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)

def register_api(app):
    form_view = PDFFormAPI.as_view('form_api')
    app.add_url_rule('/', defaults={'pdf_id': None}, view_func=form_view, methods=['GET',])
    app.add_url_rule('/', defaults={'pdf_id': None}, view_func=form_view, methods=['POST',])
    app.add_url_rule('/<int:pdf_id>', view_func=form_view, methods=['GET', 'POST', 'PUT', 'DELETE'])

def register_blueprints(app):
    app.register_blueprint(blueprint)

def register_context_processors(app):
    app.context_processor(inject_static_url)


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=int(os.environ.get('PORT', 9000)))

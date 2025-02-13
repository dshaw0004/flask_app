import os
from .app import app, db, envs
from flask import render_template, request, jsonify
from .models import AppInfo
from .src.ai.gemini import gemini_generate_content
from sqlalchemy.exc import OperationalError, PendingRollbackError

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/apps', methods=['GET'])
def get_apps():
    def inner():
        apps = AppInfo.query.all()
        return apps
    for _ in (1, 2, 3):
        try:
            apps = inner()
            return jsonify([appli.as_dict() for appli in apps])
        except OperationalError:
            pass
        except PendingRollbackError:
            db.session.rollback()
            db.session.commit()
    return "<h1>Unable to provide the data, please try again later or contact the admin</h1>", 500

@app.route('/apps', methods=['POST'])
def add_app():
    data = request.get_json()

    name = data['name']
    description = data.get('description', '')
    app_link = data['appLink']
    platform = data['platform']
    thumbnail = data.get('thumbnail', '')
    version = data.get('version')

    author = 'dshaw0004'

    new_app = AppInfo(
            name=name, description=description,
            platform=platform, version=version,
            download_link=app_link, thumbnail=thumbnail,
            author=author
            )
    for _ in (1, 2, 3):
        try:
            db.session.add(new_app)
            db.session.commit()
            return jsonify(new_app.as_dict()), 201
        except OperationalError:
            pass
        except PendingRollbackError:
            db.session.rollback()
            db.session.commit()
    return "<h1>Somethng went wrong at the server, please try again later</h1>", 500



@app.route('/apps/<app_id>', methods=['PUT'])
def update_app(app_id):
    data = request.get_json()
    # print(data)
    app_info = None
    def inner():
        application = AppInfo.query.get(app_id)
        return application
    for _ in (1, 2, 3):
        try:
            app_info = inner()
        except OperationalError:
            pass
        except PendingRollbackError:
            db.session.rollback()
            db.session.commit()
    if app_info is None:
        return jsonify({"error": "App not found"}), 404

    if data.get('version') is not None:
        app_info.version = data['version']
    if data.get('appLink') is not None:
        app_info.download_link = data['appLink']
    if data.get('description') is not None:
        app_info.description = data.get('description')
    db.session.commit()
    return jsonify(app_info.as_dict())

@app.route('/apps/<app_id>', methods=['DELETE'])
def delete_app(app_id):
    selected_app = None
    def inner():
        app_info = AppInfo.query.get(app_id)
        return app_info
    for _ in (1, 2, 3):
        try:
            selected_app = inner()
            db.session.delete(selected_app)
            db.session.commit()
            return '', 204
        except OperationalError:
            pass
        except PendingRollbackError:
            db.session.rollback()
            db.session.commit()
    # if selected_app is None:
    return jsonify({"error": "App not found"}), 404

@app.route('/ai-response', methods=['POST'])
def ai_response():
    # TODO: Need to apply rate limiting in case it get compromised [ use Flask-Limiter ]
    access_token = request.headers.get('AI-ACCESS-TOKEN') # This should not be same as gemini api key
    saved_access_token = envs.get('AI_ACCESS_TOKEN')
    if access_token is None or access_token != saved_access_token:
        return 'You are not authorized to access this endpoint', 401
    data = request.get_json()
    prompt: str = data.get('prompt')
    if not prompt:
        return 'Please provide a prompt', 400
    content = gemini_generate_content(prompt=prompt)
    return content


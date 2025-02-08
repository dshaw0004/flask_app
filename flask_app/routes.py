import os
from .app import app, db
from flask import render_template, request, jsonify
from .models import AppInfo
from .src.ai.gemini import gemini_generate_content

@app.route('/')
def index():
    return 'Hi, I am Dipankar Shaw'

@app.route('/apps', methods=['GET'])
def get_apps():
    apps = AppInfo.query.all()
    return jsonify([appli.as_dict() for appli in apps])

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

    db.session.add(new_app)
    db.session.commit()

    return jsonify(new_app.as_dict()), 201

@app.route('/apps/<app_id>', methods=['PUT'])
def update_app(app_id):
    data = request.json
    print(data)
    app_info = AppInfo.query.get(app_id)
    if app_info is None:
        return jsonify({"error": "App not found"}), 404

    if 'version' in data:
        app_info.version = data['version']
    if 'appLink' in data:
        app_info.download_link = data['appLink']
    db.session.commit()
    return jsonify(app_info.as_dict())

@app.route('/apps/<app_id>', methods=['DELETE'])
def delete_app(app_id):
    app_info = AppInfo.query.get(app_id)
    if app_info is None:
        return jsonify({"error": "App not found"}), 404

    db.session.delete(app_info)
    db.session.commit()
    return '', 204

@app.route('/ai-response/<prompt>')
def ai_response(prompt: str):
    # TODO: Need to apply rate limiting in case it get compromised [ use Flask-Limiter ]
    access_token = request.headers.get('AI_ACCESS_TOKEN') # This should not be same as gemini api key
    saved_access_token = os.getenv('AI_ACCESS_TOKEN')
    if access_token is None or access_token != saved_access_token:
        return 'You are not authorized to access this endpoint', 401
    content = gemini_generate_content(prompt=prompt)
    return content
    

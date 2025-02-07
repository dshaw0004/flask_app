from .app import app, db
from flask import render_template, request, jsonify
from .models import AppInfo

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


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data['email']
#     password = data['password']

#     user = User.query.filter_by(email=email).first()

#     if user and user.check_password(password):
#         return user.id, 200
#     else:
#         return jsonify({'message': 'Invalid email or password'}), 401

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user_info(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'}), 404

#     friends = Friend.query.filter((Friend.user_id == user_id) | (Friend.friend_id == user_id)).all()
#     friends_info = []
#     for friend in friends:
#         friend_id = friend.friend_id if friend.user_id == user_id else friend.user_id
#         friend_user = User.query.get(friend_id)
#         friends_info.append({'id': friend_user.id, 'name': friend_user.name})

#     user_info = {
#         'id': user.id,
#         'name': user.name,
#         'friends': friends_info
#     }

#     return jsonify(user_info), 200

# @app.route('/messages/<int:user1_id>/<int:user2_id>', methods=['GET'])
# def get_messages(user1_id, user2_id):
#     messages = Chat.query.filter(
#         ((Chat.sender_id == user1_id) & (Chat.receiver_id == user2_id)) |
#         ((Chat.sender_id == user2_id) & (Chat.receiver_id == user1_id))
#     ).all()

#     messages_info = []
#     for message in messages:
#         messages_info.append({
#             'sender_id': message.sender_id,
#             'receiver_id': message.receiver_id,
#             'message': message.message
#         })

#     return jsonify(messages_info), 200


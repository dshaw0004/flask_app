from app import app, socketio
from app import db
import routes

if '__main__' == __name__:
    with app.app_context():
        db.create_all()
        socketio.run(app, debug=True, port=8080, allow_unsafe_werkzeug=True)
    # app.run(host='0.0.0.0', debug=True)
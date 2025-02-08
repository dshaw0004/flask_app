from flask_app.app import app


def get_app():
    with app.app_context():
        from flask_app.app import db
        from flask_app import routes
        db.create_all()
    return app


if '__main__' == __name__:
    application = get_app()
    application.run(debug=True, port=7069, host='0.0.0.0')

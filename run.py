from flask_app.app import app


if '__main__' == __name__:
    with app.app_context():
        from flask_app.app import db
        from flask_app import routes
        db.create_all()
    app.run(debug=True)


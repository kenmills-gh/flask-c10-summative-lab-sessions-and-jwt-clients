from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, bcrypt, User, Note

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_super_secret_key_here"  # Change in production

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# --- AUTHENTICATION ROUTES ---


class Signup(Resource):
    def post(self):
        data = request.get_json()

        # Validate password confirmation matches frontend payload
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            return {"error": "Passwords do not match"}, 400

        if User.query.filter_by(username=data.get("username")).first():
            return {"error": "Username already exists"}, 400

        try:
            new_user = User(username=data.get("username"))
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()

            # Log the user in by setting the session
            session["user_id"] = new_user.id
            return new_user.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 422


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get("username")).first()

        if user and user.authenticate(data.get("password")):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.to_dict(), 200

        # Return an empty object if not logged in as expected by the frontend
        return {}, 401


# --- RESOURCE ROUTES (NOTES) ---


class NoteList(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        notes_paginated = Note.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page
        )

        return {
            "notes": [note.to_dict() for note in notes_paginated.items],
            "total": notes_paginated.total,
            "pages": notes_paginated.pages,
            "current_page": notes_paginated.page,
        }, 200

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        new_note = Note(
            title=data.get("title"), content=data.get("content"), user_id=user_id
        )
        db.session.add(new_note)
        db.session.commit()
        return new_note.to_dict(), 201


class NoteResource(Resource):
    def patch(self, id):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return {"error": "Note not found or unauthorized"}, 404

        data = request.get_json()
        if "title" in data:
            note.title = data["title"]
        if "content" in data:
            note.content = data["content"]

        db.session.commit()
        return note.to_dict(), 200

    def delete(self, id):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return {"error": "Note not found or unauthorized"}, 404

        db.session.delete(note)
        db.session.commit()
        return {}, 204


# Register Routes
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(NoteList, "/notes")
api.add_resource(NoteResource, "/notes/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)

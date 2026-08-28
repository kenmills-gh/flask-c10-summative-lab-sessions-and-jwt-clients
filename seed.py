from app import app
from models import db, User, Note
from faker import Faker
import random

fake = Faker()

with app.app_context():
    print("Deleting existing data...")
    Note.query.delete()
    User.query.delete()

    print("Creating users...")
    users = []
    for i in range(5):
        user = User(username=fake.unique.user_name())
        user.password_hash = "password123"
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Creating notes...")
    for _ in range(20):
        note = Note(
            title=fake.sentence(nb_words=4),
            content=fake.paragraph(nb_sentences=3),
            user_id=random.choice(users).id,
        )
        db.session.add(note)
    db.session.commit()
    print("Seeding complete!")

# server/seed.py
import os
import random
from faker import Faker
from werkzeug.security import generate_password_hash
from server.app import create_app
from server.config import db
from server.models import User, Record

fake = Faker()

# Real coordinates for places in Kenya (lat, long)
LOCATIONS = {
    "Nairobi CBD": (-1.286389, 36.817223),
    "Mombasa": (-4.043477, 39.668206),
    "Kisumu": (-0.102208, 34.761673),
    "Nakuru": (-0.303099, 36.080026),
    "Eldoret": (0.514311, 35.269779),
    "Thika": (-1.038757, 37.083366),
    "Machakos": (-1.517683, 37.263416),
    "Garissa": (-0.463453, 39.645440),
    "Kitale": (1.015082, 35.006199),
    "Malindi": (-3.217991, 40.120375),
    "Naivasha": (-0.720000, 36.433333),
    "Nyeri": (-0.420000, 36.950000),
    "Meru": (0.050000, 37.650000),
    "Kakamega": (0.282731, 34.751863),
    "Voi": (-3.400000, 38.566667),
}

def seed_users():
    """Create admin and regular users."""
    print("Seeding users...")
    
    # Admin user
    admin = User.query.filter_by(email="admin@ireporter.com").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@ireporter.com",
            password="Admin123!",
            is_admin=True
        )
        db.session.add(admin)
    
    # Regular users
    users = []
    for i in range(10):
        username = fake.user_name() + str(i)
        email = fake.email()
        # Check if already exists
        if not User.query.filter_by(email=email).first():
            user = User(
                username=username,
                email=email,
                password="password123",
                is_admin=False
            )
            db.session.add(user)
            users.append(user)
    
    db.session.commit()
    print(f"Created/verified admin and {len(users)} regular users.")
    return User.query.all()

def seed_records(users):
    """Create records (red-flag and intervention) for each user."""
    print("Seeding records...")
    statuses = ['pending', 'under investigation', 'rejected', 'resolved']
    types = ['red flag', 'intervention']
    
    records_created = 0
    for user in users:
        # Each user gets 2-5 records
        for _ in range(random.randint(2, 5)):
            location_name, coords = random.choice(list(LOCATIONS.items()))
            record_type = random.choice(types)
            # Decide if lat/long are present (most should have)
            lat, lon = coords if random.choice([True, False, True]) else (None, None)
            
            # Title and description based on type
            if record_type == 'red flag':
                title = f"Corruption allegation: {fake.sentence(nb_words=5)}"
                description = f"Reported at {location_name}. Details: {fake.paragraph(nb_sentences=3)}"
            else:
                title = f"Intervention needed: {fake.sentence(nb_words=5)}"
                description = f"Location: {location_name}. {fake.paragraph(nb_sentences=3)}"
            
            status = random.choice(statuses)
            
            record = Record(
                user_id=user.id,
                type=record_type,
                title=title,
                description=description,
                status=status,
                latitude=lat,
                longitude=lon
            )
            db.session.add(record)
            records_created += 1
    
    db.session.commit()
    print(f"Created {records_created} records.")
    return records_created

def seed_all():
    """Main seeding function."""
    app = create_app()
    with app.app_context():
        db.drop_all() 
        db.create_all()
        users = seed_users()
        seed_records(users)
        print("✅ Seeding completed!")

if __name__ == "__main__":
    seed_all()
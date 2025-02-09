from app import app, db  # Import both app and db from app.py

# Push the application context
with app.app_context():
    # Create the tables in the database
    db.create_all()

print("Tables created successfully!")

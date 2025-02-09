import os
from flask import Flask, render_template, request, redirect, flash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_migrate import Migrate  

app = Flask(__name__)

# Use the environment variable DATABASE_URL for Render (or local fallback)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://flower_shop_o0iu_user:ijzWwaTIaGPzGmkM6vp0Nbj96iSYMLgk@dpg-cukgktbtq21c73e75k80-a.oregon-postgres.render.com/flower_shop_o0iu')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tool
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db

# Define your models
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    project_list = Project.query.all()
    print(project_list)
    return render_template('projects.html', projects=project_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            flash("All fields are required!", "danger")
        else:
            try:
                new_message = ContactMessage(name=name, email=email, message=message)
                db.session.add(new_message)
                db.session.commit()
                flash("Your message has been sent!", "success")
                return redirect('/contact')
            except Exception as e:
                db.session.rollback()
                flash(f"Error sending message: {e}", "danger")

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

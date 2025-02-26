import os
from flask import Flask, render_template, request, redirect, flash, url_for  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_migrate import Migrate  

# Step 1: Create the Flask app object
app = Flask(__name__)

# Step 2: Set a secret key for session management (after app creation)
app.secret_key = os.urandom(24)

# Step 3: Print the DATABASE_URL from the environment
print("DATABASE_URL:", os.environ.get('DATABASE_URL'))

# Step 4: Configure the database URI for Render (or local fallback)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://flower_shop_o0iu_user:ijzWwaTIaGPzGmkM6vp0Nbj96iSYMLgk@dpg-cukgktbtq21c73e75k80-a.oregon-postgres.render.com/flower_shop_o0iu')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Step 5: Initialize the database and migration tool
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
    return render_template('projects.html', projects=project_list)

@app.route('/projects/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        if not name or not description:
            flash("Both fields are required!", "danger")
        else:
            try:
                new_project = Project(name=name, description=description)
                db.session.add(new_project)
                db.session.commit()
                flash("Project created successfully!", "success")
                return redirect(url_for('projects'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating project: {e}", "danger")
    
    return render_template('create_project.html')

@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        
        if not project.name or not project.description:
            flash("Both fields are required!", "danger")
        else:
            try:
                db.session.commit()
                flash("Project updated successfully!", "success")
                return redirect(url_for('projects'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating project: {e}", "danger")
    
    return render_template('edit_project.html', project=project)

@app.route('/projects/<int:id>/delete', methods=['POST'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        flash("Project deleted successfully!", "success")
        return redirect(url_for('projects'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting project: {e}", "danger")
    
    return redirect(url_for('projects'))

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

    # Display all messages
    messages = ContactMessage.query.all()
    return render_template('contact.html', messages=messages)

@app.route('/contact/<int:id>/delete', methods=['POST'])
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)

    try:
        db.session.delete(message)
        db.session.commit()
        flash("Message deleted successfully!", "success")
        return redirect(url_for('contact'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting message: {e}", "danger")
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)

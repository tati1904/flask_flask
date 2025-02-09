from flask import Flask, render_template, request, redirect, flash # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Erika2016@localhost:5432/flower_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

# Route for home
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    # Query the database for all projects
    project_list = Project.query.all()

    # Debugging output - print the list of projects to the console
    print(project_list)  # This will show the list of projects in the terminal

    
    return render_template('projects.html', projects=project_list)



# Route for about
@app.route('/about')
def about():
    return render_template('about.html')

# Route for skills
@app.route('/skills')
def skills():
    return render_template('skills.html')

# Route for contact
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

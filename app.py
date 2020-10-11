from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SECRET_KEY'] = '0a1s2d3f4g'
app.config['SQLALCHEMY_BINDS'] = {
    'ticket_db': 'sqlite:///tickets.db', 
    'user_db': 'sqlite:///user.db'
}


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __bind_key__ = 'user_db'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))

class Tickets(db.Model):
    __bind_key__ = 'ticket_db'

    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.Text, nullable=False)
    issue = db.Column(db.Text, nullable=False)
    employee = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.Text, nullable=False)
    date_closed = db.Column(db.Text)
    priority = db.Column(db.Integer)
    notes = db.Column(db.Text)
    #def __repr__(self):
        #return "{}, {}".format(self.issue, self.date_created)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    tickets = Tickets.query.all()
    return render_template('dashboard.html', tickets=tickets)

@app.route('/tickets')
@login_required
def ticket_manager():
    tickets = Tickets.query.all()
    return render_template('tickets.html', tickets=tickets)

@app.route('/docs')
def read_docs():
    return render_template('docs.html')
    
@app.route('/submit_ticket')
@login_required
def submit_ticket():
    return render_template('submit_ticket.html')
    
@app.route('/submission', methods=['POST'])
@login_required
def submission():
    ticket = Tickets(employee=request.form.get('ticket_employee'))
    ticket.summary = request.form.get('ticket_summary')
    ticket.issue = request.form.get('ticket_issue')
    ticket.priority = request.form.get('ticket_priority')
    ticket.date_created = datetime.now().strftime("%Y-%m-%d %H:%M")
    ticket.date_closed = "Open"
    db.session.add(ticket)
    db.session.commit()
    return redirect('/tickets')
    
@app.route('/<int:id>')
@login_required
def ticket_info(id):
    ticket = Tickets.query.filter(Tickets.id==id).first()
    return render_template('ticket_info.html', ticket=ticket)
    
@app.route('/update_notes', methods=['POST'])
@login_required
def update_notes():
    notes = request.form.get('issue_notes')
    ticket_id = request.form.get('ticket_id')
    ticket = Tickets.query.filter(Tickets.id==ticket_id).first()
    ticket.notes = notes
    db.session.commit()
    return redirect('/%i' % int(ticket_id))
    
@app.route('/close_ticket', methods=['POST'])
@login_required
def close_ticket():
    ticket_id = request.form.get('ticket_id')
    ticket = Tickets.query.filter(Tickets.id==ticket_id).first()
    ticket.date_closed = datetime.now().strftime("%Y-%m-%d %H:%M")
    db.session.commit()
    return redirect('/%i' % int(ticket_id))
    
@app.route('/reopen_ticket', methods=['POST'])
@login_required
def reopen_ticket():
    ticket_id = request.form.get('ticket_id')
    ticket = Tickets.query.filter(Tickets.id==ticket_id).first()
    ticket.date_closed = "Open"
    db.session.commit()
    return redirect('/%i' % int(ticket_id))

@app.route('/delete_ticket', methods=['POST'])
@login_required
def delete_ticket():
    ticket_id = request.form.get('ticket_id')
    ticket = Tickets.query.filter(Tickets.id==ticket_id).first()
    db.session.delete(ticket)
    db.session.commit()
    return redirect('/tickets')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        valid_user = User.query.filter_by(username=username).first()
        valid_pass = User.query.filter_by(password=password).first()

        if (not valid_user) and (not valid_pass):
            error = 'Invalid Credentials. Please try again.'
        else:
            login_user(valid_user)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html', error=error)

if __name__=="__main__":
    app.run(debug=True)

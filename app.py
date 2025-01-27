from flask import Flask, render_template

from dashboard_controller import init_dashboard
from services import db_data_population

# Initialize Flask app
app = Flask(__name__)

# Initialize Dash app
dash_app = init_dashboard(app)


@app.route('/')
def home():
    return render_template('index.html')  # Home page

@app.route('/dashboard')
def dashboard():
    return dash_app.index()  # Serve Dash app


if __name__ == '__main__':
    # prepare database on start
    db_data_population.prepare_all_databases()
    app.run(debug=True)

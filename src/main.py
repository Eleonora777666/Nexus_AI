import os
import sqlite3
from flask import Flask, render_template, request, redirect

# Initialize the Flask application
app = Flask(__name__)

# Force absolute path for Render server environment stability
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'nexus_vault.db')

# Database connection helper to handle SQLite interactions
def get_db_connection():
    # Connect to the local database file via absolute path
    conn = sqlite3.connect(DB_PATH)
    # Set the row factory to return dictionary-like Row objects
    conn.row_factory = sqlite3.Row
    return conn

# Database schema initialization
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

@app.route('/')
def index():
    """Main dashboard route: fetches and displays all stored knowledge nodes."""
    with get_db_connection() as conn:
        # Fetch all items from the database, ordered by newest first
        items = conn.execute('SELECT * FROM knowledge_base ORDER BY id DESC').fetchall()
        # Count items for the statistics bar in the UI
        count = len(items)
    # Render the futuristic glassmorphism template with data
    return render_template('index.html', items=items, count=count)

@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    """Route to handle new knowledge deployment from the UI form."""
    if request.method == 'POST':
        # Retrieve form data submitted via POST request
        topic = request.form['topic']
        content = request.form['content']
        category = request.form['category']

        # Save the received data into the Nexus Vault (database)
        with get_db_connection() as conn:
            conn.execute('INSERT INTO knowledge_base (topic, content, category) VALUES (?, ?, ?)',
                         (topic, content, category))
            conn.commit()

    # If it was a GET request or after a successful POST, safely redirect back to the dashboard
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
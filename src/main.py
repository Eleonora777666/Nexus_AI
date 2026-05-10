import sqlite3
from flask import Flask, render_template, request, redirect

# Initialize the Flask application
app = Flask(__name__)

# Database connection helper to handle SQLite interactions
def get_db_connection():
    # Connect to the local database file 'nexus_vault.db'
    conn = sqlite3.connect('nexus_vault.db')
    # Set the row factory to return dictionary-like Row objects
    conn.row_factory = sqlite3.Row
    return conn

# Database schema initialization
# This ensures the required table exists before the app starts handling requests
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

@app.route('/deploy', methods=['POST'])
def deploy():
    """Route to handle new knowledge deployment from the UI form."""
    # Retrieve form data submitted via POST request
    topic = request.form['topic']
    content = request.form['content']
    category = request.form['category']

    # Save the received data into the Nexus Vault (database)
    with get_db_connection() as conn:
        conn.execute('INSERT INTO knowledge_base (topic, content, category) VALUES (?, ?, ?)',
                     (topic, content, category))
        conn.commit()

    # Redirect user back to the dashboard to see the new entry
    return redirect('/')

if __name__ == '__main__':
    # Start the development server in debug mode for easier troubleshooting
    app.run(debug=True)
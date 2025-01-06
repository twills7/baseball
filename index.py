from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the database
    conn = sqlite3.connect('player_stats.db')
    cursor = conn.cursor()
    
    # Execute a query to retrieve data
    cursor.execute("SELECT * FROM player_stats")
    rows = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Define the HTML template
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Player Stats</title>
    </head>
    <body>
        <h1>Player Stats</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Team</th>
                <th>Average</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[0] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    
    # Render the HTML template with the data
    return render_template_string(html_template, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
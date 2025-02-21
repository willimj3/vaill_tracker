from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('legislation.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
@app.route('/search')
def search():
    state = request.args.get('state', '')
    bill_number = request.args.get('bill_number', '')
    summary = request.args.get('summary', '')
    status = request.args.get('status', '')

    db = get_db()

    if state or bill_number or summary or status:
        sql = '''
        SELECT * FROM state_legislation
        WHERE (? = '' OR state LIKE ?)
        AND (? = '' OR bill_number LIKE ?)
        AND (? = '' OR summary LIKE ?)
        AND (? = '' OR status = ?)
        ORDER BY state, bill_number
        '''

        cur = db.execute(sql, (state, f'%{state}%',
                               bill_number, f'%{bill_number}%',
                               summary, f'%{summary}%',
                               status, status))
    else:
        cur = db.execute('SELECT * FROM state_legislation ORDER BY state, bill_number')

    legislation = cur.fetchall()

    # Get statistics
    total_bills = len(legislation)
    states = len(set(law['state'] for law in legislation))
    statuses = dict()
    for law in legislation:
        statuses[law['status']] = statuses.get(law['status'], 0) + 1

    # Get all possible statuses for the dropdown
    all_statuses = [row['status'] for row in db.execute('SELECT DISTINCT status FROM state_legislation').fetchall()]

    return render_template('index.html', legislation=legislation, total_bills=total_bills,
                           states=states, statuses=statuses, all_statuses=all_statuses,
                           state=state, bill_number=bill_number, summary=summary, status=status)

@app.route('/provisions')
def provisions():
    return render_template('provisions.html')

if __name__ == '__main__':
    app.run(debug=True)

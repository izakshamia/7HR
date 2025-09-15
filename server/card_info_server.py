import sys
import os

# Add the 'server' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, render_template
from db_utils import Database
import config

app = Flask(__name__)
db = Database(config.DB_CONFIG)

@app.route('/candidate/<int:candidate_id>')
def candidate_profile(candidate_id):
    data = db.fetch_candidate_by_id(candidate_id)
    if not data:
        abort(404)
        
    # Get navigation links
    nav = db.get_adjacent_candidate_ids(candidate_id)
    
    return render_template("card_info_ui.html", c=data, nav=nav)

@app.route('/api/candidates')
def api_candidates():
    candidates = db.fetch_all_candidates_with_details()
    return jsonify(candidates)

@app.route('/api/jobs')
def api_jobs():
    jobs = db.fetch_all_jobs()
    return jsonify(jobs)

# The following is for local development only, Vercel will handle serving the React app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
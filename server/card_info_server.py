import sys
import os

# Add the 'server' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, send_from_directory, render_template
from db_utils import Database
import config

app = Flask(__name__, static_folder='../dist')
db = Database(config.DB_CONFIG)

@app.route('/candidate/<int:candidate_id>')
def candidate_profile(candidate_id):
    data = db.fetch_candidate_by_id(candidate_id)
    if not data:
        abort(404)
        
    # Get navigation links
    nav = db.get_adjacent_candidate_ids(candidate_id)
    
    return render_template("card_info_ui.html", c=data, nav=nav)

@app.route('/')
@app.route('/candidates')
def candidates():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

@app.route('/api/candidates')
def api_candidates():
    candidates = db.fetch_all_candidates_with_details()
    return jsonify(candidates)

@app.route('/api/jobs')
def api_jobs():
    jobs = db.fetch_all_jobs()
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

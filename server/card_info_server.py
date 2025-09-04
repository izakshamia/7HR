from flask import Flask, render_template, abort, jsonify
from db_utils import Database
import config

app = Flask(__name__, template_folder="templates")
db = Database(config.DB_CONFIG)

@app.route('/candidate/<int:candidate_id>')
def candidate_profile(candidate_id):
    data = db.fetch_candidate_by_id(candidate_id)
    if not data:
        abort(404)
        
    # Get navigation links
    nav = db.get_adjacent_candidate_ids(candidate_id)
    
    return render_template("card_info_ui.html", c=data, nav=nav)

@app.route('/candidates')
def candidates():
    jobs = db.fetch_all_jobs()
    return render_template("candidates.html", jobs=jobs)

@app.route('/api/candidates')
def api_candidates():
    candidates = db.fetch_all_candidates_with_details()
    return jsonify(candidates)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
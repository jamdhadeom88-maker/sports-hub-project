from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import os
from datetime import datetime, timedelta

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "sports_data.csv")

# Configure Flask to use the 'template' folder
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "template"))
app.secret_key = "sports_hub_secret_2024"

# =========================================================
# SAMPLE DATA
# =========================================================

USERS_DB = {
    "john@sports.com": {"password": "password123", "name": "John Doe"},
    "jane@sports.com": {"password": "password123", "name": "Jane Smith"},
}

PLAYERS_DB = {
    "virat_kohli": {
        "name": "Virat Kohli",
        "sport": "Cricket",
        "position": "Batsman",
        "team": "India",
        "rating": 9.8,
        "country": "India",
        "birth_date": "1988-11-05",
        "height": "5'11\"",
        "jersey": "18",
        "career_start": 2008,
        "matches": 289,
        "runs": 12800,
        "centuries": 46,
        "achievements": "ICC ODI Player of the Decade, 3x ICC World Cup Winner",
        "bio": "Virat Kohli is an Indian international cricketer who plays for India's national cricket team and is widely regarded as one of the most prolific batsmen in the modern era of cricket."
    },
    "cristiano": {
        "name": "Cristiano Ronaldo",
        "sport": "Football",
        "position": "Forward",
        "team": "Portugal",
        "rating": 9.9,
        "country": "Portugal",
        "birth_date": "1985-02-05",
        "height": "6'2\"",
        "jersey": "7",
        "career_start": 2003,
        "matches": 892,
        "goals": 890,
        "trophies": 5,
        "achievements": "5x Ballon d'Or, Champions League Winner 5 times",
        "bio": "Cristiano Ronaldo dos Santos Aveiro is a Portuguese professional footballer who is widely regarded as one of the greatest football players of all time."
    },
    "lebron": {
        "name": "LeBron James",
        "sport": "Basketball",
        "position": "Forward",
        "team": "Los Angeles Lakers",
        "rating": 9.7,
        "country": "United States",
        "birth_date": "1984-12-30",
        "height": "6'9\"",
        "jersey": "23",
        "career_start": 2003,
        "matches": 1432,
        "points": 40279,
        "championships": 4,
        "achievements": "4x NBA Champion, 4x MVP, 20x All-Star",
        "bio": "LeBron Raymone James Sr. is an American professional basketball player widely recognized as one of the greatest basketball players of all time."
    },
    "serena": {
        "name": "Serena Williams",
        "sport": "Tennis",
        "position": "Singles",
        "team": "USA",
        "rating": 9.6,
        "country": "United States",
        "birth_date": "1981-09-26",
        "height": "5'9\"",
        "jersey": "-",
        "career_start": 1995,
        "matches": 1316,
        "titles": 73,
        "grand_slams": 23,
        "achievements": "23 Grand Slam Titles, 4x Olympic Gold, 64 Weeks at World No.1",
        "bio": "Serena Jameka Williams is an American professional tennis player who is widely regarded as one of the greatest tennis players of all time."
    },
}

TOURNAMENTS_DB = [
    {
        "id": 1,
        "name": "ICC Cricket World Cup 2024",
        "sport": "Cricket",
        "category": "International",
        "status": "Ongoing",
        "year": 2024,
        "teams": 12,
        "image": "🏏",
        "stadium": "Dubai International Cricket Stadium",
        "location": "Dubai, UAE",
        "start_date": "2024-01-15",
        "end_date": "2024-03-30",
        "prize_pool": "$5.6 Million",
        "participants": "India, Australia, South Africa, England, Pakistan, New Zealand, West Indies, Bangladesh, Afghanistan, Ireland, Oman, UAE",
        "format": "ODI (One Day International)"
    },
    {
        "id": 2,
        "name": "FIFA World Cup 2022",
        "sport": "Football",
        "category": "International",
        "status": "Completed",
        "year": 2022,
        "teams": 32,
        "image": "⚽",
        "stadium": "Lusail Stadium",
        "location": "Qatar",
        "start_date": "2022-11-20",
        "end_date": "2022-12-18",
        "prize_pool": "$440 Million",
        "participants": "Argentina, France, Germany, Brazil, Spain, Belgium, Netherlands, Italy, England, Portugal, and others",
        "format": "Knockout Tournament"
    },
    {
        "id": 3,
        "name": "NBA Finals 2024",
        "sport": "Basketball",
        "category": "Professional League",
        "status": "Ongoing",
        "year": 2024,
        "teams": 30,
        "image": "🏀",
        "stadium": "Crypto.com Arena",
        "location": "Los Angeles, USA",
        "start_date": "2024-06-01",
        "end_date": "2024-06-30",
        "prize_pool": "$10 Million",
        "participants": "Boston Celtics, Dallas Mavericks, Denver Nuggets, Los Angeles Lakers, and others",
        "format": "Best of 7 Series"
    },
    {
        "id": 4,
        "name": "Wimbledon 2025",
        "sport": "Tennis",
        "category": "Grand Slam",
        "status": "Upcoming",
        "year": 2025,
        "teams": 128,
        "image": "🎾",
        "stadium": "Centre Court, Wimbledon",
        "location": "London, England",
        "start_date": "2025-06-23",
        "end_date": "2025-07-13",
        "prize_pool": "$3.1 Million",
        "participants": "Top 128 Male and Female Players",
        "format": "Single Elimination"
    },
    {
        "id": 5,
        "name": "Indian Premier League (IPL) 2024",
        "sport": "Cricket",
        "category": "Domestic League",
        "status": "Completed",
        "year": 2024,
        "teams": 10,
        "image": "🏏",
        "stadium": "Multiple Stadiums",
        "location": "India",
        "start_date": "2024-03-22",
        "end_date": "2024-05-26",
        "prize_pool": "$10 Million",
        "participants": "Chennai Super Kings, Mumbai Indians, Kolkata Knight Riders, Royal Challengers Bangalore, and others",
        "format": "T20 League"
    },
    {
        "id": 6,
        "name": "Premier League 2024-25",
        "sport": "Football",
        "category": "Premier League",
        "status": "Ongoing",
        "year": 2024,
        "teams": 20,
        "image": "⚽",
        "stadium": "Multiple Stadiums",
        "location": "England",
        "start_date": "2024-08-16",
        "end_date": "2025-05-25",
        "prize_pool": "£165 Million",
        "participants": "Manchester City, Arsenal, Liverpool, Manchester United, Chelsea, and others",
        "format": "League Format"
    },
]

# =========================================================
# LOAD DATASET
# =========================================================

def load_data():
    """Load sports dataset."""
    if not os.path.exists(DATA_PATH):
        print("Dataset not found:", DATA_PATH)
        return pd.DataFrame()

    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        return pd.DataFrame()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_sport(sport_name):
    df = load_data()
    if df.empty:
        return None
    result = df[df["sport"].astype(str).str.lower() == sport_name.lower()]
    return result.iloc[0].to_dict() if not result.empty else None


def is_logged_in():
    return "user_email" in session


# =========================================================
# AUTHENTICATION ROUTES
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email in USERS_DB and USERS_DB[email]["password"] == password:
            session["user_email"] = email
            session["user_name"] = USERS_DB[email]["name"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        
        if email not in USERS_DB:
            USERS_DB[email] = {"password": password, "name": name}
            session["user_email"] = email
            session["user_name"] = name
            return redirect(url_for("dashboard"))
        else:
            return render_template("register.html", error="Email already exists")
    
    return render_template("register.html")


# =========================================================
# MAIN ROUTES
# =========================================================

@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    df = load_data()
    
    if df.empty:
        return render_template("dashboard.html", error="Dataset not found.", 
                             total_sports=0, total_players=0, total_teams=0, 
                             total_matches=0, sports=[], user_name=session.get("user_name"))

    total_sports = len(df)
    total_players = int(df["players"].sum())
    total_teams = int(df["teams"].sum())
    total_matches = int(df["matches"].sum())
    sports = df.to_dict("records")

    return render_template("dashboard.html", error=None,
                         total_sports=total_sports, total_players=total_players,
                         total_teams=total_teams, total_matches=total_matches,
                         sports=sports, user_name=session.get("user_name"))


@app.route("/tournaments")
def tournaments():
    if not is_logged_in():
        return redirect(url_for("login"))
    
    # Get filter parameter
    category_filter = request.args.get("category", "all")
    
    filtered_tournaments = TOURNAMENTS_DB
    if category_filter != "all":
        filtered_tournaments = [t for t in TOURNAMENTS_DB if t.get("category", "").lower() == category_filter.lower()]
    
    # Get unique categories
    categories = sorted(list(set([t.get("category", "Other") for t in TOURNAMENTS_DB])))
    
    return render_template("tournaments.html", 
                         tournaments=filtered_tournaments, 
                         all_tournaments=TOURNAMENTS_DB,
                         categories=categories,
                         active_category=category_filter,
                         user_name=session.get("user_name"))


@app.route("/tournament/<int:tournament_id>")
def tournament_detail(tournament_id):
    if not is_logged_in():
        return redirect(url_for("login"))
    
    tournament = next((t for t in TOURNAMENTS_DB if t["id"] == tournament_id), None)
    if not tournament:
        return "Tournament not found", 404
    
    return render_template("tournament_detail.html", tournament=tournament, user_name=session.get("user_name"))


@app.route("/players")
def players():
    if not is_logged_in():
        return redirect(url_for("login"))
    
    return render_template("players.html", players=PLAYERS_DB, user_name=session.get("user_name"))


@app.route("/player/<player_id>")
def player_profile(player_id):
    if not is_logged_in():
        return redirect(url_for("login"))
    
    if player_id not in PLAYERS_DB:
        return "Player not found", 404
    
    player = PLAYERS_DB[player_id]
    return render_template("player_profile.html", player=player, player_id=player_id, user_name=session.get("user_name"))


@app.route("/analytics")
def analytics():
    if not is_logged_in():
        return redirect(url_for("login"))

    df = load_data()
    if df.empty:
        return render_template("analytics.html", error="Dataset not found", sports=[], user_name=session.get("user_name"))

    sports = df.to_dict("records")
    return render_template("analytics.html", sports=sports, error=None, user_name=session.get("user_name"))


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if not is_logged_in():
        return redirect(url_for("login"))

    df = load_data()
    if df.empty:
        return render_template("prediction.html", error="Dataset not found", sports=[], 
                             user_name=session.get("user_name"))

    sports_list = df["sport"].tolist()
    prediction_result = None
    
    if request.method == "POST":
        sport = request.form.get("sport")
        sport_data = get_sport(sport)
        if sport_data:
            # Simple prediction logic
            avg_players = int(sport_data["players"])
            avg_teams = int(sport_data["teams"])
            avg_matches = int(sport_data["matches"])
            
            prediction_result = {
                "sport": sport,
                "predicted_players": avg_players + 5,
                "predicted_teams": avg_teams + 2,
                "predicted_matches": avg_matches + 10,
                "confidence": 87.5,
                "trend": "upward"
            }
    
    return render_template("prediction.html", sports=sports_list, 
                         prediction=prediction_result, user_name=session.get("user_name"))


@app.route("/cricket")
def cricket():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Cricket")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/football")
def football():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Football")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/basketball")
def basketball():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Basketball")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/tennis")
def tennis():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Tennis")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/baseball")
def baseball():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Baseball")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/hockey")
def hockey():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Hockey")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


@app.route("/volleyball")
def volleyball():
    if not is_logged_in():
        return redirect(url_for("login"))
    sport = get_sport("Volleyball")
    return render_template("sports_details.html", sport=sport, user_name=session.get("user_name")) if sport else ("Sport not found", 404)


# =========================================================
# DEBUG ROUTE
# =========================================================

@app.route("/debug")
def debug():
    html = "<h1>Sports Hub Debug</h1>"
    html += f"<p><b>Base Directory:</b> {BASE_DIR}</p>"
    html += f"<p><b>Dataset Path:</b> {DATA_PATH}</p>"

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        html += "<p style='color:green;'>Dataset found!</p>"
        html += f"<p>Records: {len(df)}</p>"
        html += f"<p>Columns: {list(df.columns)}</p>"
        html += df.to_html(classes="table", index=False)
    else:
        html += "<p style='color:red;'>Dataset NOT found!</p>"

    return html


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🏆 SPORTS HUB - PROFESSIONAL EDITION")
    print("=" * 60)

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        print("✅ Dataset found!")
        print(f"   Records: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
    else:
        print("⚠️  Dataset NOT FOUND!")
        print(f"   Path: {DATA_PATH}")

    print("=" * 60)
    print("🚀 Starting server...")
    print("📱 Open: http://127.0.0.1:5000")
    print("🐛 Debug: http://127.0.0.1:5000/debug")
    print("=" * 60)

    app.run(debug=True, host="127.0.0.1", port=5000)
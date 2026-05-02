"""Election timeline tool."""


TIMELINES = {
    "general": [
        {"name": "Model Code of Conduct", "description": "MCC comes into force on election announcement day.", "duration": "Day 0"},
        {"name": "Nomination Filing", "description": "Candidates file nomination papers at the Returning Officer.", "duration": "Day 1–14"},
        {"name": "Scrutiny of Nominations", "description": "Returning Officer examines nomination papers.", "duration": "Day 15"},
        {"name": "Last Date for Withdrawal", "description": "Candidates may withdraw nominations.", "duration": "Day 16"},
        {"name": "Campaign Period", "description": "Candidates and parties campaign. Ends 48 hours before polling.", "duration": "Day 16 – Day N-2"},
        {"name": "Poll Day", "description": "Voting takes place at polling booths.", "duration": "Day N"},
        {"name": "Counting & Results", "description": "Votes counted and results declared.", "duration": "Day N+1 to N+5"},
        {"name": "Government Formation", "description": "President/Governor invites majority party/coalition to form government.", "duration": "Post-Results"},
    ],
    "state": [
        {"name": "Election Announcement", "description": "ECI announces schedule for state legislative assembly elections.", "duration": "Day 0"},
        {"name": "Nomination", "description": "Candidates file papers at district returning officers.", "duration": "Day 1–10"},
        {"name": "Campaign", "description": "Parties and candidates campaign across constituencies.", "duration": "Day 11 – Day N-2"},
        {"name": "Polling", "description": "Voting conducted in constituencies, often in phases.", "duration": "Day N"},
        {"name": "Counting", "description": "Votes counted; leading party/alliance invited to form government.", "duration": "Day N+1 to N+3"},
    ],
}


def get_election_timeline(election_type: str = "general") -> list[dict]:
    """Return the list of election phases for general or state elections."""
    return TIMELINES.get(election_type, TIMELINES["general"])

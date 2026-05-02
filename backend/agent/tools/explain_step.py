"""Explain a specific election step in plain language."""


STEPS = {
    "voter registration": {
        "title": "Voter Registration",
        "summary": "Registering to vote ensures your name appears on the Electoral Roll so you can cast a ballot.",
        "details": [
            "Visit the National Voters' Service Portal: voters.eci.gov.in",
            "Fill Form 6 online to register as a new voter.",
            "You need proof of age (birth certificate, class 10 certificate) and proof of address (Aadhaar, utility bill).",
            "After submission, a Booth Level Officer (BLO) verifies your details.",
            "Your name will appear in the final Electoral Roll published by ECI.",
        ],
        "links": ["https://voters.eci.gov.in"],
    },
    "epic card": {
        "title": "EPIC Card (Voter ID)",
        "summary": "The Elector's Photo Identity Card (EPIC) is your official voter ID issued by ECI.",
        "details": [
            "EPIC is issued automatically after successful voter registration.",
            "Download the e-EPIC (digital version) from voters.eci.gov.in.",
            "Physical card is delivered to your registered address.",
            "EPIC is used as identity proof at polling booths.",
            "You can also vote with 11 alternative photo ID documents if EPIC is unavailable.",
        ],
        "links": ["https://voters.eci.gov.in"],
    },
    "polling booth": {
        "title": "Finding Your Polling Booth",
        "summary": "Every voter is assigned a specific polling booth based on their registered address.",
        "details": [
            "Visit voters.eci.gov.in and search for your name on the Electoral Roll.",
            "Your booth details (name, address, booth number) are shown on your voter slip.",
            "Voter slips are distributed by BLOs before election day.",
            "You can also use the Voter Helpline App or call 1950 for assistance.",
        ],
        "links": ["https://voters.eci.gov.in", "https://play.google.com/store/apps/details?id=com.eci.citizen"],
    },
    "model code of conduct": {
        "title": "Model Code of Conduct (MCC)",
        "summary": "A set of guidelines issued by ECI that governs political parties and candidates during the election period.",
        "details": [
            "MCC comes into effect from the date of election announcement.",
            "It prohibits use of government machinery for campaigning.",
            "Parties cannot make new policy announcements after MCC is in force.",
            "Violations can lead to censure, FIRs, or disqualification of candidates.",
            "MCC remains in force until results are declared.",
        ],
        "links": ["https://eci.gov.in/model-code-of-conduct/"],
    },
}


def explain_step(step_name: str) -> dict:
    """
    Return a plain-language explanation of a specific election step.

    Args:
        step_name: Name of the step (e.g. 'voter registration', 'epic card').

    Returns:
        dict with title, summary, details list, and links list.
    """
    key = step_name.lower().strip()
    for known_key, info in STEPS.items():
        if known_key in key or key in known_key:
            return info
    return {
        "title": step_name,
        "summary": "No detailed information available for this step yet.",
        "details": [],
        "links": ["https://eci.gov.in"],
    }

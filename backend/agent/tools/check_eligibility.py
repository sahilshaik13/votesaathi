"""Voter eligibility checker tool."""


def check_voter_eligibility(age: int, is_citizen: bool, constituency: str = "") -> dict:
    """
    Check if a person is eligible to vote in Indian elections per ECI rules.

    Args:
        age: Age of the person in years.
        is_citizen: Whether the person is an Indian citizen.
        constituency: Name of the constituency (optional, for context).

    Returns:
        dict with keys: eligible (bool), reason (str).
    """
    if not is_citizen:
        return {"eligible": False, "reason": "Only Indian citizens are eligible to vote."}
    if age < 18:
        return {
            "eligible": False,
            "reason": f"You must be at least 18 years old to vote. You are currently {age}.",
        }
    note = f" in the {constituency} constituency" if constituency else ""
    return {
        "eligible": True,
        "reason": (
            f"You are eligible to vote{note}. Ensure you are registered on the "
            "Electoral Roll. You can verify your registration at voters.eci.gov.in."
        ),
    }

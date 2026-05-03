"""Structured FAQ answers about Indian elections."""


FAQS = [
    {
        "question": "What documents do I need to vote?",
        "answer": "You can use your EPIC (Voter ID) card. If unavailable, ECI accepts 11 alternatives: Aadhaar, Passport, Driving Licence, PAN Card, MNREGA Job Card, Health Insurance Smart Card, Pension Document with photo, NPR Smart Card, official identity documents from Central/State Govt, MP/MLA/MLCA identity cards, or bank/post office passbooks with photo.",
    },
    {
        "question": "How do I register to vote?",
        "answer": "Visit voters.eci.gov.in and submit Form 6. You need proof of age and proof of address. A Booth Level Officer (BLO) will verify your details before adding you to the Electoral Roll.",
    },
    {
        "question": "What is the Model Code of Conduct?",
        "answer": "The Model Code of Conduct (MCC) is a set of guidelines issued by ECI that regulates political parties, candidates, and the government during elections. It prohibits the use of government resources for campaigning and restricts policy announcements that could influence voters.",
    },
    {
        "question": "Can NRIs vote in Indian elections?",
        "answer": "Yes. Non-Resident Indians (NRIs) who are Indian citizens are eligible to register as voters and vote at their registered constituency in India. Currently, NRI voting requires physical presence at the polling booth. Proxy voting for NRIs is under consideration.",
    },
    {
        "question": "What is NOTA?",
        "answer": "NOTA (None of the Above) is an option on the Electronic Voting Machine (EVM) that allows a voter to register a vote without selecting any candidate. NOTA votes are counted but do not affect the result — the candidate with the highest votes still wins.",
    },
    {
        "question": "How does the EVM work?",
        "answer": "An Electronic Voting Machine (EVM) consists of a Control Unit (with the polling officer) and a Balloting Unit (with the voter). The voter presses the button next to their chosen candidate's name and symbol. A VVPAT machine prints a paper slip visible to the voter for 7 seconds for verification. EVMs are not connected to the internet.",
    },
]


def get_faq(question: str = "") -> list[dict]:
    """
    Return structured FAQ answers. If a question is provided, filter relevant ones.

    Args:
        question: Optional question string to filter results.

    Returns:
        List of FAQ dicts with 'question' and 'answer' keys.
    """
    if not question:
        return FAQS
    q_lower = question.lower()
    filtered = [faq for faq in FAQS if any(word in faq["question"].lower() for word in q_lower.split())]
    return filtered if filtered else FAQS

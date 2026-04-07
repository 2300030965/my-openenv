from app.data import TICKETS
from app.graders import grade

TASKS = {
    "ticket_triage_easy": {
        "tickets": TICKETS[:2],
        "max_steps": 4,
        "grader": grade
    },
    "ticket_triage_medium": {
        "tickets": TICKETS,
        "max_steps": 5,
        "grader": grade
    },
    "ticket_triage_hard": {
        "tickets": TICKETS,
        "max_steps": 6,
        "grader": grade
    }
}
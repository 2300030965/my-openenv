# app/tasks.py

from app.data import TICKETS
from app.graders import grade_easy, grade_medium, grade_hard

TASKS = {
    "ticket_triage_easy": {
        "tickets": TICKETS,
        "grader": grade_easy,
        "max_steps": 5
    },
    "ticket_triage_medium": {
        "tickets": TICKETS,
        "grader": grade_medium,
        "max_steps": 6
    },
    "ticket_triage_hard": {
        "tickets": TICKETS,
        "grader": grade_hard,
        "max_steps": 7
    }
}
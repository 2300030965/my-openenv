from app.data import TICKETS

# Split tickets into 3 levels (simple logic)
EASY_TICKETS = TICKETS[:1]
MEDIUM_TICKETS = TICKETS
HARD_TICKETS = TICKETS

TASKS = {
    "ticket_triage_easy": {
        "tickets": EASY_TICKETS,
        "max_steps": 4
    },
    "ticket_triage_medium": {
        "tickets": MEDIUM_TICKETS,
        "max_steps": 5
    },
    "ticket_triage_hard": {
        "tickets": HARD_TICKETS,
        "max_steps": 6
    }
}
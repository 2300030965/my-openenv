from app.models import Ticket

TICKETS = [
    Ticket(
        id="1",
        title="VPN disconnect issue",
        description="VPN disconnects every 5 minutes",
        reporter="employee",
        system="network",
        expected_priority="high",
        expected_team="network",
        required_info=["location"],
        resolution_keywords=["restart vpn", "check network"]
    ),
    Ticket(
        id="2",
        title="Laptop not charging",
        description="Battery stuck at 2%",
        reporter="employee",
        system="hardware",
        expected_priority="high",
        expected_team="hardware",
        required_info=["device_model"],
        resolution_keywords=["replace charger", "check adapter"]
    )
]
import random
from app.tasks import TASKS
from app.graders import grade
from app.models import Observation, StepResult

class SmartSupportDeskEnv:

    def __init__(self):
        self.ticket = None
        self.memory = {}
        self.history = []
        self.step_count = 0
        self.max_steps = 5
        self.done = False

    def reset(self, task_name="ticket_triage_easy"):
        task = TASKS[task_name]
        self.ticket = random.choice(task["tickets"])
        self.max_steps = task["max_steps"]

        self.memory = {"priority": None, "team": None, "resolved": False}
        self.history = []
        self.step_count = 0
        self.done = False

        return self.state()

    def state(self):
        return Observation(
            ticket_id=self.ticket.id,
            title=self.ticket.title,
            description=self.ticket.description,
            reporter=self.ticket.reporter,
            system=self.ticket.system,
            known_info={},
            missing_info=self.ticket.required_info,
            history=self.history,
            step_count=self.step_count,
            max_steps=self.max_steps,
            done=self.done,
            success=False
        )

    def step(self, action):
        self.step_count += 1
        reward = 0.0

        try:
            if action.action_type == "classify":
                self.memory["priority"] = action.payload.get("priority")
                reward += 0.2

            elif action.action_type == "assign":
                self.memory["team"] = action.payload.get("team")
                reward += 0.2

            elif action.action_type == "resolve":
                self.memory["resolved"] = True
                reward += grade(self.memory, self.ticket)
                self.done = True

            self.history.append(str(action.action_type))

        except Exception as e:
            reward -= 0.1

        if self.step_count >= self.max_steps:
            self.done = True

        return StepResult(
            observation=self.state(),
            reward=reward,
            done=self.done,
            info={}
        )
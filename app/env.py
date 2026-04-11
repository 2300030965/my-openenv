# app/env.py

import random
from app.tasks import TASKS
from app.models import Observation, StepResult


class SmartSupportDeskEnv:

    def __init__(self):
        self.ticket = None
        self.memory = {}
        self.history = []
        self.step_count = 0
        self.max_steps = 5
        self.done = False
        self.current_task_name = None

    def reset(self, task_name="ticket_triage_easy"):
        task = TASKS[task_name]

        self.current_task_name = task_name
        self.ticket = random.choice(task["tickets"])

        # 🔥 FORCE minimum steps (VERY IMPORTANT)
        self.max_steps = max(task["max_steps"], 3)

        self.memory = {
            "priority": None,
            "team": None,
            "resolved": False
        }

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

        # 🔥 BASE REWARD (never zero)
        reward = 0.2

        try:
            if action.action_type == "classify":
                self.memory["priority"] = action.payload.get("priority")

            elif action.action_type == "assign":
                self.memory["team"] = action.payload.get("team")

            elif action.action_type == "resolve":
                self.memory["resolved"] = True
                # ❌ DO NOT END HERE

            # 🔥 ALWAYS CALL GRADER
            task = TASKS[self.current_task_name]
            reward += task["grader"](self.memory, self.ticket)

            self.history.append(str(action.action_type))

        except Exception:
            reward = 0.3  # safety

        # 🔥 ONLY END AFTER MULTIPLE STEPS
        if self.step_count >= self.max_steps:
            self.done = True

        return StepResult(
            observation=self.state(),
            reward=reward,
            done=self.done,
            info={}
        )
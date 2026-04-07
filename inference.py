import os
import json
from typing import List, Optional

# ==============================
# LOAD ENV VARIABLES (VERY IMPORTANT)
# ==============================
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from openai import OpenAI
import requests

# ==============================
# ENV VARIABLES
# ==============================
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

# 🔍 DEBUG (remove later)
print("DEBUG API_KEY:", API_KEY)

TASK_NAME = os.getenv("TASK_NAME", "ticket_triage_easy")
BENCHMARK = "smart-support-desk-openenv"
MAX_STEPS = 6

BASE_URL = "http://localhost:7860"

# ==============================
# VALIDATION
# ==============================
if not API_KEY:
    raise ValueError("❌ HF_TOKEN / API_KEY is missing")

# ==============================
# OPENAI CLIENT
# ==============================
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

# ==============================
# LOGGING FUNCTIONS
# ==============================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True
    )


def log_end(success: bool, steps: int, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )

# ==============================
# SAFE JSON PARSER
# ==============================
def safe_json_parse(text: str):
    try:
        return json.loads(text)
    except:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except:
            return {
                "action_type": "resolve",
                "payload": {}
            }

# ==============================
# LLM ACTION
# ==============================
def get_action_from_llm(observation: dict) -> dict:
    prompt = f"""
You are an IT support agent.

Given this ticket:
{json.dumps(observation)}

Choose ONE action in JSON format:
- classify (priority)
- assign (team)
- resolve

Return ONLY JSON:
{{
  "action_type": "...",
  "payload": {{...}}
}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )

        text = response.choices[0].message.content.strip()
        return safe_json_parse(text)

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "action_type": "resolve",
            "payload": {}
        }

# ==============================
# MAIN
# ==============================
def main():
    rewards = []
    steps_taken = 0
    success = False

    log_start(TASK_NAME, BENCHMARK, MODEL_NAME)

    try:
        result = requests.post(
            f"{BASE_URL}/reset",
            params={"task_name": TASK_NAME}
        ).json()

        obs = result
        max_steps = obs.get("max_steps", MAX_STEPS)

        for step in range(1, max_steps + 1):

            action = get_action_from_llm(obs)

            result = requests.post(
                f"{BASE_URL}/step",
                json=action
            ).json()

            reward = float(result.get("reward", 0.0))
            done = bool(result.get("done", False))
            error = result.get("info", {}).get("last_action_error", None)

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=json.dumps(action, separators=(',', ':')),
                reward=reward,
                done=done,
                error=error
            )

            obs = result.get("observation", {})

            if done:
                success = True
                break

    except Exception as e:
        log_step(
            steps_taken if steps_taken > 0 else 1,
            "{}",
            0.00,
            True,
            str(e)
        )

    log_end(success, steps_taken, rewards)

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
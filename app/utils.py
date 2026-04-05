import json
import re
from typing import Any, Dict, List, Optional


# 🔹 1. Normalize text (lowercase, clean spaces)
def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# 🔹 2. Keyword matching (used in graders)
def keyword_match(text: str, keywords: List[str]) -> bool:
    text = normalize_text(text)
    return any(k.lower() in text for k in keywords)


# 🔹 3. Partial keyword score (for advanced grading)
def keyword_score(text: str, keywords: List[str]) -> float:
    text = normalize_text(text)
    if not keywords:
        return 0.0

    matches = sum(1 for k in keywords if k.lower() in text)
    return matches / len(keywords)


# 🔹 4. Clamp reward between 0 and 1
def clamp_reward(value: float) -> float:
    return max(0.0, min(1.0, value))


# 🔹 5. Safe JSON parse (for LLM outputs)
def safe_json_parse(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:
        return None


# 🔹 6. Validate action structure
def validate_action(action: Dict[str, Any]) -> bool:
    if not isinstance(action, dict):
        return False

    if "action_type" not in action:
        return False

    if "payload" not in action:
        return False

    return True


# 🔹 7. Pretty format action (for logs)
def format_action(action: Dict[str, Any]) -> str:
    try:
        return json.dumps(action, separators=(',', ':'))
    except Exception:
        return "{}"


# 🔹 8. Extract field safely from payload
def get_payload_field(payload: Dict[str, Any], field: str, default=None):
    return payload.get(field, default) if isinstance(payload, dict) else default


# 🔹 9. Check if required info satisfied
def check_required_info(known_info: Dict[str, Any], required_fields: List[str]) -> float:
    if not required_fields:
        return 1.0

    count = sum(1 for f in required_fields if f in known_info)
    return count / len(required_fields)


# 🔹 10. Simple logging helpers (for debugging)
def log_info(message: str):
    print(f"[INFO] {message}")


def log_error(message: str):
    print(f"[ERROR] {message}")


def log_debug(message: str):
    print(f"[DEBUG] {message}")
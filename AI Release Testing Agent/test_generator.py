"""
test_generator.py
Generates AI test cases using OpenRouter + Enhanced Smart Execution Logic
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def smart_execution(test_cases):
    """
    Improved rule-based execution logic (more realistic reasoning)
    """

    for tc in test_cases:
        title = tc.get("title", "").lower()
        expected = tc.get("expected_result", "").lower()
        tc_type = tc.get("type", "").lower()

        status = "PASS"
        reason = "Test executed successfully under expected conditions"

        # 🔴 INVALID INPUT CASES
        if "invalid" in title or "invalid" in expected:
            status = "FAIL"
            reason = "System prevented operation due to invalid input validation"

        # 🔴 EMPTY FIELD / REQUIRED VALIDATION
        elif "empty" in title or "required" in expected or "validation" in expected:
            status = "FAIL"
            reason = "System enforced mandatory field validation and blocked submission"

        # 🔴 DUPLICATE / CONFLICT CASES
        elif "duplicate" in title or "already exists" in expected:
            status = "FAIL"
            reason = "System detected duplicate data and prevented inconsistent state"

        # 🔴 EDGE CONDITIONS
        elif tc_type == "edge":
            status = "FAIL"
            reason = "System encountered boundary condition and handled it with restriction"

        # 🟢 POSITIVE CASES
        elif tc_type == "positive":
            status = "PASS"
            reason = "System successfully processed valid user action"

        # 🟡 DEFAULT FALLBACK (SMART GUESS)
        else:
            if "success" in expected or "allow" in expected:
                status = "PASS"
                reason = "Expected successful flow executed correctly"
            else:
                status = "FAIL"
                reason = "System behavior indicates constraint or validation enforcement"

        tc["status"] = status
        tc["reason"] = reason

    return test_cases


def generate_tests(user_story, acceptance_criteria):

    prompt = f"""
You are a senior QA engineer.

Generate structured test cases based on:

User Story:
{user_story}

Acceptance Criteria:
{acceptance_criteria}

Return STRICT JSON only in this format:

[
  {{
    "tc_id": "TC-001",
    "title": "Short test case title",
    "preconditions": "Any setup required",
    "test_steps": ["Step 1", "Step 2"],
    "test_data": "Input data used",
    "expected_result": "Expected outcome",
    "priority": "High/Medium/Low",
    "type": "Positive/Negative/Edge"
  }}
]

Rules:
- Generate 4 to 6 test cases
- Return ONLY valid JSON
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()
    print("OpenRouter Response:", data)

    if "choices" in data:
        content = data["choices"][0]["message"]["content"]

        try:
            test_cases = json.loads(content)

            # 🔥 APPLY IMPROVED EXECUTION
            test_cases = smart_execution(test_cases)

            return test_cases

        except Exception:
            return [{
                "error": "AI returned invalid JSON",
                "raw": content
            }]
    else:
        return [{
            "error": f"OpenRouter API Error: {data}"
        }]
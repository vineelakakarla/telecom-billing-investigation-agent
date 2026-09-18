import json
import requests
from pathlib import Path
from datetime import datetime


BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BASE_URL}/chat"

TEST_CASE_FILE = Path(__file__).parent / "test_case.json"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_FILE = RESULTS_DIR / "raw_results.json"


def load_test_cases():
    with open(TEST_CASE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def run_test_case(test_case):
    
    message = f"""{test_case["complaint"]} Customer ID: {test_case["customerId"]} Account ID: {test_case["accountId"]}Bill ID: {test_case["billId"]}"""

    payload = {
        "message": message.strip()
    }

    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return {
            "scenarioId": test_case["scenarioId"],
            "status": "SUCCESS",
            "complaint": test_case["complaint"],
            "actualResponse": data.get("response"),
            "error": None
        }

    except Exception as e:
        return {
            "scenarioId": test_case["scenarioId"],
            "status": "ERROR",
            "complaint": test_case["complaint"],
            "actualResponse": None,
            "error": str(e)
        }


def main():

    test_cases = load_test_cases()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    results = {
        "executionTimestamp": datetime.now().isoformat(),
        "totalScenarios": len(test_cases),
        "results": []
    }

    for test_case in test_cases:

        print(
            f"Running {test_case['scenarioId']}..."
        )

        result = run_test_case(test_case)

        results["results"].append(result)

        print(
            f"{test_case['scenarioId']} → {result['status']}"
        )

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nEvaluation execution completed.")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
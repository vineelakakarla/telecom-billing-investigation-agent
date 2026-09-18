# evaluation/evaluator.py

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
TEST_CASE_FILE = BASE_DIR / "test_case.json"
RAW_RESULTS_FILE = BASE_DIR / "results" / "raw_results.json"
EVALUATION_RESULTS_FILE = BASE_DIR / "results" / "evaluation_results.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_root_cause(expected, actual_response):
    if not actual_response:
        return False

    return expected.lower() in actual_response.lower()


def evaluate_evidence(actual_response):
    if not actual_response:
        return False

    # Initial implementation:
    # response must contain some evidence-oriented information.
    evidence_terms = [
        "bill",
        "charge",
        "usage",
        "event",
        "subscription",
        "discount",
        "tax",
        "roaming",
        "billing"
    ]

    response = actual_response.lower()

    return any(term in response for term in evidence_terms)


def evaluate_test_case(test_case, raw_result):

    if raw_result["status"] == "ERROR":
        return {
            "scenarioId": test_case["scenarioId"],
            "status": "ERROR",
            "reason": raw_result["error"]
        }

    actual_response = raw_result["actualResponse"]

    root_cause_passed = evaluate_root_cause(
        test_case["expectedRootCause"],
        actual_response
    )

    evidence_passed = True

    if test_case["evaluation"]["agentMustProvideEvidence"]:
        evidence_passed = evaluate_evidence(actual_response)

    checks = {
        "rootCause": root_cause_passed,
        "evidence": evidence_passed
    }

    passed_checks = sum(checks.values())
    total_checks = len(checks)

    if passed_checks == total_checks:
        status = "PASS"
    elif passed_checks > 0:
        status = "PARTIAL"
    else:
        status = "FAIL"

    return {
        "scenarioId": test_case["scenarioId"],
        "status": status,
        "checks": checks,
        "expectedRootCause": test_case["expectedRootCause"],
        "expectedOutcome": test_case["expectedOutcome"],
        "actualResponse": actual_response
    }


def main():

    test_cases = load_json(TEST_CASE_FILE)
    raw_results = load_json(RAW_RESULTS_FILE)

    raw_results_by_id = {
        result["scenarioId"]: result
        for result in raw_results["results"]
    }

    evaluation_results = []

    for test_case in test_cases:

        scenario_id = test_case["scenarioId"]

        raw_result = raw_results_by_id.get(scenario_id)

        if not raw_result:
            evaluation_results.append({
                "scenarioId": scenario_id,
                "status": "ERROR",
                "reason": "No execution result found"
            })
            continue

        result = evaluate_test_case(
            test_case,
            raw_result
        )

        evaluation_results.append(result)

        print(
            f"{scenario_id} → {result['status']}"
        )

    summary = {
        "totalScenarios": len(evaluation_results),
        "passed": sum(
            r["status"] == "PASS"
            for r in evaluation_results
        ),
        "partial": sum(
            r["status"] == "PARTIAL"
            for r in evaluation_results
        ),
        "failed": sum(
            r["status"] == "FAIL"
            for r in evaluation_results
        ),
        "errors": sum(
            r["status"] == "ERROR"
            for r in evaluation_results
        )
    }

    output = {
        "summary": summary,
        "results": evaluation_results
    }

    EVALUATION_RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        EVALUATION_RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nEvaluation completed.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
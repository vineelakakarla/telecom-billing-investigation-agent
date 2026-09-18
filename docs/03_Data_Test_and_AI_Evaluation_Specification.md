# 03 — Data, Test & AI Evaluation Specification

## 1. Purpose

This document defines the data used by the prototype, test scenarios, evaluation approach, grounding requirements, and success criteria.

## 2. Data Model

The prototype represents the following major billing entities:

```text
Customer
  |
Account
  |
Product
  |
Bill
  |
Bill Item
  |
Usage / Billing Event
```

The data is synthetic and stored in JSON files.

## 3. Data Used by the Agent

The investigation can use:

- Customer information
- Account information
- Product information
- Bill totals
- Bill items
- Usage events
- Billing events
- Historical billing information
- Billing knowledge/rules

## 4. Data-to-Tool Mapping

| Investigation Need | Capability |
|---|---|
| Identify customer | Customer retrieval |
| Understand account | Account retrieval |
| Inspect product charges | Product billing retrieval |
| Inspect current bill | Bill retrieval |
| Investigate customer billing history | Customer billing retrieval |
| Interpret billing rule | Billing knowledge retrieval |

## 5. Test Strategy

Testing covers:

1. Billing increase investigations.
2. Billing verification.
3. Billing errors.
4. Roaming-related investigations.
5. Multiple billing causes.
6. Investigation limitations.
7. Human-review scenarios.
8. Evidence grounding.
9. Non-invention/hallucination control.
10. Backend/agent failure handling.

## 6. Test Scenario Catalogue

| ID | Type | Customer | Account | Bill | Expected Root Cause |
|---|---|---|---|---|---|
| SC001 | BILLING_INCREASE | C1005 | A1010 | B10008 | Late-rated roaming event |
| SC002 | BILLING_INCREASE | C1001 | A1002 | B10001 | Increased usage |
| SC003 | BILLING_INCREASE | C1002 | A1003 | B10002 | New subscription charge |
| SC004 | BILLING_INCREASE | C1002 | A1004 | B10003 | Expired discount |
| SC005 | BILLING_INCREASE | C1003 | A1005 | B10004 | One-time charge |
| SC006 | BILLING_INCREASE | C1004 | A1007 | B10005 | Tax increase |
| SC007 | BILLING_ERROR | C1004 | A1008 | B10006 | Duplicate charge |
| SC008 | BILLING_VERIFICATION | C1005 | A1009 | B10007 | No billing issue |
| SC009 | BILLING_INCREASE | C1005 | A1010 | B10008 | Multiple billing causes |
| SC010 | INVESTIGATION_LIMITATION | C1006 | A1012 | B10009 | Insufficient information |
| SC011 | BILLING_INCREASE | C1007 | A1013 | B10010 | Roaming usage |
| SC012 | BILLING_VERIFICATION | C1007 | A1014 | B10011 | Bill comparison required |
| SC013 | BILLING_INCREASE | C1008 | A1015 | B10012 | Higher usage charges |
| SC014 | BILLING_ERROR | C1009 | A1017 | B10013 | Unrecognized charge |
| SC015 | HUMAN_REVIEW | C1009 | A1018 | B10014 | Human review required |

## 7. Evaluation Requirements

The existing `test_cases.json` is the source of truth for expected outcomes and evaluation flags.

The evaluation configuration requires:

- Evidence must be provided.
- Data must not be invented.
- Human review is allowed where applicable.

## 8. Evaluation Dimensions

### 8.1 Root Cause

Does the response identify the expected cause when the available data supports it?

### 8.2 Evidence

Does the response provide concrete billing evidence such as bill values, charge amounts, dates, events, products, or other retrieved information?

### 8.3 Grounding

Are factual billing claims supported by retrieved tool or knowledge results?

### 8.4 Non-Invention

Does the response avoid unsupported customer, billing, usage, tax, discount, or event information?

### 8.5 Expected Outcome

Does the response address the intended investigation outcome defined by the scenario?

### 8.6 Investigation Limitation

For insufficient-information cases, does the response clearly state what cannot be confirmed?

### 8.7 Human Review

For cases requiring human review, does the response avoid presenting an uncertain conclusion as a final confirmed resolution?

## 9. Grounding and Hallucination Tests

The evaluator should flag responses that:

- Introduce billing amounts not present in retrieved data.
- Introduce events not present in the data.
- Claim a product or charge exists without evidence.
- State a business rule as fact without relevant knowledge or data support.
- Present an unsupported root cause as confirmed.

## 10. Test Execution

The evaluation runner sends each scenario to the FastAPI `/chat` endpoint.

The request includes:

```text
Complaint
Customer ID
Account ID
Bill ID
```

The raw API response contains the application status and final response.

The evaluator should use the API `status` field as the execution status rather than introducing a separate `executionStatus` field.

## 11. Evaluation Metrics

| Metric | Definition |
|---|---|
| Scenario Pass Rate | Percentage of scenarios meeting required evaluation criteria |
| Root Cause Accuracy | Percentage of applicable scenarios with supported expected cause |
| Evidence Coverage | Percentage of applicable responses containing sufficient evidence |
| Grounding Rate | Percentage of factual claims supported by retrieved information |
| Non-Invention Rate | Percentage of responses without unsupported billing facts |
| Limitation Handling | Correct handling of insufficient-information scenarios |
| Human Review Handling | Correct escalation/qualification for review scenarios |
| Execution Success Rate | Percentage of scenarios completing without backend/agent execution failure |

## 12. Current Evaluation Status

Final evaluation metrics are pending the latest rerun after the agent-side LLM completion failure handling was implemented.

Earlier execution results included successful detailed responses for SC001–SC009 and backend failures for later scenarios caused by an LLM completion limit. Those earlier failures should not be treated as final agent-quality results.

## 13. Defect Analysis

When a scenario fails, classify the issue as one of:

- Data/retrieval issue
- Tool-selection issue
- Tool-execution issue
- Agent reasoning issue
- Grounding issue
- Prompt/guardrail issue
- Response-format issue
- Evaluation logic issue
- Infrastructure/LLM availability issue

## 14. Exit Criteria

The evaluation should be considered complete when:

- All 15 scenarios have been executed successfully or have a documented infrastructure exception.
- Root-cause expectations have been assessed.
- Evidence requirements have been assessed.
- Non-invention requirements have been assessed.
- Limitation and human-review cases have been assessed.
- Evaluation defects have been separated from infrastructure failures.
- Final metrics and observations have been documented.

# 05 — AI BA Portfolio Case Study

## 1. Executive Overview

The Telecom Billing Investigation Agent is an AI Business Analyst portfolio project focused on a practical telecom BSS problem: helping investigate why a customer's bill is higher than expected.

The project demonstrates the BA lifecycle from business problem identification through requirements, solution design, prototype implementation, testing, and AI evaluation.

## 2. Business Problem

A billing complaint can require investigation across several related entities. A support agent may need to inspect customer, account, product, bill, bill items, usage, billing events, historical billing information, and billing rules.

The project uses an AI agent to coordinate this investigation.

## 3. AI BA Role Demonstrated

The project demonstrates the following BA activities:

- Define the business problem.
- Establish objectives and scope.
- Identify stakeholders.
- Convert the problem into business and functional requirements.
- Define non-functional requirements.
- Model use cases and user stories.
- Identify business rules.
- Define data and tool requirements.
- Design AI-agent behavior.
- Define evaluation scenarios.
- Identify risks, security, privacy, and governance considerations.
- Assess prototype limitations.

## 4. Requirement-to-Solution Approach

```text
Business Problem
      |
Business Requirements
      |
Functional + Non-Functional Requirements
      |
Use Cases / User Stories
      |
Solution Architecture
      |
AI Agent + Tools + Knowledge
      |
Prototype
      |
Test Scenarios
      |
AI Evaluation
      |
Risk / Governance / Production Considerations
```

## 5. Proposed Solution

The prototype uses:

- Streamlit for the user interface.
- FastAPI for the backend API.
- LiteLLM Router for model abstraction.
- An LLM-based tool-calling agent.
- Billing retrieval tools.
- Synthetic telecom billing data.
- Billing knowledge and vector retrieval.
- Prompt guardrails.
- Controlled LLM and tool failure handling.

## 6. Example Investigation

A customer asks:

> Why is my bill higher this month?

The agent can:

1. Identify the relevant bill.
2. Retrieve bill details.
3. Inspect billing items/events.
4. Retrieve customer/account/product information where required.
5. Retrieve relevant billing knowledge.
6. Compare available billing information.
7. Identify evidence supporting a billing cause.
8. Explain the result in business-friendly language.

For example, one evaluation scenario involves a late-rated roaming event. The expected investigation outcome is that a previous-period roaming event was rated and billed in the current period.

## 7. Prototype Implementation

The implementation is organized around clear responsibilities:

```text
frontend/app.py
      |
backend/main.py
      |
telecom_billing_agent_litellm_app.py
      |
llm_router.py / llm_config.py
      |
tools.py
      |
billing_data_tool.py
      |
data/*.json
```

Knowledge retrieval is provided separately through the billing knowledge layer.

## 8. Important BA Design Decisions

### Tool-Based Investigation

Instead of asking the LLM to answer from general knowledge, billing information is retrieved through explicit tools.

### Evidence-Based Responses

The agent is instructed to use retrieved billing information and not invent values.

### Separation of Concerns

Billing-data business logic is separated from tool schemas and agent orchestration.

### Model Abstraction

LiteLLM provides a logical model interface so that the agent is not tightly coupled to a provider-specific implementation.

### Human Oversight

The solution assists investigation but does not autonomously perform billing corrections or financial adjustments.

## 9. AI Guardrails

The current prompt guardrails require the agent to:

- Use retrieved billing information.
- Avoid invented billing data.
- Avoid presenting unsupported causes as confirmed.
- State when available information is insufficient.

## 10. Evaluation Approach

Fifteen scenarios cover:

- Billing increases.
- Billing errors.
- Billing verification.
- Roaming.
- Multiple causes.
- Insufficient information.
- Human review.

Evaluation checks:

- Root cause.
- Evidence.
- Grounding.
- Non-invention.
- Expected outcome.
- Limitation handling.
- Human-review handling.
- Execution success.

Final evaluation metrics remain pending the latest rerun after LLM completion failure handling was added.

## 11. Challenges and Decisions

### Challenge: Tool Calling with LiteLLM

The initial migration encountered tool-calling issues.

**Decision:** Validate the LiteLLM Router independently and then implement the agent as a generic tool-calling loop.

### Challenge: Backend Failure

The `/chat` endpoint returned an internal error when an LLM completion failed.

**Decision:** Add controlled exception handling around LLM completion calls.

### Challenge: Tool Failure

A tool failure could otherwise terminate the investigation.

**Decision:** Convert tool exceptions into controlled tool results that can be handled by the agent.

### Challenge: Evaluation Context

The first evaluation runner sent only the complaint and omitted customer/account/bill identifiers.

**Decision:** Include scenario identifiers in the evaluation request.

## 12. Current Outcome

The prototype currently demonstrates:

- End-to-end Streamlit → FastAPI → agent flow.
- LiteLLM-based model routing.
- Tool-calling investigation.
- Billing data retrieval.
- Billing knowledge retrieval.
- Synthetic telecom billing data.
- Basic grounding guardrails.
- Controlled LLM failure handling.
- Controlled tool failure handling.
- Evaluation scenarios for representative billing cases.

## 13. Current Limitations

The project should not be presented as production-ready.

Current limitations include:

- Synthetic data.
- No production BSS/CRM integration.
- No formal performance benchmark.
- No production availability certification.
- Production security/privacy controls remain to be implemented.
- Final evaluation metrics are pending.
- Standardized response-format enforcement is still a refinement.

## 14. Interview Walkthrough

A concise interview explanation:

> “I designed a Telecom Billing Investigation Agent around a real BSS billing-support problem. I started with the business problem and translated it into business, functional and non-functional requirements, use cases, user stories and acceptance criteria. I then designed an agent architecture where the LLM does not directly invent billing answers; it calls controlled billing tools and retrieves billing knowledge. I implemented the prototype using Streamlit, FastAPI and LiteLLM, with synthetic telecom billing data. I also added guardrails for grounding and non-invention and explicit handling for LLM and tool failures. Finally, I defined 15 evaluation scenarios covering billing increases, billing errors, verification, limitations and human review.”

## 15. Interview Questions This Project Can Support

### Why did you use an AI agent?

Because the investigation can require multiple retrieval steps and decisions about which billing information is needed. Tool-calling allows the model to coordinate those steps.

### Why not use only RAG?

RAG is useful for billing rules and domain knowledge, but customer-specific billing facts must come from structured billing data. The solution therefore combines knowledge retrieval with tools.

### Why use LiteLLM?

It provides a model/provider abstraction layer and keeps the agent logic less dependent on one provider implementation.

### How did you address hallucination?

The agent is instructed to use retrieved billing information and knowledge, not invent billing data, and not confirm unsupported root causes.

### How did you test the agent?

Fifteen scenarios were defined with expected outcomes and evaluation requirements covering evidence and non-invention, along with limitation and human-review cases.

### What would you do before production?

Integrate real BSS/CRM sources, implement authentication and authorization, establish privacy controls, benchmark performance, add structured observability, complete security review, and finalize AI evaluation.

## 16. Portfolio Artifacts

The project artifacts are organized into:

1. Business Requirements & Functional Specification
2. Solution & AI Design Specification
3. Data, Test & AI Evaluation Specification
4. Risk, Security, Governance & Traceability
5. AI BA Portfolio Case Study

# 02 — Solution & AI Design Specification

## 1. Purpose

This document describes the solution architecture and AI design of the Telecom Billing Investigation Agent.

## 2. Solution Architecture

```text
Streamlit UI
     |
     | HTTP POST /chat
     v
FastAPI Backend
     |
     v
Billing Investigation Agent
     |
     +--------------------+
     |                    |
     v                    v
LiteLLM Router       Billing Tools
     |                    |
     v                    v
LLM Provider         Billing Data
                          |
                          v
                    Synthetic JSON

Agent
  |
  +--> Billing Knowledge / Vector Store
```

## 3. Implemented Components

| Component | Purpose |
|---|---|
| `frontend/app.py` | Streamlit user interface |
| `backend/main.py` | FastAPI application and `/health`, `/chat` endpoints |
| `backend/telecom_billing_agent_litellm_app.py` | Agent orchestration and tool-calling loop |
| `backend/llm_router.py` | LiteLLM Router integration |
| `backend/llm_config.py` | LLM/model configuration |
| `backend/tools.py` | Tool definitions, dispatch, and execution |
| `backend/billing_data_tool.py` | Billing data retrieval/business logic |
| `backend/prompts.py` | Agent instructions and guardrails |
| `knowledge/*.md` | Billing-domain knowledge |
| `data/*.json` | Synthetic telecom billing data |

## 4. End-to-End Flow

1. User enters a billing complaint in Streamlit.
2. Streamlit sends an HTTP POST request to FastAPI `/chat`.
3. FastAPI passes the request to the billing investigation agent.
4. The agent sends the request to the LiteLLM Router.
5. The LLM determines whether billing tools are required.
6. Tool calls are returned by the LLM.
7. The agent executes the requested tools.
8. Tool results are appended to the conversation.
9. The agent calls the LLM again using the retrieved evidence.
10. The loop continues until the LLM produces a final response.
11. FastAPI returns the response to Streamlit.

## 5. Agent Orchestration

The agent uses a tool-calling loop rather than attempting to answer billing questions from the prompt alone.

Conceptually:

```text
User Request
   |
LLM Decision
   |
Tool Call?
  / Yes  No
 |    |
Execute Tool
 |
Tool Result
 |
LLM Reasoning
 |
Final Response
```

This enables the agent to investigate multiple billing entities before producing an answer.

## 6. Tool Design

The tool layer separates tool schemas and dispatch from the underlying billing-data implementation.

Current retrieval capabilities include:

- Customer details
- Account details
- Product billing information
- Bill information
- Customer billing information
- Billing knowledge retrieval

The business logic remains in `billing_data_tool.py`, while `tools.py` provides the callable interface exposed to the LLM.

## 7. Knowledge and RAG

The knowledge layer contains telecom billing rules covering areas such as:

- Billing rules
- Roaming
- Tax
- Discounts
- Late rating
- Subscription
- Customer/account
- Order/service
- Payment
- Privacy/security/escalation

Knowledge retrieval is exposed through the `search_billing_knowledge(query)` capability.

The purpose is to provide business-rule context that cannot reliably be derived from raw billing records alone.

## 8. LLM and LiteLLM

LiteLLM provides an abstraction between the agent and the underlying LLM provider.

The project uses the logical model name:

```text
telecom-agent
```

The router configuration maps this logical model to the configured LLM provider/model.

Benefits of the abstraction include separation of agent logic from provider-specific configuration and easier future model changes.

## 9. Prompt Design

The agent instructions define:

- Role as telecom billing investigation assistant.
- Requirement to use billing tools when data is required.
- Requirement to analyze billing entities and knowledge.
- Requirement to explain supported causes.
- Requirement to use only retrieved information.
- Prohibition on invented billing data.
- Requirement to distinguish confirmed causes from unconfirmed possibilities.
- Markdown and currency-formatting guidance.

Basic guardrails are implemented in the prompt.

## 10. Failure Handling

### LLM Failure

LLM completion calls are wrapped with exception handling. A failure produces a controlled response rather than an uncontrolled API failure.

### Tool Failure

Tool execution is wrapped with exception handling. A failed tool call is returned to the agent as a controlled error result so that the model can handle the situation without fabricating data.

### Missing Billing Data

Existing billing retrieval logic handles unavailable customer/billing identifiers by returning a no-data outcome.

## 11. API Layer

The current backend exposes:

- `GET /health` — service health check.
- `POST /chat` — billing investigation endpoint.

The frontend communicates with the backend through HTTP rather than importing the backend agent directly.

## 12. Response Design

The current implementation provides business-friendly billing explanations grounded in retrieved data.

A more standardized response structure can be introduced as a later refinement, for example:

- Investigation Summary
- Root Cause
- Evidence
- Billing Impact
- Comparison
- Next Action

This is a response-design refinement, not treated as a completed implementation requirement in the current prototype.

## 13. Human-in-the-Loop

The agent is designed as an investigation assistant rather than an autonomous billing correction system.

Human review remains appropriate when:
- Evidence is insufficient.
- A billing dispute requires operational action.
- A financial adjustment is required.
- Production business rules require escalation.

## 14. Prototype vs Production

### Prototype

- Synthetic billing data.
- Streamlit UI.
- FastAPI backend.
- LiteLLM Router.
- Tool-calling agent.
- Billing knowledge retrieval.
- Basic AI guardrails.
- Controlled LLM/tool failures.

### Production Considerations

- Authentication and authorization.
- Real BSS/CRM/billing integration.
- Production vector-store controls.
- Data privacy and retention.
- Structured observability.
- Performance/load testing.
- Availability and disaster recovery.
- Security review.
- Human escalation workflow.

## 15. Key Design Decisions

1. Keep billing retrieval logic separate from agent orchestration.
2. Expose business capabilities through controlled tools.
3. Use LiteLLM to abstract the model provider.
4. Use knowledge retrieval for billing-rule context.
5. Use tool results as evidence for billing explanations.
6. Handle LLM and tool failures explicitly.
7. Use synthetic data for the prototype.

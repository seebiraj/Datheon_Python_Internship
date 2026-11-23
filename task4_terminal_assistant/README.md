# Task 4: Rule-Based Interactive Terminal Assistant / Chatbot

## Overview & Goal
Build a responsive conversational terminal assistant with multi-intent recognition using keyword matching and Python's regular expressions (`re`) module.

## Features
- **Multi-Intent Recognition Taxonomy**:
  - `greeting`: Welcomes the user with contextual salutations.
  - `business_hours`: Operating schedule and platform availability.
  - `products_catalog`: Suite of services, developer programs, and tracks.
  - `pricing_discounts`: Free tier policies and enterprise scopes.
  - `refund_returns`: Money-back guarantee and terms.
  - `technical_support`: Troubleshooting and developer environment guidance.
  - `contact_agent`: Support email and LinkedIn directory.
  - `datheon_internship`: 4-week task milestones, submission instructions, and certification criteria.
  - `help_topics`: Interactive directory menu.
  - `goodbye`: Graceful conversation teardown.
- **Conversational State Management**:
  - `INIT` -> `AWAITING_QUERY` -> `RESOLVED` / `FALLBACK` -> `EXIT`
- **Dynamic Dataset Configuration**: Decoupled from Python code via `faq_dataset.json`.
- **Intelligent Fallback Architecture**: Offers suggestions and available topics when confidence is low.
- **Clean Exit Commands**: Recognizes `bye`, `exit`, `quit`, and `goodbye`.

## File Manifest
- `chatbot.py`: Main interactive assistant engine and command-line interface.
- `faq_dataset.json`: Structured intent schemas, regex patterns, and response pools.
- `demo_run.py`: Scripted automated dialogue validation suite.

## How to Run
```bash
# Interactive terminal chat
python task4_terminal_assistant/chatbot.py

# Automated test demo
python task4_terminal_assistant/demo_run.py
```

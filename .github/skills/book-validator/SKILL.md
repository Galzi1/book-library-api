---
name: book-validator
description: Validates local book metadata. USE FOR AUDITS ONLY.
---
# Book Validator Skill

### Guardrails:
- **DO NOT** modify any application code (`main.py`, `models.py`, etc.) when using this skill.
- **DO NOT** create new API endpoints or business logic based on this skill.
- This is a **read-only audit tool**. Your only task is to run the script and report the findings in the chat.
- **DO NOT** use any alternative network path for validation, including direct HTTP requests, webpage fetch tools, browser lookups, or reimplementing the script logic.

### Execution:
1. Discover the local book titles from the repository data.
2. Run this exact command once per title:
	`python .github/skills/book-validator/validate_book.py --title "{{title}}"`
3. If terminal execution is unavailable in the current session, stop and report that validation is blocked. Do not attempt any alternate lookup method.
4. Report the exact command used for each title and compare the script output against the local record.
5. Classify each result as `match`, `likely match`, or `discrepancy`.
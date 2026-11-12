# Call Center App dashboard

**Feature** 001 · **Status** Initial specification for partner review

A call center manager can compare team and agent performance, investigate a weekly trend, and choose a coaching focus using fictional data. The [bake-off contract](../../Documents/Call%20Center%20App%20Contract.docx) defines the shared tests and scoring. The [reporting and governance document](../../Documents/Call%20Center%20Spec.docx) records additional credit union reporting ideas for discussion.

## Manager workflows

1. **Review performance (P1).** Open the dashboard on the shared dataset of 20 fictional agents, three teams and eight weeks. See calls handled, first-contact resolution, customer satisfaction, average handling time and quality review score.
2. **Compare agents (P1).** Choose a team and an inclusive date range. Every summary, comparison row, trend and coaching suggestion reflects that selection.
3. **Select a coaching priority (P1).** Open an agent to see the measured value, fictional target and reason for each suggestion. Insufficient observations suppress the corresponding advice.
4. **Inspect a trend (P2).** Review weekly results for an individual agent and reconcile them to the selected period.

## Calculation and coaching rules

Compute rates from summed numerators and denominators. Display rates, quality and minutes to one decimal place and apply thresholds before rounding. Zero denominators display N/A.

| Measure | Calculation | Coaching condition |
| --- | --- | --- |
| Calls handled | Sum of handled calls | Context only |
| Quality | Total quality points / review count | Below 90 out of 100 with at least 3 reviews |
| Resolution | Resolved on first contact / calls handled | Below 80% with at least 20 calls |
| Satisfaction | Positive ratings / responses | Below 85% with at least 5 responses |
| Handling time | Total handling seconds / calls handled / 60 | Above 8 minutes with at least 20 calls, and sufficient evidence that quality and resolution meet target |

Show up to three priorities in table order, starting with quality. With sufficient data and no triggers, show “Maintain current performance.” With incomplete evidence and no triggers, explain that the assessment is incomplete.

## Acceptance and boundaries

Use contract tests AT01 through AT10 for both builds. Include weighted aggregation, exact-target values, insufficient observations, invalid rows, empty results and changing teams while viewing an agent. For example, 8 of 10 and 45 of 90 calls resolved together yield 53.0%. A manager should be able to filter, compare, inspect a trend and explain one coaching suggestion.

Use the same generated CSVs for both builds. Login, live integrations, real employee data and saved coaching notes are outside this first version. Before implementation, the partners should freeze the shared files and confirm whether any additional credit union reports belong in the scored scope.

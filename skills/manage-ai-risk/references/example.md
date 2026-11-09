# Teaching example

## Request
An AI agent processes 2,000 invoice drafts per month. A teaching assumption is 2% harmful errors and USD 100 mean loss per harmful error. A claimed control blocks 75%, but no test has run. Show exposure and next steps.

## Response checks
Calculate USD 4,000 monthly inherent expected direct loss. USD 1,000 is only a conditional illustration if 75% effective, not verified residual exposure. Keep control cost and tail scenarios separate; propose tests and owners.


## Completed teaching calculation
Scope: 2,000 invoice drafts per month; probability 2% per draft that an error survives review and causes a harmful outcome; mean direct loss USD 100 conditional on a harmful error. These are teaching assumptions, not measured results.
Expected harmful errors: 2,000 × 0.02 = 40 per month. Expected direct loss: 40 × USD 100 = USD 4,000 per month. The model assumes the exposure count and conditional loss describe the same workload; it excludes other harms and control cost.
A proposed 75% effective control would leave 40 × (1 − 0.75) = 10 harmful errors and USD 1,000 expected direct loss per month under the same assumptions. That is a conditional illustration, not verified residual exposure. Effectiveness has not been measured.
Failure flow: invoice source → extraction → amount draft → review → posting. A wrong amount that passes review can cause a loss; a detected draft error may cause rework instead.
Control test: finance operations prepares a held-out sample with known correct values, including unusual formats and missing information. Measure harmful errors caught and missed, review time, false alarms and duplicate-posting prevention. Set sample size and acceptance criteria with the risk owner before running it.
Tail scenario: a shared parsing fault affects many invoices, or a large invoice is wrong while the reviewer is unavailable. Estimate those consequences separately; the average USD 100 must not hide them.
Decision: risk owner to review test results and control cost before accepting exposure. No mitigation date or risk acceptance is confirmed.

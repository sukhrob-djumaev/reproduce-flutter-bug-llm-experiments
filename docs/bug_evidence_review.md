# Evidence review: what published studies say about the bug mix (draft, docs only)

Prepared 2026-10-12 at the user's request, after the model-selection review. This is a first-pass search, not a systematic review. Search snippets and abstracts were read; full-text percentages were **not** verified unless stated. It proposes nothing to the protocol; any change to protocol §6 (taxonomy) or §7 (dataset composition) is an amendment requiring user approval, a new experiment version, and separate reporting.

## What we were looking for
Evidence to justify (a) the four defect classes in §6, and (b) the target proportions in §7 (about 25 cases: unhandled exception 5–7, incorrect application state 6–8, structural rendering fault 5–7, silent error condition 5–7).

## What was found
| Question | Finding | Source |
| --- | --- | --- |
| Is there a published bug-taxonomy/distribution study specific to Flutter? | **None found** in three searches (one extended). The closest are a 2017 proposal to mine cross-platform framework bugs (no results) and a Stack Overflow topic study of Flutter questions (developer difficulties: state management, widgets, navigation, packages, persistence; not framework defects). | [arXiv 1701.06767](https://arxiv.org/pdf/1701.06767), [Wambua et al., 2024](https://www.researchgate.net/publication/381224589_What_Do_Flutter_Developers_Ask_About_An_Empirical_Study_on_Stack_Overflow_Posts) |
| Android functional vs crash bugs | 399 functional bugs from 8 open-source Android apps analyzed for root causes, symptoms and oracles (ISSTA 2023; no distribution in the abstract). 1,862 confirmed crash reports from 418 open-source apps (MOBILESoft 2019). | [ISSTA 2023](https://2023.issta.org/details/issta-2023-technical-papers/97/An-Empirical-Study-of-Functional-Bugs-in-Android-Apps), [MOBILESoft 2019](https://research.knu.ac.kr/en/publications/characterizing-android-specific-crash-bugs/) |
| Crash share in bug-reproduction benchmarks | ReBL's evaluation set: 96 reports from 54 apps, **73 crash (76%) / 23 non-crash (24%)**, assembled from six existing sources after removing duplicates, uninstallable and no-longer-reproducible reports. TreeMind uses 93 reports from three benchmarks and focuses on crashes. | [ReBL, arXiv 2407.05165](https://arxiv.org/html/2407.05165), [TreeMind](https://arxiv.org/abs/2509.22431v2) |
| Generic symptom shares in another domain | Federated-learning frameworks: functional errors 544/1,119 and crashes 341/1,119 (≈49% and ≈30%). Not transferable to Flutter. | [arXiv 2308.05014](https://arxiv.org/pdf/2308.05014) |

## Observations (not conclusions)
1. Flutter-specific evidence is missing in what I found, so the Flutter mix cannot be justified from a published Flutter study yet. That absence is itself reportable.
2. Adjacent Android evidence consistently separates **crash** from **non-crash/functional** bugs and shows benchmark sets skew toward crashes, partly because crashes are easier to reproduce and score. Our classes map roughly: `unhandled_exception` ≈ crash/exception; `incorrect_application_state` ≈ functional; `structural_rendering_fault` ≈ UI/rendering (no clear published counterpart found); `silent_error_condition` ≈ functional/logging with no crash.
3. Our current pool (5 unhandled exception, 6 incorrect state, 2 structural, 0 silent; 10 of 13 from flutter/flutter) follows what could be reproduced, not a published distribution, and the §7 quotas are design targets without a cited basis.
4. Reproducibility filtering will bias any dataset. A defensible claim is "proportions among reproducible, independently scoreable UI bugs", with deviations documented.

## Options for the user (no action taken)
A. **Keep §6/§7 as designed** and state in the write-up that they are design choices, with this review as the stated search for evidence and its null result for Flutter.
B. **Deeper bounded review:** read the full ReBL, ISSTA 2023 and MOBILESoft 2019 papers for category definitions and shares, and search MSR/ICSE/EMSE directly for Flutter or cross-platform studies.
C. **Measure it ourselves:** sample flutter/flutter and popular package issues (using the existing repository labels such as crash/regression plus a manual classification of a random sample into our four classes) and report the observed distribution with sampling details. Strongest evidence, most effort; needs a defined sampling protocol approved first.

Recommendation: B first (cheap, produces citations), then decide on C only if B confirms no Flutter-specific study; adjust §7 only through a documented amendment.

## Limits
Search was done with a general web search tool, with US-only results; databases (ACM DL, IEEE Xplore, Scholar) were not queried. Several results came from aggregator pages. Treat all numbers above as leads until checked against the papers.

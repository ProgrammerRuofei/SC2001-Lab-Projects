# Execution Plan and Completion Criteria

The plan uses work stages without assuming calendar dates. Complete the four assignment requirements before deciding on extensions.

| Stage | A | B | C | Completion criterion |
| --- | --- | --- | --- | --- |
| 1: Understanding and interfaces | Explain recurrence and base cases | Trace examples and start graph | Learn entry point; run framework checks | All members agree on unlimited supply and unused capacity |
| 2: Implementation and reasoning | Write DP, pseudocode, and proof | Complete graph and independent enumeration | Prepare report; review CLI | Core TODO resolved and graph fully expanded |
| 3: Integration checks | Fix algorithm issues | Run fixed cases and enumeration comparisons | Save actual output | make test and make check-solution both pass |
| 4: Submission preparation | Review theory and complexity | Review graph and manual results | Assemble report and reproduction steps | Every requirement maps to a completed deliverable |

## Dependencies

Shared interfaces -> DP implementation -> algorithm acceptance -> two actual sample runs -> final result discussion.

Recurrence derivation, graph construction, manual examples, and the report structure can proceed alongside DP implementation. Independent enumeration can be written first, but comparison requires the DP implementation.

## Final checklist

- [ ] Part (1): recurrence includes base cases, legal-item conditions, and the case where no item fits.
- [ ] Part (2): complete P(15) dependency graph, including all legal branches.
- [ ] Part (3): bottom-up pseudocode and evaluation-order explanation match the code.
- [ ] Part (4): general implementation and actual outputs of 28 and 16 for the two examples.
- [ ] Fixed cases, boundary cases, and independent small-case enumeration checks pass.
- [ ] All members can trace at least one complete small example.
- [ ] Final report TODOs are resolved and actual result provenance is preserved.
- [ ] All documentation and report content, including figure labels and captions, is in English.
- [ ] Submission format and deadline are checked against separate course notices.

## Current completed work

Directory structure, shared types and interfaces, assignment fixtures, CLI entry point, validation, output formatting, Makefile, initial tests, and working documents are provided. The solver, complete subproblem graph, formal execution results, and final report remain team tasks.

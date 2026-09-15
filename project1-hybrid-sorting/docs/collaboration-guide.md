# Collaboration guide

This document records our team conventions. These are not additional course
requirements.

## Branches

- `main` is the stable branch for reviewed milestones and final deliverables.
- `develop` is the integration branch for completed team work.
- Each task is developed on a short-lived branch created from `develop`.

Use descriptive branch names:

- `feature/insertion-sort`
- `feature/merge-sort`
- `feature/experiment-runner`
- `docs/report-analysis`
- `fix/comparison-counting`

Do not implement new work directly on `main`. Avoid direct work on `develop`
when a feature branch is practical.

## Starting a task

Before creating a feature branch:

```bash
git switch develop
git pull
git switch -c feature/short-description
```

Tell the other members which files or task you are working on, especially before
editing shared files such as `sorting.hpp`, `sorting.cpp`, or experiment-result
summaries.

## Commits

- Keep each commit focused on one logical change.
- Use concise commit messages that describe the change.
- Do not commit build outputs, virtual environments, editor settings, or large
  generated input arrays.
- Small CSV summaries and useful figures may be committed.
- Do not commit results that have not been checked or whose generation settings
  are undocumented.

Example commit messages:

```text
Add insertion sort implementation
Add duplicate-value sorting tests
Document fixed-S experiment procedure
```

## Pull requests into develop

1. Push the feature branch to GitHub.
2. Open a pull request targeting `develop`, not `main`.
3. Describe what changed, how it was tested, and any unresolved questions.
4. Ask at least one other team member to review it.
5. Address review comments and confirm that the project builds and relevant
   tests pass before merging.
6. Delete the feature branch after it has been merged and is no longer needed.

The author should not merge while requested changes remain unresolved.

## Correctness and measurement review

For sorting changes, reviewers should check:

- correctness and boundary cases;
- inclusive range assumptions: `[left, right]`;
- possible off-by-one or out-of-bounds access;
- key-comparison counting against
  [`comparison-counting.md`](comparison-counting.md);
- that tests compare the result with a trusted sorted result;
- that algorithm code remains separate from experiment infrastructure.

## Experiment changes

- Record the input size `n`, threshold `S`, random-value range, number of runs,
  timing method, and relevant environment details.
- Reuse equivalent input data when comparing algorithms in the same experiment.
- Keep raw large datasets and raw run files out of Git.
- Do not edit measured values manually. If processing is required, keep the
  processing script or document the procedure.
- Clearly distinguish proposed parameters, actual parameters, and results.

## Merging develop into main

Merge `develop` into `main` only for a reviewed milestone. Before opening the
pull request:

- confirm the program builds from a clean checkout;
- run all current correctness tests;
- confirm required documentation is current;
- check that no large generated data or local build files are included;
- ask at least one teammate to review the pull request.

Use a pull request from `develop` to `main`. Do not force-push either shared
branch. For the final submission milestone, all three members should confirm the
contents before merging.

## Merge conflicts

Do not resolve conflicts by discarding another member's changes without checking
with them. Update the feature branch from `develop`, resolve each conflict
deliberately, rebuild, rerun relevant tests, and ask for help when the intended
behavior is unclear.

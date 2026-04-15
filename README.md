# innersource-scorecard

> Inner-source health scorecard — grades repos on discoverability, documentation, contribution friction, and adoption.

![CI](https://github.com/brianpelow/innersource-scorecard/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`innersource-scorecard` grades any GitHub repository against a
comprehensive inner-source health rubric covering discoverability,
documentation quality, contribution friction, and adoption signals.
It generates a letter grade and AI-powered improvement recommendations.

Built for platform engineering teams in regulated financial services
and manufacturing who want to systematically improve the reusability
and quality of internal shared services.

## Scorecard dimensions

| Dimension | Weight | Checks |
|-----------|--------|--------|
| Discoverability | 25% | README, description, topics, license |
| Documentation | 30% | ADRs, CONTRIBUTING, CHANGELOG, API docs |
| Contribution friction | 25% | PR templates, CI, issue templates, CODEOWNERS |
| Adoption signals | 20% | Stars, forks, external contributors, recent activity |

## Quick start

```bash
pip install innersource-scorecard

innersource-scorecard score brianpelow/repoforge
innersource-scorecard score brianpelow/repoforge --format json
innersource-scorecard batch brianpelow --limit 10
```

## Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Exemplary inner-source health |
| B | 75-89 | Good, minor improvements needed |
| C | 60-74 | Adequate, notable gaps |
| D | 45-59 | Poor, significant work required |
| F | 0-44 | Failing inner-source standards |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0
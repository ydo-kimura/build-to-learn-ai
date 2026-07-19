# Curriculum Review Fix Plan

This plan is the single source of truth for the current curriculum review remediation.

## Scope

- Japanese curriculum under `curriculum/`
- Documentation and visual assets only; no application runtime redesign
- Preserve existing user changes and unrelated worktree changes

## Plan-Level Checklist

- [x] 1. Add explicit learning objectives, prerequisites, effort guidance, and staged practice guidance to the roadmap.
- [x] 2. Correct structural inconsistencies in Units 36 and 37 and clarify capstone boundaries.
- [x] 3. Correct Transformer explanations and examples, including positional information and toy-model limitations.
- [x] 4. Correct Agent, structured extraction, evaluation, and security claims so validation is not presented as a guarantee.
- [x] 5. Improve practice scaffolding and failure-mode exercises for beginner progression.
- [x] 6. Align visual explanations and document cover/diagram guidance with each unit's actual implementation.
- [x] 7. Run build, diagram, Markdown/code, link, and asset checks; update audit and state.
- [x] 8. Add Unit 0 scope guidance, Unit 22 tokenizer foundations, and Unit 23 token-count/streaming practice.
- [x] 9. Add Unit 35/36 foundational chapters, shift Capstones to Unit 37〜42, and update navigation and references.
- [x] 10. Synchronize the English curriculum with Unit 0〜42 structure, Unit 22/23 additions, and Unit 35/36 content.

## Completion Evidence

- `npm run docs:build`
- `python3 scripts/verify_curriculum_diagrams.py`
- Python fenced-block syntax validation
- Local Markdown link and image-reference validation
- Review of all changed files against this checklist

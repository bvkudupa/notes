---
name: organize-course-notes
description: Organize rough course notes, scripts, data, and screenshots into a numbered lesson folder and integrate the material into the chapter's single README. Use when the user asks to organize everything, patch rough notes, or prepare the next course session.
---

# Organize course notes

When the user asks to organize course notes (including "organize everything"),
finish the whole staging-to-documentation workflow in one pass. The user
should only need to provide topic details or missing screenshots when the
material does not establish them.

## Workflow

1. Identify the chapter root, its single README, and all `rough_notes.md`
   files. Read every rough note completely. Inspect every related script,
   data file, screenshot, and existing lesson folder before editing.
2. Infer the topic and sequence from the notes and assets. If an essential
   topic detail or screenshot is genuinely missing or ambiguous, ask one
   focused question using the ask-user tool. Otherwise proceed without asking
   the user to restate context.
3. Follow the chapter's existing numbered lesson and directory conventions.
   If the material is a new lesson, create the next appropriately numbered
   folder. Group scripts and input/output data with that lesson; put lesson
   visuals in its `screenshots/` subfolder.
4. Rename generic screenshots (`image.png`, `image-1.png`, etc.) to concise,
   descriptive kebab-case names based on their content. Update every affected
   Markdown reference. Do not rename screenshots with established,
   meaningful names without a reason.
5. Integrate all useful teaching content from the rough notes into the
   chapter README: lesson title and learning-path entry, explanations,
   commands, relevant code examples or links to runnable scripts, and
   screenshots. Preserve technical meaning, correct inaccurate explanations
   when facts can be verified, and use relative links consistent with the
   chapter.
6. Make moved scripts work from the documented command location and avoid
   machine-specific absolute paths. Preserve existing behavior and unrelated
   work. Do not move, overwrite, or delete generated databases or other local
   data without checking their purpose and adding an appropriate ignore rule.
7. Only after confirming that every useful point, asset, and code sample from
   the rough notes is represented in the README or its referenced lesson
   files, clear the contents of `rough_notes.md` while keeping the file as an
   empty staging file for the next session. Never clear notes containing
   unprocessed or omitted material.
8. Validate README relative links, screenshot references, script syntax, and
   `git diff --check`. Run focused tests or example checks when applicable.
   Report what was organized, any verification, and any material left
   unprocessed.

## Constraints

- Keep one chapter README unless the chapter already uses another convention.
- Make changes surgical and consistent with neighboring lessons.
- Do not silently drop rough-note content; link or incorporate it.
- Do not commit unless explicitly asked.
- Use Markdown file links in the final response for workspace files.

# Contributing to Pinecone Agent Reference

Thank you for your interest in contributing! This project provides instructions for AI coding assistants, so contributions must be concise, avoid duplication, and maximize value per token.

## How to Contribute

- **Reporting bugs** - Issues with instructions not working as expected
- **Fixing bugs** - Errors in documentation or code examples
- **Improving clarity** - Making instructions more effective for assistants
- **Removing redundancy** - Eliminating duplicate or unnecessary content
- **Adding essential content** - Only when it fills a critical gap

## Getting Started

1. Fork and clone the repository
2. Create a branch: `git checkout -b your-branch-name`
3. Make your changes following the guidelines below
4. Test with an actual coding assistant (see Testing section)
5. Submit a pull request

## Contribution Guidelines

### Token Efficiency (Critical)

This documentation is consumed by AI assistants, so every token counts:

- **Be concise** - Remove unnecessary words, examples, or explanations
- **Avoid duplication** - Don't repeat information already covered elsewhere
- **Eliminate redundancy** - If something is explained in `PINECONE.md`, don't repeat it in language-specific files
- **Skip obvious content** - Don't explain basic concepts assistants already know
- **Prefer references** - Link to detailed docs rather than copying content
- **Remove filler** - Cut phrases like "it's important to note", "as you can see", etc.

### Documentation Standards

- **Accuracy**: Code examples must work with current SDK versions
- **Clarity**: Direct, actionable instructions
- **Completeness**: Include only essential context
- **Consistency**: Follow existing style and structure

### Code Examples

- **Minimal examples** - Show only what's necessary, not full applications
- **Test all examples** - Verify they work before submitting
- **Current SDKs only** - Use latest stable versions
- **Essential imports** - Include only what's needed
- **No verbose comments** - Code should be self-explanatory or minimally commented

### Markdown Formatting

- Proper heading hierarchy
- Language tags for code blocks
- Consistent formatting
- No unnecessary formatting (avoid excessive bold, italics, etc.)

### File Organization

- Documentation in `.agents/` folder
- Naming: `PINECONE-{topic}.md`
- Update `PINECONE.md` navigation when adding files
- Keep related content together

### Link Verification

If your changes add or modify any URLs:

- **Run the link checker**: `python3 utils/check_links.py --recursive`
- **Fix broken links** before submitting
- See `utils/README_check_links.md` for usage details

## Testing

**Critical**: All changes must be tested with an actual coding assistant to verify the instructions work.

### Testing Process

1. **Install your changes** in a test project:

   ```bash
   # Copy .agents/ folder to a test project
   # Add snippet to AGENTS.md (or CLAUDE.md/GEMINI.md)
   ```

2. **Test with an assistant**:

   - Ask questions related to your changes
   - Verify the assistant references the correct documentation
   - Confirm the assistant provides accurate answers based on your changes
   - Check that instructions are followed correctly

3. **What to verify**:

   - Does the assistant find and use the new/changed instructions?
   - Are the instructions clear enough for the assistant to follow?
   - Does the assistant avoid outdated or incorrect information?
   - Is the response accurate and helpful?

4. **Document your testing** in the PR:
   - Which assistant(s) you tested with (Cursor, Claude Code, etc.)
   - What questions you asked
   - What responses you received
   - Any issues encountered

### Testing Checklist

- [ ] Changes tested with at least one coding assistant
- [ ] Assistant correctly references new/changed documentation
- [ ] Assistant provides accurate information
- [ ] No confusion or incorrect guidance observed
- [ ] Code examples work when tested
- [ ] URLs verified (if any URLs were added/modified): `python3 utils/check_links.py --recursive`

## Pull Request Process

1. **Update your fork**:

   ```bash
   git remote add upstream https://github.com/pinecone-io/pinecone-agents-ref.git
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make changes** following guidelines above

3. **Test thoroughly**:

   - Verify markdown renders correctly
   - Test code examples
   - **Test with a coding assistant** (required)
   - **Check URLs** - If you added or modified any URLs, verify them using `utils/check_links.py`:
     ```bash
     python3 utils/check_links.py --recursive
     ```
     Or check specific files:
     ```bash
     python3 utils/check_links.py --files path/to/file.md
     ```

4. **Commit**:

   ```bash
   git commit -m "Brief description"
   ```

5. **Push and open PR** with:
   - Clear title
   - Description of changes and why
   - Testing details (which assistant, what you tested)
   - Related issue numbers

### Commit Messages

- Imperative mood: "Add Python example" not "Added Python example"
- First line under 72 characters
- Reference issues: "Fix typo (#123)"

## What to Contribute

### High Priority

- **Bug fixes** - Errors, broken examples, incorrect information
- **SDK updates** - Keeping examples current
- **Token optimization** - Removing redundancy and unnecessary content
- **Clarity improvements** - Making instructions more effective

### Medium Priority

- **Essential examples** - Only if they fill a critical gap
- **Cross-references** - Helpful navigation links

### Avoid

- **Verbose explanations** - Keep it concise
- **Duplicate content** - Reference instead of copying
- **Obvious information** - Skip what assistants already know
- **Formatting-only changes** - Unless fixing inconsistencies
- **Major additions** - Discuss in an issue first

## Reporting Issues

When reporting issues:

- **Clear title** describing the problem
- **Context** - What were you trying to do?
- **Assistant tested** - Which assistant(s) you used
- **Expected vs actual** - What should happen vs what happened
- **Affected files** - Which documentation files
- **Check duplicates** - Search existing issues first

## Review Process

- All PRs reviewed by maintainers
- Reviews focus on: accuracy, token efficiency, and assistant effectiveness
- Testing with assistants is required
- Feedback may be requested - please be responsive
- Once approved, changes will be merged

Thank you for contributing! 🎉

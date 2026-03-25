---
name: jupyter-analysis
description: 'Skill to read, analyze, process Jupyter Notebooks (.ipynb) as Technical Research Reports with LaTeX, citations, and theory-code-result integration (Astrophysics)'
argument-hint: 'Mention the target notebook file'
---

# Jupyter Analysis Skill

## When to Use
- Whenever the user asks you to analyze, read, summarize, or debug a Jupyter Notebook (`.ipynb`).
- When extracting code, deciphering outputs, and generating formal technical research reports.

## Tools & Procedure
1. **Contextualize**: Understand the overarching project context by reading files like `CONTEXT.md` or `CLAUDE.md`.
2. **Get Notebook Summary**: Use the `copilot_getNotebookSummary` tool first with the absolute path of the notebook.
3. **Avoid Raw JSON**: Do not use `read_file` on the entire `.ipynb` file right away to avoid base64 image strings and metadata pollution.
4. **Read Specific Contents**: Using the line ranges from the summary, use the `read_file` tool to inspect specific code or Markdown cells.
5. **Inspect Outputs**: Use the `read_notebook_cell_output` tool to read outputs, tracebacks, and results.

## Report Generation (Technical Research Report)
Your primary goal is to generate a comprehensive, well-structured Technical Research Report in Markdown format.

**⚡ CRITICAL INSTRUCTIONS (MUST FOLLOW):**
1. **Explicit Code Blocks**: You MUST extract and show the referenced code within markdown code blocks (e.g., ` ```python `). Include the full cell if necessary or its logical flow. **Crucially, preserve all original inline comments.** Do not just summarize what the code does; you MUST display the code itself.
2. **Render Images Directly**: Images and figures produced by the notebook MUST be displayed visually directly within the markdown report. You must link, embed, or save the actual outputs so the images render inline in the final document, not just describe them textually.
3. **Direct Cell Linking**: To guarantee navigability, EVERYTHING (theory, code, results, images) must have an integrated link connecting DIRECTLY to the specific cell in the notebook. Use VS Code's file link format with line numbers corresponding to the start of the cell (e.g., `[Cell 3: Data Load](notebook.ipynb#L45)`).

### General Formatting & Structure:
- **Theory-Code-Result Flow**: Contextualize the project. Link **theory + code + result** for each cell to seamlessly interrelate the entire pipeline.
- **Theory & Justification**: Explain the *why* and *how*. You MUST include the mathematical, statistical, theoretical, or physical underpinnings (crucial for astrophysics notebooks). Use LaTeX (`$math$`, `$$math$$`) for all mathematical expressions.
- **Tests & Trials**: Extract and explicitly describe all results, including explanations of any tests or trials present in the notebook, even if they seem disorganized.
- **Citations & References**: Reference all theoretical foundation, methods, and external knowledge using formal alphanumeric citation style (e.g., [1], [2]). At the end of the report, include a formal **References** section detailing all sources.

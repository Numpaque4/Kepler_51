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

- **Structure**: Contextualize the project, explain where it comes from, how it is implemented, and what is obtained. Link **theory + code + result** for each cell to seamlessly interrelate the entire flow.
- **Navegability & Links**: To guarantee navigability between the report and the notebook, EVERYTHING must have an integrated link connecting to the specific section of the notebook (e.g., Markdown anchors or explicit VS Code file links with line numbers like `[notebook.ipynb](notebook.ipynb#L10)` or referencing explicit cell names/numbers) where the figures, code cells, or results are visualized.
- **Theory & Justification**: Explain the *why* and *how*. You MUST include the mathematical, statistical, theoretical, or physical underpinnings (crucial for astrophysics notebooks).
- **Formatting**: Use Markdown extensively. Use LaTeX (`$math$`, `$$math$$`) for all mathematical expressions. Use properly styled code blocks.
- **Results, Images, and Tests**: Extract and explicitly describe all results. Reference inline images and figures, explaining what they represent within the flow. Include explanations of any tests or trials present in the notebook, even if they seem disorganized.
- **Citations & References**: Reference all theoretical foundation, methods, and external knowledge using formal alphanumeric citation style (e.g., [1], [2]). At the end of the report, include a formal **References** section detailing all sources, including any implicit knowledge or searches you performed to sustain the analysis.

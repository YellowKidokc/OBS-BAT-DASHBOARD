# Adaptive YAML Builder

Files:
- adaptive_yaml_builder.py
- adaptive_yaml_schema.yaml
- adaptive_yaml_memory.json (auto-created after first run)
- LAUNCH_ADAPTIVE_YAML.bat

What it does:
- Suggests values based on your past selections
- Carries `tags` forward automatically every run
- Prompts row-by-row and asks: "Done with this row?"
- Writes YAML frontmatter back to the target note

Run:
- LAUNCH_ADAPTIVE_YAML.bat "O:\_Theophysics_v3\06_NOTES\Untitled.md"

Customize rows/options in:
- adaptive_yaml_schema.yaml

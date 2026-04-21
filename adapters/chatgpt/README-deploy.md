# Deploying Peplink Advisor as a ChatGPT Custom GPT

This adapter turns `core/` into a ChatGPT Custom GPT. The build produces a zip containing:

- `instructions.md` — paste into the GPT's **Instructions** field
- `knowledge/` — upload every file in this folder as Knowledge
- `config.json` — the settings to apply (name, description, capabilities)

## One-time setup

1. Run `python3 build/build_chatgpt.py` from the repo root. The artifact lands in `dist/peplink-advisor-chatgpt-<version>.zip`.
2. In ChatGPT, go to **Explore GPTs → Create**.
3. Skip the conversational builder and switch to **Configure**.
4. Fill in the fields from `config.json`:
   - **Name:** Peplink Advisor
   - **Description:** (from config.json)
   - **Instructions:** paste the full contents of `instructions.md`
   - **Conversation starters:** (from config.json)
5. Under **Recommended model**, leave ChatGPT's current default in place unless you have a specific reason to pin a currently available model in your workspace.
6. Under **Capabilities**, enable **Code Interpreter & Data Analysis**. Leave Web search, Image generation, and Canvas off unless you have a reason.
7. Under **Knowledge**, upload every file from the `knowledge/` folder. All files should be in the root of the Knowledge area — do not nest them in subfolders; ChatGPT flattens paths.
8. Save as **Only me** first and test with prompts that force `query.py` to execute, such as:
   - `List the available router models.`
   - `Show the full spec card for Balance 20X.`
   - `Compare HD2 MBX 5G and HD4 MBX 5G on Performance and Interfaces.`
9. Then change to **Anyone with the link** or **GPT Store** when you're happy.

## Updates

When the dataset or solutions change, re-run `build_chatgpt.py`, unzip the new artifact, and:

- **Instructions changed?** Paste the new `instructions.md` into the Instructions field.
- **Knowledge changed?** Delete all Knowledge files and re-upload from the new `knowledge/` folder. ChatGPT does not support in-place file updates.

That's it. The GPT picks up changes the next time someone opens a conversation with it.

## Known limitations vs. the Anthropic version

- No auto-discovery — users must pick this GPT explicitly.
- Knowledge files are eagerly loaded, not progressively disclosed. This is fine for a ~1 MB dataset; don't bundle anything much larger.
- No connector access; recommendations are dataset-grounded only.
- The ChatGPT `code_interpreter` sandbox resets each session, so `query.py` re-imports on each turn. That's fine, just slightly slower than a long-lived process.

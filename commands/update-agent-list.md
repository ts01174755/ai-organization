# Update Agent List Command

## Command: `/update-agents`

**Purpose:** Regenerate the agent directory from current agent definitions.

## What It Does

This command scans the `/root/.claude/agents/` directory and generates:

1. **AGENT_DIRECTORY.md** - Complete agent directory with full descriptions and examples
2. **agent-list.txt** - Simple text list of all agent names (alphabetically sorted)

## Usage

```bash
# Run the update command
python3 /root/.claude/scripts/generate-agent-list.py
```

Or as a command:
- `/update-agents`
- "Update agent list"
- "Refresh agent directory"

## Generated Files

All files are saved in `/root/.claude/data/`:

- `AGENT_DIRECTORY.md` - Complete listing with descriptions (no categories, alphabetical order)
- `agent-list.txt` - Simple name list

## When to Update

**Note:** The `juvenile-agent-task-matcher` automatically runs this update every time it executes, so manual updates are rarely needed.

Manual update may be useful when:
- You want to review the agent directory without running task-matcher
- Debugging or verifying agent definitions
- Generating documentation for reference

## Integration with Agent Ecosystem

The generated files are used by:
- **juvenile-agent-task-matcher** - Automatically updates and reads the directory for matching
- **Manual reference** - Quick lookup of available agents and their capabilities
- **Documentation** - Understanding the current agent ecosystem state

The agent directory shows:
- Agent names with badges (🔧 Consolidated, ⚡ Optimized)
- Full descriptions including examples from YAML frontmatter
- Alphabetical organization (no categorization)
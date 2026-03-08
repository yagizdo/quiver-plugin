# Quiver

Session continuity, agent orchestration, and development workflows for Claude Code. Never lose context between sessions — carry your decisions, progress, and next steps forward automatically.

## Quick Start

```bash
/plugin marketplace add yagizdo/quiver
/plugin install quiver@yagizdo/quiver
```

Then try your first command:

```
/handover
```

## Installation

### Plugin Install (recommended)

```bash
/plugin install quiver@yagizdo/quiver
```

## Components

| Component | Count |
|-----------|-------|
| Commands | 8 |
| Hooks | 1 |
| Skills | 3 |
| Agents | 2 |

## Commands

### Session Handover

| Command | Description |
|---------|-------------|
| `/handover` | Build an 8-section handover note with freshness checks and quality gates |
| `/load-handover` | Load the most recent handover and highlight top priorities |

### Cleanup

| Command | Description |
|---------|-------------|
| `/delete-last-handover` | Show and delete the most recent handover file with confirmation |
| `/delete-all-handovers` | List all handover files, confirm, then delete everything |

### Git

| Command | Description |
|---------|-------------|
| `/commit` | Generate a Conventional Commits message from staged changes, commit, and optionally push |

### Agent Development

| Command | Description |
|---------|-------------|
| `/create-agent` | Scaffold a new agent interactively from a description or Q&A walkthrough |
| `/create-agents-md` | Analyze project context and generate an AGENTS.md checklist for AI agents |

### Maintenance

| Command | Description |
|---------|-------------|
| `/repair-skill` | Diagnose and fix a broken skill by analyzing structure and verifying API references |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `pre-compact-handover` | PreCompact | Summarizes the conversation and saves a handover before Claude compacts context |

## Skills

### Agent Orchestration

| Skill | Description |
|-------|-------------|
| `orchestrate-agents` | Discover agents, plan an optimal team, and coordinate parallel or sequential execution |

### Agent Development

| Skill | Description |
|-------|-------------|
| `create-agent` | Agent authoring reference — frontmatter spec, category definitions, body structure, and quality gates |

### Maintenance

| Skill | Description |
|-------|-------------|
| `repair-skill` | Diagnose broken skills, verify API references against current docs, and apply targeted repairs |

## Agents

### Review

| Agent | Description |
|-------|-------------|
| `code-review` (`quiver:review:code-review`) | 5-phase PR review with severity ratings and file:line references |
| `security-audit` (`quiver:review:security-audit`) | Adversarial security auditor covering web, API, and mobile attack surfaces |

## How It Works

- **Session handovers** — structured summaries of your work: git state, decisions made, current progress, and planned next steps
- **Auto-save on compact** — PreCompact hook captures context automatically before Claude compacts the conversation
- **Retention policy** — keeps the 3 most recent handovers, prunes older ones automatically
- **Agent orchestration** — discover your local and plugin agents, assemble teams, and run subtasks in parallel
- **Agent scaffolding** — create new agents interactively with smart defaults and best practices

## External Dependencies

This plugin connects to [context7](https://mcp.context7.com) as an MCP server for library documentation lookups. The connection is configured in `plugin.json` under `mcpServers`. No authentication is required. Library/framework names from your codebase are sent to the service during best-practices checks.

## Uninstall

```
/uninstall quiver
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Superdesign is a VS Code extension that functions as an AI-powered design agent. It generates UI mockups, components, and wireframes from natural language prompts directly in IDEs (Cursor, Windsurf, Claude Code, VS Code).

## Build & Development Commands

```bash
npm install          # Install dependencies
npm run watch        # Development (watch mode)
npm run compile      # Type-check + lint + build
npm run package      # Package for production
npm run lint         # Lint only
npm run check-types  # Type-check only
```

## Testing

```bash
npm test             # Run all VSCode integration tests
npm run test:llm     # LLM service tests
npm run test:core    # Core component tests
npm run test:tools   # File operation tools
npm run test:agent   # Combined LLM + core tests
```

## Architecture

### Dual-Context Build System
- **Extension Context**: Node.js (CJS) - main VSCode extension
- **Webview Context**: Browser (ESM) - React 19 UI in webview panels

Post-build: `@anthropic-ai/claude-code` copied to `dist/node_modules/` for Claude Code binary provider.

### LLM Provider System
Abstract `LLMProvider` base class with factory pattern (`LLMProviderFactory`):
- `ClaudeApiProvider` - Anthropic SDK with API keys
- `ClaudeCodeProvider` - Claude Code binary for local execution
- OpenAI/OpenRouter support via `CustomAgentService`

### Tool System
Tools in `src/tools/` follow factory pattern: `create*Tool()` with Zod schemas.
- Validate workspace paths (prevent directory traversal)
- Standardized utilities: `handleToolError()`, `validateWorkspacePath()`, `createSuccessResponse()`

### Extension <-> Webview Communication
Message-based via `postMessage()`. Webview uses `acquireVsCodeApi()`. Security via nonce-based CSP.

## Key Directories

- `src/providers/` - LLM provider implementations
- `src/services/` - Business logic (agent orchestration, chat, logging)
- `src/tools/` - AI tool implementations (file ops, bash, search)
- `src/webview/` - React UI components and hooks
- `src/types/` - TypeScript interfaces
- `.superdesign/` - User-generated design iterations

## Configuration

VSCode settings:
- `superdesign.llmProvider`: `claude-api` (default) or `claude-code`
- `superdesign.aiModelProvider`: `anthropic`, `openai`, or `openrouter`
- `superdesign.anthropicApiKey`, `openaiApiKey`, `openrouterApiKey`
- `superdesign.thinkingBudget`: Token budget for extended thinking (default: 50000)

## Git Commit Conventions

Use conventional prefixes: `fix:`, `feat:`, `perf:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`

## UI Design Standards

For UI/frontend design tasks, follow the rules in `.cursor/rules/design.mdc`:
- Output to `.superdesign/design_iterations/` folder
- Use Flowbite + Tailwind CSS via CDN
- Avoid indigo/blue colors unless specified
- Responsive designs with 4pt/8pt spacing
- Lucide icons, Google Fonts
- Step-by-step workflow: Layout -> Theme -> Animation -> HTML generation

# Dotfiles

My personal dotfiles managed with [chezmoi](https://www.chezmoi.io/) for Neovim, WezTerm, Zed, Claude Code, and other tools.

## Overview

This repository contains my personal development environment configurations:

- **Neovim**: LazyVim-based setup with extensive language support and development tools
- **WezTerm**: Modern terminal emulator with dynamic theme switching
- **Zed**: Lightweight editor configuration
- **Claude Code**: AI coding assistant with custom hooks, agents, and plugins
- **.agents**: AI agent skills for various engineering workflows

## Prerequisites

- Git
- A Unix-like shell (bash/zsh/fish)

## Installation

### Quick Start (Recommended)

Run the included setup script. It installs chezmoi, applies dotfiles, installs Homebrew, installs Task, and then runs the full Taskfile:

```bash
curl -fsSL https://raw.githubusercontent.com/sidarth-23/dotfiles/main/install.sh | bash
```

Or, if you already have the repo cloned:

```bash
bash install.sh
```

### What the script does

1. Installs chezmoi (via Homebrew if available, otherwise binary)
2. Initializes chezmoi with this repo and applies all dotfiles
3. Installs Homebrew (Linux/macOS)
4. Installs Task (go-task)
5. Runs `task setup` to install all development tools

### Manual Setup

If you prefer to do it manually:

```bash
# 1. Install chezmoi
brew install chezmoi

# 2. Initialize and apply dotfiles
chezmoi init --apply https://github.com/sidarth-23/dotfiles.git

# 3. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 4. Install Task
curl -fsSL https://taskfile.dev/install.sh | sh

# 5. Run full setup
task setup
```

## Repository Structure

This repo uses chezmoi's naming convention where dotfiles are stored with a `dot_` prefix:

| Source (this repo) | Target (home directory) |
|---|---|
| `dot_config/` | `~/.config/` |
| `dot_claude/` | `~/.claude/` |
| `dot_agents/` | `~/.agents/` |

This avoids hidden files in the source tree and prevents conflicts with chezmoi's own configuration files.

## Features

### Neovim (LazyVim)
- Multiple themes (GitHub, Catppuccin, Tokyo Night, Gruvbox)
- File explorer (nvim-tree)
- Auto-save functionality
- LSP support for multiple languages
- Integrated formatters and linters
- Git integration
- Custom keymaps

### WezTerm
- System-based theme switching
- GitHub color schemes
- 95% transparency
- Custom cursor and tab bar settings
- High performance (120 FPS)

### Zed
- System-based theme switching
- Custom font sizes
- GitHub Dark Default theme

### Claude Code
- **Hooks**: Git safety, commit validation, file protection, package manager enforcement
- **Plugins**: LSP integrations (Go, TypeScript, Rust), superpowers, commit-commands, context7, frontend-design
- **Status Line**: Custom visual feedback via ccstatusline
- **Skills**: AI agent skills via `.agents/skills/`
- **Installation**: Automated via Taskfile (`task cc:setup`)

## Updating

### Update dotfiles

```bash
# Pull latest changes and apply
chezmoi update

# Or manually:
chezmoi git pull
chezmoi apply
```

### Update Neovim plugins

```bash
nvim --headless "+Lazy! sync" +qa
```

## Customization

Edit files directly with chezmoi:

```bash
chezmoi edit ~/.config/nvim/lua/config/options.lua
chezmoi edit ~/.claude/settings.json
```

After editing, apply changes:

```bash
chezmoi apply
```

Or commit and push back to the repo:

```bash
chezmoi git add .
chezmoi git commit -m "your message"
chezmoi git push
```

## License

MIT License - feel free to use and modify as you like.

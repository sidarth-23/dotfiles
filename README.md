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

- [chezmoi](https://www.chezmoi.io/install/)
- Neovim (>= 0.9.0)
- WezTerm
- Zed Editor
- Task (go-task)
- Git
- Homebrew (for Linux)
- Volta (Node.js version manager)
- Rust/Cargo

## Installation

### 1. Install chezmoi

```bash
# macOS / Linux
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b $HOME/.local/bin

# Or via Homebrew
brew install chezmoi
```

### 2. Initialize chezmoi with this repo

```bash
chezmoi init --apply https://github.com/sidarth-23/dotfiles.git
```

This will clone the repo into `~/.local/share/chezmoi` and immediately apply all dotfiles to your home directory.

### 3. Install Claude Code and plugins

```bash
# Full setup (install Claude Code + marketplaces + plugins)
task cc:setup

# Or install individually:
task cc:install        # Install Claude Code CLI only
task cc:marketplaces   # Install marketplaces only
task cc:plugins        # Install plugins only
```

**Note:** Due to a Claude bug with `~` paths in plugin configuration files, plugins must be installed via CLI commands rather than copying plugin JSON files.

### 4. Install additional tools

```bash
# Homebrew (Linux)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Volta
curl https://get.volta.sh | bash

# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
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

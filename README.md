# Dotfiles

My personal dotfiles for Fish shell, Neovim, WezTerm, and Zed editor configurations.

## Overview

This repository contains my personal development environment configurations:

- **Fish Shell**: Custom shell configuration with Volta, Homebrew, and Rust integration
- **Neovim**: LazyVim-based setup with extensive language support and development tools
- **WezTerm**: Modern terminal emulator with dynamic theme switching
- **Zed**: Lightweight editor configuration

## Prerequisites

- Fish Shell
- Neovim (>= 0.9.0)
- WezTerm
- Zed Editor
- Git
- Homebrew (for Linux)
- Volta (Node.js version manager)
- Rust/Cargo

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git ~/.dotfiles
   ```

2. Create symbolic links:
   ```bash
   # Fish
   ln -s ~/.dotfiles/fish ~/.config/fish

   # Neovim
   ln -s ~/.dotfiles/nvim ~/.config/nvim

   # WezTerm
   ln -s ~/.dotfiles/wezterm ~/.config/wezterm

   # Zed
   ln -s ~/.dotfiles/zed ~/.config/zed
   ```

3. Install Homebrew (Linux):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

4. Install Volta:
   ```bash
   curl https://get.volta.sh | bash
   ```

5. Install Rust:
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

## Features

### Fish Shell
- Custom color scheme
- Integration with package managers
- Enhanced shell experience

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

## Updating

1. Pull the latest changes:
   ```bash
   cd ~/.dotfiles
   git pull
   ```

2. Update Neovim plugins:
   ```bash
   nvim --headless "+Lazy! sync" +qa
   ```

## Customization

Each tool's configuration can be customized by editing the respective configuration files:

- Fish: `~/.config/fish/config.fish`
- Neovim: `~/.config/nvim/lua/config/*.lua`
- WezTerm: `~/.config/wezterm/wezterm.lua`
- Zed: `~/.config/zed/settings.json`

## License

MIT License - feel free to use and modify as you like.

#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/sidarth-23/dotfiles.git"
REPO_DIR="$HOME/development/personal/dotfiles"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[dotfiles]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[dotfiles]${NC} $1"
}

error() {
    echo -e "${RED}[dotfiles]${NC} $1"
    exit 1
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "darwin";;
        CYGWIN*|MINGW*|MSYS*) echo "windows";;
        *)          echo "unknown";;
    esac
}

OS=$(detect_os)
log "Detected OS: $OS"

# 1. Install chezmoi if missing
install_chezmoi() {
    if command -v chezmoi &>/dev/null; then
        log "chezmoi already installed: $(chezmoi --version | head -1)"
        return 0
    fi

    log "Installing chezmoi..."
    
    if [ "$OS" = "linux" ] || [ "$OS" = "darwin" ]; then
        if command -v brew &>/dev/null; then
            brew install chezmoi
        else
            sh -c "$(curl -fsLS get.chezmoi.io)" -- -b "$HOME/.local/bin"
            export PATH="$HOME/.local/bin:$PATH"
        fi
    elif [ "$OS" = "windows" ]; then
        error "Windows: Please install chezmoi manually from https://www.chezmoi.io/install/"
    else
        error "Unsupported OS. Please install chezmoi manually."
    fi

    if ! command -v chezmoi &>/dev/null; then
        error "chezmoi installation failed. Please install manually."
    fi
    
    log "chezmoi installed successfully"
}

# 2. Initialize and apply chezmoi
setup_chezmoi() {
    if [ -d "$HOME/.local/share/chezmoi/.git" ]; then
        warn "chezmoi already initialized. Updating..."
        chezmoi update
    else
        log "Initializing chezmoi with $REPO_URL..."
        chezmoi init --apply "$REPO_URL"
    fi
    log "Dotfiles applied successfully"
}

# 3. Install Homebrew if missing (required for Taskfile tools)
install_homebrew() {
    if command -v brew &>/dev/null; then
        log "Homebrew already installed: $(brew --version | head -1)"
        return 0
    fi

    log "Installing Homebrew..."
    
    if [ "$OS" = "linux" ] || [ "$OS" = "darwin" ]; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add to PATH for current session if installed
        if [ "$OS" = "linux" ] && [ -d /home/linuxbrew/.linuxbrew/bin ]; then
            eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
        elif [ "$OS" = "darwin" ] && [ -d /opt/homebrew/bin ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    else
        error "Homebrew is only supported on Linux and macOS."
    fi

    if ! command -v brew &>/dev/null; then
        error "Homebrew installation failed. Please install manually."
    fi
    
    log "Homebrew installed successfully"
}

# 4. Install Task (go-task) if missing
install_task() {
    if command -v task &>/dev/null; then
        log "Task already installed: $(task --version)"
        return 0
    fi

    log "Installing Task (go-task)..."
    
    if [ "$OS" = "linux" ] || [ "$OS" = "darwin" ]; then
        if command -v brew &>/dev/null; then
            brew install go-task
        elif [ "$OS" = "linux" ]; then
            # Install via snap or binary
            if command -v snap &>/dev/null; then
                sudo snap install task --classic
            else
                # Binary install
                local task_version="v3.42.1"
                local task_url="https://github.com/go-task/task/releases/download/${task_version}/task_linux_amd64.tar.gz"
                curl -fsSL "$task_url" | tar -xz -C "$HOME/.local/bin" task
                chmod +x "$HOME/.local/bin/task"
                export PATH="$HOME/.local/bin:$PATH"
            fi
        fi
    elif [ "$OS" = "windows" ]; then
        error "Windows: Please install Task manually from https://taskfile.dev/installation/"
    else
        error "Unsupported OS. Please install Task manually."
    fi

    if ! command -v task &>/dev/null; then
        error "Task installation failed. Please install manually."
    fi
    
    log "Task installed successfully"
}

# 4. Run the Taskfile
run_taskfile() {
    local taskfile_path
    
    # Find the taskfile in the chezmoi source or repo
    if [ -f "$HOME/.local/share/chezmoi/Taskfile.yml" ]; then
        taskfile_path="$HOME/.local/share/chezmoi"
    elif [ -f "$REPO_DIR/Taskfile.yml" ]; then
        taskfile_path="$REPO_DIR"
    else
        warn "Taskfile.yml not found in expected locations"
        return 1
    fi

    log "Running Taskfile from $taskfile_path..."
    
    if [ "$OS" = "windows" ]; then
        warn "Windows detected. Skipping automated task run."
        warn "Please run the following commands manually:"
        warn "  cd $taskfile_path"
        warn "  task setup"
    else
        (cd "$taskfile_path" && task setup)
    fi
}

# Main execution
main() {
    log "Starting dotfiles setup..."
    
    install_chezmoi
    setup_chezmoi
    install_homebrew
    install_task
    run_taskfile
    
    log "Setup complete!"
    log ""
    log "Next steps:"
    log "  - chezmoi managed files are now in place"
    log "  - Run 'task --list' in ~/.local/share/chezmoi to see available tasks"
    log "  - Edit dotfiles with: chezmoi edit <file>"
    log "  - Apply changes with: chezmoi apply"
}

main "$@"

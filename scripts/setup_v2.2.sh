#!/bin/bash

# AOKhmer v2.2 - One-Command Setup Script
# This script sets up the entire development environment for v2.2

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print banner
print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}                                                          ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}          🎵 AOKHMER v2.2 SETUP SCRIPT 🎵                ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}                                                          ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}   Automated Environment Setup for MARS Architecture     ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}                                                          ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing=()
    
    if ! command_exists git; then
        missing+=("git")
    fi
    
    if ! command_exists docker; then
        missing+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing+=("docker-compose")
    fi
    
    if ! command_exists python3; then
        missing+=("python3")
    fi
    
    if ! command_exists pip3; then
        missing+=("pip3")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing prerequisites: ${missing[*]}"
        log_info "Please install the missing tools and run this script again."
        exit 1
    fi
    
    log_success "All prerequisites satisfied!"
}

# Setup Python environment
setup_python() {
    log_info "Setting up Python environment..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies if pyproject.toml exists
    if [ -f "pyproject.toml" ]; then
        log_info "Installing Python dependencies..."
        pip install -e ".[dev]"
    elif [ -f "requirements.txt" ]; then
        log_info "Installing requirements..."
        pip install -r requirements.txt
    fi
    
    log_success "Python environment ready!"
}

# Setup environment files
setup_env() {
    log_info "Setting up environment files..."
    
    if [ ! -f ".env.v2.2" ]; then
        if [ -f ".env.v2.2.example" ]; then
            log_info "Creating .env.v2.2 from template..."
            cp .env.v2.2.example .env.v2.2
            log_warning "Please edit .env.v2.2 with your actual API keys and configuration!"
        else
            log_error ".env.v2.2.example not found!"
            exit 1
        fi
    else
        log_info ".env.v2.2 already exists, skipping..."
    fi
    
    # Create other necessary env files
    if [ ! -f ".env" ]; then
        ln -s .env.v2.2 .env 2>/dev/null || true
    fi
    
    log_success "Environment files configured!"
}

# Setup git hooks
setup_git_hooks() {
    log_info "Setting up git hooks..."
    
    if [ -f "scripts/install_git_hooks.sh" ]; then
        bash scripts/install_git_hooks.sh
    elif [ -f "scripts/install_git_hooks.ps1" ]; then
        log_warning "Git hooks script is PowerShell. Please run manually if needed."
    fi
    
    log_success "Git hooks configured!"
}

# Create necessary directories
create_directories() {
    log_info "Creating project directories..."
    
    mkdir -p 80-Sessions/2026-02
    mkdir -p 90-Project-Board/01-High-Backlog
    mkdir -p backend/logs
    mkdir -p backend/storage
    mkdir -p chroma_data
    mkdir -p export_chat
    mkdir -p 70-Training/best-practices
    
    log_success "Directories created!"
}

# Setup Docker infrastructure
setup_docker() {
    log_info "Setting up Docker infrastructure..."
    
    # Pull required images
    log_info "Pulling Docker images..."
    docker-compose -f 30-Implementation/docker-compose.yml pull
    
    log_success "Docker images ready!"
}

# Generate initial project map
generate_project_map() {
    log_info "Generating initial project map..."
    
    if [ -f "scripts/project_map_generator.py" ]; then
        source venv/bin/activate
        python scripts/project_map_generator.py
        log_success "Project map generated!"
    else
        log_warning "Project map generator not found, skipping..."
    fi
}

# Run AHA detector
run_aha_detector() {
    log_info "Running AHA moment detector..."
    
    if [ -f "scripts/aha_detector.py" ]; then
        source venv/bin/activate
        python scripts/aha_detector.py || true
        log_success "AHA moments analyzed!"
    else
        log_warning "AHA detector not found, skipping..."
    fi
}

# Setup IDE configuration
setup_ide() {
    log_info "Setting up IDE configuration..."
    
    # VS Code settings
    if command_exists code; then
        log_info "VS Code detected, installing extensions..."
        
        # List of recommended extensions
        extensions=(
            "ms-python.python"
            "ms-python.vscode-pylance"
            "ms-python.black-formatter"
            "charliermarsh.ruff"
            "ms-python.isort"
            "eamodio.gitlens"
            "github.copilot"
            "ms-vscode.vscode-json"
            "redhat.vscode-yaml"
            "ms-azuretools.vscode-docker"
        )
        
        for ext in "${extensions[@]}"; do
            code --install-extension "$ext" 2>/dev/null || true
        done
        
        log_success "VS Code extensions installed!"
    fi
    
    log_success "IDE configuration complete!"
}

# Verify installation
verify_setup() {
    log_info "Verifying installation..."
    
    local errors=()
    
    # Check Python
    if ! source venv/bin/activate && python --version >/dev/null 2>&1; then
        errors+=("Python virtual environment")
    fi
    
    # Check Docker
    if ! docker info >/dev/null 2>&1; then
        errors+=("Docker daemon")
    fi
    
    # Check env file
    if [ ! -f ".env.v2.2" ]; then
        errors+=(".env.v2.2 file")
    fi
    
    if [ ${#errors[@]} -eq 0 ]; then
        log_success "All verifications passed!"
        return 0
    else
        log_error "Verification failed for: ${errors[*]}"
        return 1
    fi
}

# Print next steps
print_next_steps() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}              🎉 SETUP COMPLETE! 🎉                       ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "1. ${YELLOW}Edit environment variables:${NC}"
    echo "   nano .env.v2.2  # Add your API keys"
    echo ""
    echo "2. ${YELLOW}Start the infrastructure:${NC}"
    echo "   cd 30-Implementation && docker-compose up -d"
    echo ""
    echo "3. ${YELLOW}Run database migrations:${NC}"
    echo "   cd backend && alembic upgrade head"
    echo ""
    echo "4. ${YELLOW}Start the development server:${NC}"
    echo "   uvicorn src.main:app --reload"
    echo ""
    echo "5. ${YELLOW}Access services:${NC}"
    echo "   • API: http://localhost:8000"
    echo "   • Dify: http://localhost:5001"
    echo "   • n8n: http://localhost:5678"
    echo "   • Prefect: http://localhost:4200"
    echo "   • Grafana: http://localhost:3000"
    echo "   • Prometheus: http://localhost:9090"
    echo ""
    echo "6. ${YELLOW}Useful commands:${NC}"
    echo "   • Generate project map: python scripts/project_map_generator.py"
    echo "   • Detect AHA moments: python scripts/aha_detector.py"
    echo "   • Run tests: pytest backend/tests"
    echo "   • Format code: black backend/src"
    echo "   • Lint code: ruff check backend/src"
    echo ""
    echo -e "${GREEN}Happy coding! 🚀${NC}"
    echo ""
}

# Main setup function
main() {
    print_banner
    
    log_info "Starting AOKhmer v2.2 setup..."
    
    # Check if we're in the right directory
    if [ ! -f "AGENTS.md" ]; then
        log_error "Please run this script from the project root directory!"
        exit 1
    fi
    
    # Run setup steps
    check_prerequisites
    create_directories
    setup_python
    setup_env
    setup_git_hooks
    setup_docker
    generate_project_map
    run_aha_detector
    setup_ide
    
    # Verify
    if verify_setup; then
        print_next_steps
    else
        log_error "Setup completed with warnings. Please check the errors above."
        exit 1
    fi
}

# Handle script interruption
trap 'log_error "Setup interrupted!"; exit 1' INT TERM

# Run main function
main "$@"

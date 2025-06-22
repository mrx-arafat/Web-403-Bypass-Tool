#!/bin/bash

# 🚀 Advanced 403 Bypass Tool Suite - Installation Script
# This script installs all dependencies and sets up the environment

set -e

echo "🚀 Advanced 403 Bypass Tool Suite - Installation"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        return 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        return 0
    elif command -v pip &> /dev/null; then
        print_success "pip found"
        return 0
    else
        print_error "pip not found. Please install pip"
        return 1
    fi
}

# Install core dependencies
install_core_deps() {
    print_status "Installing core dependencies..."
    
    # Core dependencies that are required
    CORE_DEPS=(
        "aiohttp>=3.9.0"
        "requests>=2.31.0"
        "PyYAML>=6.0"
        "numpy>=1.24.0"
        "pandas>=2.0.0"
        "tqdm>=4.65.0"
        "colorama>=0.4.6"
    )
    
    for dep in "${CORE_DEPS[@]}"; do
        print_status "Installing $dep..."
        pip3 install "$dep" || {
            print_error "Failed to install $dep"
            return 1
        }
    done
    
    print_success "Core dependencies installed"
}

# Install ML dependencies
install_ml_deps() {
    print_status "Installing machine learning dependencies..."
    
    ML_DEPS=(
        "scikit-learn>=1.3.0"
        "scipy>=1.10.0"
    )
    
    for dep in "${ML_DEPS[@]}"; do
        print_status "Installing $dep..."
        pip3 install "$dep" || {
            print_warning "Failed to install $dep (ML features may be limited)"
        }
    done
    
    print_success "ML dependencies installed"
}

# Install optional dependencies
install_optional_deps() {
    print_status "Installing optional dependencies..."
    
    OPTIONAL_DEPS=(
        "beautifulsoup4>=4.12.0"
        "PyJWT>=2.8.0"
        "rich>=13.4.0"
        "dnspython>=2.4.0"
        "psutil>=5.9.0"
        "tabulate>=0.9.0"
    )
    
    for dep in "${OPTIONAL_DEPS[@]}"; do
        print_status "Installing $dep..."
        pip3 install "$dep" || {
            print_warning "Failed to install $dep (some features may be limited)"
        }
    done
    
    print_success "Optional dependencies installed"
}

# Make scripts executable
make_executable() {
    print_status "Making scripts executable..."
    
    SCRIPTS=(
        "advanced-403-bypass.py"
        "smart-batch-bypass.py"
        "legendary-403-bypass.py"
        "legendary-403-bypass.sh"
        "batch-403-bypass.py"
        "demo.py"
    )
    
    for script in "${SCRIPTS[@]}"; do
        if [ -f "$script" ]; then
            chmod +x "$script"
            print_success "Made $script executable"
        else
            print_warning "$script not found"
        fi
    done
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    DIRS=(
        "logs"
        "reports"
        "configs"
        "wordlists"
        "results"
    )
    
    for dir in "${DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "Created directory: $dir"
        fi
    done
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python imports
    python3 -c "
import aiohttp
import requests
import yaml
import numpy
import pandas
print('✅ All core modules imported successfully')
" || {
        print_error "Core module import test failed"
        return 1
    }
    
    # Test ML imports
    python3 -c "
try:
    import sklearn
    import scipy
    print('✅ ML modules imported successfully')
except ImportError as e:
    print('⚠️  Some ML modules missing:', e)
" || {
        print_warning "Some ML modules may be missing"
    }
    
    # Test script syntax
    for script in advanced-403-bypass.py smart-batch-bypass.py legendary-403-bypass.py; do
        if [ -f "$script" ]; then
            python3 -m py_compile "$script" && {
                print_success "$script syntax check passed"
            } || {
                print_error "$script syntax check failed"
                return 1
            }
        fi
    done
    
    print_success "Installation test completed"
}

# Show usage information
show_usage() {
    echo ""
    echo "🎯 Installation Complete!"
    echo "========================"
    echo ""
    echo "Available tools:"
    echo "  • advanced-403-bypass.py    - Next generation bypass tool with AI"
    echo "  • smart-batch-bypass.py     - ML-powered batch testing"
    echo "  • legendary-403-bypass.py   - Comprehensive classic tool"
    echo "  • legendary-403-bypass.sh   - Bash version for portability"
    echo ""
    echo "Quick start:"
    echo "  python3 advanced-403-bypass.py https://target.com -p /admin"
    echo "  python3 smart-batch-bypass.py https://target.com -p modern-paths.txt"
    echo ""
    echo "Configuration:"
    echo "  Edit config.yaml to customize settings"
    echo ""
    echo "Documentation:"
    echo "  README_ADVANCED.md - Comprehensive documentation"
    echo "  TOOL_SUMMARY.md    - Quick reference"
    echo ""
    echo "Happy ethical hacking! 🛡️"
}

# Main installation process
main() {
    echo "Starting installation process..."
    echo ""
    
    # Check prerequisites
    check_python || exit 1
    check_pip || exit 1
    
    # Install dependencies
    install_core_deps || exit 1
    install_ml_deps
    install_optional_deps
    
    # Setup environment
    make_executable
    create_directories
    
    # Test installation
    test_installation || {
        print_error "Installation test failed. Please check the errors above."
        exit 1
    }
    
    # Show usage
    show_usage
    
    print_success "Installation completed successfully!"
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Advanced 403 Bypass Tool Suite - Installation Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --core-only    Install only core dependencies"
        echo "  --test         Test existing installation"
        echo "  --clean        Clean previous installation"
        echo ""
        exit 0
        ;;
    --core-only)
        print_status "Installing core dependencies only..."
        check_python || exit 1
        check_pip || exit 1
        install_core_deps || exit 1
        make_executable
        test_installation || exit 1
        print_success "Core installation completed!"
        ;;
    --test)
        print_status "Testing existing installation..."
        test_installation || exit 1
        print_success "Installation test passed!"
        ;;
    --clean)
        print_status "Cleaning previous installation..."
        pip3 uninstall -y aiohttp requests PyYAML numpy pandas scikit-learn scipy tqdm colorama rich 2>/dev/null || true
        print_success "Cleanup completed!"
        ;;
    *)
        main
        ;;
esac
#!/bin/bash

# This script automates the installation of Java, Python dependencies, and Java compilation.

# Step 1: Install Homebrew if not already installed
echo "Checking if Homebrew is installed..."
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "Homebrew is already installed."
fi

# Step 2: Install OpenJDK if not already installed
echo "Checking if OpenJDK is installed..."
if ! brew list openjdk &>/dev/null; then
    echo "OpenJDK not found. Installing OpenJDK..."
    brew install openjdk@17
    echo 'export JAVA_HOME="/opt/homebrew/opt/openjdk"' >> ~/.zprofile
    echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zprofile
    source ~/.zprofile
else
    echo "OpenJDK is already installed."
fi


# Step 3: Install Python if not already installed
echo "Checking if Python3 is installed..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Installing Python3..."
    brew install python
else
    echo "Python3 is already installed."
fi

# Step 4: Install Python dependencies using pip
echo "Installing Python dependencies..."

# Install NumPy
echo "Installing NumPy..."
pip3 install numpy

# Install UltraJSON (ujson)
echo "Installing UltraJSON..."
pip3 install ujson

# Install SciPy
echo "Installing SciPy..."
pip3 install scipy

# Install Matplotlib
echo "Installing Matplotlib..."
pip3 install matplotlib

# Install pandas
echo "Installing pandas..."
pip3 install pandas

# Install pandas
echo "Installing PyQt6..."
pip3 install PyQt6

# Step 5: Compile the Java file

script_dir="$(cd "$(dirname "$0")" && pwd)"
java_file="$script_dir/clean2.java"

echo "Compiling Java file (clean2.java)..."
if ! javac "$java_file"; then
    echo "Error: Compilation failed."
    exit 1
else
    echo "Java file compiled successfully."
fi
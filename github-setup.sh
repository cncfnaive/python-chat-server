#!/bin/bash

# GitHub Setup Script for Docker Container
# Run this inside the container: ./github-setup.sh

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║              GitHub Setup Wizard                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Configure Git identity
echo "📝 Step 1: Configure Git Identity"
echo "─────────────────────────────────"

read -p "Enter your name (for commits): " GIT_NAME
read -p "Enter your email (GitHub email): " GIT_EMAIL

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo "✅ Git identity configured!"
echo ""

# Step 2: Choose authentication method
echo "🔐 Step 2: Choose Authentication Method"
echo "────────────────────────────────────────"
echo "1) SSH Key (recommended for frequent use)"
echo "2) Personal Access Token (simpler setup)"
echo ""
read -p "Choose option (1 or 2): " AUTH_METHOD

if [ "$AUTH_METHOD" = "1" ]; then
    # SSH Key Setup
    echo ""
    echo "🔑 Generating SSH Key..."
    echo "─────────────────────────"
    
    # Generate SSH key
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f ~/.ssh/id_ed25519 -N ""
    
    # Start ssh-agent and add key
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  📋 COPY THIS SSH PUBLIC KEY TO GITHUB                   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "────────────────────────────────────────────────────────────"
    echo ""
    echo "👉 Steps to add to GitHub:"
    echo "   1. Go to: https://github.com/settings/keys"
    echo "   2. Click 'New SSH key'"
    echo "   3. Paste the key above"
    echo "   4. Click 'Add SSH key'"
    echo ""
    read -p "Press Enter after adding the key to GitHub..."
    
    # Test SSH connection
    echo ""
    echo "🧪 Testing GitHub SSH connection..."
    ssh -T git@github.com -o StrictHostKeyChecking=no || true
    
    echo ""
    echo "✅ SSH setup complete!"
    echo ""
    echo "📌 Use SSH URLs for your repos:"
    echo "   git remote add origin git@github.com:USERNAME/REPO.git"
    
else
    # Personal Access Token Setup
    echo ""
    echo "🎫 Personal Access Token Setup"
    echo "───────────────────────────────"
    echo ""
    echo "👉 Steps to create a token:"
    echo "   1. Go to: https://github.com/settings/tokens"
    echo "   2. Click 'Generate new token (classic)'"
    echo "   3. Give it a name, select 'repo' scope"
    echo "   4. Click 'Generate token'"
    echo "   5. Copy the token (you won't see it again!)"
    echo ""
    read -p "Press Enter when you have your token ready..."
    
    # Configure credential helper to store token
    git config --global credential.helper store
    
    echo ""
    echo "✅ Token auth configured!"
    echo ""
    echo "📌 Use HTTPS URLs for your repos:"
    echo "   git remote add origin https://github.com/USERNAME/REPO.git"
    echo ""
    echo "💡 When you push, enter:"
    echo "   - Username: your GitHub username"
    echo "   - Password: paste your token"
    echo ""
    echo "   (Credentials will be saved after first use)"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✅ GitHub Setup Complete!                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Your code is in: /workspace"
echo ""
echo "🚀 Quick commands to push your code:"
echo "   cd /workspace"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git branch -M main"
echo "   git remote add origin <your-repo-url>"
echo "   git push -u origin main"
echo ""

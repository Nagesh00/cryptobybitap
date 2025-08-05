#!/usr/bin/env python3
"""
GitHub Repository Verification Script
Verifies that all local changes have been successfully pushed to GitHub
"""

import subprocess
import sys
from datetime import datetime

def run_git_command(command):
    """Run a git command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("🔍 GITHUB REPOSITORY VERIFICATION")
    print("=" * 50)
    print(f"📅 Verification Time: {datetime.now()}")
    print("=" * 50)
    
    # Check git status
    print("📋 Checking Git Status...")
    stdout, stderr, code = run_git_command("git status --porcelain")
    if code == 0:
        if stdout:
            print(f"⚠️  Uncommitted changes found:")
            print(stdout)
        else:
            print("✅ Working directory clean")
    else:
        print(f"❌ Error checking status: {stderr}")
    
    # Check remote URL
    print("\n🌐 Checking Remote Repository...")
    stdout, stderr, code = run_git_command("git remote get-url origin")
    if code == 0:
        print(f"✅ Remote URL: {stdout}")
    else:
        print(f"❌ Error getting remote URL: {stderr}")
    
    # Check local vs remote commits
    print("\n📊 Checking Commit Synchronization...")
    
    # Fetch latest
    print("📥 Fetching latest from GitHub...")
    run_git_command("git fetch origin")
    
    # Check if local is ahead
    stdout, stderr, code = run_git_command("git log --oneline origin/master..HEAD")
    if code == 0:
        if stdout:
            print(f"⚠️  Local commits not on GitHub:")
            for line in stdout.split('\n'):
                if line.strip():
                    print(f"   • {line}")
        else:
            print("✅ No local commits ahead of GitHub")
    
    # Check if remote is ahead
    stdout, stderr, code = run_git_command("git log --oneline HEAD..origin/master")
    if code == 0:
        if stdout:
            print(f"⚠️  GitHub commits not in local:")
            for line in stdout.split('\n'):
                if line.strip():
                    print(f"   • {line}")
        else:
            print("✅ No GitHub commits ahead of local")
    
    # Show recent commits on GitHub
    print("\n📚 Recent Commits on GitHub:")
    stdout, stderr, code = run_git_command("git log --oneline origin/master -5")
    if code == 0:
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   • {line}")
    
    # Show local commits
    print("\n💻 Recent Local Commits:")
    stdout, stderr, code = run_git_command("git log --oneline HEAD -5")
    if code == 0:
        for line in stdout.split('\n'):
            if line.strip():
                print(f"   • {line}")
    
    print("\n" + "=" * 50)
    print("✅ VERIFICATION COMPLETE")
    print("🌐 Check your repository at: https://github.com/Nagesh00/cryptobybitap")
    print("=" * 50)

if __name__ == "__main__":
    main()

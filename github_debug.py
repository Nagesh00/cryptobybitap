#!/usr/bin/env python3
"""
GitHub Repository Debug Script
Checks for common GitHub issues and provides fixes
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def check_github_status():
    """Check GitHub repository status"""
    print("🔍 GITHUB REPOSITORY DEBUG")
    print("=" * 50)
    print(f"📅 Debug Time: {datetime.now()}")
    print(f"📂 Repository: https://github.com/Nagesh00/cryptobybitap")
    print("=" * 50)

def check_git_configuration():
    """Check git configuration"""
    print("\n📋 Git Configuration:")
    try:
        # Check remote URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Remote URL: {result.stdout.strip()}")
        else:
            print("   ❌ No remote origin configured")
            return False
        
        # Check current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"   ✅ Current Branch: {branch}")
            if branch != 'master' and branch != 'main':
                print(f"   ⚠️  Warning: Unusual branch name '{branch}'")
        
        # Check last commit
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Last Commit: {result.stdout.strip()}")
        
        # Check if there are unpushed commits
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("   ⚠️  Uncommitted changes found")
        else:
            print("   ✅ Working tree clean")
            
        return True
    except Exception as e:
        print(f"   ❌ Git configuration error: {e}")
        return False

def check_required_files():
    """Check if all required files are present"""
    print("\n📁 Required Files Check:")
    
    critical_files = [
        'README.md',
        'bot.py',
        'web_dashboard.py',
        'requirements.txt',
        'web_requirements.txt',
        'config.example.json',
        'utils/logger.py',
        'strategies/moving_average.py',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    for file in critical_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n   ⚠️  Missing {len(missing_files)} critical files")
        return False
    else:
        print("   ✅ All critical files present")
        return True

def check_github_pages_compatibility():
    """Check GitHub Pages compatibility"""
    print("\n🌐 GitHub Pages Compatibility:")
    
    # Check for index.html (GitHub Pages)
    if os.path.exists('index.html'):
        print("   ✅ index.html found (GitHub Pages ready)")
    else:
        print("   ℹ️  No index.html (GitHub Pages not configured)")
    
    # Check for docs folder
    if os.path.exists('docs/'):
        print("   ✅ docs/ folder found")
    else:
        print("   ℹ️  No docs/ folder")
    
    # Check README structure
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if '# ' in content:
                print("   ✅ README.md has proper header")
            else:
                print("   ⚠️  README.md missing main header")
    
    return True

def check_security_issues():
    """Check for security issues in the repository"""
    print("\n🛡️ Security Check:")
    
    security_issues = []
    
    # Check if config.json is tracked
    if os.path.exists('config.json'):
        result = subprocess.run(['git', 'ls-files', 'config.json'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("   ⚠️  WARNING: config.json is tracked by git!")
            print("   🔧 FIX: Add config.json to .gitignore")
            security_issues.append("config.json tracked")
        else:
            print("   ✅ config.json not tracked (good)")
    
    # Check .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if 'config.json' in gitignore_content:
                print("   ✅ config.json in .gitignore")
            else:
                print("   ⚠️  config.json not in .gitignore")
                security_issues.append("config.json not ignored")
            
            if 'logs/' in gitignore_content:
                print("   ✅ logs/ directory ignored")
            else:
                print("   ⚠️  logs/ directory not ignored")
    else:
        print("   ❌ .gitignore file missing")
        security_issues.append("missing .gitignore")
    
    if not security_issues:
        print("   ✅ No security issues found")
        return True
    else:
        print(f"   ⚠️  Found {len(security_issues)} security issues")
        return False

def check_dependencies():
    """Check dependency files"""
    print("\n📦 Dependencies Check:")
    
    # Check requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            deps = f.read().strip().split('\n')
            print(f"   ✅ requirements.txt ({len(deps)} dependencies)")
            
            # Check for critical dependencies
            critical_deps = ['pybit', 'pandas', 'numpy']
            for dep in critical_deps:
                found = any(dep in line for line in deps)
                if found:
                    print(f"      ✅ {dep}")
                else:
                    print(f"      ❌ {dep} missing")
    else:
        print("   ❌ requirements.txt missing")
    
    # Check web_requirements.txt
    if os.path.exists('web_requirements.txt'):
        with open('web_requirements.txt', 'r') as f:
            web_deps = f.read().strip().split('\n')
            print(f"   ✅ web_requirements.txt ({len(web_deps)} dependencies)")
            
            # Check for Flask
            flask_found = any('flask' in line.lower() for line in web_deps)
            if flask_found:
                print("      ✅ Flask dependencies")
            else:
                print("      ❌ Flask dependencies missing")
    else:
        print("   ❌ web_requirements.txt missing")
    
    return True

def check_repository_structure():
    """Check repository structure"""
    print("\n🏗️ Repository Structure:")
    
    expected_structure = {
        'Root Files': ['README.md', 'bot.py', 'web_dashboard.py'],
        'Config Files': ['requirements.txt', 'web_requirements.txt', 'config.example.json'],
        'Directories': ['utils/', 'strategies/', 'templates/'],
        'Debug Tools': ['debug_all.py', 'run_dashboard.py', 'start_dashboard.py']
    }
    
    for category, items in expected_structure.items():
        print(f"\n   📂 {category}:")
        for item in items:
            if os.path.exists(item):
                print(f"      ✅ {item}")
            else:
                print(f"      ❌ {item} missing")
    
    return True

def generate_github_fixes():
    """Generate fixes for common GitHub issues"""
    print("\n🔧 GITHUB ISSUE FIXES:")
    print("=" * 50)
    
    print("\n📋 Common GitHub Issues & Solutions:")
    
    print("\n1. Repository Not Showing Properly:")
    print("   - Refresh browser cache (Ctrl+F5)")
    print("   - Try incognito/private browsing mode")
    print("   - Check: https://github.com/Nagesh00/cryptobybitap")
    
    print("\n2. Files Not Appearing:")
    print("   - Ensure files are committed: git add . && git commit -m 'Update'")
    print("   - Push to GitHub: git push origin master")
    print("   - Check branch: git branch -a")
    
    print("\n3. README Not Displaying:")
    print("   - Ensure README.md has proper markdown formatting")
    print("   - Check file encoding (should be UTF-8)")
    print("   - Verify file is in root directory")
    
    print("\n4. Web Dashboard Not Working for Others:")
    print("   - Ensure all dependencies are in requirements files")
    print("   - Add clear setup instructions to README")
    print("   - Test with fresh clone: git clone <repo-url>")
    
    print("\n5. Security Issues:")
    print("   - Never commit config.json with real API keys")
    print("   - Use config.example.json for templates")
    print("   - Keep .gitignore updated")
    
    print("\n6. GitHub Pages Setup (Optional):")
    print("   - Create index.html file")
    print("   - Enable GitHub Pages in repository settings")
    print("   - Choose source branch (usually main/master)")

def create_github_actions_workflow():
    """Create GitHub Actions workflow for testing"""
    print("\n⚙️ Creating GitHub Actions Workflow...")
    
    os.makedirs('.github/workflows', exist_ok=True)
    
    workflow_content = """name: Bot Testing

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r web_requirements.txt
    
    - name: Test imports
      run: |
        python -c "from utils.logger import setup_logger; print('Logger OK')"
        python -c "from strategies.moving_average import MovingAverageStrategy; print('Strategy OK')"
    
    - name: Test bot structure
      run: |
        python -c "import bot; print('Bot module OK')"
        python -c "import web_dashboard; print('Web dashboard OK')"
"""
    
    try:
        with open('.github/workflows/test.yml', 'w') as f:
            f.write(workflow_content)
        print("   ✅ GitHub Actions workflow created")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create workflow: {e}")
        return False

def main():
    """Run all GitHub debug checks"""
    check_github_status()
    
    checks = [
        ("Git Configuration", check_git_configuration),
        ("Required Files", check_required_files),
        ("GitHub Pages Compatibility", check_github_pages_compatibility),
        ("Security Issues", check_security_issues),
        ("Dependencies", check_dependencies),
        ("Repository Structure", check_repository_structure),
    ]
    
    passed = 0
    failed = 0
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ Error in {check_name}: {e}")
            failed += 1
    
    # Create GitHub Actions workflow
    if create_github_actions_workflow():
        print("   ✅ GitHub Actions workflow added")
    
    print("\n" + "=" * 50)
    print("📊 GITHUB DEBUG SUMMARY")
    print("=" * 50)
    print(f"✅ Checks Passed: {passed}")
    print(f"❌ Checks Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    generate_github_fixes()
    
    print("\n🎯 QUICK ACTIONS:")
    print("- Visit: https://github.com/Nagesh00/cryptobybitap")
    print("- Refresh browser if issues persist")
    print("- Check GitHub status: https://githubstatus.com")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

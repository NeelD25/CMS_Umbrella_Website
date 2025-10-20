import os
import subprocess
import sys

def run_cmd(command, cwd=None):
    """Run shell commands and show output/errors."""
    try:
        # Capture output for better error reporting in the main function
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            text=True, 
            capture_output=True, # Capture stdout/stderr
            check=False # Do not raise an exception on non-zero exit code
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def pause():
    input("\nPress Enter to close...")

def push_project(repo_url, folder="."):
    """Commit and push a full project."""
    print("--- Preparing Commit ---")
    if not os.path.exists(os.path.join(folder, ".git")):
        run_cmd("git init", cwd=folder)

    # 1. Add all changes
    if not run_cmd("git add .", cwd=folder): return
    
    # 2. Commit the changes
    if not run_cmd('git commit -m "Auto commit from GitPush.py"', cwd=folder):
        print("Note: Nothing new to commit or commit failed.")
    
    # 3. Set up remote
    if not run_cmd("git branch -M main", cwd=folder): return
    # The original code's remove/add is fine for universal setup
    run_cmd("git remote remove origin", cwd=folder) # Safe to remove if it doesn't exist
    if not run_cmd(f"git remote add origin {repo_url}", cwd=folder): return

    # 4. Push
    print("\n--- Attempting Push ---")
    if run_cmd("git push -u origin main", cwd=folder):
        print("\n✅ Project successfully pushed to GitHub.")
    else:
        print("\n❌ Push rejected! Remote might contain new work.")
        print("Please try option 4 to automatically fix the synchronization issue.")


def fix_and_push(repo_url, folder="."):
    """Fix the 'rejected' error by pulling, then retrying the push."""
    print("\n--- Starting Fix Process (Pulling Remote Changes) ---")

    # 1. Ensure remote is set (like in push_project)
    run_cmd("git remote remove origin", cwd=folder)
    if not run_cmd(f"git remote add origin {repo_url}", cwd=folder): 
        print("Failed to set remote URL.")
        return

    # 2. Pull changes from remote
    # This fetches remote changes and attempts to merge them with your local commit.
    print("Running: git pull origin main...")
    if not run_cmd("git pull origin main", cwd=folder):
        print("\n❌ Auto-fix FAILED. Git could not automatically merge the changes.")
        print("You may have merge conflicts. Please resolve them manually in the terminal.")
        return

    # 3. Retry the push
    print("\n--- Retrying Push after Successful Pull ---")
    if run_cmd("git push origin main", cwd=folder):
        print("\n✅ Project successfully synchronized and pushed to GitHub.")
    else:
        print("\n❌ Push FAILED again. Check terminal output for errors.")


def push_single_file(repo_url, folder="."):
    """Let user pick one file to upload."""
    files = []
    for root, dirs, fs in os.walk(folder):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in fs:
            # Skip hidden files like .gitkeep or .gitignore
            if not f.startswith('.'):
                full_path = os.path.join(root, f)
                # Only show paths relative to the current folder
                relative_path = os.path.relpath(full_path, folder) 
                files.append(relative_path)

    if not files:
        print("No non-hidden files found in the current directory.")
        return

    print("\nSelect a file to upload:\n")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    try:
        choice = int(input("\nEnter file number: "))
        file_to_push = files[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    if not os.path.exists(os.path.join(folder, ".git")):
        run_cmd("git init", cwd=folder)
        run_cmd("git branch -M main", cwd=folder)
        run_cmd(f"git remote add origin {repo_url}", cwd=folder)
    
    run_cmd(f'git add "{file_to_push}"', cwd=folder)
    run_cmd(f'git commit -m "Updated {os.path.basename(file_to_push)}"', cwd=folder)
    run_cmd("git push origin main", cwd=folder)
    print(f"\n✅ File '{os.path.basename(file_to_push)}' uploaded successfully.")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== GitHub Push Utility ===\n")
    print("1. Upload full project (first time)")
    print("2. Upload a specific file")
    print("3. Upload / update whole project (existing repo)")
    print("4. FIX: Push was rejected ('fetch first' error) 🛠️")

    choice = input("\nEnter your choice (1/2/3/4): ").strip()

    if choice in ["1", "2", "3", "4"]:
        repo_url = input("\nEnter your GitHub repo URL (ending with .git): ").strip()
    else:
        print("Invalid choice.")
        pause()
        return

    if choice == "1":
        push_project(repo_url)
    elif choice == "2":
        push_single_file(repo_url)
    elif choice == "3":
        # Options 1 and 3 are the same function, as 'push_project' handles init/setup
        push_project(repo_url)
    elif choice == "4":
        fix_and_push(repo_url)

    pause()

if __name__ == "__main__":
    main()
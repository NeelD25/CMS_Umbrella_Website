import os
import subprocess
import sys

def run_cmd(command, cwd=None):
    """Run shell commands and show output/errors."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def pause():
    input("\nPress Enter to close...")

def push_project(repo_url, folder="."):
    """Commit and push a full project."""
    if not os.path.exists(os.path.join(folder, ".git")):
        run_cmd("git init", cwd=folder)

    run_cmd("git add .", cwd=folder)
    run_cmd('git commit -m "Auto commit from GitPush.py"', cwd=folder)
    run_cmd("git branch -M main", cwd=folder)
    run_cmd("git remote remove origin", cwd=folder)
    run_cmd(f"git remote add origin {repo_url}", cwd=folder)
    run_cmd("git push -u origin main", cwd=folder)
    print("\n✅ Project successfully pushed to GitHub.")

def push_single_file(repo_url, folder="."):
    """Let user pick one file to upload."""
    files = []
    for root, dirs, fs in os.walk(folder):
        for f in fs:
            if not f.startswith(".git"):
                full_path = os.path.join(root, f)
                files.append(full_path)

    if not files:
        print("No files found.")
        return

    print("\nSelect a file to upload:\n")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    try:
        choice = int(input("\nEnter file number: "))
        file_to_push = files[choice - 1]
    except:
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

    choice = input("\nEnter your choice (1/2/3): ").strip()

    repo_url = input("\nEnter your GitHub repo URL (ending with .git): ").strip()

    if choice == "1":
        push_project(repo_url)
    elif choice == "2":
        push_single_file(repo_url)
    elif choice == "3":
        push_project(repo_url)
    else:
        print("Invalid choice.")

    pause()

if __name__ == "__main__":
    main()

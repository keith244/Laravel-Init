import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import subprocess
import shutil


def validate_environment_tools_exist():
    composer_path = shutil.which('composer')
    tools = ['composer','php','git']
    all_valid = True

    for tool in tools:
        tool_path = shutil.which(tool)
        if tool_path:
            print(f"{tool} found at {tool_path} ---- ok")
            try:
                result = subprocess.run([tool_path,"--version"], check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f'Version: {result.stdout.strip().split()[0:3]}')
            except subprocess.CalledProcessError as e:
                print(f"Error running {tool}: {e.stderr}")
                all_valid=False
        else:
            print(f"{tool} not found in PATH")
            all_valid = False
    return all_valid    



def create_project_folder():
    # asks for project name
    while True:
        folder_name = input("Enter project name: ").strip()
        if not folder_name:
            print("x Project name cannot be empty.")
            continue

        if not all(c.isalnum() or c in '-_' for c in folder_name):
            print("x Use only letters, numbers, hyphens, and underscores.")
            continue
        # valid name, break
        print(f"Project name: {folder_name}")
        break

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost',True)
    root.update()

    # user selects directory
    selected_directory = filedialog.askdirectory(
            title=f"Select location for '{folder_name}' project"
        )
    if not selected_directory:
        print('✗ No folder selected.')
        return None
    
    target_path = Path(selected_directory) / folder_name
    
    if target_path.exists():
        print(f"✗ Folder '{folder_name}' already exists at {selected_directory}!")
        print("Please choose a different name or location.")
        return None
    
    # create folder
    try:
        target_path.mkdir(parents=True, exist_ok=False)
        print(f"✓ Folder created: {target_path}")
        return target_path
    except Exception as e:
        print(f"✗ Error creating folder: {e}")
        return None    

    
def install_laravel(project_path):
    # Install laravel in specified directory
    if not project_path:
        print("No valid project path provided")
        return False
    
    composer_path = shutil.which('composer')
    if not composer_path:
        print('Composer not found')
        return False
    
    print(f'\nInstalling Laravel in {project_path}...')
    try:
        
        result = subprocess.run(
            [composer_path, 'create-project', '--prefer-dist', 'laravel/laravel', str(project_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Laravel installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Laravel: {e.stderr}")
        return False
    




def initialise_git(project_path):
    tool = 'git'
    tool_path = shutil.which(tool)
    
    if not tool_path:
        print(f"{tool} not found in PATH")
        return False
    
    print(f"{tool} found at {tool_path} ---- ok")

    run_kwargs = {
        'cwd': project_path,
        'check': True,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'text': True
    }


    # change working directory, run git commands
    try:
        subprocess.run([
            tool,
            "init"
        ],**run_kwargs)
        print(f"Git repository initialised in {project_path} using CLI.")

        repo_link = input("Enter link to github repo (leave blank to skip): ").strip()

        if repo_link:
            subprocess.run([
                tool, 'add', '.'
            ],**run_kwargs)
            git_commit = input("Enter first commit message (leave blank for 'First commit'): ")
            commit_msg = git_commit if git_commit else "First commit"

            subprocess.run([tool,"commit","-m",commit_msg],**run_kwargs)
            subprocess.run([tool,"branch","-M","main"],**run_kwargs)
            subprocess.run([tool, "remote", "add", "origin", repo_link], **run_kwargs)
            subprocess.run([tool, "push", "-u", "origin", "main"], **run_kwargs)
            print(f"Successfully pushed to remote repo {repo_link}")
        else:
            print("Skipping remote repository setup.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error with Git operation: {e.stderr}")
        return False

# if initialise_git(project_path='C:\\Users\\User\\OneDrive\\Desktop\\LARA_PROJECTS\\test2'):
#     create_project_folder()

def main():
    print("=== Laravel Setup Automation ===\n")
    
    # Step 1: Validate environment
    print("Step 1: Validating environment...")
    if not validate_environment_tools_exist():
        print("\n✗ Environment validation failed. Please install missing tools.")
        return
    
    print("\n✓ Environment validation passed!\n")
    
    # Step 2: Create project folder
    print("Step 2: Creating project folder...")
    project_path = create_project_folder()
    
    if not project_path:
        print("✗ Setup cancelled.")
        return
    
    # Step 3: Install Laravel
    print("\nStep 3: Installing Laravel...")
    if install_laravel(project_path):
        print(f"\nSetup complete! Your Laravel project is at: {project_path}")
    else:
        print("\n✗ Laravel installation failed.")
    
    print("Step 4: Initialise Git repository")
    setup_git = input("Set up git remote repository? (y/n): ").lower()
    if setup_git == 'y':
        if initialise_git(project_path):
            print(f'Set up complete.')
            print(f"\nYour Laravel project is ready at:")
            print(f"  {project_path}")

        else:
            print("Git set up failed, but your laravel project is ready.")
    else:
        print("Skipping Git remote setup.")


if __name__ == "__main__":
    main()
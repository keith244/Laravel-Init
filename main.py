import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import subprocess
import shutil


def validate_environment_tools_exist():
    composer_path = shutil.which('composer')
    tools = ['composer','php']
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
    root = tk.Tk()
    root.withdraw()

    # user selects directory
    selected_directory = filedialog.askdirectory(title="Select parent folder")

    if selected_directory:
        # ask for folder name
        folder_name = input("Enter folder name: ") 

        # create path and directory

        target_path = Path(selected_directory)/folder_name
        if target_path.exists():
            print(f"Error: Folder '{folder_name}' already exists at {selected_directory}!")
            print("Please choose a different name.")
            return None
        target_path.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {target_path}")
        return target_path
    else:
        print('No folder created. ')
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

if __name__ == "__main__":
    main()
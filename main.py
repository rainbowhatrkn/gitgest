import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import os

# Fonction pour exécuter les commandes Git
def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        output_text.insert(tk.END, f"$ {command}\n{result.stdout}\n")
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"$ {command}\n{e.stderr}\n")

# Fonction pour lister les dépôts (dossiers avec un .git)
def list_repositories():
    repos = []
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            repos.append(root)
    return repos

# Fonction pour mettre à jour les branches disponibles dans le dépôt sélectionné
def update_branches():
    selected_repo = repo_var.get()
    os.chdir(selected_repo)
    result = subprocess.run("git branch -a", shell=True, capture_output=True, text=True)
    branches = [branch.strip().replace("* ", "") for branch in result.stdout.splitlines()]
    branch_menu['values'] = branches
    os.chdir("..")

# Fonction pour mettre à jour les tags disponibles dans le dépôt sélectionné
def update_tags():
    selected_repo = repo_var.get()
    os.chdir(selected_repo)
    result = subprocess.run("git tag", shell=True, capture_output=True, text=True)
    tags = [tag.strip() for tag in result.stdout.splitlines()]
    tag_menu['values'] = tags
    os.chdir("..")

# Interface graphique principale
def create_gui():
    root = tk.Tk()
    root.title("Git Command Center")
    root.configure(bg="black")

    # Style des widgets
    btn_style = {"bg": "#00FF00", "fg": "black", "font": ("Courier", 12, "bold")}
    lbl_style = {"bg": "black", "fg": "#00FF00", "font": ("Courier", 10, "bold")}
    output_style = {"bg": "black", "fg": "#00FF00", "font": ("Courier", 10), "insertbackground": "#00FF00"}

    # Variables pour les sélections
    global repo_var, branch_var, tag_var
    repo_var = tk.StringVar()
    branch_var = tk.StringVar()
    tag_var = tk.StringVar()

    # Liste des dépôts disponibles
    tk.Label(root, text="Select Repository:", **lbl_style).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    repos = list_repositories()
    repo_menu = ttk.Combobox(root, textvariable=repo_var, values=repos, state="readonly", font=("Courier", 10))
    repo_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    repo_menu.bind("<<ComboboxSelected>>", lambda e: [update_branches(), update_tags()])

    # Liste des branches disponibles
    tk.Label(root, text="Select Branch:", **lbl_style).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    branch_menu = ttk.Combobox(root, textvariable=branch_var, values=[], state="readonly", font=("Courier", 10))
    branch_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Liste des tags disponibles
    tk.Label(root, text="Select Tag:", **lbl_style).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    tag_menu = ttk.Combobox(root, textvariable=tag_var, values=[], state="readonly", font=("Courier", 10))
    tag_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Zone de texte pour afficher les résultats
    global output_text
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, **output_style)
    output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Frame pour les boutons
    button_frame = tk.Frame(root, bg="black")
    button_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Commandes Git adaptées à l'interface
    commands = {
        "Init Repository": "git init",
        "Add All": "git add --all",
        "Commit": "git commit -m 'Initial commit'",
        "Status": "git status",
        "Log": "git log",
        "Checkout Branch": lambda: f"git checkout {branch_var.get()}",
        "Merge Branch": lambda: f"git merge {branch_var.get()}",
        "Reset Hard": "git reset --hard HEAD",
        "Clone Repo": lambda: f"git clone {repo_var.get()}",
        "Pull": "git pull origin master",
        "Push": lambda: f"git push --set-upstream origin {branch_var.get()}",
        "Stash": "git stash",
        "Apply Stash": "git stash apply",
        "Create Tag": lambda: f"git tag {tag_var.get()}",
        "View Diff": "git diff",
        "Delete Branch": lambda: f"git branch -d {branch_var.get()}",
        "Add Remote": lambda: f"git remote add origin {repo_var.get()}",
        "Remove Remote": lambda: f"git remote remove origin"
    }

    # Création des boutons pour chaque commande Git
    for i, (label, command) in enumerate(commands.items()):
        def on_button_click(cmd=command):
            if callable(cmd):
                cmd = cmd()
            run_git_command(cmd)

        btn = tk.Button(button_frame, text=label, command=on_button_click, **btn_style)
        btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")

    # Configuration du redimensionnement
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(3, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    # Lancement de l'interface
    root.mainloop()

if __name__ == "__main__":
    create_gui()
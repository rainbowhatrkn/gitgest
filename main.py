import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import subprocess
import os

# Fonction pour exécuter les commandes Git
def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        output_text.insert(tk.END, f"$ {command}\n{result.stdout}\n")
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"$ {command}\n{e.stderr}\n")

# Fonction pour sélectionner un répertoire contenant un dépôt Git
def select_repository():
    selected_repo = filedialog.askdirectory()
    if selected_repo:
        repo_var.set(selected_repo)
        os.chdir(selected_repo)
        update_branches()
        update_tags()

# Fonction pour mettre à jour les branches disponibles dans le dépôt sélectionné
def update_branches():
    result = subprocess.run("git branch -a", shell=True, capture_output=True, text=True)
    branches = [branch.strip().replace("* ", "") for branch in result.stdout.splitlines()]
    branch_menu['values'] = branches

# Fonction pour mettre à jour les tags disponibles dans le dépôt sélectionné
def update_tags():
    result = subprocess.run("git tag", shell=True, capture_output=True, text=True)
    tags = [tag.strip() for tag in result.stdout.splitlines()]
    tag_menu['values'] = tags

# Interface graphique principale
def create_gui():
    root = tk.Tk()
    root.title("Git Command Center")
    root.configure(bg="#1C1C1C")

    # Style des widgets
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Courier", 12, "bold"), background="#00FF00", foreground="black")
    style.configure("TLabel", font=("Courier", 10, "bold"), background="#1C1C1C", foreground="#00FF00")
    style.configure("TFrame", background="#1C1C1C", borderwidth=2, relief="groove")
    style.configure("TCombobox", selectbackground="#00FF00", fieldbackground="#1C1C1C", background="#00FF00", foreground="black")
    style.map('TButton', background=[('active', '#00AA00')])

    # Variables pour les sélections
    global repo_var, branch_var, tag_var
    repo_var = tk.StringVar()
    branch_var = tk.StringVar()
    tag_var = tk.StringVar()

    # Frame principale
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Gestionnaire de fichiers pour sélectionner le dépôt
    ttk.Label(main_frame, text="Select Repository:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    repo_entry = ttk.Entry(main_frame, textvariable=repo_var, width=50)
    repo_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    browse_button = ttk.Button(main_frame, text="Browse", command=select_repository)
    browse_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

    # Liste des branches disponibles
    ttk.Label(main_frame, text="Select Branch:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    global branch_menu
    branch_menu = ttk.Combobox(main_frame, textvariable=branch_var, values=[], state="readonly")
    branch_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Liste des tags disponibles
    ttk.Label(main_frame, text="Select Tag:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    global tag_menu
    tag_menu = ttk.Combobox(main_frame, textvariable=tag_var, values=[], state="readonly")
    tag_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Zone de texte pour afficher les résultats
    global output_text
    output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, bg="#000000", fg="#00FF00", font=("Courier", 10), insertbackground="#00FF00", borderwidth=2, relief="sunken")
    output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Frame pour les boutons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

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

        btn = ttk.Button(button_frame, text=label, command=on_button_click)
        btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")

    # Configuration du redimensionnement
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)  # Zone de texte s'étend bien

    # Assurez-vous que la zone de texte prend tout l'espace disponible verticalement
    main_frame.grid_rowconfigure(4, weight=1)
    output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    # Lancement de l'interface
    root.mainloop()

if __name__ == "__main__":
    create_gui()
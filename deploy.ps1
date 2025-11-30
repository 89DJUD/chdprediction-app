param(
    [string]$RepoName = "chd-streamlit-app",
    [string]$Visibility = "private",
    [string]$RemoteName = "origin"
)

Write-Host "=== 🚀 Déploiement automatique GitHub + Streamlit Cloud ===" -ForegroundColor Cyan

# -------------------------
# 1) INIT GIT
# -------------------------
if (-not (Test-Path ".git")) {
    Write-Host "📌 Initialisation du dépôt Git..."
    git init
} else {
    Write-Host "📌 Dépôt Git déjà initialisé."
}

# -------------------------
# 2) GITIGNORE
# -------------------------
if (-not (Test-Path ".gitignore")) {
@"
.vscode/
__pycache__/
.venv/
Model.pkl
*.pkl
"@ | Out-File -Encoding utf8 ".gitignore"
Write-Host "📌 .gitignore créé."
} else {
    Write-Host "📌 .gitignore existe déjà."
}

# -------------------------
# 3) Git LFS pour Model.pkl
# -------------------------
if (-not (Get-Command git-lfs -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ Git LFS non installé. Installer depuis : https://git-lfs.com/"
    exit
}

git lfs install
git lfs track "*.pkl"
Write-Host "📌 Git LFS configuré pour les fichiers .pkl"

# -------------------------
# 4) ADD / COMMIT
# -------------------------
Write-Host "📌 Ajout des fichiers..."
git add .

Write-Host "📌 Commit..."
git commit -m "Auto deploy initial"

# -------------------------
# 5) CREATE REMOTE (GitHub CLI obligatoire)
# -------------------------
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "📌 Vérification dépôt GitHub..."

    gh repo view $RepoName 2>$null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✔️ Le repo GitHub existe déjà."
    } else {
        Write-Host "📌 Création du repo GitHub..."
        gh repo create $RepoName --$Visibility --source=. --remote=$RemoteName --push
        Write-Host "✔️ Repo GitHub créé et push effectué."
    }
} else {
    Write-Host "❌ GitHub CLI non installé."
    Write-Host "➡️ Installe-le ici : https://cli.github.com/"
    exit
}

# -------------------------
# 6) PUSH (au cas où)
# -------------------------
Write-Host "📌 Push final..."
git push -u $RemoteName main

# -------------------------
# 7) MESSAGE STREAMLIT
# -------------------------
Write-Host ""
Write-Host "=== 🎉 Déploiement GitHub terminé ===" -ForegroundColor Green
Write-Host "➡️ Rendez-vous maintenant sur : https://streamlit.io/cloud"
Write-Host "➡️ Cliquez sur 'New app'"
Write-Host "➡️ Sélectionnez le repo : $RepoName"
Write-Host "➡️ Fichier à lancer : app.py"
Write-Host ""
Write-Host "🚀 Votre application sera en ligne dans quelques secondes !"

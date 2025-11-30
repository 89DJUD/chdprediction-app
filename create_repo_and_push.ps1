# Powershell script to initialize a git repo and push to GitHub using GH CLI
# Usage: ./create_repo_and_push.ps1 -RepoName "your-repo-name" -Visibility public
param(
    [string]$RepoName = "cardique-2",
    [ValidateSet("public","private")][string]$Visibility = "public",
    [string]$RemoteName = "origin"
)

# Check for git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not installed. Please install git and try again."
    exit 1
}

# Initialize git if not already
if (-not (Test-Path .git)) {
    git init
    git add -A
    git commit -m "Initial commit"
} else {
    Write-Host "Git repository already initialized."
}

# If gh CLI is available, use it to create remote
if (Get-Command gh -ErrorAction SilentlyContinue) {
    try {
        $existing = gh repo view --repo $RepoName 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Remote GitHub repo already exists; it won't be created."
        } else {
            gh repo create $RepoName --$Visibility --source=. --remote=$RemoteName --push
            Write-Host "Created GitHub repo and pushed changes."
        }
    } catch {
        Write-Error "Failed to create GitHub repo using gh CLI: $_"
    }
} else {
    Write-Host "gh CLI not found. Add a remote manually, then push the repo. Example:"
    Write-Host "git remote add origin https://github.com/<your-username>/$RepoName.git"
    Write-Host "git push -u origin main"
}

Write-Host "Done. If you plan to use Streamlit Cloud, go to https://streamlit.io/cloud to create a new app and connect your GitHub repo."

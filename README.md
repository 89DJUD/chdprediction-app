# CHD Streamlit App

This repository contains a Streamlit app (`app.py`) and model training script (`codemodel.py`) for predicting risk of heart disease (CHD).

## Quick Local Run (Virtual Environment)

1. Create a venv and activate it (Windows PowerShell):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run app.py
```


---

## Deployment options

You can deploy this Streamlit app in several ways; choose one that fits your needs.

### 1) Streamlit Community Cloud (recommended for a quick deploy)
- Pros: quick, free for public repos, minimal config.
- Cons: repo must be public (or use a team plan), limited resources.

Steps:
1. Push repository to GitHub.
2. Go to https://streamlit.io/cloud, sign in and choose **New app**.
3. Choose your GitHub repo and branch. Set the main file (`app.py`) as the entrypoint.
4. Click Deploy.


### 2) Docker + Render (or any Docker-friendly host)
- Pros: Fully customizable, supports private repos, consistent environment.
- Cons: Need a container service (Render, AWS, Azure, GCP, etc.)

Steps (Render example):
1. Create a Dockerfile (already provided).
2. Push repo to GitHub.
3. On Render (https://render.com), create a new Web Service and link your GitHub repo.
4. Render will build the container and run the app using the CMD in your Dockerfile.

### 3) Azure Web App (Container or Python)
- Pros: Enterprise features, scaling.
- Cons: Slightly more complex setup.

See Azure docs for deploying a containerized web app.


---

## Notes & Troubleshooting

- scikit-learn version matters for pickled models. This project uses `scikit-learn==1.6.1` to match the model. If you re-train, keep versions consistent.
- The `imblearn` import works via `pip install imbalanced-learn` (package name `imbalanced-learn`).
- If your model file (`Model.pkl`) is large, consider hosting it on cloud storage (S3, Azure Blob) and loading it at runtime; then exclude `Model.pkl` from git and configure environment variables for the URL.

If you want, I can automatically create a GitHub repo and push your code, or help you choose the best hosting option (Streamlit Cloud vs Docker-based service).

## Automate repo creation and push (Windows PowerShell)

There's a helper script included to initialize a Git repo and push it to GitHub using the `gh` CLI. If you don't have the GH CLI, the script will give you the exact commands to run manually.

1. Make sure you have `git` and (optionally) `gh` installed.
2. Configure `gh` if you're going to use it: `gh auth login`
3. Run the script:

```powershell
.\create_repo_and_push.ps1 -RepoName "cardique-2" -Visibility public
```

This initializes the repo if needed, commits everything, creates a GitHub repository, and pushes the code. You can later connect the GitHub repo to Streamlit Cloud.
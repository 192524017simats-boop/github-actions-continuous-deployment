# Practical 14 — Continuous Deployment using GitHub Actions

## Included
- Flask To-Do application
- Dockerfile
- GitHub Actions workflow: build image, push to Docker Hub, then trigger Render deployment
- Render blueprint example

## A. Create GitHub repository and push
Create a public GitHub repository named `github-actions-continuous-deployment`.
In PowerShell, from this folder:
```powershell
git init
git add .
git commit -m "Add Flask To-Do app and GitHub Actions deployment"
git branch -M main
git remote add origin https://github.com/192524017simats-boop/github-actions-continuous-deployment.git
git push -u origin main
```
If the repository URL differs, replace it with your own URL.

## B. Docker Hub
The workflow publishes:
`bhavya77/github-actions-todo:latest`
and a commit-specific tag.

Create a Docker Hub access token (Account Settings > Personal access tokens).
In GitHub repository Settings > Secrets and variables > Actions, add:
- `DOCKERHUB_USERNAME` = `bhavya77`
- `DOCKERHUB_TOKEN` = your Docker Hub access token (never put it in source code)

## C. Cloud deployment using Render
1. Sign in to Render and create a Web Service using the Docker image `docker.io/bhavya77/github-actions-todo:latest`.
2. Set health check path to `/health`; the app listens on port 5000 (Render detects the exposed port).
3. In the Render service, create/copy its Deploy Hook.
4. In GitHub Settings > Secrets and variables > Actions, add `RENDER_DEPLOY_HOOK` = the full Deploy Hook URL.
5. Push a small change to `app.py` and open the GitHub repository's Actions tab. A successful run builds and pushes the image, then calls the Render deploy hook.

IMPORTANT: The workflow automatically builds and pushes on every push to `main`. The cloud step only runs after you create the Render service and add the deploy-hook secret. Cloud hosting cannot be activated by code alone; it needs your Render account and service.

## D. Local test
```powershell
docker build -t github-actions-todo .
docker run --rm -p 5002:5000 github-actions-todo
```
Open http://localhost:5002 and http://localhost:5002/health.

## Evidence screenshots
1. GitHub repository files including `.github/workflows/deploy.yml`
2. GitHub Actions successful run
3. Docker Hub repository showing `github-actions-todo`
4. Render service showing Live and the application in browser

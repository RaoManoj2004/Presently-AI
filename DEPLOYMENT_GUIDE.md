# 🚀 Deployment Guide for Presently

This guide will help you deploy your **Presently** application to the web so anyone can use it. Because your application uses specialized tools like LibreOffice and Poppler, we will use **Docker** to deploy it.

We recommend using **Render.com** as it has great support for Docker applications and offers a free tier/low-cost options.

## Prerequisite: GitHub
Ensure your latest code (including the `Dockerfile` I just created) is pushed to GitHub.
1. `git add .`
2. `git commit -m "Add Docker deployment configuration"`
3. `git push origin main`

## Step 1: Create a Render Account
1. Go to [dashboard.render.com](https://dashboard.render.com/)
2. Sign up with your **GitHub** account.

## Step 2: Create a New Web Service
1. Click the **New +** button and select **Web Service**.
2. Select **"Build and deploy from a Git repository"**.
3. Connect your GitHub account if you haven't already.
4. Find and select your repository: `Presently-AI`.

## Step 3: Configure the Service
Fill in the details as follows:

- **Name**: `presently-app` (or whatever you like)
- **Region**: Choose the one closest to you (e.g., Singapore, Frankfurt, Oregon).
- **Runtime**: Select **Docker** (This is crucial!).
- **Branch**: `main`
- **Region**: Defaults are fine.

## Step 4: Environment Variables
Scroll down to the **Environment Variables** section and click **"Add Environment Variable"**. You must add your Google API Key here.

- **Key**: `GOOGLE_API_KEY`
- **Value**: `Your_Actual_Google_API_Key_Here` (Copy this from your local `.env` file)

> **Note:** Do NOT upload your `.env` file to GitHub or Render directly. using Environment Variables is the secure way.

## Step 5: Deploy
1. Click **"Create Web Service"**.
2. Render will now start building your Docker image. 
   - *Note: This might take 5-10 minutes the first time because it needs to install LibreOffice and other dependencies.*
3. You will see logs scrolling in the dashboard.
4. Once completed, you will see a green **"Live"** badge.
5. Your app will be available at a URL like `https://presently-app.onrender.com`.

## Troubleshooting

### Build Failures
If the build fails due to memory limits (LibreOffice is heavy), you may need to upgrade to the **Starter Plan** ($7/month) on Render, which offers more RAM. The free tier might be tight for building this specific Docker image.

### "Internal Server Error" on Generation
If the video generation fails:
1. Check the logs in the Render dashboard.
2. Ensure `GOOGLE_API_KEY` is set correctly.
3. Note that the free tier of hostings might experience timeouts for long video generations (over 30-60 seconds). If this happens, you might need a paid plan with longer timeout limits.

## Alternative: Railway.app
If you prefer [Railway](https://railway.app/):
1. Login with GitHub.
2. "New Project" -> "Deploy from GitHub repo".
3. Select your repo.
4. Add the `GOOGLE_API_KEY` in the "Variables" tab.
5. Railway handles Dockerfiles automatically.

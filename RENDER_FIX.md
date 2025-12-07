# Render Deployment Fix Guide

## Problem
Your Render deployment was failing with the error:
```
ValueError: Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments.
```

This occurred because the `GOOGLE_API_KEY` environment variable was not configured in Render.

## Solutions Applied

### 1. Code Changes ✅
I've updated all files that use the Google Generative AI API to defer initialization until the functions are actually called. This prevents the application from crashing at startup if the environment variable is missing.

**Files Modified:**
- `src/most_similar_image.py`
- `src/text_to_audio.py`
- `src/generate_image.py`
- `src/music_selection.py`
- `src/content_generator.py`

**What Changed:**
- Client initialization is now deferred until the first API call
- Better error messages that tell you exactly what's missing
- Application can start even if API key is not set (will fail only when API features are used)

### 2. Environment Variable Configuration Required ⚠️

You **MUST** add the `GOOGLE_API_KEY` environment variable in your Render dashboard.

#### Steps to Add Environment Variable on Render:

1. **Go to Render Dashboard**
   - Navigate to https://dashboard.render.com/
   - Select your web service (presently-ai-1)

2. **Access Environment Settings**
   - Click on your service
   - Go to the "Environment" tab in the left sidebar

3. **Add the API Key**
   - Click "Add Environment Variable"
   - **Key**: `GOOGLE_API_KEY`
   - **Value**: Your actual Google API key (copy from your local `.env` file or Google Cloud Console)
   - Click "Save Changes"

4. **Redeploy**
   - After saving, Render will automatically trigger a new deployment
   - Wait for the deployment to complete
   - Your application should now start successfully!

## How to Get Your Google API Key

If you don't have your API key handy:

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it into Render's environment variables

## Testing Locally

Before pushing to Render, you can test locally to ensure everything still works:

```powershell
# Make sure you have a .env file with your API key
# It should contain:
# GOOGLE_API_KEY=your_actual_api_key_here

# Run the application
python web/app.py
```

## Deployment Checklist

- [x] Code changes applied to handle missing API key gracefully
- [ ] Push changes to GitHub
- [ ] Add `GOOGLE_API_KEY` to Render environment variables
- [ ] Wait for automatic redeployment on Render
- [ ] Verify application starts without errors
- [ ] Test the application functionality

## Next Steps

1. **Commit and push these changes:**
   ```powershell
   git add .
   git commit -m "Fix: Defer Google AI client initialization to prevent startup crashes"
   git push origin main
   ```

2. **Add the environment variable in Render** (as described above)

3. **Monitor the deployment logs** in Render to confirm it starts successfully

## Expected Result

After completing these steps, you should see in the Render logs:
```
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: X
```

And your service should be accessible at: https://presently-ai-1.onrender.com

## Troubleshooting

### Still seeing the error after adding the environment variable?
- Make sure you saved the environment variable in Render
- Check that there are no extra spaces in the key or value
- Verify the API key is valid by testing it locally first

### Application starts but API features don't work?
- Check the Render logs for error messages
- Verify the API key has the necessary permissions
- Ensure you're not hitting API rate limits

---

If you encounter any other issues, check the Render logs for specific error messages.

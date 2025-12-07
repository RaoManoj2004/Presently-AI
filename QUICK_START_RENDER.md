# 🚀 Quick Start - Add Environment Variable to Render

## ⚠️ CRITICAL STEP - Do This Now!

Your code changes have been pushed to GitHub. Render will automatically redeploy, BUT it will still fail unless you add the environment variable.

## 📋 Step-by-Step Instructions

### 1. Open Render Dashboard
Go to: https://dashboard.render.com/

### 2. Select Your Service
Click on **presently-ai-1** (or your service name)

### 3. Go to Environment Tab
- Look for "Environment" in the left sidebar
- Click on it

### 4. Add Environment Variable
Click the **"Add Environment Variable"** button

Fill in:
- **Key**: `GOOGLE_API_KEY` (exactly as written, case-sensitive)
- **Value**: Your Google API key (from your local development or Google AI Studio)

### 5. Save
Click **"Save Changes"**

Render will automatically trigger a new deployment.

---

## 🔑 Where to Get Your Google API Key

If you don't have your API key:

1. Go to: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click "Create API Key" or use an existing one
4. Copy the key

**Important**: The key starts with something like `AIza...`

---

## ✅ Verification

After adding the environment variable and the deployment completes:

1. Check Render logs - you should see:
   ```
   [INFO] Booting worker with pid: X
   ```
   Without any `ValueError` about missing API key

2. Visit your site: https://presently-ai-1.onrender.com
   It should load without errors!

---

## 📞 Still Having Issues?

If the deployment still fails after adding the environment variable:

1. **Double-check the variable name**: Must be exactly `GOOGLE_API_KEY`
2. **Verify the API key is valid**: Test it locally first
3. **Check for spaces**: Make sure there are no extra spaces before/after the key
4. **Wait for deployment**: Give Render a few minutes to redeploy after saving

---

**Next Steps After Adding the Variable:**
Just wait for Render to redeploy (usually 2-5 minutes), then test your application!

# 🔑 Add GOOGLE_API_KEY to Render - Step-by-Step Guide

## ✅ Current Status
Your code is working perfectly! The error message you're seeing is **EXPECTED** and means our error handling is working correctly.

**The Error:**
```
GOOGLE_API_KEY environment variable is not set. 
Please configure it in your Render dashboard under Environment variables.
```

**What This Means:**
- ✓ Your application deployed successfully
- ✓ Error handling is working
- ✗ You just need to add the API key

---

## 📋 Step-by-Step Instructions

### Step 1: Get Your Google API Key

You need to copy your API key from one of these sources:

#### Option A: From Your Local `.env` File
1. Open the file: `c:\Users\Admin\Desktop\Manoj Rao S\presently\.env`
2. Look for the line that says: `GOOGLE_API_KEY=...`
3. Copy everything after the `=` sign (should start with `AIza...`)

#### Option B: Create a New API Key
If you don't have one or can't find it:
1. Go to: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

---

### Step 2: Add the Key to Render

#### 🌐 Open Render Dashboard
1. **Go to:** https://dashboard.render.com/
2. **Sign in** to your account
3. You'll see your services list

#### 🎯 Select Your Service
1. **Click on:** `presently-ai-1` (or your service name)
2. You'll see your service details page

#### ⚙️ Go to Environment Settings
1. Look at the **left sidebar**
2. **Click on:** "Environment" (has a gear icon ⚙️)
3. You'll see environment variables page

#### ➕ Add the API Key
1. **Click:** Blue "Add Environment Variable" button
2. **Fill in:**
   - **Key:** `GOOGLE_API_KEY` (exactly as written, case-sensitive!)
   - **Value:** Paste your API key (the one starting with `AIza...`)
3. **Click:** "Save Changes" button

#### ⏳ Wait for Deployment
- Render will automatically start a new deployment
- This takes about **2-3 minutes**
- You'll see "Deploying..." status

---

## 🎯 Visual Guide

### What You're Looking For:

**In Render Dashboard > Your Service > Environment:**

```
┌─────────────────────────────────────────────┐
│  Environment Variables                      │
├─────────────────────────────────────────────┤
│                                             │
│  [+ Add Environment Variable]  ← Click this│
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Key:   GOOGLE_API_KEY              │   │
│  │ Value: AIza...your_actual_key...   │   │
│  │                                     │   │
│  │        [Save Changes]               │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## ✅ Verification Steps

### After Adding the Environment Variable:

1. **Wait 2-3 minutes** for Render to redeploy

2. **Check Render Logs:**
   - Go to: Render Dashboard > Your Service > Logs
   - Look for: `[INFO] Booting worker with pid: X`
   - Should **NOT** see: `ValueError: Missing key`

3. **Test Your Application:**
   - Go to: https://presently-ai-1.onrender.com
   - Login
   - Try generating a presentation
   - Should work without API key errors!

---

## ⚠️ Common Mistakes to Avoid

### ❌ Wrong Key Name
```
GOOGLE_API_KEY     ✓ Correct
google_api_key     ✗ Wrong (case matters!)
GOOGLE-API-KEY     ✗ Wrong (use underscore, not dash)
API_KEY            ✗ Wrong (must be exact name)
```

### ❌ Extra Spaces
Make sure there are **NO spaces** before or after the key:
```
AIzaSyC...         ✓ Correct
 AIzaSyC...        ✗ Wrong (space before)
AIzaSyC...         ✗ Wrong (space after)
```

### ❌ Wrong Value Format
Your API key should:
- Start with `AIza`
- Be about 39 characters long
- Contain only letters, numbers, and maybe `-` or `_`

---

## 🆘 Troubleshooting

### "I don't see the Environment tab"
- Make sure you're on the service detail page, not the main dashboard
- Look for tabs like: Overview, Events, **Environment**, Logs, Settings

### "The key still doesn't work"
1. **Double-check the key value** - Copy-paste again to be sure
2. **Check for typos** in the variable name
3. **Wait for deployment to finish** - Takes 2-3 minutes
4. **Check Render logs** for any new errors

### "I don't have an API key"
1. Go to https://aistudio.google.com/apikey
2. Sign in with Google
3. Create a new API key
4. Enable billing if needed (has free tier!)

---

## 📸 Quick Reference

**Where to find things in Render:**

1. **Dashboard:** https://dashboard.render.com/
2. **Your Service:** Click on `presently-ai-1`
3. **Environment Tab:** Left sidebar → Environment
4. **Logs:** Left sidebar → Logs (to verify deployment)

---

## 🚀 Expected Result

After adding the environment variable and waiting for deployment:

### ✅ Success Looks Like:
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 8
==> Your service is live 🎉
```

### ✅ Testing Should Work:
1. Visit https://presently-ai-1.onrender.com
2. Login
3. Enter a URL to scrape
4. Generate presentation
5. **No API key errors!** ✨

---

## ⏱️ Timeline

- **Now:** Add the environment variable (takes 1 minute)
- **+0-1 min:** Render starts deployment
- **+2-3 min:** Deployment completes
- **+3 min:** Test your application - should work!

---

**🎯 Bottom Line:** Go to Render Dashboard → Your Service → Environment → Add `GOOGLE_API_KEY` → Save → Wait 3 minutes → Test!

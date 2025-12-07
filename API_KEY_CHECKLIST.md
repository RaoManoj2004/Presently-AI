# ✅ Quick Checklist - Add API Key to Render

## Your Mission: Add GOOGLE_API_KEY to Render

Follow these 5 simple steps:

---

## ☑️ Step 1: Get Your API Key

**Choose ONE option:**

### Option A: From Local .env File
- [ ] Open: `c:\Users\Admin\Desktop\Manoj Rao S\presently\.env`
- [ ] Find line: `GOOGLE_API_KEY=AIza...`
- [ ] Copy everything after `=`

### Option B: Create New Key
- [ ] Go to: https://aistudio.google.com/apikey
- [ ] Sign in
- [ ] Click "Create API Key"
- [ ] Copy the key

**Your API Key (should start with `AIza`):**
```
AIza________________________________ (paste here for reference)
```

---

## ☑️ Step 2: Open Render Dashboard

- [x] Go to: https://dashboard.render.com/ ← **ALREADY OPEN!**
- [ ] Sign in (if needed)

---

## ☑️ Step 3: Navigate to Environment

- [ ] Click on your service: **`presently-ai-1`**
- [ ] Look at left sidebar
- [ ] Click on: **"Environment"** (has a ⚙️ gear icon)

---

## ☑️ Step 4: Add the Environment Variable

- [ ] Click blue **"Add Environment Variable"** button
- [ ] **Key:** Type exactly: `GOOGLE_API_KEY`
- [ ] **Value:** Paste your API key (from Step 1)
- [ ] Click **"Save Changes"**

**Double-check:**
- [ ] Key name is exactly `GOOGLE_API_KEY` (uppercase, with underscores)
- [ ] No spaces before or after the value
- [ ] Value starts with `AIza`

---

## ☑️ Step 5: Wait for Deployment

- [ ] Render shows "Deploying..." message
- [ ] Wait **2-3 minutes** for deployment to complete
- [ ] Check **Logs** tab for: `[INFO] Booting worker`
- [ ] Should NOT see any `ValueError` about missing API key

---

## ✅ Verification

After deployment completes:

- [ ] Go to: https://presently-ai-1.onrender.com
- [ ] Login with your account
- [ ] Try generating a presentation
- [ ] Should work without API key errors! 🎉

---

## 🆘 If Something Goes Wrong

### Can't find Environment tab?
- Make sure you clicked on your service first
- Environment should be in the left sidebar

### Still getting API key error?
- Check spelling: `GOOGLE_API_KEY` (exact match)
- Check for extra spaces in the value
- Make sure deployment finished (check Logs)

### Don't have an API key?
- Go to: https://aistudio.google.com/apikey
- Create one (it's free!)
- Come back and add it to Render

---

## 📞 Need Help?

**Windows are open:**
- ✓ Render Dashboard (browser)
- ✓ Detailed Guide (Notepad - `ADD_API_KEY_TO_RENDER.md`)

**Next steps:**
1. Follow checklist above
2. Add the environment variable
3. Wait 2-3 minutes
4. Test your application!

---

**You've got this! The application is 99% there - just needs the API key! 💪**

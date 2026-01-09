# 🚀 DEPLOYMENT INSTRUCTIONS - Netlify

## Quick Start (2 Minutes)

### Step 1: Prepare Your Files
Your deployment folder already contains:
- ✅ `psycho-pictionary.html` (main game file)
- ✅ `netlify.toml` (configuration)
- ✅ `README.md` (documentation)

### Step 2: Deploy to Netlify

#### **EASIEST: Drag & Drop**
1. Go to https://app.netlify.com
2. Create a free account (or sign in)
3. **Drag and drop** the entire `/psycho/frontend` folder onto the page
4. Wait 30 seconds ⏳
5. Your game is LIVE! 🎉

#### **OPTION 2: GitHub + Auto Deploy**
```bash
cd /Users/maryamnaz/Desktop/psycho/frontend
git init
git add .
git commit -m "Initial commit: Psycho Pictionary game"
git remote add origin https://github.com/YOUR_USERNAME/psycho-pictionary.git
git push -u origin main
```
Then connect your GitHub repo to Netlify for auto-deployments.

#### **OPTION 3: Using Netlify CLI**
```bash
npm install -g netlify-cli
cd /Users/maryamnaz/Desktop/psycho/frontend
netlify login
netlify deploy --prod
```

---

## What You Get After Deployment

- 🌐 **Public URL**: `https://your-game.netlify.app`
- ⚡ **Free HTTPS**: Automatic SSL certificate
- 🚀 **CDN**: Global content delivery
- 📱 **Mobile Optimized**: Responsive design works everywhere
- 💾 **No Backend Needed**: All data stored locally in user browsers
- 🔄 **Auto Deploy**: Updates whenever you push to GitHub

---

## Post-Deployment

### Share Your Game
```
Share this link with friends/students:
https://your-game.netlify.app
```

### Monitor Usage
- Visit Netlify dashboard to see analytics
- Track how many players use your game
- No personal data is collected (stored locally only)

### Customize (Optional)
Edit `netlify.toml` to:
- Change site name
- Add custom domains
- Configure redirects

---

## Features Included

✅ Player registration (name + age)
✅ 3 difficulty levels with 90+ words
✅ Dashboard with player statistics
✅ Psychology insights & analysis
✅ Story mode with keyword validation
✅ Leaderboards & performance tracking
✅ Fully responsive design
✅ No server/backend required
✅ All data stored locally (privacy-safe)

---

## Technical Details

- **Framework**: Pure HTML5 + CSS3 + JavaScript (no dependencies)
- **Size**: 79 KB
- **Performance**: Instant load, smooth gameplay
- **Compatibility**: Works on all modern browsers
- **Hosting**: Works on ANY static hosting (Netlify, GitHub Pages, Vercel, etc.)

---

## Troubleshooting

**Q: Getting a 404 error?**
A: Make sure `netlify.toml` is deployed. Check the "Deploys" tab in Netlify.

**Q: Player data not saving?**
A: Check browser localStorage in DevTools. It should show player data.

**Q: Want to use a custom domain?**
A: Go to Netlify > Site Settings > Domain Management > Add custom domain

---

## Next Steps

1. ✅ Deploy to Netlify (follow above)
2. ✅ Test the game in your live URL
3. ✅ Share with friends/students
4. ✅ Customize with your own words (edit HTML if needed)

---

**Ready?** Click "Deploy" now! 🚀

Questions? Check the README.md for more info.

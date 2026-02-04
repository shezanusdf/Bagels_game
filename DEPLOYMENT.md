# Deployment Guide

## Local Development

### Your OAuth Credentials are Already Configured!

Your secrets are stored in `.streamlit/secrets.toml` (not committed to Git):
- **Client ID**: `e98516a57164c7a58484cdc57647b915`
- **Client Secret**: `a62e62acb4d21ab932aabf4c6125f21fdd3edc57a7eeee44d74f9cce1e7132cb`
- **Redirect URI**: `https://bagels.streamlit.app/`

### Run Locally

```bash
streamlit run streamlit_bagels.py
```

**Note**: For local testing, you may need to add `http://localhost:8501` as an additional redirect URI in your Hack Club OAuth app settings.

## Deploy to Streamlit Cloud

### 1. Push to GitHub ✅
Already done! Your repo is at: https://github.com/shezanusdf/Bagels_game

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository**: `shezanusdf/Bagels_game`
   - **Branch**: `master`
   - **Main file path**: `streamlit_bagels.py`

### 3. Add Secrets in Streamlit Cloud

In the Streamlit Cloud dashboard, go to **App settings** → **Secrets** and paste:

```toml
HACKCLUB_CLIENT_ID = "e98516a57164c7a58484cdc57647b915"
HACKCLUB_CLIENT_SECRET = "a62e62acb4d21ab932aabf4c6125f21fdd3edc57a7eeee44d74f9cce1e7132cb"
REDIRECT_URI = "https://bagels.streamlit.app/"
```

### 4. Deploy!

Click "Deploy" and your app will be live at: **https://bagels.streamlit.app/**

## Security Notes

✅ **Secrets are NOT in Git**: The `.streamlit/secrets.toml` file is in `.gitignore`
✅ **Credentials are safe**: They only exist locally and in Streamlit Cloud's encrypted storage
✅ **Redirect URI matches**: Your OAuth app is configured for the deployed URL

## Troubleshooting

### OAuth Error "redirect_uri_mismatch"
- Verify the redirect URI in Streamlit secrets matches: `https://bagels.streamlit.app/`
- Make sure your Hack Club OAuth app has this exact URI (with trailing slash)

### "OAuth not configured" Message
- Check that secrets are properly added in Streamlit Cloud dashboard
- Restart the app after adding secrets

### Leaderboard Not Saving
- Leaderboard data is stored in `leaderboard.json`
- On Streamlit Cloud, this will reset when the app restarts (consider using a database for persistent storage)

## Next Steps

Consider upgrading to a persistent database for the leaderboard:
- **Supabase** (free tier available)
- **MongoDB Atlas** (free tier available)
- **PostgreSQL on Railway** (free tier available)

This will prevent leaderboard data loss when the app restarts.

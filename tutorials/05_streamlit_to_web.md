# Tutorial 5, Ship a Streamlit app to the web

We will deploy the chat app skeleton.

## Step 1, run locally

```bash
pip install streamlit anthropic openai
export ANTHROPIC_API_KEY=...
streamlit run courses/06-genai/streamlit_app_skeleton.py
```

## Step 2, push to GitHub

```bash
git init
git add .
git commit -m "Initial AI for Caribbeans app"
git remote add origin https://github.com/yourname/your-app.git
git push -u origin main
```

## Step 3, deploy on Streamlit Community Cloud

1. Go to share.streamlit.io.
2. Connect your GitHub.
3. Pick the repo and the file path to the Streamlit script.
4. Add your `ANTHROPIC_API_KEY` as a secret in the app settings.
5. Click Deploy.

## Step 4, share

You get a URL like `https://yourapp.streamlit.app`. Share it.

## When to graduate from Streamlit

- You need authentication (use Supabase or Clerk).
- You need to handle payments (Stripe).
- You need real time chat with streaming (Next.js with Vercel AI SDK).
- You need a mobile native app (React Native or Flutter).

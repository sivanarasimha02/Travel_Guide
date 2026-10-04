#!/usr/bin/env bash
# ==============================================================================
# AI Travel Guide - Deployment Script (Frontend: Vercel | Backend: Render)
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "======================================================="
echo "🌍 AI Travel Guide - Deployment Manager"
echo "   Frontend: Vercel | Backend: Render"
echo "======================================================="

ACTION="${1:-help}"

case "$ACTION" in
  vercel)
    echo "▲ Deploying Frontend to Vercel..."
    if command -v vercel &> /dev/null; then
      vercel --prod
    elif command -v npx &> /dev/null; then
      npx vercel --prod
    else
      echo "⚠️  Vercel CLI not found."
      echo "To deploy to Vercel:"
      echo "1. Install Vercel CLI: npm install -g vercel"
      echo "2. Run: vercel --prod"
      echo "Or import your GitHub repo directly on https://vercel.com/new"
    fi
    ;;

  render)
    echo "🚀 Render Backend Deployment Preparation..."
    echo "1. Ensure your git repo is committed & pushed to GitHub/GitLab:"
    echo "   git add ."
    echo "   git commit -m 'Deploy to Render & Vercel'"
    echo "   git push origin main"
    echo ""
    echo "2. In Render (https://dashboard.render.com/):"
    echo "   - Click 'New +' -> 'Web Service'"
    echo "   - Connect your repository"
    echo "   - Render will auto-detect settings from render.yaml / Procfile:"
    echo "     * Build Command: pip install -r requirements.txt"
    echo "     * Start Command: gunicorn --bind 0.0.0.0:\$PORT --workers 2 --threads 4 --timeout 120 Backend.app:app"
    echo "   - Add Environment Variables in Render Dashboard:"
    echo "     * GEMINI_API_KEY"
    echo "     * MURF_API_KEY"
    echo ""
    echo "3. After deploying on Render, copy your service URL (e.g. https://your-backend.onrender.com)"
    echo "   and update RENDER_BACKEND_URL in Frontend/index.js (or deploy frontend to Vercel)."
    ;;

  prod)
    echo "🚀 Starting Backend locally with Gunicorn (Production Mode)..."
    if [ ! -d ".venv" ]; then
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q -r requirements.txt
    PORT="${PORT:-5001}"
    echo "Running at http://127.0.0.1:$PORT"
    exec gunicorn --bind "0.0.0.0:$PORT" --workers 2 --threads 4 --timeout 120 Backend.app:app
    ;;

  dev|local)
    echo "🛠️  Starting Backend locally (Development Mode)..."
    if [ ! -d ".venv" ]; then
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -q -r requirements.txt
    exec python Backend/app.py
    ;;

  *)
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commands:"
    echo "  ./deploy.sh vercel    Deploy frontend to Vercel"
    echo "  ./deploy.sh render    Show Render backend deployment guide"
    echo "  ./deploy.sh prod      Run backend locally with Gunicorn (port 5001)"
    echo "  ./deploy.sh dev       Run backend locally with Flask (port 5001)"
    echo ""
    ;;
esac

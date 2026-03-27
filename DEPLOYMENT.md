# OTT Platform Deployment Guide

## Prerequisites

- GitHub account with the repository
- Render account (free tier available)
- MongoDB Atlas account (free tier)

## Step 1: Set up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Create a database user
4. Get the connection string: `mongodb+srv://username:password@cluster.mongodb.net/dbname`

## Step 2: Deploy Backend to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ott-platform-backend
   - **Root Directory**: backend
   - **Environment**: Docker
   - **Branch**: main
   - **Build Command**: (leave empty, uses Dockerfile)
   - **Start Command**: (leave empty, uses Dockerfile CMD)
5. Add Environment Variables:
   - `MONGO_URL`: your MongoDB connection string
   - `DB_NAME`: cineai (or your chosen name)
6. Click "Create Web Service"

## Step 3: Deploy Frontend to Render

1. In Render Dashboard, click "New" → "Web Service"
2. Connect the same GitHub repository
3. Configure:
   - **Name**: ott-platform-frontend
   - **Root Directory**: frontend
   - **Environment**: Docker
   - **Branch**: main
4. Add Environment Variable:
   - `REACT_APP_BACKEND_URL`: https://your-backend-service-name.onrender.com
5. Click "Create Web Service"

## Step 4: Update Frontend API URL

After backend is deployed, update the REACT_APP_API_URL in the frontend service with the actual backend URL.

## Step 5: Access Your App

- Frontend: https://your-frontend-service-name.onrender.com
- Backend API: https://your-backend-service-name.onrender.com/api

## Alternative: Vercel Deployment

If you prefer Vercel:

1. **Frontend on Vercel**:
   - Import repository to Vercel
   - Set root directory to `frontend`
   - Add environment variable: `REACT_APP_BACKEND_URL`

2. **Backend on Vercel** (more complex):
   - Would require converting to serverless functions
   - Or deploy backend separately on Render

## Notes

- Render free tier has limitations (750 hours/month)
- MongoDB Atlas free tier: 512MB storage
- Make sure to update CORS in backend if needed for the frontend domain

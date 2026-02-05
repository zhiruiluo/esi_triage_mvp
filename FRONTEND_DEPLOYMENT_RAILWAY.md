# Frontend Deployment to Railway

## Setup Instructions

1. **Create new service in Railway**
   - Go to your existing project on Railway
   - Click "New Service" → "GitHub repo"
   - Select your repo (zhiruiluo/esi_triage_mvp)

2. **Configure service settings**
   - Name: `esi-triage-frontend`
   - Root Directory: (leave empty)

3. **Add environment variables**
   - `NEXT_PUBLIC_API_URL`: Your backend Railway URL (e.g., `https://your-backend-domain.railway.app`)

4. **Set build & start commands**
   - Build: (auto-detect should work)
   - Start: `npm start` or use railway-frontend.toml

5. **Deploy**
   - Click deploy and wait for build to complete

## Notes

- Frontend will be deployed to its own Railway domain
- It connects to the backend via `NEXT_PUBLIC_API_URL` environment variable
- Both services are in the same Railway project for easy management
- Updates to main branch will trigger automatic redeployment

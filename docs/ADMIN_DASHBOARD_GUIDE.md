# Admin Dashboard Guide

## 🎉 New: Admin Web Dashboard

You now have a **visual admin dashboard** at `/admin` route!

### Features

✅ **Login Screen** - Secure API key authentication
✅ **Visual Layer Control** - Toggle RAG on/off with buttons
✅ **Confidence Sliders** - Adjust thresholds with visual sliders
✅ **Global Toggle** - Enable/disable all RAG with one click
✅ **Real-time Stats** - View current configuration
✅ **Knowledge Sources** - See which sources each layer uses

---

## 🔐 Authentication

### How It Works

1. **API Key Based**: Simple and secure
2. **Header Authentication**: All requests include `X-Admin-Key` header
3. **Session Storage**: API key stored in browser session (cleared on close)
4. **Environment Variable**: Set `ADMIN_API_KEY` in your environment

### Default API Key

```bash
Default: admin123
```

⚠️ **CHANGE THIS IN PRODUCTION!**

### Set Custom API Key

**Backend (Railway)**:
```bash
# In Railway dashboard, add environment variable:
ADMIN_API_KEY=your-secure-key-here
```

**Local Development**:
```bash
# In .env file:
ADMIN_API_KEY=your-secure-key-here
```

---

## 🚀 Access the Dashboard

### Live (Once Deployed)

```
https://your-frontend.railway.app/admin
```

### Local Development

```bash
# Terminal 1: Start backend
cd app
python -m uvicorn main:app --reload

# Terminal 2: Start frontend
cd nextjs-app
npm run dev

# Open in browser:
http://localhost:3000/admin
```

---

## 📱 Using the Dashboard

### 1. Login

1. Navigate to `/admin`
2. Enter your API key (default: `admin123`)
3. Click "Login"
4. API key is saved in session (auto-logout on browser close)

### 2. View Configuration

- **Global RAG Status**: See if RAG is enabled/disabled globally
- **All 7 Layers**: View each layer's configuration
- **Knowledge Sources**: See which sources each layer uses
- **Confidence Thresholds**: Current threshold values displayed

### 3. Toggle Layers

**Enable/Disable Individual Layer:**
- Click the "Enabled"/"Disabled" button on any layer card
- Layer 1 (Sanity Check) cannot be toggled (no RAG needed)

**Global Toggle:**
- Click the global "Enabled"/"Disabled" button at the top
- Affects all layers at once (emergency switch)

### 4. Adjust Confidence Thresholds

**Using Slider:**
- Drag the slider left (0.5) for permissive (more knowledge)
- Drag the slider right (1.0) for strict (high confidence only)
- Changes save automatically on release

**Recommended Values:**
- **0.50-0.70**: Aggressive (maximum knowledge coverage)
- **0.75-0.85**: Balanced (recommended for production)
- **0.90-1.00**: Strict (only high-confidence knowledge)

---

## 🔧 API Authentication (cURL)

All admin API endpoints now require authentication:

```bash
# View config
curl https://backend.railway.app/admin/rag/config \
  -H "X-Admin-Key: admin123"

# Enable layer
curl -X POST https://backend.railway.app/admin/rag/layer/3/enable \
  -H "X-Admin-Key: admin123"

# Update threshold
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.85" \
  -H "X-Admin-Key: admin123"
```

### Without API Key

```bash
# Returns 401 Unauthorized
curl https://backend.railway.app/admin/rag/config
# Response: {"detail": "Admin API key required. Include X-Admin-Key header."}
```

### With Wrong API Key

```bash
# Returns 403 Forbidden
curl https://backend.railway.app/admin/rag/config \
  -H "X-Admin-Key: wrong-key"
# Response: {"detail": "Invalid admin API key"}
```

---

## 🎨 Dashboard Screenshots

### Login Screen
```
┌─────────────────────────────────────┐
│        Admin Login                  │
│                                     │
│  Enter your admin API key to        │
│  access the RAG configuration       │
│  dashboard.                         │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Admin API Key               │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │         Login               │   │
│  └─────────────────────────────┘   │
│                                     │
│  Default API key: admin123          │
└─────────────────────────────────────┘
```

### Main Dashboard
```
┌──────────────────────────────────────────────────┐
│  RAG Admin Dashboard          [Logout]           │
├──────────────────────────────────────────────────┤
│  Global RAG Control                              │
│  Global RAG Status              [Enabled ✓]      │
│  RAG is enabled for all layers                   │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  Layer 3: Red Flag Detection      [Enabled ✓]    │
│  Detect ESI-2 criteria using handbook...         │
│                                                  │
│  Knowledge Sources:                              │
│  [esi_handbook] [acs_protocols] [sepsis_criteria]│
│                                                  │
│  Confidence Threshold: 0.85                      │
│  ●─────────────────○─────────────────            │
│  0.5 (Permissive)              1.0 (Strict)      │
└──────────────────────────────────────────────────┘
```

---

## 🔒 Security Best Practices

### For Production

1. **Change Default API Key**
   ```bash
   # Railway environment variable
   ADMIN_API_KEY=generate-strong-random-key-here
   ```

2. **Use Strong Key**
   ```bash
   # Generate secure random key (example)
   openssl rand -hex 32
   # Output: 8f3e9d2c1a4b7e6f...
   ```

3. **Rotate Regularly**
   - Change API key every 30-90 days
   - Update in Railway environment variables
   - Inform authorized admins

4. **Limit Access**
   - Only share with authorized personnel
   - Use separate keys for different environments
   - Never commit keys to Git

### Future Enhancements

For production-scale deployments, consider upgrading to:

- **JWT Authentication**: Token-based with expiration
- **OAuth 2.0**: Integration with Google/Microsoft/GitHub
- **Role-Based Access Control (RBAC)**: Different permission levels
- **Audit Logging**: Track who changed what and when
- **IP Whitelisting**: Restrict access by IP address
- **Multi-Factor Authentication (MFA)**: Additional security layer

---

## 🐛 Troubleshooting

### "Invalid API key" Error

**Problem**: Getting 403 Forbidden
**Solution**: 
1. Check API key matches `ADMIN_API_KEY` environment variable
2. Verify no extra spaces in API key
3. Check Railway environment variables are set

### Dashboard Won't Load

**Problem**: Blank page or errors
**Solution**:
1. Check backend is running: `curl https://backend.railway.app/health`
2. Verify frontend deployed correctly
3. Check browser console for errors

### API Key Not Persisting

**Problem**: Have to login every page refresh
**Solution**:
1. API key is intentionally stored in sessionStorage (cleared on browser close)
2. This is for security - re-login after closing browser
3. For longer persistence, consider JWT tokens (future enhancement)

### Can't Toggle Layer

**Problem**: Layer 1 won't toggle
**Solution**:
- Layer 1 (Sanity Check) doesn't use RAG - toggle disabled by design
- All other layers (2-7) should toggle normally

---

## 📊 Monitoring

### What to Monitor

```bash
# Check authentication working
curl https://backend.railway.app/admin/rag/stats \
  -H "X-Admin-Key: your-key"

# Monitor dashboard usage
# (Check Railway logs for admin endpoint access)

# Track configuration changes
# (All changes logged in backend)
```

### Dashboard Activity

Railway logs will show:
```
INFO: Admin endpoint accessed: /admin/rag/config
INFO: Layer 3 RAG toggled: enabled
INFO: Threshold updated: layer 3 -> 0.85
```

---

## 🎯 Quick Start

### First Time Setup

1. **Deploy to Railway** (if not already done)
   ```bash
   git push  # Auto-deploys to Railway
   ```

2. **Set Admin API Key** (Railway Dashboard)
   ```
   Environment Variables → Add Variable
   ADMIN_API_KEY = your-secure-key
   ```

3. **Access Dashboard**
   ```
   https://your-frontend.railway.app/admin
   ```

4. **Login with API Key**
   - Enter the API key you set in step 2
   - Click "Login"

5. **Start Configuring**
   - Toggle layers
   - Adjust thresholds
   - Monitor in real-time

---

## 📝 Summary

**What You Have:**

✅ **Web Dashboard**: Visual admin interface at `/admin`
✅ **API Key Auth**: Secure access with `X-Admin-Key` header
✅ **Visual Controls**: Buttons, sliders, toggles
✅ **Real-time Updates**: See changes immediately
✅ **Session Security**: Auto-logout on browser close
✅ **Both Methods**: Web UI + cURL API

**Default Access:**
- **URL**: `https://your-frontend.railway.app/admin`
- **API Key**: `admin123` (CHANGE IN PRODUCTION!)
- **Storage**: SessionStorage (secure, temporary)

**Next Steps:**
1. Deploy to Railway
2. Set secure `ADMIN_API_KEY`
3. Access `/admin` route
4. Start configuring RAG layers!

🚀 **Admin dashboard is ready to use!**

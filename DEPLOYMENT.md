# EnTrack Deployment Guide for Render

## Overview
This guide will help you deploy your EnTrack Django application to Render with PostgreSQL database.

## Prerequisites
- GitHub account with your EnTrack repository
- Render account (free tier available)

## Step 1: Prepare Your Repository

### Files Added/Modified:
- ✅ `requirements.txt` - Updated with PostgreSQL and production dependencies
- ✅ `entrack/settings.py` - Updated for production environment
- ✅ `dashboard/forms.py` - Fixed duplicate email validation
- ✅ `render.yaml` - Render deployment configuration
- ✅ `Procfile` - Process file for Render
- ✅ `runtime.txt` - Python version specification
- ✅ `env.example` - Environment variables template

## Step 2: Deploy to Render

### Option A: Using Render Dashboard (Recommended)

1. **Create a New Web Service:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the Service:**
   - **Name:** `entrack` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn entrack.wsgi`
   - **Plan:** Free (or paid if you prefer)

3. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a secure secret key (you can use Django's `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (replace with your actual domain)

### Option B: Using render.yaml (Alternative)

1. **Create a PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name it `entrack-db`
   - Note the connection details

2. **Deploy using render.yaml:**
   - Push your code to GitHub
   - The `render.yaml` file will automatically configure your deployment

## Step 3: Database Setup

### Automatic Migration (Recommended):
Render will automatically run migrations during deployment if you use the `render.yaml` configuration.

### Manual Migration (if needed):
```bash
# Connect to your Render service via SSH or use Render's shell
python manage.py migrate
python manage.py collectstatic --noinput
```

## Step 4: Create Superuser (Optional)

To access Django admin panel:
```bash
python manage.py createsuperuser
```

## Step 5: Verify Deployment

1. **Check your application URL:** `https://your-app-name.onrender.com`
2. **Test registration:** Try registering with the same email twice (should show error)
3. **Test login/logout:** Verify authentication works
4. **Test calculator:** Ensure the calculator page loads correctly

## Environment Variables Reference

### Development (.env file):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (Render):
```env
DATABASE_URL=postgresql://... (automatically set by Render)
SECRET_KEY=... (set manually)
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
```

## Troubleshooting

### Common Issues:

1. **Static Files Not Loading:**
   - Ensure `python manage.py collectstatic --noinput` is in build command
   - Check WhiteNoise middleware is in settings.py

2. **Database Connection Errors:**
   - Verify DATABASE_URL is set correctly
   - Check PostgreSQL service is running

3. **Template Errors:**
   - All template issues have been fixed in this update
   - Calculator, settings, and logout should work correctly

4. **Email Validation Not Working:**
   - The duplicate email validation has been added to the registration form
   - Test by trying to register with the same email twice

### Useful Commands:
```bash
# Check application status
python manage.py check

# View logs (in Render dashboard)
# Go to your service → Logs

# Run migrations manually
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

## Security Notes

- ✅ SECRET_KEY is now environment-based
- ✅ DEBUG is disabled in production
- ✅ ALLOWED_HOSTS is configured
- ✅ WhiteNoise handles static files securely
- ✅ Database credentials are environment-based

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Verify all environment variables are set
3. Ensure your GitHub repository is up to date
4. Test locally first with the same environment variables

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure email settings for notifications
3. Set up monitoring and backups
4. Consider upgrading to paid plan for better performance

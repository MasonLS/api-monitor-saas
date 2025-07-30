# Deploy to Heroku

## Prerequisites
1. Create a Heroku account at https://heroku.com
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

## Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create api-monitor-app
   # Note: Replace 'api-monitor-app' with your preferred name
   ```

3. **Add PostgreSQL database (free)**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Deploy from GitHub**
   ```bash
   git push heroku main
   ```

5. **Scale up the worker**
   ```bash
   heroku ps:scale worker=1
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

## Alternative: Deploy via Heroku Dashboard

1. Go to https://dashboard.heroku.com
2. Click "New" → "Create new app"
3. Choose app name and region
4. Go to "Deploy" tab
5. Connect to GitHub
6. Search for "api-monitor-saas"
7. Enable automatic deploys
8. Click "Deploy Branch"

## Useful Commands

- View logs: `heroku logs --tail`
- Run shell: `heroku run bash`
- Check status: `heroku ps`
- Restart app: `heroku restart`

## Costs
- Eco Dyno: $5/month (1000 hours)
- PostgreSQL Mini: $5/month
- Total: ~$10/month for production app

## Environment Variables
Set these in Heroku dashboard under Settings → Config Vars:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`

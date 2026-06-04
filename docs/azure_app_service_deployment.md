# Azure App Service Deployment

## Cost Guardrail

Use Azure for Students and choose the App Service F1 Free plan only.

Do not choose Basic, Standard, Premium, Container Apps, Virtual Machines,
Cosmos DB, Azure SQL, or paid storage for this demo.

## Architecture

```text
GitHub Pages dashboard
        |
        v
Azure App Service F1 Free API
        |
        v
MongoDB Atlas M0 Free
```

## Create the Web App

1. In the Azure portal, search for `App Services`.
2. Click `Create`.
3. Choose `Web App`.
4. Runtime stack: `Python`.
5. Publish: `Code`.
6. Operating system: `Linux`.
7. Pricing plan: choose `F1 Free`.

If you cannot select F1 Free, stop and do not create the app.

## GitHub Deployment

Connect the GitHub repository:

```text
urvilgodhani/data_projects
```

Use the `main` branch.

## App Settings

Add these application settings:

```text
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=digital_fulfillment_ops
SIMULATION_INTERVAL_SECONDS=60
STORE_UPDATE_PERCENT=0.10
LIVE_RETENTION_HOURS=72
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Keep `MONGODB_URI` secret. Do not commit it to GitHub.

## Startup Command

Set the startup command to:

```text
bash startup.sh
```

The script uses one worker so the simulator does not create duplicate live
ticks.

## Verify

Open:

```text
https://YOUR-AZURE-APP.azurewebsites.net/health
```

Expected:

```json
{
  "status": "ok",
  "mongodb_connected": true,
  "live_retention_hours": 72
}
```

After verification, update `live-config.js` with the Azure URL and push.

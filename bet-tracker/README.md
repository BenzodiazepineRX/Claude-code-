# Live Bet Tracker (AWS)

A private web app: upload a bet slip screenshot (or type it in), and it tracks every leg live
using ESPN's free public scoreboards, then settles the slip and adds it to your daily profit,
sport breakdown and charts.

## What runs on AWS (all in the project's selected Region)
| Piece | Service |
|---|---|
| Website | S3 + CloudFront |
| Private login | Amazon Cognito (only invited users, no self sign-up) |
| API | API Gateway (HTTP API) + Lambda (`backend/app.py`) |
| Live checker every 2 min | EventBridge rule + Lambda (`app.tracker_handler`) |
| Slips database | DynamoDB |
| Screenshot reading | Amazon Bedrock (Claude Sonnet 4.6, falls back to Nova Lite) |

Live data: `backend/espn.py` (NBA, NFL, soccer, tennis; moneyline, spread, totals, team totals,
player props). ESPN's feeds are unofficial and could change; anything not found can be marked by hand.

## Deploy (outline)
1. Zip `backend/*.py` and upload it plus `infra/template.yaml` to a private S3 bucket.
2. Create the CloudFormation stack from the template (`CodeBucket`, `CodeKey` parameters).
3. Upload `frontend/*` to the `SiteBucketName` output, plus a `config.js`:
   `window.BT_CONFIG={region:"us-east-2",clientId:"<UserPoolClientId>",apiUrl:"<ApiUrl>"};`
4. Invite yourself: `cognito-idp AdminCreateUser` with your email (a temporary password is emailed).

## Remove everything
Delete the CloudFormation stack (empty the two S3 buckets first) and the code bucket.

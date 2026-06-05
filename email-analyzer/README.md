## 📧 Daily Email Analyzer Agent

An automated agent that runs every morning at 7 AM, fetches your unread Gmail emails, summarizes them using AI, and sends you a beautiful summary email.

### Features

✨ **Daily Automation**: Runs automatically every morning at 7 AM  
🤖 **AI-Powered Summaries**: Uses OpenAI GPT to intelligently summarize emails  
📧 **Email Delivery**: Sends formatted summary directly to your inbox  
✅ **Auto-Mark as Read**: Automatically marks processed emails as read  
🔐 **Secure**: Uses Gmail App Passwords and OAuth2 authentication  
📊 **Beautiful Formatting**: HTML-formatted summary emails with styling  

### Setup Instructions

#### 1. Gmail Setup

**Step 1: Enable Gmail API**
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a new project
- Enable the **Gmail API**
- Create OAuth 2.0 credentials (Desktop application)
- Download the credentials file as `credentials.json`

**Step 2: Create Gmail App Password**
- Enable 2-Factor Authentication on your Gmail account
- Go to [Google Account Security](https://myaccount.google.com/security)
- Find "App passwords" section
- Select Mail and Windows Computer (or your device)
- Generate an app-specific password
- Save this password - you'll need it later

#### 2. OpenAI API Setup

- Go to [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Keep it safe - you'll need it for configuration

#### 3. GitHub Secrets Configuration

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

```
GMAIL_USER                = your-email@gmail.com
GMAIL_APP_PASSWORD        = your-app-specific-password
GMAIL_CREDENTIALS_PATH    = base64-encoded credentials.json content
OPENAI_API_KEY           = sk-...
RECIPIENT_EMAIL          = your-email@gmail.com (can be same as GMAIL_USER)
```

**To encode credentials.json to base64:**
```bash
base64 -i credentials.json | tr -d '\n'
```

#### 4. Local Testing

```bash
cd email-analyzer

# Install dependencies
npm install

# Create .env file with your configuration
cp .env.example .env
# Edit .env with your values

# Place credentials.json in this directory
cp /path/to/credentials.json ./credentials.json

# Run the analyzer
npm start
```

### Workflow Scheduling

The workflow is configured to run at:
- **1:30 AM UTC** (which equals 7:00 AM IST)
- **Adjust the cron expression** in `.github/workflows/email-analyzer.yml` for your timezone

#### Cron Time Examples:
```
# 7:00 AM UTC
'0 7 * * *'

# 7:00 AM EST (UTC-5)
'0 12 * * *'

# 7:00 AM IST (UTC+5:30)
'30 1 * * *'

# 7:00 AM PST (UTC-8)
'0 15 * * *'
```

### Project Structure

```
email-analyzer/
├── index.js              # Main entry point
├── gmail-client.js       # Gmail API integration
├── email-sender.js       # Email sending functionality
├── summarizer.js         # AI-powered email summarization
├── package.json          # Dependencies
├── .env.example          # Environment template
└── README.md            # This file
```

### How It Works

1. **Authentication**: Connects to Gmail using OAuth2 credentials
2. **Fetch**: Retrieves up to 10 unread emails
3. **Summarize**: Uses OpenAI GPT-3.5-turbo to summarize each email
4. **Format**: Creates a beautiful HTML email with summaries and key points
5. **Send**: Sends the summary email to your inbox
6. **Cleanup**: Marks all processed emails as read

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GMAIL_USER` | Your Gmail address | Yes |
| `GMAIL_APP_PASSWORD` | Gmail app-specific password | Yes |
| `GMAIL_CREDENTIALS_PATH` | Path to credentials.json | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `RECIPIENT_EMAIL` | Email to send summary to | No (defaults to GMAIL_USER) |

### Troubleshooting

**"Gmail credentials file not found"**
- Ensure credentials.json is in the email-analyzer directory
- Or set GMAIL_CREDENTIALS_PATH environment variable

**"Failed to authenticate with Gmail"**
- Verify OAuth2 credentials are valid
- Check that Gmail API is enabled in Google Cloud Console

**"OpenAI API error"**
- Verify your API key is correct
- Check account has available credits
- Review OpenAI rate limits

**Workflow not triggering**
- Check GitHub Actions is enabled in repository settings
- Verify cron schedule syntax
- Manually trigger workflow_dispatch for testing

### Manual Trigger

Run the workflow manually from GitHub:
1. Go to Actions tab
2. Select "Daily Email Analyzer"
3. Click "Run workflow"

### Cost Considerations

- **Gmail API**: Free (up to 1M daily queries)
- **OpenAI API**: Paid based on usage (~$0.001-0.002 per email summary)
- **GitHub Actions**: Free (2000 minutes/month for private repos)

### Future Enhancements

- [ ] Support for multiple email folders
- [ ] Custom summarization templates
- [ ] Filter emails by sender/subject
- [ ] Schedule multiple runs per day
- [ ] Slack/Discord notifications
- [ ] Database logging for history
- [ ] Advanced NLP analysis
- [ ] Email categorization

### License

MIT

### Support

For issues or questions:
1. Check troubleshooting section
2. Review GitHub Actions logs
3. Check OpenAI and Gmail API documentation

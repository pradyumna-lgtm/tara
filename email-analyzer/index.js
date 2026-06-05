require('dotenv').config();
const GmailClient = require('./gmail-client');
const EmailSummarizer = require('./summarizer');
const EmailSender = require('./email-sender');
const fs = require('fs');
const path = require('path');

async function runEmailAnalyzer() {
  console.log('🚀 Starting Daily Email Analyzer Agent...');
  console.log(`⏰ Running at: ${new Date().toLocaleString()}`);

  try {
    // Initialize Gmail Client
    const credentialsPath = process.env.GMAIL_CREDENTIALS_PATH || './credentials.json';
    
    if (!fs.existsSync(credentialsPath)) {
      console.error(`❌ Gmail credentials file not found at: ${credentialsPath}`);
      console.error('Please set up Gmail credentials. See setup instructions in README.md');
      process.exit(1);
    }

    const gmailClient = new GmailClient(credentialsPath);
    const authenticated = await gmailClient.authenticate();

    if (!authenticated) {
      console.error('❌ Failed to authenticate with Gmail');
      process.exit(1);
    }

    // Fetch unread emails
    console.log('📥 Fetching unread emails...');
    const unreadEmails = await gmailClient.getUnreadEmails(10);

    if (unreadEmails.length === 0) {
      console.log('✅ No unread emails. Nothing to summarize.');
      process.exit(0);
    }

    console.log(`✅ Found ${unreadEmails.length} unread emails`);

    // Summarize emails
    console.log('🤖 Summarizing emails with AI...');
    const summarizer = new EmailSummarizer(process.env.OPENAI_API_KEY);
    const summaries = await summarizer.summarizeEmails(unreadEmails);

    console.log(`✅ Generated ${summaries.length} summaries`);

    // Send summary email
    console.log('📧 Sending summary email...');
    const emailSender = new EmailSender(
      process.env.GMAIL_USER,
      process.env.GMAIL_APP_PASSWORD
    );

    const summaryData = {
      summaries,
      emailCount: unreadEmails.length,
      timestamp: new Date().toISOString()
    };

    const sent = await emailSender.sendSummary(
      process.env.RECIPIENT_EMAIL || process.env.GMAIL_USER,
      summaryData
    );

    if (!sent) {
      console.error('❌ Failed to send summary email');
      process.exit(1);
    }

    // Mark emails as read
    console.log('📍 Marking emails as read...');
    for (const email of unreadEmails) {
      await gmailClient.markAsRead(email.id);
    }

    console.log('✅ All tasks completed successfully!');
    console.log('✅ Email Analyzer Agent finished');
    process.exit(0);

  } catch (error) {
    console.error('❌ Error in Email Analyzer Agent:', error);
    process.exit(1);
  }
}

// Run the analyzer
runEmailAnalyzer();

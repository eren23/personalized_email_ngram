# Email-Based Text Prediction

A machine learning model that learns from your email writing style to provide text suggestions.

## Features

- Connects to Gmail to learn from your sent emails
- Uses N-gram language modeling for text prediction
- Provides real-time text suggestions
- Secure email authentication using environment variables

## Setup

1. Clone the repository:
    git clone https://github.com/eren23/personal_mail_ngram.git
    cd personal_mail_ngram

2. Install dependencies:
    pip install -r requirements.txt

3. Create a `.env` file with your Gmail credentials:
    EMAIL_ADDRESS=your.email@gmail.com
    EMAIL_PASSWORD=your_app_password

**Important Gmail Setup:**
- You'll need to enable IMAP in your Gmail settings
- If you use 2-Factor Authentication (recommended):
  1. Go to Google Account Settings > Security
  2. Under "Signing in to Google," select "App passwords"
  3. Generate a new app password and use it in your `.env` file
- If not using 2FA, you'll need to enable "Less secure app access"

## Usage

### Training the Model

Run the training script to download your emails and train the model:

    python main.py

The script will:
1. Download your recent sent emails
2. Clean and process the text
3. Train the N-gram model
4. Save the model to `email_ngram_model.pkl`

### Getting Text Predictions

Use the inference script to get text suggestions:

    python inference.py

Commands while using the inference script:
- Type some words to get suggestions
- Enter 'q' to quit
- Enter 'num X' to change number of suggestions (e.g., 'num 10')
- Enter 'debug' to see cleaned input

## Project Structure

- `main.py`: Training script
- `inference.py`: Text prediction interface
- `ngram_model.py`: N-gram model implementation
- `email_downloader.py`: Gmail connection and email downloading
- `email_cleaner.py`: Text preprocessing utilities

## Security Considerations

- Never commit your `.env` file (it's in .gitignore)
- Use App Passwords instead of your main Gmail password
- The model is stored locally and your emails never leave your machine
- All email processing is done locally on your computer

## Troubleshooting

1. Gmail Connection Issues:
   - Ensure IMAP is enabled in Gmail settings
   - Check that your App Password is correct
   - Verify your internet connection

2. Model Training Issues:
   - Ensure you have sufficient disk space
   - Check that your Gmail account has sent emails
   - Verify all dependencies are installed correctly

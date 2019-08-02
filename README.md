# FullSend

FullSend is an automated email service that helps the Purdue Electric Racing team manage mass communication in and around our organization. This was built using Microsoft Graph integration with our Purdue emails, and is *only accessible to students who are verified to be on the Purdue Electric Racing team*.


## Prerequisites

- Python version 3.5.2 or later.

## Development environment

- Create a new virtualenv: `python3 -m venv venv`
- Activate: `source venv/bin/activate`
- Install prerequisistes `pip install -r requirements.txt`

## Register the app

Head over to https://apps.dev.microsoft.com to quickly get a application ID and password. Click the **Sign in** link and sign in with either your Microsoft account (Outlook.com), or your work or school account (Office 365).

Once you're signed in, click the **Add an app** button. Enter `FullSend` for the name and click **Create application**. After the app is created, locate the **Application Secrets** section, and click the **Generate New Password** button. Copy the password now and save it to a safe place. Once you've copied the password, click **Ok**.

Locate the **Platforms** section, and click **Add Platform**. Choose **Web**, then enter `http://localhost:8000/mail/gettoken/` under **Redirect URIs**.

> **NOTE:** The values in **Redirect URIs** are case-sensitive, so be sure to match the case!

Click **Save** to complete the registration. Copy the **Application Id** and save it along with the password you copied earlier. We'll need those values soon.

## Configure the sample

1. Open the `.\FullSend\authhelper.py` file.
1. Replace `YOUR APP ID HERE` with the **Application Id** from the registration you just created.
1. Replace `YOUR APP PASSWORD HERE` with the password you copied earlier.
1. Run migrations by entering `python3 manage.py migrate` from the command prompt.
1. Run the project by entering `python3 manage.py runserver` from the command prompt.

## Services used
* [Sentry.io](https://sentry.io/welcome/) - Used to monitor all errors
* [UptimeRobot](https://uptimerobot.com/) - Used to keep heroku dyno active and monitor server uptime.

## Acknowledgements
This project was started using the [Outlook REST APIs Python Tutorial](https://docs.microsoft.com/en-us/outlook/rest/python-tutorial).

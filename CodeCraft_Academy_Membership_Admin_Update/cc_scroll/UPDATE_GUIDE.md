# Updating FelixForge Academy without losing accounts or progress

## Before replacing files

1. Stop the Flask server.
2. Make a backup of your current database. For the default local setup, copy `codecraft.db` to a safe folder outside the project.
3. Extract the new ZIP over the existing project folder. Do not delete the database file. If you extract into a brand-new folder, copy the old `codecraft.db` into that folder beside `app.py` before starting the app.
4. Keep the same `SECRET_KEY` in `.env`. Do not generate a new one for every update.
5. Keep using the same database. On a hosted multi-user website, use a managed PostgreSQL database and keep its `DATABASE_URL` unchanged between releases.
6. Install any newly listed dependencies with `pip install -r requirements.txt`, then start the app with `python app.py`.

The app uses a 30-day remember-me cookie. A code-only update should not normally sign users out when the secret key and browser cookie remain valid. Users may still need to sign in again if cookies are cleared or expire, the secret key changes, or the account is changed.

## Configure the administrator account

For a local installation, open the project folder and copy `.env.example` to a new file named `.env` (keep the leading dot). Open `.env` in a text editor and set these values. Do not put them in `app.py`, a public HTML file, or GitHub. For Railway or another host, add the same three names in the service/project **Variables / Environment Variables** settings instead:

```dotenv
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=use-a-unique-password-of-at-least-16-characters
```

The app provisions the administrator account from these settings when it starts. It stores a password hash, not the plain password. The configured admin password is authoritative: changing the environment variable rotates the administrator login password at the next app startup. Never commit `.env` or publish the admin password. After starting the app, sign in at `/login` using the configured admin email and password, then open `/admin`.

Sign in with the configured email and password, then open `/admin`.

## What is preserved

- User accounts and password hashes
- Lesson completion records
- Lesson bookmarks and personal notes
- Saved coding projects and portfolios
- Quiz attempts and scores
- Community posts and notifications

The lesson update routine keeps existing lesson IDs and appends new lessons. Do not delete or replace the live database when updating the application.


## Final exam and certificate payments
- Course final exams now contain 50 multiple-choice questions and use a 45-minute timer. Existing question and result rows are preserved; the startup seeder adds missing question-bank entries.
- Learners must complete every lesson and score at least 80% before certificate checkout becomes available.
- Set `PAYSTACK_SECRET_KEY` and `CERTIFICATE_FEE_NAIRA` in the private `.env` file or Railway service Variables. The default fee is ₦2,000 per course certificate and can be changed before launch.
- Payment is initialized on the server and verified directly with Paystack before certificate display is enabled. Card details are handled by Paystack's hosted checkout and are not stored by FelixForge Academy.
- Add the Paystack webhook URL if you later enable webhook-based reconciliation; the current learner flow verifies the transaction on the return callback.
- The certificate is a FelixForge Academy completion certificate, not an accredited academic or professional qualification. Review local consumer/payment rules and provider eligibility with a parent/guardian before accepting real payments.
- Add `urllib`/Paystack connectivity is built into Python; no extra payment SDK is required.

# Reusable FastAPI Authentication Starter Kit

A production-quality, modular, and highly extensible Authentication Module built for FastAPI. It serves as a secure starter kit for future FastAPI projects, microservices, and hackathons.

## 🚀 Key Features

- **Layered Architecture**: Strict separation of concerns (Routers, Services, Repositories, Helpers).
- **SQLAlchemy 2.x ORM**: Type-safe declarative model mappings, connection pooling, and auto table creation.
- **Secure Password Hashing**: Clean bcrypt hashing without outdated wrappers like passlib.
- **OTP Verification Flow**: Secure 6-digit cryptographically random OTP generation, SHA-256 hashing, timing-attack-safe comparison (`compare_digest`), purpose checking, and expiration sweeps.
- **HS256 JWT Authentication**: Access token creation containing only `user_id`, `username`, `role`, and expiration claims.
- **Extensible Roles**: Dynamic role-based schema (default: `USER`, supporting `ADMIN`, `MODERATOR`, etc.).
- **Separated HTML Templates**: Decoupled, beautifully designed email templates loaded and rendered via Jinja2.
- **Notification Abstraction**: Modular design utilizing the Dependency Inversion Principle. Easily swap SMTP for SendGrid, Twilio, or other channels.
- **Global Exception Mapping**: Sanitized exception handlers preventing database leakage (tracebacks, queries) to API clients.
- **Audit Logging**: Structured auditing for all authentication events (never logging passwords or plain OTPs).
- **Sleek Test UI**: Modern, responsive dark-themed testing dashboard utilizing glassmorphism and toast alerts.

---

## 📂 Folder Structure

```
app/
    config/
        settings.py         # Config loader utilizing pydantic-settings
    database/
        database.py         # SQLAlchemy engine, base model, session manager
    common/
        interfaces.py       # Notification abstractions (BaseNotificationService)
    auth/
        constants.py        # Extensible roles and OTP purpose enums
        models.py           # Database models (User and OTPVerification tables)
        schemas.py          # Request and response Pydantic models
        exceptions.py       # Reusable, granular API exceptions
        validators.py       # Password complexity validator rules
        password_service.py # Hashing & verification using native bcrypt
        jwt_service.py      # Token generation and validation (HS256)
        otp_service.py      # Random number generation & secure matching (SHA-256)
        email_service.py    # SMTP email rendering & sending (implementing BaseNotificationService)
        repository.py       # Database CRUD queries (SQLAlchemy 2.x standard)
        service.py          # Unified business processes orchestration
        router.py           # Pure HTTP routers and dependency injection
        responses.py        # Standardized API response format helpers
    main.py                 # FastAPI setup, middleware configuration, global handlers

templates/                  # HTML email templates
    registration.html
    login.html
    forgot_password.html

static/                     # Test frontend client dashboard
    index.html
```

---

## ⚙️ Environment Configurations (`.env`)

Configure parameters using a `.env` file at the root:

| Key | Description | Default |
|---|---|---|
| `PROJECT_NAME` | Project name displayed in emails & frontend | `"FastAPI Auth Starter"` |
| `DATABASE_URL` | Local PostgreSQL connection string | `"postgresql://postgres:postgres@localhost:5432/test"` |
| `JWT_SECRET` | Secret key used to sign HS256 tokens | *(Auto-configured)* |
| `SMTP_HOST` | Outgoing SMTP mail server | `"smtp.gmail.com"` |
| `SMTP_PORT` | Port for TLS encryption | `587` |
| `SMTP_EMAIL` | Account email sending the notifications | `"your-email@gmail.com"` |
| `SMTP_PASSWORD` | App Password generated in Gmail security | `"your-gmail-app-password"` |
| `OTP_EXPIRY` | Time before an OTP code expires (seconds) | `300` (5 minutes) |
| `RESEND_DELAY` | Rate limit delay between OTP resends (seconds)| `45` |
| `ENABLE_LOGIN_OTP` | Toggle requiring OTP check during login | `false` |

---

## 🏁 Quick Setup

### 1. Database Creation
Ensure you have a PostgreSQL database named `test` running locally. You can create it via your PostgreSQL shell or GUI (e.g. pgAdmin, DBeaver):
```sql
CREATE DATABASE test;
```

### 2. Dependency Installation
Create a virtual environment and install the required modules:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Running the Server
Start the development server:
```bash
uvicorn app.main:app --reload
```
Once started, the backend will automatically generate the `users` and `otp_verifications` tables.

### 4. Developer Testing Mode
If the Gmail SMTP parameters are not configured, the email service will output a **Developer Mock Email** statement directly to the terminal stdout containing the generated OTP. This allows you to copy the code and test the validation endpoints without setting up an email account.

---

## 🔒 Security Auditing Logs

The system records standard-compliant logs:
- `[AUDIT] Registration Success: username=...`
- `[AUDIT] Login Success: username=...`
- `[AUDIT] OTP Generated: user_id=..., purpose=...`
- `[AUDIT] OTP Verified: user_id=..., purpose=...`
- `[AUDIT] Password Reset Success: user_id=...`
- `[ERROR] Unexpected System Exception: error=...`

Plaintext OTPs, verification hashes, and passwords are fully masked from the logging streams.

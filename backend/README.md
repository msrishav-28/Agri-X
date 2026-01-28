# AgriX Node.js Backend

Authentication, file uploads, and user management API.

**Port:** `5001`

---

## Tech Stack

- **Runtime:** Node.js 18+
- **Framework:** Express 5
- **Database:** MongoDB (Mongoose)
- **Auth:** JWT + bcrypt
- **File Upload:** Cloudinary
- **SMS:** Twilio

---

## API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/signup` | POST | Register new user |
| `/api/auth/login` | POST | Login with email/password |
| `/api/auth/login-phone` | POST | Login with phone/password |
| `/api/auth/me` | GET | Get current user (JWT) |

### User Profile
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/user/profile` | PUT | Update user profile |
| `/api/user/picture` | PUT | Update profile picture |

### OTP
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/otp/send` | POST | Send OTP via SMS |
| `/api/otp/verify` | POST | Verify OTP |

---

## Environment Variables

Create `.env` file (see `.env.example`):

```bash
# Database
MONGO_URI=mongodb+srv://...

# Server
PORT=5001
NODE_ENV=development

# Auth
JWT_SECRET=your_secret_key

# Cloudinary (Image uploads)
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# Twilio (SMS/WhatsApp)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_SMS_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

---

## Quick Start

```bash
# Install dependencies
npm install

# Development
npm run dev

# Production
npm start
```

---

## Project Structure

```
backend/
├── src/
│   ├── index.js        # Entry point
│   ├── config/         # DB & env config
│   ├── controllers/    # Route handlers
│   ├── middleware/     # Auth, uploads
│   ├── models/         # Mongoose schemas
│   ├── routes/         # API routes
│   └── utils/          # Helpers
├── package.json
└── .env.example
```

---

## Connecting from Mobile App

In `MobileApp/backendConfig.js`:
```javascript
export const BACKEND_URL = `http://YOUR_IP:5001`;
```

Replace `YOUR_IP` with your computer's local IP (run `ipconfig` on Windows).

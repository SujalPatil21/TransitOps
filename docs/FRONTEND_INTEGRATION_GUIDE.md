# Frontend Integration Guide

This document provides a comprehensive integration guide for the frontend team to interact with the backend APIs. It covers authentication, RBAC, the Fleet module, and general API conventions. **All endpoints documented here are verified against the current backend implementation.**

---

## SECTION 1: Project Overview

The backend is built with FastAPI and follows a RESTful architecture. 

### Architecture & Flows
- **Authentication:** Uses JSON Web Tokens (JWT). The user exchanges credentials for a JWT, which must be attached as a Bearer token in the `Authorization` header of subsequent requests.
- **Role-Based Access Control (RBAC):** The system has four primary roles, each associated with specific business modules. Endpoints are strictly protected based on the user's role.
- **Dashboards:** Users should be redirected to their respective module dashboards upon successful login based on their role.

### Roles and Dashboards
| Role | Associated Dashboard Route (Frontend) |
|---|---|
| Fleet Manager | `/fleet/dashboard` |
| Dispatcher | `/dispatcher/dashboard` |
| Safety Officer | `/safety/dashboard` |
| Financial Analyst | `/finance/dashboard` |

---

## SECTION 2: Authentication

All authentication endpoints are prefixed with `/auth`. 

### `POST /auth/login`
Authenticates a user and returns a JWT access token.

- **URL:** `/auth/login`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "email": "manager@example.com",
  "password": "Password123!"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "requires_otp": false,
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "role": "Fleet Manager",
    "username": "fleet_manager"
  }
}
```

### `POST /auth/register`
Registers a new user and dispatches a verification code to their email.

- **URL:** `/auth/register`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "username": "new_user",
  "email": "new_user@example.com",
  "password": "Password123!",
  "role": "Fleet Manager"
}
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully. Please check your email for the OTP.",
  "data": {
    "user": {
      "id": 5,
      "email": "new_user@example.com",
      "username": "new_user",
      "role": "Fleet Manager",
      "is_active": true,
      "is_verified": false
    }
  }
}
```

### `POST /auth/verify-otp`
Verifies a 6-digit OTP code corresponding to user activation (REGISTRATION), sign-in challenge (LOGIN), or recovery (FORGOT_PASSWORD).

- **URL:** `/auth/verify-otp`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "email": "new_user@example.com",
  "purpose": "REGISTRATION",
  "otp": "123456"
}
```
*(Valid purposes: `REGISTRATION`, `LOGIN`, `FORGOT_PASSWORD`)*

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Email successfully verified. You can now login.",
  "data": null
}
```

### `POST /auth/resend-otp`
Resends verification codes for Registration, Login, or Password Recovery. Rate-limited to one request every 45 seconds.

- **URL:** `/auth/resend-otp`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "email": "new_user@example.com",
  "purpose": "REGISTRATION"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "A new OTP has been sent to your email.",
  "data": null
}
```

### `POST /auth/forgot-password`
Triggers the recovery process, emailing a password reset authorization code.

- **URL:** `/auth/forgot-password`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "email": "manager@example.com"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "If an account with that email exists, a password reset OTP has been sent.",
  "data": null
}
```

### `POST /auth/reset-password`
Overwrites the account password after confirming a valid reset verification OTP.

- **URL:** `/auth/reset-password`
- **Method:** `POST`
- **Authentication:** None

**Request JSON:**
```json
{
  "email": "manager@example.com",
  "otp": "123456",
  "new_password": "NewPassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Password updated successfully. You can now login with your new password.",
  "data": null
}
```

### `GET /auth/me`
Validates the token authorization and returns current user details.

- **URL:** `/auth/me`
- **Method:** `GET`
- **Authentication:** Required (Bearer Token)

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "User profile retrieved successfully.",
  "data": {
    "user": {
      "id": 1,
      "email": "manager@example.com",
      "username": "fleet_manager",
      "role": "Fleet Manager",
      "is_active": true,
      "is_verified": true
    }
  }
}
```

---

## SECTION 3: RBAC

### How Roles are Returned
Upon successful login (`POST /auth/login`), the `role` field is provided in the `data` object of the response payload. It is also included in the token payload and can be retrieved using `/auth/me`.

### How Frontend Should Store Role
Store the user's role securely in application state (e.g., Redux, Context, Zustand) or local storage alongside the JWT access token. 

### How Frontend Should Redirect Users
Upon successful authentication, inspect the `role` field and route the user to their designated dashboard:
- `Fleet Manager` → `/fleet/dashboard`
- `Dispatcher` → `/dispatcher/dashboard`
- `Safety Officer` → `/safety/dashboard`
- `Financial Analyst` → `/finance/dashboard`

*(Note: The frontend role selection mock-up used during testing is temporary and must not exist in production. Trust the role returned by the backend login API.)*

### Seeded Demo Accounts (Development Only)
Use these accounts to test RBAC and access respective modules:
- **Fleet Manager:** `manager@example.com` (Password: `Password123!`)
- **Dispatcher:** `dispatcher@example.com` (Password: `Password123!`)
- **Safety Officer:** `safety@example.com` (Password: `Password123!`)
- **Financial Analyst:** `financial@example.com` (Password: `Password123!`)

---

## SECTION 4: Fleet APIs

All Fleet endpoints require the `Fleet Manager` role. Other roles will receive a `403 Forbidden` response.
All endpoints are prefixed with `/fleet`.

### `GET /fleet/vehicles`
Lists all vehicles in the registry.

- **Method:** `GET`
- **URL:** `/fleet/vehicles`
- **Headers:** `Authorization: Bearer <token>`
- **Required Role:** Fleet Manager

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Vehicles retrieved successfully.",
  "data": {
    "vehicles": [
      {
        "id": 1,
        "registration_number": "MH01AB1234",
        "vehicle_type": "Truck",
        "manufacturer": "Tata",
        "model": "Prima",
        "manufacturing_year": 2022,
        "capacity_kg": 15000.0,
        "odometer": 12050.5,
        "status": "AVAILABLE",
        "created_at": "2024-03-15T10:30:00Z",
        "updated_at": "2024-03-15T10:30:00Z"
      }
    ]
  }
}
```

### `POST /fleet/vehicles`
Registers a new vehicle in the system.

- **Method:** `POST`
- **URL:** `/fleet/vehicles`
- **Headers:** `Authorization: Bearer <token>`
- **Required Role:** Fleet Manager

**Request JSON:**
```json
{
  "registration_number": "MH01AB1234",
  "vehicle_type": "Truck",
  "manufacturer": "Tata",
  "model": "Prima",
  "manufacturing_year": 2024,
  "capacity_kg": 15000,
  "odometer": 0
}
```
*(Note: Do not include `status` in the request body. It defaults to `AVAILABLE`.)*

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Vehicle created successfully.",
  "data": {
    "vehicle": {
      "id": 5,
      "registration_number": "MH01AB1234",
      "vehicle_type": "Truck",
      "manufacturer": "Tata",
      "model": "Prima",
      "manufacturing_year": 2024,
      "capacity_kg": 15000.0,
      "odometer": 0.0,
      "status": "AVAILABLE",
      "created_at": "2026-07-12T13:49:44.200927",
      "updated_at": "2026-07-12T13:49:44.200927"
    }
  }
}
```

### `GET /fleet/vehicles/{id}`
Retrieves details of a specific vehicle.

- **Method:** `GET`
- **URL:** `/fleet/vehicles/{id}`
- **Headers:** `Authorization: Bearer <token>`
- **Required Role:** Fleet Manager

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Vehicle retrieved successfully.",
  "data": {
    "vehicle": {
      "id": 1,
      "registration_number": "MH01AB1234",
      "vehicle_type": "Truck",
      "manufacturer": "Tata",
      "model": "Prima",
      "manufacturing_year": 2022,
      "capacity_kg": 15000.0,
      "odometer": 12050.5,
      "status": "AVAILABLE",
      "created_at": "2024-03-15T10:30:00Z",
      "updated_at": "2024-03-15T10:30:00Z"
    }
  }
}
```

### `PATCH /fleet/vehicles/{id}`
Partially updates an existing vehicle. Only explicitly provided fields are modified.

- **Method:** `PATCH`
- **URL:** `/fleet/vehicles/{id}`
- **Headers:** `Authorization: Bearer <token>`
- **Required Role:** Fleet Manager

**Request JSON (Partial):**
```json
{
  "manufacturer": "Volvo",
  "odometer": 1500.5
}
```
*(Note: Do not include `status` in the request body. Changes to `status` are rejected here.)*

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Vehicle updated successfully.",
  "data": {
    "vehicle": {
      "id": 1,
      "registration_number": "MH01AB1234",
      "vehicle_type": "Truck",
      "manufacturer": "Volvo",
      "model": "Prima",
      "manufacturing_year": 2022,
      "capacity_kg": 15000.0,
      "odometer": 1500.5,
      "status": "AVAILABLE",
      "created_at": "2024-03-15T10:30:00Z",
      "updated_at": "2026-07-12T13:49:44.852717"
    }
  }
}
```

### `PATCH /fleet/vehicles/{id}/retire`
Permanently retires a vehicle. This action is irreversible.

- **Method:** `PATCH`
- **URL:** `/fleet/vehicles/{id}/retire`
- **Headers:** `Authorization: Bearer <token>`
- **Required Role:** Fleet Manager

**Request JSON:**
None required.

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Vehicle retired successfully.",
  "data": {
    "vehicle": {
      "id": 1,
      "registration_number": "MH01AB1234",
      "vehicle_type": "Truck",
      "manufacturer": "Volvo",
      "model": "Prima",
      "manufacturing_year": 2022,
      "capacity_kg": 15000.0,
      "odometer": 1500.5,
      "status": "RETIRED",
      "created_at": "2024-03-15T10:30:00Z",
      "updated_at": "2026-07-12T13:49:45.093412"
    }
  }
}
```

---

## SECTION 5: Validation Rules

The backend strictly enforces the following rules. The frontend should display these errors appropriately when the backend returns them (HTTP 422, 409, or 400).

- **Registration Number Uniqueness:** Registration numbers are normalized (whitespace removed, converted to uppercase) before validation. `MH01AB1234` and `mh01ab1234` are treated as identical. Duplicates will trigger an HTTP 409 Conflict.
- **Missing Required Fields (POST):** During creation, `registration_number`, `vehicle_type`, `manufacturer`, `model`, `manufacturing_year`, `capacity_kg`, and `odometer` are mandatory.
- **Capacity:** Must be greater than `0`. Cannot be `0` or negative.
- **Odometer:** Must be greater than or equal to `0`. Cannot be negative.
- **Status Restrictions:** The `status` field is controlled exclusively by business workflows (like the `/retire` endpoint). Including `status` in a `POST` or `PATCH` payload will trigger a validation error.
- **Retirement Rules:** Retiring a vehicle changes its status to `RETIRED`. This is irreversible. Attempting to update or re-retire a `RETIRED` vehicle will trigger an HTTP 400 error.

---

## SECTION 6: Error Handling

The standard error response format is identical for all endpoints:
```json
{
  "success": false,
  "message": "Human-readable error description.",
  "errorCode": "ERROR_CODE_STRING"
}
```

### Common Error Responses

**Validation Error (422 Unprocessable Content):**
```json
{
  "success": false,
  "message": "capacity_kg must be greater than 0.",
  "errorCode": "VALIDATION_ERROR"
}
```

**Conflict / Duplicate (409 Conflict):**
```json
{
  "success": false,
  "message": "Vehicle with registration number MH01AB1234 already exists.",
  "errorCode": "DUPLICATE_REGISTRATION"
}
```

**Not Found (404 Not Found):**
```json
{
  "success": false,
  "message": "Vehicle not found.",
  "errorCode": "VEHICLE_NOT_FOUND"
}
```

**Unauthorized (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid authentication credentials.",
  "errorCode": "UNAUTHORIZED"
}
```

**Forbidden (403 Forbidden):**
```json
{
  "success": false,
  "message": "Insufficient permissions to access this resource.",
  "errorCode": "FORBIDDEN"
}
```

**Business Rule Violation (400 Bad Request):**
```json
{
  "success": false,
  "message": "Vehicle is already retired.",
  "errorCode": "VEHICLE_RETIREMENT_FAILED"
}
```

---

## SECTION 7: Frontend Responsibilities

To integrate smoothly, the frontend **MUST**:

- **Store the JWT securely:** Manage the `access_token` returned from `/auth/login` and attach it to all subsequent API requests in the `Authorization: Bearer <token>` header.
- **Handle token expiration:** Redirect the user to the login screen if the backend returns a `401 Unauthorized` response.
- **Redirect by Role:** Route the user to the correct dashboard path after logging in based on the `role` property in the login response.
- **Handle 403 Forbidden:** Display an appropriate "Access Denied" screen if the user attempts to access a module they do not have permissions for (e.g. Dispatcher trying to fetch Fleet data).
- **Display validation errors:** Extract the `message` from the error JSON and display it near the relevant form fields.
- **Prevent duplicate submissions:** Disable submit buttons during pending requests to prevent double-firing `/fleet/vehicles`.
- **Handle loading states:** Show skeleton loaders or spinners while fetching lists or individual vehicle details.

---

## SECTION 8: Backend Responsibilities

The frontend should **NOT** implement the following logic, as the backend already enforces it robustly:

- **RBAC Enforcement:** You do not need to hide APIs on the client-side for security; the backend will reject any request with `403 Forbidden` if the user's role does not permit access.
- **Duplicate Registration Checks:** You do not need to query the list of vehicles to check for uniqueness before creating a vehicle. The backend performs uppercase/whitespace normalization and enforces a unique constraint, returning `409 Conflict` if violated.
- **Vehicle Status Protection:** You do not need to manually set `status: "AVAILABLE"` when creating a vehicle. The backend does this automatically.
- **Business Rules:** The backend enforces all rules regarding vehicle retirement (e.g., rejecting updates on retired vehicles, rejecting double-retirement).
- **Password Hashing:** Passwords are sent in plaintext over HTTPS and hashed by the backend. Do not hash passwords on the client.
- **JWT Validation:** The backend automatically validates signatures and expiration times.

---

## SECTION 9: Current Development Status

| Feature / Module | Status | Notes |
|---|---|---|
| **Authentication Flow** | ✅ Completed | Login, Register, OTP, Password Reset, JWT fully implemented. |
| **RBAC** | ✅ Completed | Permissions matrix and JWT role claims are fully active. |
| **Fleet Module** | ✅ Completed | Full CRUD and business logic strictly tested and ready for integration. |
| **Dispatcher Module** | 🚧 In Progress | Endpoints are stubbed/pending backend implementation. |
| **Safety Module** | 🚧 In Progress | Endpoints are stubbed/pending backend implementation. |
| **Finance Module** | 🚧 In Progress | Endpoints are stubbed/pending backend implementation. |
| **Analytics & Dashboards** | 📅 Planned | Data aggregation endpoints pending. |

---

## SECTION 10: Frontend Checklist

- [ ] **Login Screen:** Implement login form, capture JWT and role from response.
- [ ] **Role-based Navigation:** Redirect users to `/fleet/dashboard`, `/dispatcher/dashboard`, etc., based on their role.
- [ ] **JWT Storage:** Securely store the token and append `Authorization: Bearer <token>` to all protected API calls.
- [ ] **Logout:** Clear the JWT and redirect to `/login`.
- [ ] **Forgot Password Flow:** Implement UI for `/forgot-password`, `/verify-otp`, and `/reset-password`.
- [ ] **Fleet Dashboard (List):** Fetch and render `GET /fleet/vehicles` for the Fleet Manager.
- [ ] **Create Vehicle Form:** Post to `/fleet/vehicles`, displaying `422` and `409` error messages from the backend gracefully.
- [ ] **Edit Vehicle Form:** Use `PATCH /fleet/vehicles/{id}` for partial updates. Do not send unchanged fields unless necessary.
- [ ] **Vehicle Retirement:** Implement a confirmation modal before calling `PATCH /fleet/vehicles/{id}/retire`, as this is irreversible.
- [ ] **Loading States:** Implement visual feedback during all asynchronous operations.
- [ ] **Error Handling:** Implement a global Axios/Fetch interceptor to handle `401` (logout) and `403` (unauthorized access screen).

---

## SECTION 11: Known Limitations

- **Testing Users:** The 4 demo accounts are seeded into the database dynamically on startup for testing purposes. These are temporary and will be removed in the production environment.
- **Future Modules:** Modules outside of `Auth` and `Fleet` (Dispatcher, Safety, Finance) are structurally created but their domain logic and database tables are not yet finalized. Do not attempt to integrate with them until further notice.

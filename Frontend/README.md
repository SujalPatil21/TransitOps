# TransitOps - Smart Transport Operations Platform

TransitOps is an enterprise SaaS platform built to digitize vehicle registries, driver management, dispatch logs, maintenance operations, and fuel logs for fleet companies. This repository contains the frontend codebase.

---

## 🛠️ Technology Stack

- **Framework**: React (Vite)
- **Language**: JavaScript (JSX)
- **Styling**: Tailwind CSS v4 (native CSS variables) + Custom `shadcn/ui` style primitives
- **Routing**: React Router DOM (v6)
- **APIs**: Axios (pre-configured instance)
- **Icons**: Lucide React

---

## 📁 Project Structure

```
d:/Odoo Frontend/
├── package.json
├── vite.config.js
├── index.html
├── README.md
├── src/
│   ├── main.jsx                      # Entry point
│   ├── App.jsx                       # Main Router switch
│   ├── lib/
│   │   └── utils.js                  # Tailwind class merge helper (cn)
│   ├── styles/
│   │   ├── theme.css                 # CSS variables for colors, spacing, borders
│   │   └── globals.css               # Resets, scrollbars, body styles
│   ├── layouts/
│   │   ├── PublicLayout.jsx          # Public branding pages layout wrapper
│   │   └── DashboardLayout.jsx       # Protected pages grid layout wrapper
│   ├── config/
│   │   ├── roles.js                  # Central roles constants
│   │   ├── routes.js                 # Central route paths and element imports
│   │   ├── navigation.js             # Sidebar structural menu definitions
│   │   └── accessControl.js          # Centralized route permissions & visibility logic
│   ├── constants/
│   │   ├── vehicleStatus.js          # Available, On Trip, In Shop, Retired
│   │   ├── driverStatus.js           # Available, On Trip, Off Duty, Suspended
│   │   ├── tripStatus.js             # Draft, Dispatched, Completed, Cancelled
│   │   ├── maintenanceStatus.js      # Active, Closed
│   │   └── fuelTypes.js              # Fuel, Toll, Maintenance, Other
│   ├── context/
│   │   └── AuthContext.jsx           # Maintains user session state
│   ├── hooks/
│   │   └── useAuth.js                # Custom session hook
│   ├── services/                     # Async API Promise layers
│   │   ├── api/
│   │   │   └── axios.js              # Central configured Axios instance
│   │   ├── authService.js
│   │   ├── vehicleService.js
│   │   └── ...
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.jsx           # Presentation-only sidebar component
│   │   │   └── Topbar.jsx            # Breadcrumbs and profile header
│   │   ├── shared/
│   │   │   ├── ProtectedRoute.jsx    # Auth boundary checking
│   │   │   ├── PublicRoute.jsx       # Public-only route redirect
│   │   │   ├── DataTable.jsx         # Skeletons for tabular lists
│   │   │   ├── StatCard.jsx          # KPI data widget
│   │   │   └── ...
│   │   └── ui/
│   │       ├── Button.jsx            # Custom primary, secondary buttons
│   │       ├── Card.jsx              # Card border wrappers
│   │       └── ...
│   └── pages/
│       ├── landing/                  # LandingPage
│       ├── login/                    # LoginPage (includes role selection selector)
│       ├── fleet-manager/            # Dash: Fleet, Vehicle Status, Maint Alerts
│       ├── dispatcher/               # Dash: Active Trips, Scheduled, Delivery Status
│       ├── safety-officer/           # Dash: Compliance, Expiry trackers, Alerts
│       └── financial-analyst/        # Dash: Fuel, Costs, Analytics
```

---

## 🚀 How to Run

1. **Clone the repository** and navigate to the project directory:
   ```bash
   cd "D:/Odoo Frontend"
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Configure environment variables**:
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. **Start the local development server**:
   ```bash
   npm run dev
   ```

---

## 🔒 Centralized Access Control (RBAC)

The application supports Role-Based Access Control from the foundation:
- Roles are declared in `src/config/roles.js`.
- Route permissions and sidebar link visibilities are managed in `src/config/accessControl.js`.
- Dashboard pages are separated by role directories (e.g. `/dispatcher/dashboard`).
- All other resource modules (e.g. `/vehicles`, `/drivers`) remain configurable in `accessControl.js`, letting you adjust permissions instantly.

---

## 🔌 Backend Integration Blueprint

All data fetching is handled through files in `src/services/` which export async Promise methods. 

To swap mock data for live REST API calls:
1. Ensure the backend endpoint URL is set in `.env` (`VITE_API_URL`).
2. Inside `src/services/api/axios.js`, notice that requests automatically inject the `transitops_token` JWT header if stored in the session.
3. Edit the relevant service file (e.g. `vehicleService.js`):
   ```javascript
   import api from './api/axios';

   export const getVehicles = async () => {
     const response = await api.get('/vehicles');
     return response.data;
   };
   ```
4. Component files consume services asynchronously and do not need to be refactored when APIs go live.

# 🌌 RideSphere

> **RideSphere** is a premium, modern, and unified Multi-Vehicle Rental, Ride Booking, & Tourism Platform. By combining the features of Uber, Turo, Airbnb, and Booking.com into a single, high-performance ecosystem, RideSphere provides a seamless ride-sharing and travel booking experience for customers and partners.

---

## ✨ Core Platforms & Portals

RideSphere bridges the gap between passengers, fleet owners, drivers, and tour operators with a multi-role stakeholder architecture:

*   **🚗 Ride Booking & Sharing (Uber/Careem style):** On-demand ride matchmaking with real-time driver coordinates, dynamic fare calculation, and instant payment validation.
*   **🚲 Vehicle Renting (Turo style):** Cataloged self-drive rentals spanning cars, bikes, and luxury fleets with custom filters and owner approvals.
*   **🗺️ Tourism & Booking (Airbnb style):** Expertly-guided local tour listings, reservations, itinerary details, and operators approval channels.
*   **🛡️ Verification & Auth Guards:** Complete guest interception gate, role-based access control, super admin authentication, and automated audit trails.

---

## 🎨 Premium Design System

The application relies on a modern, high-contrast light mode layout optimized for professional and luxury aesthetics:
*   **Background Canvas:** Deep, clean slate background (`#F8FAFC`) with dark navy (`#0F172A`) typography and Royal Blue (`#2563EB`) interaction accents.
*   **Glassmorphic Accents:** Elegant backdrop blur cards, subtle borders (`border-slate-800/80`), and polished hover states.
*   **Fully Mobile Responsive:** The custom [Navbar](frontend/src/components/Navbar.tsx) collapses dense search and authentication controls behind an interactive mobile drawer with smooth slide-in transitions.

---

## 🔒 Authentication & Role-Based Access Control (RBAC)

RideSphere enforces a secure access model where guests can browse catalog listings but must register to perform bookings, rentals, or administrative reviews:

| Stakeholder Role | Access Level & Dashboard Capabilities |
| :--- | :--- |
| **Guest User** | Browse home, read vehicle & tour catalogs, check reviews. Cannot book, rent, pay, or access dashboards. |
| **Customer** | Complete ride requests, rent self-drive vehicles, book tours, manage wallets, and view active trips. |
| **Fleet Owner** | Register vehicles, audit rentals, manage fleet logs, and track dynamic earnings. |
| **Driver** | Complete license and police checks, view matching rides, toggle availability status, and track routes. |
| **Tour Operator** | Upload tourism licenses, manage itinerary bookings, and coordinate guide assignments. |
| **Admin** | Verification queue to approve or reject pending drivers, owners, and operators. |
| **Super Admin** | Core configurations, database settings, and hardware key biometric signature checks. |

---

## 🛠️ Technology Stack

### Backend
*   **Framework:** FastAPI (Python 3.11+)
*   **ORM:** SQLAlchemy with Asyncpg (supporting PostgreSQL in production)
*   **Database:** SQLite (local development)
*   **Security:** JWT Tokens, bcrypt hashing, and MFA/hardware key check simulation.

### Frontend
*   **Framework:** Next.js 16 (App Router, Turbopack)
*   **Styling:** Tailwind CSS v4, Lucide Icons
*   **State Sync:** LocalStorage and cross-tab window storage event synchronization.

---

## 🚀 Getting Started

### 1. Backend Setup

1.  Navigate to the backend folder:
    ```bash
    cd backend
    ```
2.  Set up a Python virtual environment and activate it:
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Seed the database with mock vehicles, tours, and accounts:
    ```bash
    python seed_data.py
    ```
5.  Start the development server:
    ```bash
    uvicorn app.main:app --reload
    ```

### 2. Frontend Setup

1.  Navigate to the frontend folder:
    ```bash
    cd frontend
    ```
2.  Install packages:
    ```bash
    npm install
    ```
3.  Start the Next.js development server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📈 Continuous Integration & Code Style

We enforce standard formatting and code quality checks through GitHub Actions:
*   **Workflow Path:** `.github/workflows/main.yml`
*   **Python Formatter:** `black`
*   **Python Imports Sorting:** `isort --profile black`
*   **Linter:** `flake8`
*   **Node Runner:** Runs on Node.js 24 (using `actions/checkout@v4` and `actions/setup-python@v5` to prevent Node.js 20 deprecation warnings).

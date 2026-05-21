# Health Connect V1.0 Implementation Plan

This document outlines the architectural plan, database schema, API integration logic, and code structure for **Health Connect**, a mobile healthcare app focused on appointment booking for semi-urban and rural India.

## User Review Required

> [!IMPORTANT]
> Please review the chosen tech stack and database schema. Once approved, I will begin generating the exact project files into a new workspace directory (`C:\Users\abdul\.gemini\antigravity\scratch\health_connect`). 

## Open Questions

> [!WARNING]
> 1. **Authentication:** Should we use Firebase Auth for OTP/Phone-based login (highly recommended for rural India), or build a custom JWT/OTP system?
> 2. **Map Rendering:** I recommend using `flutter_map` for rendering OpenStreetMap data in Flutter. Does this sound acceptable?

## Proposed Tech Stack

*   **Mobile Frontend:** **Flutter**. Provides cross-platform (Android/iOS) capabilities with a single codebase, excellent performance, and robust libraries for map integrations (`flutter_map`) and graceful degradation (offline-first UI handling).
*   **Backend:** **Node.js (TypeScript) with Express**. Handles high concurrency well and makes it easy to implement near real-time updates (using Socket.io or Server-Sent Events) for appointment confirmations.
*   **Database:** **PostgreSQL with PostGIS extension**. Crucial for the pan-India scalability requirement. PostGIS allows for highly optimized spatial queries (e.g., finding doctors within a specific radius of a user's location).
*   **ORM:** **Prisma**. Provides type-safe database access and easy schema management.
*   **Mapping & Geolocation:** **OpenStreetMap (OSM) via Overpass API** for fetching nearby healthcare facilities, and **Nominatim** for geocoding/search.

---

## Database Schema (PostgreSQL + Prisma)

Here is the proposed schema for handling Users, Doctors, and Appointments.

```prisma
// schema.prisma

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [postgis]
}

enum Role {
  PATIENT
  DOCTOR
}

enum AppointmentStatus {
  PENDING
  ACCEPTED
  REJECTED
  COMPLETED
  CANCELLED
}

model User {
  id           String   @id @default(uuid())
  phone        String   @unique
  name         String
  role         Role     @default(PATIENT)
  passwordHash String?  // Or handled via Firebase Auth
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt

  // Relations
  doctorProfile DoctorProfile?
  appointments  Appointment[]  @relation("PatientAppointments")
}

model DoctorProfile {
  id             String   @id @default(uuid())
  userId         String   @unique
  user           User     @relation(fields: [userId], references: [id])
  specialization String
  clinicName     String
  fees           Float
  latitude       Float
  longitude      Float
  // Note: In actual raw SQL, we will create a PostGIS GEOMETRY(Point, 4326) column for optimized queries.
  
  slots          AppointmentSlot[]
}

model AppointmentSlot {
  id              String   @id @default(uuid())
  doctorId        String
  doctor          DoctorProfile @relation(fields: [doctorId], references: [id])
  startTime       DateTime
  endTime         DateTime
  isBooked        Boolean  @default(false)
  
  appointment     Appointment?
}

model Appointment {
  id              String   @id @default(uuid())
  patientId       String
  patient         User     @relation("PatientAppointments", fields: [patientId], references: [id])
  slotId          String   @unique
  slot            AppointmentSlot @relation(fields: [slotId], references: [id])
  status          AppointmentStatus @default(PENDING)
  notes           String?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
}
```

---

## API Integration Logic: OpenStreetMap (Overpass API)

To fetch nearby hospitals, clinics, and pharmacies based on dynamic GPS coordinates, we will use the Overpass API. This logic will be implemented on the Node.js backend to prevent exposing Overpass queries directly on the client and to allow for caching responses (saving bandwidth for low-connection users).

```typescript
// backend/src/services/osmService.ts
import axios from 'axios';

const OVERPASS_API_URL = 'https://overpass-api.de/api/interpreter';

export const fetchNearbyHealthcareFacilities = async (lat: number, lon: number, radiusMeters: number = 5000) => {
  // Query to find nodes tagged as hospital, clinic, or pharmacy within the radius
  const query = `
    [out:json][timeout:25];
    (
      node["amenity"~"hospital|clinic|pharmacy"](around:${radiusMeters},${lat},${lon});
      way["amenity"~"hospital|clinic|pharmacy"](around:${radiusMeters},${lat},${lon});
      relation["amenity"~"hospital|clinic|pharmacy"](around:${radiusMeters},${lat},${lon});
    );
    out center;
  `;

  try {
    const response = await axios.post(OVERPASS_API_URL, query, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    // Map the OSM data to a simplified structure for the mobile app
    return response.data.elements.map((el: any) => ({
      id: el.id,
      name: el.tags?.name || 'Unnamed Facility',
      type: el.tags?.amenity || 'unknown',
      latitude: el.lat || el.center?.lat,
      longitude: el.lon || el.center?.lon,
    }));
  } catch (error) {
    console.error("Error fetching from Overpass API:", error);
    throw new Error("Failed to fetch nearby facilities");
  }
};
```

---

## Core Mobile UI & Backend Controllers (Planned Output)

Once this plan is approved, I will generate the following codebase structures:

### Backend (Node.js/Express)
*   **`controllers/appointmentController.ts`**: Logic for fetching available slots, creating an appointment, and doctors accepting/rejecting appointments.
*   **`controllers/searchController.ts`**: Logic for searching doctors by name/specialization and fetching OSM data.

### Mobile App (Flutter)
*   **`screens/patient/home_screen.dart`**: Contains the search bar and the `flutter_map` widget integrating the Overpass API data.
*   **`screens/patient/doctor_profile_screen.dart`**: Shows doctor details and a dynamic grid of available `AppointmentSlot`s.
*   **`screens/patient/booking_confirmation_screen.dart`**: Handles the offline-capable booking submission.
*   **`screens/doctor/dashboard_screen.dart`**: Inbox UI for doctors to see pending requests and schedule views.

## Verification Plan

### Automated Tests
*   Backend: Unit tests for the Overpass API integration service to ensure data is parsed correctly.
*   Backend: API tests for the appointment booking flow (preventing double-booking of slots).

### Manual Verification
*   We will run the Flutter app locally using `flutter run` or inspect the generated UI code to ensure it adheres to the "simple, intuitive" directive.
*   Verify that backend endpoints handle simulated network latency appropriately.

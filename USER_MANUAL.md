# Professor Academic Portal - User Manual

Welcome to your luxury academic portal. This document provides instructions on how to manage your site, ensure its security, and handle updates.

## Quick Start: Admin Credentials
The portal has been pre-seeded with **Dr. Syed Haider Ali's** profile.

- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 1. Accessing the Admin Portal

The administrative interface is where you manage all content, including Publications, Courses, and Research data.

- **URL**: `http://your-domain.com/admin/` (or `http://127.0.0.1:8000/admin/` locally)
- **Login**: Use your administrative credentials.
- **Security Note**: The portal is protected by **django-axes**, which prevents brute-force attacks. Multiple failed login attempts will temporarily lock the account for security.

## 2. Dynamic Content Management

### Adding a New Publication or Course
Follow these 3 steps to update your portfolio:
1. **Navigate**: In the Admin Sidebar, click on **Publications** or **Courses** under the "Portfolio" section.
2. **Create**: Click the **"Add"** button in the top right corner.
3. **Save**: Fill in the required fields (Title, Year, Description, etc.) and click **"Save"**. The site will update instantly.

### Editing Content
Simply click on any existing entry to modify its details. We use a **Glassmorphism UI** for the admin panel (Unfold) to ensure a premium editing experience.

## 3. The "Soft Delete" Safety Net (Recycle Bin)

To prevent accidental data loss, the portal uses a **Soft Delete** system.
- When you "delete" a Publication or Course, it is not immediately removed from the database.
- It is moved to the **Recycle Bin** (marked as deleted).
- To permanently delete or restore an item, go to the item's list view and use the status filters to find "Deleted" items.

## 4. Maintenance Mode

If you are performing a major overhaul of your research data:
1. Go to the Admin Dashboard.
2. Look for the **Maintenance Mode** section.
3. Toggle the state to **"On"**.
4. The public will see a luxury **"Under Construction"** splash page while you work. Admins can still see the site normally.

## 5. Security & Backups

### Automated Backups
The system is configured to create daily encrypted backups of your database.
- **Encryption**: Backups are encrypted using **AES-256 bit encryption at rest**.
- **Location**: Backups are stored in the `backups/` directory.
- **Command**: To manually trigger a backup, run:
  ```bash
  python manage.py backup_db
  ```

### Data Protection
Your sensitive research data and credentials are encrypted. The encryption key is stored securely in your environment variables. **Never share your `.env` file.**

---
*Created by Antigravity AI Coding Assistant*

# Ticket Booking API

## Overview

This is a simple ticket booking API that allows users to register, purchase event tickets, and manage events. The system includes role-based access control, ensuring that only authorized users can perform specific actions.

## Technologies Used

- Django (Backend Framework)
- Django REST Framework (API development)
- PostgreSQL (Database)
- JWT Authentication

## API Endpoints

### User Registration

- `POST /api/register/` - Register a user (Admin/User)
- `POST /api/login/` - Login a user (Admin/User)
- `POST /api/logout/` - Logout a user (Admin/User)

### Event Management

- `POST /api/events/` - Create a new event (Admin only)
- `PUT /api/events/{id}/` - Update a new event (Admin only)
- `GET /api/events/` - Fetch all events (Admin and User)
- `GET /api/events/{id}` - Retrieve a specific event (Admin and User)

### Ticket Purchase

- `POST /api/events/{id}/purchase/` - Purchase tickets for an event (User Only)

## Installation & Setup

1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <project_folder>
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the server:
   ```sh
   python manage.py runserver
   ```

## Authentication & Authorization

- Users need to register and authenticate using JWT token-based authentication.
- Admins can create and manage events.
- Users can only purchase tickets.

## License

This project is open-source.

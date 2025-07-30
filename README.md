# Appointment Scheduler with Calendar Sync & Reminders

Just a quick project I made while practicing Django and backend development.
This is part of my journey as I learn and improve my skills, one project at a time.

## About the Project

This Django-based web app allows users to schedule appointments with date, time, and details.
It includes authentication, form handling, validation, and a clean user interface using Bootstrap.

Each project I build helps me reinforce what I’ve learned and explore new tools and features.

## Features

- User registration and login
- Create, view, and manage appointments
- Prevent duplicate bookings (one user cannot book same time twice)
- Appointment status (Pending, Confirmed, Canceled)
- Admin dashboard with custom user model
- Google Calendar sync *(planned)*
- Email reminders *(planned)*

## Technologies Used

- Python
- Django
- HTML
- CSS
- Bootstrap
- JavaScript

## How to Use

1. **Clone the repository**
`git clone https://github.com/AsHkAn-Django/appointment-scheduler.git`

2. **Navigate into the project folder**
`cd appointment-scheduler`

3. **Create and activate a virtual environment**
```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Apply migrations & start the server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## About Me
Hi, I'm Ashkan — a junior Django developer transitioning from a background in teaching English as a second language.
I'm currently focused on improving my backend skills and building practical web applications.
****
# Shotokan United Backend

This is the backend for the Shotokan United website, built using Django and Django REST Framework (DRF). It provides essential functionalities such as user authentication, real-time notifications, task scheduling, and social authentication via third-party services. The backend supports secure communication with the frontend and integrates with Google Cloud for file storage and email services.

## Features

- **Cross-Origin Resource Sharing (CORS)**: CORS headers are configured for secure frontend-backend communication.
- **Social Authentication**: Allows login and registration via third-party services using `social-auth-app-django`.
- **Google Cloud Integration**: Manages storage, email services, and other functionalities through Google Cloud.
- **RESTful API**: Full REST API built using Django REST Framework (DRF) for managing resources like users, messages, and more.
- **Real-time Notifications**: Implements real-time WebSocket-based notifications using `django-channels`.
- **Task Scheduling**: Asynchronous task queuing implemented using Django Celery with Redis.
- **Secure Authentication**: JWT-based authentication using `djoser` for secure login, registration, and password management.
  
## Technologies Used

- **Django**: 4.2.7
- **Django REST Framework**: 3.15.1
- **Djoser**: 2.2.3
- **Django Channels**: 4.1.0
- **Django Celery with Redis**: for task queuing
- **PostgreSQL**: as the database
- **Google Cloud**: for file storage and email services
- **Redis**: for background task management
- **Daphne**: for WebSocket handling

## Installation

### Prerequisites

- **Python**: 3.8+
- **PostgreSQL**
- **Redis**
- **Google Cloud credentials** (for Google Cloud Storage or email integration)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/shotokan-united-backend.git
    cd shotokan-united-backend
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    # Install system depencences by running
    cat ~/project/install/requirements.system | xargs sudo aptitude install
    # OR
    cat ~/project/install/requirements.system | xargs sudo apt install
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and configure the following variables:
    ```bash
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/shotokan
    REDIS_URL=redis://localhost:6379/0
    GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
    GOOGLE_CLOUD_CREDENTIALS=path-to-your-google-cloud-credentials.json
    ```

5. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

8. **Run Celery worker**:
    ```bash
    celery -A shotokan_united worker --loglevel=info
    ```

9. **Run Daphne server for WebSockets**:
    ```bash
    daphne -b 0.0.0.0 -p 8001 shotokan_united.asgi:application
    ```

## Usage

- **API Documentation**: You can access the API documentation at `/api/docs/` after starting the server.
- **Admin Panel**: The Django admin panel is accessible at `/admin/` for managing users, notifications, and other resources.

## Task Queuing

This project uses Celery with Redis as the message broker for background task management. Celery is configured to handle tasks such as sending emails, processing notifications, and other long-running tasks.

To start Celery workers:

```bash
celery -A shotokan_united worker --loglevel=info
```


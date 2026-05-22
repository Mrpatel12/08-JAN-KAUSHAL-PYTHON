# Bookaro

A professional Django project for managing services and bookings.

## Project Structure

- `Accounts/`: User authentication and profile management.
- `Bookings/`: Core booking logic and management.
- `Dashboard/`: Admin and user dashboard views.
- `Services/`: Service catalog and details.
- `Bookaro/`: Project configuration (settings, URLs, WSGI/ASGI).
- `templates/`: Global HTML templates.
- `static/`: Global static assets (CSS, JS, Images).
- `media/`: User-uploaded content.

## Getting Started

1. **Clone the repository**
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## License

This project is licensed under the MIT License.

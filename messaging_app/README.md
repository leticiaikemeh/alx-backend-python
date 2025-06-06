`# 📩 Messaging App (Django + Django REST Framework)

This is a RESTful messaging application built with Django and Django REST Framework. It supports user registration, creating conversations, and sending messages between users.

---

## 🚀 Features

- Custom user model with email-based authentication
- One-to-many and many-to-many relationships using Django ORM
- RESTful API endpoints for:
  - Listing and creating conversations
  - Sending and retrieving messages
- Clean, modular code structure using Django best practices
- Swagger auto-generated API documentation
- Environment variable support using `.env`

---

## 🛠 Project Structure

```bash
messaging_app/
├── chats/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── messaging_app/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
`

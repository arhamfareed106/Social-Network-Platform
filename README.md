# Social Network Platform

## Project Overview

A comprehensive social networking application built with Django, featuring real-time communication, user interactions, and modern web technologies.

### Key Features

- 👤 User Management
  - User registration and authentication
  - Personalized user profiles
  - Avatar uploads
  - Follow/Unfollow system

- 📝 Post System
  - Create posts with text and images
  - Like and comment functionality
  - Personalized content feed

- 💬 Real-time Chat
  - WebSocket-powered messaging
  - Multi-user chat rooms
  - Instant message delivery

### Technology Stack

- **Backend**: Django 4.2.7
- **Real-time Communication**: Django Channels
- **Frontend**: Bootstrap 5
- **Database**: SQLite (default)
- **Image Processing**: Pillow
- **Form Handling**: Django Crispy Forms

### Prerequisites

- Python 3.13.0
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/social-network.git
cd social-network
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

### Configuration

- Default admin credentials:
  - Username: admin
  - Password: admin123

### Project Structure

```
social_network/
│
├── users/           # User management app
│   ├── models.py    # User profile model
│   ├── views.py     # User-related views
│   └── forms.py     # User registration and profile forms
│
├── posts/           # Posts management app
│   ├── models.py    # Post and comment models
│   ├── views.py     # Post-related views
│   └── forms.py     # Post creation forms
│
├── chat/            # Real-time chat app
│   ├── models.py    # Chat room and message models
│   ├── consumers.py # WebSocket consumers
│   └── routing.py   # WebSocket routing
│
└── templates/       # HTML templates
```

### Key Functionalities

- User Registration and Authentication
- Profile Creation and Editing
- Post Creation with Rich Media
- Like and Comment System
- Real-time Chat Rooms
- User Following System

### Security Features

- Django's built-in CSRF protection
- User authentication for sensitive actions
- Input validation and sanitization

### Future Roadmap

- [ ] Implement advanced search functionality
- [ ] Add user notifications
- [ ] Enhance privacy settings
- [ ] Implement user blocking/muting
- [ ] Add unit and integration tests

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### License

Distributed under the MIT License. See `LICENSE` for more information.

### Contact

Arham Fareed - arhamfareed575@gmail.com

Project Link: [https://github.com/arhamfareed106/Social-Network-Platform]

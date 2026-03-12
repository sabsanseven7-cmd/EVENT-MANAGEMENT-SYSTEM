# Event Management System

A modern Flask-based web application for managing events with user authentication, booking system, and AI chatbot assistance.

## 🚀 Features

- **User Registration & Authentication**: Secure user accounts with bcrypt password hashing
- **Event Booking System**: Book weddings, birthdays, corporate events, and more
- **Admin Dashboard**: Comprehensive admin panel with statistics and booking management
- **AI Chatbot**: Interactive assistant for event inquiries and support
- **Responsive Design**: Modern UI with Tailwind CSS
- **Database Management**: SQLite database with proper relationships
- **Flash Messages**: User-friendly feedback system
- **Security**: Environment-based configuration and secure session management

## 🛠️ Quick Setup

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Manual Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration

4. Run the application:
```bash
python app.py
```

5. Access at `http://localhost:5000`

## 🔐 Default Credentials

### Admin Access
- Username: `admin` (configurable in .env)
- Password: `admin123` (configurable in .env)

## 📁 Project Structure

```
├── app.py                  # Main Flask application
├── setup.py               # Automated setup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── event.db              # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── landing.html      # Modern landing page
│   ├── login.html        # User/Admin login
│   ├── register.html     # User registration
│   ├── events.html       # Event booking page
│   ├── my_bookings.html  # User booking history
│   ├── admin_dashboard.html # Admin panel
│   └── chatbot.html      # AI assistant widget
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📊 Database Schema

### Users Table
- `id` (INTEGER PRIMARY KEY)
- `username` (TEXT UNIQUE NOT NULL)
- `password` (TEXT NOT NULL) - bcrypt hashed
- `email` (TEXT UNIQUE)
- `created_at` (TIMESTAMP)

### Events Table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `description` (TEXT)
- `price` (DECIMAL)
- `category` (TEXT NOT NULL)
- `created_at` (TIMESTAMP)

### Bookings Table
- `id` (INTEGER PRIMARY KEY)
- `username` (TEXT NOT NULL)
- `event_type` (TEXT NOT NULL)
- `date` (TEXT NOT NULL)
- `guests` (INTEGER NOT NULL)
- `status` (TEXT DEFAULT 'pending')
- `created_at` (TIMESTAMP)

### Chats Table
- `id` (INTEGER PRIMARY KEY)
- `user_message` (TEXT NOT NULL)
- `bot_reply` (TEXT NOT NULL)
- `created_at` (TIMESTAMP)

## 🌐 API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET/POST /login` - User/Admin authentication
- `GET/POST /register` - User registration

### User Routes (Authentication Required)
- `GET /events` - Event listing and booking
- `POST /book` - Create event booking
- `GET /my_bookings` - User booking history
- `GET /logout` - Logout

### Admin Routes (Admin Authentication Required)
- `GET /admin_dashboard` - Admin panel with statistics
- `POST /admin/booking/<id>/status` - Update booking status

### API Routes
- `POST /chat` - Chatbot API

## 🤖 AI Chatbot Features

The integrated chatbot can help with:
- Event pricing information
- Contact details
- Booking guidance
- Event-specific questions (weddings, birthdays, corporate)
- General inquiries

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **Session Management**: Secure Flask sessions
- **Input Validation**: Form validation and sanitization
- **Environment Configuration**: Sensitive data in environment variables
- **SQL Injection Protection**: Parameterized queries
- **CSRF Protection**: Built-in Flask security

## 🎨 UI/UX Improvements

- Modern gradient design
- Responsive layout for all devices
- Interactive elements with hover effects
- Flash message system for user feedback
- Professional admin dashboard
- Intuitive navigation

## 📈 Recent Improvements

1. **Security Enhancements**
   - Added bcrypt password hashing
   - Environment-based configuration
   - Input validation and sanitization

2. **Database Improvements**
   - Added proper relationships
   - Enhanced schema with timestamps
   - Default event data seeding

3. **UI/UX Overhaul**
   - Modern landing page design
   - Improved forms with validation
   - Professional admin dashboard
   - Better navigation and user flow

4. **Feature Additions**
   - User booking history
   - Admin booking management
   - Enhanced chatbot responses
   - Statistics dashboard

5. **Code Quality**
   - Better error handling
   - Flash message system
   - Modular code structure
   - Comprehensive documentation

## 🚀 Next Level Features

This application is now production-ready with:
- Secure authentication system
- Professional UI/UX design
- Comprehensive admin tools
- Enhanced chatbot functionality
- Proper database relationships
- Security best practices

## 📝 License

This project is open source and available under the MIT License.
from flask import Flask, render_template, request, redirect, session, jsonify, flash
import sqlite3
import os
import re
import hashlib
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Try to import bcrypt, fallback to hashlib if not available
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("Warning: bcrypt not available, using hashlib (less secure)")

load_dotenv()

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

# Configuration
class Config:
    DATABASE = 'event.db'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'event_images')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(Config.DATABASE, timeout=20.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def close_db_connection(conn):
    """Safely close database connection"""
    if conn:
        try:
            conn.close()
        except:
            pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def ensure_upload_folder():
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = None
    try:
        conn = get_db()

        # Create users table with basic structure first
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )""")

        # Check if email column exists, if not add it
        try:
            conn.execute("SELECT email FROM users LIMIT 1")
        except sqlite3.OperationalError:
            # Email column doesn't exist, add it
            conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
            print("✅ Added email column to users table")

        # Check if created_at column exists, if not add it (without default)
        try:
            conn.execute("SELECT created_at FROM users LIMIT 1")
        except sqlite3.OperationalError:
            # created_at column doesn't exist, add it without default
            conn.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP")
            print("✅ Added created_at column to users table")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            event_type TEXT NOT NULL,
            date TEXT NOT NULL,
            guests INTEGER NOT NULL
        )""")

        # Check if status column exists in bookings, if not add it
        try:
            conn.execute("SELECT status FROM bookings LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE bookings ADD COLUMN status TEXT DEFAULT 'pending'")
            print("✅ Added status column to bookings table")

        # Check if created_at column exists in bookings, if not add it
        try:
            conn.execute("SELECT created_at FROM bookings LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE bookings ADD COLUMN created_at TIMESTAMP")
            print("✅ Added created_at column to bookings table")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_reply TEXT NOT NULL
        )""")

        # Check if created_at column exists in chats, if not add it
        try:
            conn.execute("SELECT created_at FROM chats LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE chats ADD COLUMN created_at TIMESTAMP")
            print("✅ Added created_at column to chats table")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        try:
            conn.execute("SELECT image_url FROM events LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE events ADD COLUMN image_url TEXT")
            print("Added image_url to events")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS venues(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        try:
            conn.execute("SELECT venue_id FROM bookings LIMIT 1")
        except sqlite3.OperationalError:
            conn.execute("ALTER TABLE bookings ADD COLUMN venue_id INTEGER")
            conn.execute("ALTER TABLE bookings ADD COLUMN venue_name TEXT")
            print("Added venue_id, venue_name to bookings")

        existing_venues = conn.execute("SELECT COUNT(*) FROM venues").fetchone()[0]
        if existing_venues == 0:
            conn.executemany("INSERT INTO venues (name, address, capacity) VALUES (?, ?, ?)",
                             [('Grand Ballroom', '123 Event Street, City Center', 500),
                              ('Garden Pavilion', '456 Park Avenue', 200),
                              ('Conference Hall A', '789 Business Park', 150)])
            print("Added default venues")

        existing_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if existing_events == 0:
            default_events = [
                ('Wedding Package', 'Complete wedding planning with decoration, catering, and photography', 50000.00, 'Wedding', None),
                ('Birthday Celebration', 'Birthday party setup with cake, decorations, and entertainment', 20000.00, 'Birthday', None),
                ('Corporate Event', 'Professional corporate event management with AV setup', 40000.00, 'Corporate', None),
                ('Anniversary Special', 'Romantic anniversary celebration setup', 30000.00, 'Anniversary', None),
                ('Baby Shower', 'Beautiful baby shower arrangement with themed decorations', 25000.00, 'Baby Shower', None)
            ]
            conn.executemany("INSERT INTO events (name, description, price, category, image_url) VALUES (?, ?, ?, ?, ?)", default_events)
            print("Added default events")

        conn.commit()
        
    except Exception as e:
        print(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        close_db_connection(conn)

def hash_password(password):
    if BCRYPT_AVAILABLE:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
        # Fallback to hashlib (less secure, for development only)
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(password, hashed):
    if BCRYPT_AVAILABLE:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    else:
        # Fallback comparison
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed

init_db()

# ---------- ROUTES ----------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/events")
def events():
    conn = None
    try:
        conn = get_db()
        events_list = conn.execute("SELECT * FROM events ORDER BY category, name").fetchall()
        venues_list = conn.execute("SELECT * FROM venues ORDER BY name").fetchall()
        return render_template("events.html", events=events_list, venues=venues_list)
    finally:
        close_db_connection(conn)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip()

        # Validation
        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("register.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", "error")
            return render_template("register.html")

        conn = None
        try:
            conn = get_db()
            hashed_password = hash_password(password)
            
            # Check if email column exists
            try:
                if email:
                    conn.execute("INSERT INTO users(username, password, email) VALUES (?,?,?)",
                                 (username, hashed_password, email))
                else:
                    conn.execute("INSERT INTO users(username, password, email) VALUES (?,?,?)",
                                 (username, hashed_password, None))
            except sqlite3.OperationalError:
                # Email column doesn't exist, insert without it
                conn.execute("INSERT INTO users(username, password) VALUES (?,?)",
                             (username, hashed_password))
            
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect("/login")
            
        except sqlite3.IntegrityError as e:
            flash("Username already exists", "error")
            return render_template("register.html")
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower():
                flash("Database is busy, please try again in a moment", "error")
            else:
                flash(f"Database error: {str(e)}", "error")
            return render_template("register.html")
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")
            return render_template("register.html")
        finally:
            close_db_connection(conn)

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("login.html")

        if role == "admin":
            if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
                session["admin"] = True
                session["username"] = username
                flash("Admin login successful", "success")
                return redirect("/admin_dashboard")
            else:
                flash("Invalid admin credentials", "error")
                return render_template("login.html")

        # User login
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password(password, user['password']):
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect("/events")
        else:
            flash("Invalid username or password", "error")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    username = session.get("user") or session.get("username")
    session.clear()
    if username:
        flash(f"Goodbye, {username}!", "info")
    return redirect("/")

@app.route("/book", methods=["POST"])
def book():
    if "user" not in session:
        flash("Please login to book an event", "error")
        return redirect("/login")

    event_id = request.form.get("event_id")
    venue_id = request.form.get("venue_id")
    date = request.form.get("date")
    guests = request.form.get("guests")

    if not all([event_id, date, guests]):
        flash("All fields are required", "error")
        return redirect("/events")
    if not venue_id:
        flash("Please select a venue", "error")
        return redirect("/events")

    try:
        guests = int(guests)
        if guests <= 0:
            flash("Number of guests must be positive", "error")
            return redirect("/events")
    except ValueError:
        flash("Invalid number of guests", "error")
        return redirect("/events")

    # Validate date is in the future
    try:
        booking_date = datetime.strptime(date, '%Y-%m-%d')
        if booking_date.date() <= datetime.now().date():
            flash("Booking date must be in the future", "error")
            return redirect("/events")
    except ValueError:
        flash("Invalid date format", "error")
        return redirect("/events")

    conn = None
    try:
        conn = get_db()
        event = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
        venue = conn.execute("SELECT * FROM venues WHERE id=?", (venue_id,)).fetchone()
        if not event:
            flash("Invalid event selected", "error")
            return redirect("/events")
        if not venue:
            flash("Invalid venue selected", "error")
            return redirect("/events")
        if guests > venue['capacity']:
            flash(f"Guest count exceeds venue capacity ({venue['capacity']}). Please choose another venue.", "error")
            return redirect("/events")
        conn.execute("""
            INSERT INTO bookings(username, event_type, date, guests, status, venue_id, venue_name)
            VALUES (?,?,?,?,?,?,?)
        """, (session["user"], event['name'], date, guests, 'confirmed', venue['id'], venue['name']))
        conn.commit()
        flash(f"Booking confirmed for {event['name']} at {venue['name']} on {date}!", "success")
        return redirect("/my_bookings")
    finally:
        close_db_connection(conn)

@app.route("/my_bookings")
def my_bookings():
    if "user" not in session:
        flash("Please login to view bookings", "error")
        return redirect("/login")
    
    conn = get_db()
    bookings = conn.execute("""
        SELECT * FROM bookings 
        WHERE username=? 
        ORDER BY created_at DESC
    """, (session["user"],)).fetchall()
    conn.close()
    
    return render_template("my_bookings.html", bookings=bookings)

# ---------- ADMIN ----------
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session["admin"] = True
            session["username"] = username
            return redirect("/admin_dashboard")
        
        flash("Invalid admin credentials", "error")
        return render_template("admin_login.html")

    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        flash("Admin access required", "error")
        return redirect("/admin")

    conn = get_db()
    
    # Get statistics
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_bookings = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    pending_bookings = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='pending'").fetchone()[0]
    
    # Get recent bookings with more details
    bookings = conn.execute("""
        SELECT b.*, u.email 
        FROM bookings b 
        LEFT JOIN users u ON b.username = u.username 
        ORDER BY b.created_at DESC 
        LIMIT 20
    """).fetchall()
    
    # Get recent chats
    chats = conn.execute("""
        SELECT * FROM chats 
        ORDER BY created_at DESC 
        LIMIT 10
    """).fetchall()
    
    conn.close()

    return render_template("admin_dashboard.html",
                           bookings=bookings,
                           chats=chats,
                           stats={
                               'total_users': total_users,
                               'total_bookings': total_bookings,
                               'pending_bookings': pending_bookings
                           })

@app.route("/admin/booking/<int:booking_id>/status", methods=["POST"])
def update_booking_status(booking_id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    new_status = request.json.get("status")
    if new_status not in ["pending", "confirmed", "cancelled"]:
        return jsonify({"error": "Invalid status"}), 400
    conn = None
    try:
        conn = get_db()
        conn.execute("UPDATE bookings SET status=? WHERE id=?", (new_status, booking_id))
        conn.commit()
        return jsonify({"success": True})
    finally:
        close_db_connection(conn)

# ---------- ADMIN VENUES ----------
@app.route("/admin/venues", methods=["GET", "POST"])
def admin_venues():
    if "admin" not in session:
        flash("Admin access required", "error")
        return redirect("/admin")
    conn = None
    try:
        conn = get_db()
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            address = request.form.get("address", "").strip()
            capacity = request.form.get("capacity", "0")
            if name and address:
                try:
                    cap = int(capacity)
                    if cap > 0:
                        conn.execute("INSERT INTO venues (name, address, capacity) VALUES (?, ?, ?)", (name, address, cap))
                        conn.commit()
                        flash("Venue added successfully", "success")
                except ValueError:
                    flash("Capacity must be a positive number", "error")
            else:
                flash("Name and address are required", "error")
        venues_list = conn.execute("SELECT * FROM venues ORDER BY name").fetchall()
        return render_template("admin_venues.html", venues=venues_list)
    finally:
        close_db_connection(conn)

@app.route("/admin/venues/<int:venue_id>/edit", methods=["GET", "POST"])
def admin_venue_edit(venue_id):
    if "admin" not in session:
        flash("Admin access required", "error")
        return redirect("/admin")
    conn = None
    try:
        conn = get_db()
        venue = conn.execute("SELECT * FROM venues WHERE id=?", (venue_id,)).fetchone()
        if not venue:
            flash("Venue not found", "error")
            return redirect("/admin/venues")
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            address = request.form.get("address", "").strip()
            capacity = request.form.get("capacity", "0")
            if name and address:
                try:
                    cap = int(capacity)
                    if cap > 0:
                        conn.execute("UPDATE venues SET name=?, address=?, capacity=? WHERE id=?", (name, address, cap, venue_id))
                        conn.commit()
                        flash("Venue updated successfully", "success")
                        return redirect("/admin/venues")
                except ValueError:
                    flash("Capacity must be a positive number", "error")
            else:
                flash("Name and address are required", "error")
        return render_template("admin_venue_edit.html", venue=venue)
    finally:
        close_db_connection(conn)

# ---------- ADMIN EVENTS ----------
@app.route("/admin/events", methods=["GET"])
def admin_events_list():
    if "admin" not in session:
        flash("Admin access required", "error")
        return redirect("/admin")
    conn = None
    try:
        conn = get_db()
        events_list = conn.execute("SELECT * FROM events ORDER BY category, name").fetchall()
        return render_template("admin_events.html", events=events_list)
    finally:
        close_db_connection(conn)

@app.route("/admin/events/<int:event_id>/edit", methods=["GET", "POST"])
def admin_event_edit(event_id):
    if "admin" not in session:
        flash("Admin access required", "error")
        return redirect("/admin")
    conn = None
    try:
        conn = get_db()
        event = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
        if not event:
            flash("Event not found", "error")
            return redirect("/admin/events")
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            price = request.form.get("price", "0")
            category = request.form.get("category", "").strip()
            image_url = request.form.get("image_url", "").strip() or None

            # Handle image file upload
            image_file = request.files.get("image_file")
            if image_file and image_file.filename and allowed_file(image_file.filename):
                size = getattr(image_file, "content_length", None)
                if size and size > Config.MAX_IMAGE_SIZE:
                    flash("Image must be under 5 MB", "error")
                else:
                    ensure_upload_folder()
                    ext = image_file.filename.rsplit(".", 1)[1].lower()
                    filename = f"event_{event_id}_{int(time.time())}.{ext}"
                    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                    image_file.save(filepath)
                    image_url = f"/static/event_images/{filename}"

            if name and category:
                try:
                    p = float(price)
                    if p >= 0:
                        conn.execute("UPDATE events SET name=?, description=?, price=?, category=?, image_url=? WHERE id=?",
                                     (name, description, p, category, image_url, event_id))
                        conn.commit()
                        flash("Event updated successfully", "success")
                        return redirect("/admin/events")
                except ValueError:
                    flash("Price must be a number", "error")
            else:
                flash("Name and category are required", "error")
        return render_template("admin_event_edit.html", event=event)
    finally:
        close_db_connection(conn)

# ---------- CHATBOT ----------
def _extract_guest_count(msg):
    m = re.search(r'\b(\d{1,4})\s*(?:guests?|people|persons?|pax)\b', msg, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r'\b(?:for|about)\s*(\d{1,4})\b', msg, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r'\b(\d{1,4})\b', msg)
    if m:
        return int(m.group(1))
    return None

@app.route("/chat", methods=["POST"])
def chat():
    msg_raw = request.json.get("message", "").strip()
    msg = msg_raw.lower()
    if not msg:
        return jsonify({"reply": "Please type a message!"})

    conn = None
    try:
        conn = get_db()
        events = conn.execute("SELECT id, name, description, price, category FROM events ORDER BY price").fetchall()
    finally:
        close_db_connection(conn)

    guest_count = _extract_guest_count(msg)
    price_list_str = "\n".join([f"• {e['name']}: Rs.{e['price']:,.0f}" for e in events])

    if guest_count is not None and guest_count > 0:
        if any(w in msg for w in ["wedding", "marriage"]):
            ev = next((e for e in events if "wedding" in e["category"].lower() or "wedding" in e["name"].lower()), events[0] if events else None)
            if ev:
                reply = f"For a wedding with **{guest_count}** guests we recommend:\n\n**{ev['name']}** – Rs.{ev['price']:,.0f}\n{ev['description']}\n\nPick a venue that fits {guest_count} guests on the Events page!"
            else:
                reply = f"For {guest_count} guests, head to Events to choose a package and venue."
        elif any(w in msg for w in ["birthday", "party"]):
            ev = next((e for e in events if "birthday" in e["category"].lower() or "birthday" in e["name"].lower()), None)
            ev = ev or (next((e for e in events if e["price"] < 40000), None) if events else None) or (events[0] if events else None)
            if ev:
                reply = f"For a birthday with **{guest_count}** guests:\n\n**{ev['name']}** – Rs.{ev['price']:,.0f}\n{ev['description']}\n\nSelect a venue with capacity ≥{guest_count} on the Events page!"
            else:
                reply = f"For {guest_count} guests, check our Events page for packages and venues."
        elif any(w in msg for w in ["corporate", "business", "office"]):
            ev = next((e for e in events if "corporate" in e["category"].lower() or "corporate" in e["name"].lower()), events[0] if events else None)
            if ev:
                reply = f"For a corporate event with **{guest_count}** attendees:\n\n**{ev['name']}** – Rs.{ev['price']:,.0f}\n{ev['description']}\n\nChoose a venue when you book!"
            else:
                reply = f"For {guest_count} guests, see Events and pick a venue."
        else:
            ev = events[0] if events else None
            if ev:
                reply = f"For **{guest_count}** guests you might like:\n\n**{ev['name']}** – Rs.{ev['price']:,.0f}\n{ev['description']}\n\nView all options on the Events page!"
            else:
                reply = f"For {guest_count} guests, head to Events to book."
    elif any(word in msg for word in ["price", "cost", "fee", "charge"]):
        reply = f"Here are our event packages:\n{price_list_str}\n\nPrices include basic setup. Contact us for custom packages!"
    elif any(word in msg for word in ["contact", "phone", "call", "reach"]):
        reply = "Call us at +91 9876543210\nEmail: events@company.com\nAvailable 9 AM - 8 PM"
    elif any(word in msg for word in ["book", "booking", "reserve"]):
        if "user" in session:
            reply = "Great! Go to Events, choose a package and venue, then pick your date. You can book from there!"
        else:
            reply = "Please login first to book. Registration is quick and easy!"
    elif any(word in msg for word in ["cheapest", "budget", "affordable"]):
        ev = events[0] if events else None
        reply = f"Our most affordable option is **{ev['name']}** at Rs.{ev['price']:,.0f}.\n\n{ev['description']}\n\nSee all: {price_list_str}" if ev else "Contact us for quotes."
    elif any(word in msg for word in ["recommend", "suggest", "which", "what event"]):
        reply = f"Popular packages:\n{price_list_str}\n\nTell me the event type and guests (e.g. birthday for 50 people) for a tailored suggestion!"
    elif any(word in msg for word in ["wedding", "marriage"]):
        reply = "Our wedding packages include venue decoration, catering, photography, music. Starting from Rs.50,000. How many guests? I can suggest a venue size!"
    elif any(word in msg for word in ["birthday", "party"]):
        reply = "Birthday packages include themed decorations, cake, games, photography. Starting from Rs.20,000! Tell me how many guests for a better suggestion."
    elif any(word in msg for word in ["corporate", "business", "office"]):
        reply = "Corporate events include professional setup, AV, catering, coordination. Starting from Rs.40,000!"
    elif any(word in msg for word in ["hello", "hi", "hey"]):
        reply = "Hello! I can help with event prices, suggestions (e.g. birthday for 50 people), venues, booking, and contact details. What do you need?"
    else:
        reply = "I can help with: **Prices** – ask 'what are the prices?' | **Suggestions** – e.g. 'birthday for 50 people' | **Contact** | **Booking** – login and go to Events. What would you like?"

    conn = None
    try:
        conn = get_db()
        conn.execute("INSERT INTO chats(user_message, bot_reply) VALUES (?,?)", (msg_raw, reply))
        conn.commit()
    finally:
        close_db_connection(conn)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

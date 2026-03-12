# 🧪 Event Management System - Testing Checklist

## Before Testing
1. Start the application: `python app.py`
2. Open browser to: `http://localhost:5000`

## ✅ Manual Testing Checklist

### 🏠 Landing Page (/)
- [ ] Page loads without errors
- [ ] Navigation buttons work (Events, Login, Register)
- [ ] Modern design displays correctly
- [ ] Event cards show pricing
- [ ] Chatbot button appears in bottom-right

### 👤 User Registration (/register)
- [ ] Registration form displays
- [ ] All fields are required (username, email, password)
- [ ] Password minimum 6 characters validation
- [ ] Success message after registration
- [ ] Redirect to login page
- [ ] Error handling for duplicate username/email

### 🔐 User Login (/login)
- [ ] Login form displays
- [ ] User/Admin role selection works
- [ ] Valid user login redirects to events page
- [ ] Invalid credentials show error message
- [ ] Flash messages display correctly

### 👨‍💼 Admin Login
- [ ] Admin login with: username=`admin`, password=`admin123`
- [ ] Redirects to admin dashboard
- [ ] Admin dashboard shows statistics
- [ ] Bookings table displays
- [ ] Chat logs visible
- [ ] Booking status can be updated

### 🎉 Events Page (/events)
- [ ] Events display in cards
- [ ] Pricing shows correctly
- [ ] Login required message for non-logged users
- [ ] Date picker works (minimum tomorrow)
- [ ] Guest number input validation
- [ ] Booking form submission works

### 📅 My Bookings (/my_bookings)
- [ ] User bookings display
- [ ] Booking status shows correctly
- [ ] Empty state for no bookings
- [ ] Navigation works

### 🤖 Chatbot Testing
- [ ] Chatbot button opens/closes chat window
- [ ] Type "hello" - gets welcome message
- [ ] Type "price" - shows event pricing
- [ ] Type "contact" - shows contact info
- [ ] Type "wedding" - shows wedding info
- [ ] Type "book" - shows booking guidance
- [ ] Messages save to database (check admin panel)

### 🔄 Navigation & Flow
- [ ] All navigation links work
- [ ] Logout functionality works
- [ ] Session management works
- [ ] Flash messages appear and disappear
- [ ] Responsive design on mobile

### 🛡️ Security Testing
- [ ] Cannot access admin pages without admin login
- [ ] Cannot access user pages without user login
- [ ] Password hashing works (check database)
- [ ] Session timeout works
- [ ] Input validation prevents empty submissions

## 🚨 Common Issues & Solutions

### Registration Error
**Problem**: "Create Account" button not working
**Solution**: 
1. Check if all fields are filled
2. Ensure password is 6+ characters
3. Try different username/email
4. Check browser console for errors

### Login Issues
**Problem**: Cannot login after registration
**Solution**:
1. Ensure correct username/password
2. Select correct role (User/Admin)
3. Check if registration was successful

### Events Not Loading
**Problem**: Events page shows no events
**Solution**:
1. Database might not be initialized
2. Restart the application
3. Check console for database errors

### Chatbot Not Responding
**Problem**: Chatbot doesn't reply
**Solution**:
1. Check network tab in browser
2. Ensure server is running
3. Try refreshing the page

## 📊 Expected Test Results

### Successful Registration Flow:
1. Fill registration form → Success message
2. Redirect to login → Login with new credentials
3. Access events page → See available events
4. Make booking → Confirmation message
5. Check "My Bookings" → See booking listed

### Admin Flow:
1. Login as admin → Access dashboard
2. View statistics → See user/booking counts
3. Check bookings → See all user bookings
4. Update booking status → Status changes
5. View chat logs → See chatbot conversations

## 🎯 Performance Checks
- [ ] Pages load within 2 seconds
- [ ] No console errors in browser
- [ ] Database operations complete quickly
- [ ] Responsive design works on mobile
- [ ] Images and styles load correctly

## 📝 Notes
- Default admin: username=`admin`, password=`admin123`
- Database file: `event.db` (auto-created)
- All passwords are hashed for security
- Flash messages provide user feedback
- Chatbot responses are contextual and helpful
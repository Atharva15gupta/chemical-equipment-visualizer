# Quick Setup Guide

This guide will help you get the Chemical Equipment Visualizer up and running quickly.

## ⚡ Quick Start (5 Minutes)

### Step 1: Backend Setup

```bash
# Open Terminal/Command Prompt
cd chemical-equipment-visualizer/backend

# Install Python dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 pandas==2.1.3 reportlab==4.0.7

# Setup database
python manage.py makemigrations equipment
python manage.py migrate

# Start backend server
python manage.py runserver
```

✅ Backend should now be running at http://localhost:8000

### Step 2: Web Frontend Setup (New Terminal)

```bash
# Open a NEW terminal window
cd chemical-equipment-visualizer/frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

✅ Web app should open automatically at http://localhost:3000

### Step 3: Test the Application

1. Go to http://localhost:3000
2. Click "Register" and create an account
3. Login with your credentials
4. Upload the `sample_equipment_data.csv` file
5. Click "Upload & Analyze"
6. Explore the results!

### Step 4: Desktop App (Optional)

```bash
# Open another NEW terminal
cd chemical-equipment-visualizer/desktop

# Install dependencies
pip install PyQt5==5.15.10 matplotlib==3.8.2 pandas==2.1.3 requests==2.31.0

# Run desktop app
python main.py
```

## 🔍 Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can register a new user
- [ ] Can login successfully
- [ ] Can upload CSV file
- [ ] Charts display correctly
- [ ] Can download PDF report
- [ ] History shows uploaded files

## 🚨 Common Issues & Solutions

### Issue: "Module not found" errors

**Solution:**
```bash
# For Python modules
pip install -r requirements.txt

# For Node modules
npm install
```

### Issue: Port already in use

**Solution for Backend:**
```bash
# Use a different port
python manage.py runserver 8001
# Then update API URL in frontend/src/services/api.js
```

**Solution for Frontend:**
```bash
# Kill the process using port 3000
# Windows: netstat -ano | findstr :3000
# Mac/Linux: lsof -ti:3000 | xargs kill
```

### Issue: CORS errors

**Solution:**
Check that `CORS_ALLOW_ALL_ORIGINS = True` is set in `backend/config/settings.py`

### Issue: Database errors

**Solution:**
```bash
cd backend
rm db.sqlite3  # Delete old database
python manage.py makemigrations
python manage.py migrate
```

## 📱 Testing with Sample Data

The project includes `sample_equipment_data.csv` with 20 equipment entries. Use this to test all features:

1. Upload the file
2. Check that it shows 20 total equipment
3. Verify the charts display correctly
4. Download the PDF report
5. Upload again to test history (keeps last 5)

## 🎬 Creating Demo Video

Record your screen showing:

1. **Backend Start** (10 seconds)
   - Show terminal with `python manage.py runserver`

2. **Web App Demo** (60 seconds)
   - Register/Login
   - Upload CSV
   - Show charts and data
   - Download PDF

3. **Desktop App Demo** (40 seconds)
   - Login
   - Upload CSV
   - Show all tabs
   - Download PDF

4. **Features Showcase** (20 seconds)
   - History feature
   - Multiple uploads

**Recommended Tools:**
- OBS Studio (Free)
- Loom (Easy to use)
- QuickTime (Mac)
- Windows Game Bar (Windows)

## 📤 Submission Checklist

Before submitting:

- [ ] Code pushed to GitHub
- [ ] README.md complete
- [ ] All features working
- [ ] Demo video recorded (2-3 minutes)
- [ ] Tested on clean environment
- [ ] Screenshots/video uploaded
- [ ] Form submitted: https://forms.gle/bSiKezbM4Ji9xnw66

## 🆘 Need Help?

If you encounter issues:

1. Check this guide's troubleshooting section
2. Read the main README.md
3. Check console/terminal for error messages
4. Verify all dependencies are installed
5. Ensure backend is running before frontend

## 🎯 Success Criteria

Your submission should demonstrate:

✅ Working Django REST API backend
✅ React web interface with Chart.js
✅ PyQt5 desktop application with Matplotlib
✅ CSV upload and processing
✅ Data visualization (charts)
✅ PDF report generation
✅ User authentication
✅ History management (last 5 datasets)
✅ Professional code organization
✅ Clear documentation

Good luck! 🚀

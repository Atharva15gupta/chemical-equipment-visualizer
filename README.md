# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for analyzing and visualizing chemical equipment parameters. Built with Django REST Framework backend, React.js web frontend, and PyQt5 desktop application.

## 🎯 Features

- **CSV Upload & Analysis**: Upload equipment data and get instant statistical analysis
- **Data Visualization**: Interactive charts showing equipment distribution and parameter averages
- **History Management**: Automatically stores last 5 uploaded datasets
- **PDF Report Generation**: Download detailed PDF reports of your analysis
- **Basic Authentication**: Secure user registration and login
- **Dual Interface**: Access via web browser or desktop application

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Web interface with charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Desktop application |
| Backend | Django + Django REST Framework | API server |
| Data Handling | Pandas | CSV processing & analytics |
| Database | SQLite | Data persistence |
| Report Generation | ReportLab | PDF reports |

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django backend
│   ├── config/                # Project configuration
│   ├── equipment/             # Main app
│   ├── media/                 # Uploaded files
│   ├── manage.py
│   └── requirements.txt
├── frontend/                  # React web app
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   └── *.css
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── desktop/                   # PyQt5 desktop app
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv  # Sample data file
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- pip

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The web app will open automatically at `http://localhost:3000`

### 3. Desktop Application Setup (PyQt5)

```bash
# Navigate to desktop directory
cd desktop

# Create virtual environment (if not using backend's)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

## 📊 Usage Guide

### Web Application

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload CSV**: Click "Choose File" and select a CSV file with equipment data
3. **Analyze**: Click "Upload & Analyze" to process the data
4. **View Results**: See summary statistics, charts, and detailed data table
5. **Download PDF**: Generate and download a PDF report
6. **View History**: Check your last 5 uploads in the History section

### Desktop Application

1. **Login**: Enter credentials and click "Login" (or register first)
2. **Select File**: Click "Select CSV File" and choose your data file
3. **Upload**: Click "Upload & Analyze"
4. **Explore Tabs**:
   - **Summary**: View statistical overview
   - **Charts**: See pie and bar charts
   - **Data Table**: Browse all equipment entries
   - **History**: View past uploads
5. **Download PDF**: Click "Download PDF Report" to save a report

## 📄 CSV File Format

Your CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,8.2,120
Pump-B2,Pump,200.3,12.5,85
Heat Exchanger-C3,Heat Exchanger,180.7,10.1,95
```

**Required Columns:**
- Equipment Name (string)
- Type (string)
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

A sample CSV file (`sample_equipment_data.csv`) is provided in the root directory.

## 🔐 Authentication

The application uses Django's built-in authentication with session-based auth for both web and desktop clients.

**Default Test User:**
- Create your own user via the registration form
- Or use Django admin to create users

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | Login user |
| `/api/datasets/upload/` | POST | Upload CSV file |
| `/api/datasets/history/` | GET | Get last 5 datasets |
| `/api/datasets/{id}/download_pdf/` | GET | Download PDF report |

## 🔧 Configuration

### Backend Configuration

Edit `backend/config/settings.py` for:
- Database settings
- CORS configuration
- Media file storage
- Authentication settings

### Frontend Configuration

Edit `frontend/src/services/api.js` to change:
- API base URL (default: `http://localhost:8000/api`)

### Desktop Configuration

Edit `desktop/main.py` to change:
- API base URL (currently hardcoded as `http://localhost:8000`)

## 🎨 Features Demonstrated

1. ✅ **CSV Upload** - Both web and desktop interfaces
2. ✅ **Data Summary API** - Statistical analysis via Django REST Framework
3. ✅ **Visualization** - Chart.js (web) and Matplotlib (desktop)
4. ✅ **History Management** - Automatic storage of last 5 datasets
5. ✅ **PDF Report Generation** - ReportLab integration
6. ✅ **Basic Authentication** - User registration and login
7. ✅ **Sample CSV** - Provided for testing

## 🐛 Troubleshooting

### Backend Issues

**"No module named 'django'"**
```bash
pip install -r requirements.txt
```

**Database errors**
```bash
python manage.py migrate
```

**CORS errors from frontend**
- Check `CORS_ALLOW_ALL_ORIGINS` in settings.py
- Ensure backend is running on port 8000

### Frontend Issues

**"npm command not found"**
- Install Node.js from nodejs.org

**Module not found errors**
```bash
npm install
```

**Can't connect to backend**
- Ensure backend is running at http://localhost:8000
- Check CORS settings

### Desktop App Issues

**"No module named 'PyQt5'"**
```bash
pip install -r requirements.txt
```

**Connection refused**
- Ensure Django backend is running
- Check API URL in main.py

## 📦 Building for Production

### Web Frontend

```bash
cd frontend
npm run build
```

Deploy the `build/` directory to your web server.

### Desktop Application

Package with PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed desktop/main.py
```

### Backend

- Set `DEBUG = False` in settings.py
- Configure a production database (PostgreSQL recommended)
- Set up a proper web server (Gunicorn + Nginx)
- Configure environment variables for secrets

## 🎥 Demo Video

Create a 2-3 minute video showing:
1. Backend setup and running
2. Web app login and CSV upload
3. Data visualization and PDF download
4. Desktop app demonstration
5. History feature showcase

## 📝 License

This project is created for educational purposes as part of an internship screening task.

## 👥 Author

[Your Name]
- GitHub: [Your GitHub Profile]
- Email: [Your Email]

## 🙏 Acknowledgments

- Django REST Framework documentation
- React.js community
- PyQt5 documentation
- Chart.js and Matplotlib libraries

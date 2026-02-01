#!/bin/bash

echo "========================================"
echo "Chemical Equipment Visualizer - Setup"
echo "========================================"
echo ""

echo "Step 1: Setting up Backend..."
cd backend
echo "Installing Python dependencies..."
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 pandas==2.1.3 reportlab==4.0.7

echo ""
echo "Setting up database..."
python manage.py makemigrations equipment
python manage.py migrate

echo ""
echo "Step 2: Creating superuser (optional)"
echo "You can skip this by pressing Ctrl+C"
python manage.py createsuperuser

echo ""
echo "========================================"
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Run backend:  cd backend && python manage.py runserver"
echo "2. Run frontend: cd frontend && npm install && npm start"
echo "3. Run desktop:  cd desktop && python main.py"
echo "========================================"

import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QTabWidget, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


class LoginWindow(QWidget):
    """Login and Registration Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.session = requests.Session()  # Shared session for cookies
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumWidth(300)
        form_layout.addWidget(QLabel('Username:'))
        form_layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel('Password:'))
        form_layout.addWidget(self.password_input)
        
        # Email (for registration)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email (optional for registration)')
        form_layout.addWidget(QLabel('Email:'))
        form_layout.addWidget(self.email_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.login)
        btn_layout.addWidget(login_btn)
        
        register_btn = QPushButton('Register')
        register_btn.clicked.connect(self.register)
        btn_layout.addWidget(register_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def get_csrf_token(self):
        """Fetch CSRF token from the server"""
        try:
            response = self.session.get('http://localhost:8000/api/auth/csrf/')
            if response.status_code == 200:
                return self.session.cookies.get('csrftoken')
        except Exception as e:
            print(f"Error fetching CSRF token: {e}")
        return None
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            # Get CSRF token first
            csrf_token = self.get_csrf_token()
            headers = {}
            if csrf_token:
                headers['X-CSRFToken'] = csrf_token
            
            response = self.session.post(
                'http://localhost:8000/api/auth/login/',
                json={'username': username, 'password': password},
                headers=headers
            )
            
            if response.status_code == 200:
                self.parent_window.login_success(username, self.session)
            else:
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Connection error: {str(e)}')
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            # Get CSRF token first
            csrf_token = self.get_csrf_token()
            headers = {}
            if csrf_token:
                headers['X-CSRFToken'] = csrf_token
            
            response = self.session.post(
                'http://localhost:8000/api/auth/register/',
                json={'username': username, 'password': password, 'email': email},
                headers=headers
            )
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
                self.password_input.clear()
                self.email_input.clear()
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Registration failed'))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Connection error: {str(e)}')


class DashboardWindow(QWidget):
    """Main Dashboard Widget"""
    
    def __init__(self, username, session, parent=None):
        super().__init__(parent)
        self.username = username
        self.session = session  # Use the session passed from LoginWindow
        self.current_data = None
        self.init_ui()
        self.load_history()
    
    def get_csrf_token(self):
        """Get CSRF token from session cookies"""
        return self.session.cookies.get('csrftoken')
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel(f'Welcome, {self.username}')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(header)
        
        # Upload section
        upload_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        upload_layout.addWidget(self.file_label)
        
        select_btn = QPushButton('Select CSV File')
        select_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(select_btn)
        
        upload_btn = QPushButton('Upload & Analyze')
        upload_btn.clicked.connect(self.upload_file)
        upload_layout.addWidget(upload_btn)
        
        layout.addLayout(upload_layout)
        
        # Tabs for different views
        self.tabs = QTabWidget()
        
        # Summary Tab
        self.summary_widget = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_widget.setLayout(self.summary_layout)
        self.tabs.addTab(self.summary_widget, 'Summary')
        
        # Charts Tab
        self.charts_widget = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_widget.setLayout(self.charts_layout)
        self.tabs.addTab(self.charts_widget, 'Charts')
        
        # Data Table Tab
        self.table_widget = QWidget()
        self.table_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table_layout.addWidget(self.table)
        self.table_widget.setLayout(self.table_layout)
        self.tabs.addTab(self.table_widget, 'Data Table')
        
        # History Tab
        self.history_widget = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_layout.addWidget(self.history_table)
        self.history_widget.setLayout(self.history_layout)
        self.tabs.addTab(self.history_widget, 'History')
        
        layout.addWidget(self.tabs)
        
        # Download PDF button
        pdf_btn = QPushButton('Download PDF Report')
        pdf_btn.clicked.connect(self.download_pdf)
        layout.addWidget(pdf_btn)
        
        self.setLayout(layout)
        self.selected_file = None
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
    
    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, 'Error', 'Please select a file first')
            return
        
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token()
            headers = {}
            if csrf_token:
                headers['X-CSRFToken'] = csrf_token
            
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = self.session.post(
                    'http://localhost:8000/api/datasets/upload/',
                    files=files,
                    headers=headers
                )
            
            if response.status_code == 201:
                self.current_data = response.json()
                self.display_results()
                self.load_history()
                QMessageBox.information(self, 'Success', 'File uploaded successfully!')
            else:
                error_msg = response.json().get('error', 'Upload failed') if response.headers.get('content-type', '').startswith('application/json') else 'Upload failed'
                QMessageBox.warning(self, 'Error', error_msg)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload error: {str(e)}')
    
    def display_results(self):
        if not self.current_data:
            return
        
        summary = self.current_data['summary']
        data = self.current_data['data']
        
        # Clear previous content
        for i in reversed(range(self.summary_layout.count())): 
            self.summary_layout.itemAt(i).widget().setParent(None)
        
        # Display summary
        summary_text = f"""
        <h2>Summary Statistics</h2>
        <p><b>Total Equipment Count:</b> {summary['total_count']}</p>
        <p><b>Average Flowrate:</b> {summary['avg_flowrate']:.2f}</p>
        <p><b>Average Pressure:</b> {summary['avg_pressure']:.2f}</p>
        <p><b>Average Temperature:</b> {summary['avg_temperature']:.2f}</p>
        
        <h3>Equipment Type Distribution:</h3>
        """
        for eq_type, count in summary['type_distribution'].items():
            summary_text += f"<p>{eq_type}: {count}</p>"
        
        summary_label = QLabel(summary_text)
        summary_label.setWordWrap(True)
        self.summary_layout.addWidget(summary_label)
        
        # Display charts
        self.display_charts(summary)
        
        # Display data table
        self.display_table(data)
    
    def display_charts(self, summary):
        # Clear previous charts
        for i in reversed(range(self.charts_layout.count())): 
            self.charts_layout.itemAt(i).widget().setParent(None)
        
        # Create figure with subplots
        fig = Figure(figsize=(12, 5))
        
        # Pie chart for type distribution
        ax1 = fig.add_subplot(121)
        labels = list(summary['type_distribution'].keys())
        sizes = list(summary['type_distribution'].values())
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Equipment Type Distribution')
        
        # Bar chart for average parameters
        ax2 = fig.add_subplot(122)
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [summary['avg_flowrate'], summary['avg_pressure'], summary['avg_temperature']]
        ax2.bar(parameters, values, color=['#36A2EB', '#FF6384', '#4BC0C0'])
        ax2.set_title('Average Parameters')
        ax2.set_ylabel('Value')
        
        fig.tight_layout()
        
        # Add canvas to layout
        canvas = FigureCanvas(fig)
        self.charts_layout.addWidget(canvas)
    
    def display_table(self, data):
        if not data:
            return
        
        df = pd.DataFrame(data)
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())
        
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.table.resizeColumnsToContents()
    
    def load_history(self):
        try:
            response = self.session.get('http://localhost:8000/api/datasets/history/')
            if response.status_code == 200:
                history = response.json()
                self.display_history(history)
        except Exception as e:
            print(f'Error loading history: {str(e)}')
    
    def display_history(self, history):
        self.history_table.setRowCount(len(history))
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            'Filename', 'Date', 'Count', 'Avg Flowrate', 'Avg Pressure'
        ])
        
        for i, dataset in enumerate(history):
            self.history_table.setItem(i, 0, QTableWidgetItem(dataset['filename']))
            self.history_table.setItem(i, 1, QTableWidgetItem(dataset['uploaded_at'][:16]))
            self.history_table.setItem(i, 2, QTableWidgetItem(str(dataset['total_count'])))
            self.history_table.setItem(i, 3, QTableWidgetItem(f"{dataset['avg_flowrate']:.2f}"))
            self.history_table.setItem(i, 4, QTableWidgetItem(f"{dataset['avg_pressure']:.2f}"))
        
        self.history_table.resizeColumnsToContents()
    
    def download_pdf(self):
        if not self.current_data:
            QMessageBox.warning(self, 'Error', 'No data to download')
            return
        
        dataset_id = self.current_data['dataset_id']
        
        try:
            response = self.session.get(
                f'http://localhost:8000/api/datasets/{dataset_id}/download_pdf/',
                stream=True
            )
            
            if response.status_code == 200:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF', f'equipment_report_{dataset_id}.pdf', 'PDF Files (*.pdf)'
                )
                
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'PDF downloaded successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to download PDF')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Download error: {str(e)}')


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget with stacked layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Login window
        self.login_window = LoginWindow(self)
        self.central_widget.addWidget(self.login_window)
        
        self.show()
    
    def login_success(self, username, session):
        # Create and show dashboard
        self.dashboard = DashboardWindow(username, session, self)
        self.central_widget.addWidget(self.dashboard)
        self.central_widget.setCurrentWidget(self.dashboard)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

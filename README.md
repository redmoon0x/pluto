# Subject Feedback System

A Flask-based intranet application for collecting and managing student feedback for different subjects. Designed for easy deployment in college/university networks.

## Features

- **One feedback per computer**: Uses PC hostname to ensure one feedback per computer per subject
- **Excel-based storage**: All feedback stored in a single Excel file with separate sheets per subject
- **Secure admin access**: Password-protected admin dashboard with session management
- **Responsive design**: Works on all devices within the intranet
- **Easy deployment**: Minimal setup required for intranet deployment
- **Bulk download**: Download all feedback data in a single Excel file
- **Session tracking**: Maintains submission history across browser restarts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/subject-feedback-system.git
cd subject-feedback-system
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create configuration files:
   - Create `.env` file with admin password:
     ```
     ADMIN_PASSWORD=your_secure_password
     ```
   - Create `subjects.txt` with one subject per line:
     ```
     Subject 1
     Subject 2
     Subject 3
     ```

## Intranet Deployment Guide

### Windows (IIS)

1. Install IIS and WFASTCGI:
   ```bash
   # Install wfastcgi in your virtual environment
   pip install wfastcgi
   wfastcgi-enable
   ```

2. Create Web.config in project root:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <configuration>
     <system.webServer>
       <handlers>
         <add name="FlaskHandler" 
              path="*" 
              verb="*" 
              modules="FastCgiModule" 
              scriptProcessor="C:\Path\To\Your\venv\Scripts\python.exe|C:\Path\To\Your\venv\Lib\site-packages\wfastcgi.py"
              resourceType="Unspecified" />
       </handlers>
     </system.webServer>
     <appSettings>
       <add key="PYTHONPATH" value="C:\Path\To\Your\ProjectFolder" />
       <add key="WSGI_HANDLER" value="app.app" />
     </appSettings>
   </configuration>
   ```

3. Set folder permissions:
   - Give IIS_IUSRS read & execute permissions
   - Give write permission for feedback.xlsx location

### Linux (Apache)

1. Install Apache and mod_wsgi:
   ```bash
   sudo apt-get install apache2 libapache2-mod-wsgi-py3
   ```

2. Create WSGI file (wsgi.py):
   ```python
   import sys
   sys.path.insert(0, '/path/to/project')
   from app import app as application
   ```

3. Configure Apache virtual host:
   ```apache
   <VirtualHost *:80>
       ServerName your_server_name
       WSGIDaemonProcess feedback python-path=/path/to/project:/path/to/venv/lib/python3.x/site-packages
       WSGIProcessGroup feedback
       WSGIScriptAlias / /path/to/project/wsgi.py
       
       <Directory /path/to/project>
           Require all granted
       </Directory>
   </VirtualHost>
   ```

### Running for Development

```bash
# Run in development mode
python app.py

# Access the application
# Student interface: http://localhost:5000
# Admin interface: http://localhost:5000/admin
```

## Security Notes

1. Always change the default admin password in `.env`
2. Use HTTPS in production
3. Restrict network access to intranet only
4. Regular backup of feedback.xlsx
5. Monitor disk space for Excel file growth

## Project Structure

```
subject-feedback-system/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── subjects.txt       # List of subjects
├── .env              # Configuration file
├── feedback.xlsx     # Data storage (auto-created)
└── templates/        # HTML templates
    ├── admin.html
    ├── admin_dashboard.html
    ├── feedback_form.html
    ├── guidelines.html
    ├── index.html
    └── ...
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

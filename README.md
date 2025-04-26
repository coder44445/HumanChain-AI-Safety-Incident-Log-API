# AI Safety Incident Log Service

A simple RESTful API service for logging and managing AI safety incidents. This guide will help you set up and run the application step by step.

## Technology Stack
- **Language**: Python
- **Framework**: Flask
- **Database**: MySQL
- **ORM**: SQLAlchemy

## 🚀 Quick Start Guide

### Prerequisites
1. **Python 3.x**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation:
     ```bash
     python --version
     ```

2. **MySQL Server**
   - Download from [mysql.com](https://dev.mysql.com/downloads/installer/)
   - Choose "MySQL Installer for Windows"
   - During installation:
     - Remember your root password
     - Choose "Server only" or "Full" installation
     - Complete the installation wizard

### Installation Steps

1. **Clone and Setup Project**
   ```bash
   # Create project directory
   mkdir ai-safety-incidents
   cd ai-safety-incidents

   # Create and activate virtual environment
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Create `.env` file in project root
   - Add these configurations (replace the values with your own configuration):
     ```
     DB_USERNAME=<USER_NAME>
     DB_PASSWORD=<YOUR_MYSQL_PASSWROD>
     DB_HOST=localhost
     DB_NAME=<YOUR_DB_NAME>
     ```

4. **Populate Database (Optional)**
   - Run the populate script to add sample incidents:
     ```bash
     python populate_db.py
     ```
   - This will add 3 sample incidents to your database:
     1. AI Model Bias in Hiring System
     2. Chatbot Misinformation Incident
     3. Data Privacy Breach in AI Training

5. **Start the Application**
   ```bash
   flask run
   ```
   The server will start at: http://127.0.0.1:5000

## 📚 API Documentation

### Endpoints

1. **Get All Incidents**
   ```bash
   curl http://localhost:5000/incidents
   ```
   - Method: GET
   - URL: `/incidents`
   - Response: List of all incidents

2. **Log a New Incident**
   ```bash
   curl -X POST http://localhost:5000/incidents \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Incident", "description": "This is a test", "severity": "Medium"}'
   ```
   - Method: POST
   - URL: `/incidents`
   - Body: JSON with title, description, and severity
   - Severity options: Low, Medium, High

3. **Get Single Incident**
   ```bash
   curl http://localhost:5000/incidents/1
   ```
   - Method: GET
   - URL: `/incidents/{id}`
   - Response: Incident details or 404 if not found

4. **Delete Incident**
   ```bash
   curl -X DELETE http://localhost:5000/incidents/1
   ```
   - Method: DELETE
   - URL: `/incidents/{id}`
   - Response: 204 No Content or 404 if not found

## 🆘 Troubleshooting

1. **MySQL Connection Issues**
   - Verify MySQL server is running
   - Check credentials in `.env` file
   - Ensure MySQL server is accessible

2. **Application Errors**
   - Check error messages in terminal
   - Verify all installation steps
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` if modules are missing

3. **Port Conflicts**
   - Change port in `app.py`:
     ```python
     app.run(debug=True, port=5001)
     ```

## Design Decisions

1. **Database Auto-Creation**
   - Application automatically creates database if missing
   - Simplifies setup process for users
   - Reduces manual configuration steps

2. **Sample Data**
   - Includes populate_db.py script for quick testing
   - Provides realistic sample incidents
   - Helps users understand the data structure

3. **Simple Architecture**
   - Focus on core REST API functionality
   - Clear separation of concerns
   - Easy to understand and maintain

4. **Error Handling**
   - Comprehensive error handling
   - Clear error messages
   - Proper HTTP status codes

## 📞 Support

For additional help:
1. Check terminal error messages
2. Verify installation steps
3. Ensure MySQL is running
4. Review `.env` configuration 
class DatabaseConnection:
    def connect(self):
        return "Database connected"
    
    def query(self, sql):
        if not sql:
            raise ValueError("SQL query cannot be empty")
        return f"Executing: {sql}"
    
    def disconnect(self):
        return "Database disconnected"

class FileLogger:
    def write_log(self, message):
        if not message:
            raise ValueError("Log message cannot be empty")
        return f"Log written: {message}"

class EmailService:
    def send_notification(self, email, subject):
        if not email or not subject:
            raise ValueError("Email and subject are required")
        return f"Email sent to {email}: {subject}"

class ReportGenerator:
    def __init__(self):
        self.db = DatabaseConnection()
        self.logger = FileLogger()
        self.email = EmailService()
    
    def generate_monthly_report(self, recipient_email):
        try:
            self.db.connect()
            data = self.db.query("SELECT * FROM sales WHERE month = CURRENT_MONTH")
            report = f"Monthly Report Data: {data}"
            
            self.logger.write_log(f"Monthly report generated for {recipient_email}")
            self.email.send_notification(recipient_email, "Monthly Sales Report")
            
            self.db.disconnect()
            return f"Report successfully generated and sent to {recipient_email}"
        except ValueError as e:
            self.logger.write_log(f"Error generating report: {e}")
            return f"Report generation failed: {e}"

if __name__ == "__main__":
    report_system = ReportGenerator()
    
    result = report_system.generate_monthly_report("manager@company.com")
    print(result)
    
    error_result = report_system.generate_monthly_report("")
    print(error_result)
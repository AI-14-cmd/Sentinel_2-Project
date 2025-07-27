# Sentinel_2 Project/Anni_code.py

import os
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static", "sentinel_output"))
os.makedirs(output_dir, exist_ok=True)
dense_forest_pct = 80.0 # approx
light_forest_pct = 19.5 # approx
deforested_pct = 3  # approx

# Email configuration - UPDATE THESE WITH YOUR ACTUAL VALUES
EMAIL_SENDER = "aniruddhneje@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "qqfl vyzl bfpd plsz"  # Your 16-character Gmail App Password
EMAIL_RECIPIENT = "nejeaniruddh@gmail.com"  # Where you want to receive the report
EMAIL_SUBJECT = "Sentinel-2 Forest Analysis Report"

# Load Sentinel-2 bands
# This version uses only simulated data and never references any real file paths or the P:/ drive.
def load_bands():
    try:
        # Simulated data for demonstration (always used, never any file I/O)
        band_red = np.random.random((1000, 1000))  # Simulated Red band
        band_nir = np.random.random((1000, 1000))  # Simulated NIR band

        logger.info(f"Shape of band_red: {band_red.shape}")
        logger.info(f"Shape of band_nir: {band_nir.shape}")
        return band_red, band_nir
    except Exception as e:
        logger.error(f"Error loading bands: {str(e)}")
        raise

# Calculate NDVI
def calculate_ndvi(red, nir):
    try:
        # Avoid division by zero
        denominator = red + nir
        mask = denominator > 0
        
        # Initialize NDVI array with zeros
        ndvi = np.zeros_like(red)
        
        # Calculate NDVI only where denominator > 0
        ndvi[mask] = (nir[mask] - red[mask]) / denominator[mask]
        
        return ndvi
    except Exception as e:
        logger.error(f"Error calculating NDVI: {str(e)}")
        raise

# Classify forest cover using predefined percentages
def classify_forest(ndvi):
    try:
        # Count total valid pixels
        total_valid = np.sum(~np.isnan(ndvi))
        
        # Calculate pixel counts based on predefined percentages
        dense_count = int(total_valid * dense_forest_pct / 100)
        light_count = int(total_valid * light_forest_pct / 100)
        deforested_count = int(total_valid * deforested_pct / 100)
        
        # Ensure the total adds up exactly to total_valid by adjusting dense_count
        adjustment = total_valid - (dense_count + light_count + deforested_count)
        dense_count += adjustment
        
        logger.info(f"Total valid pixels in NDVI data: {total_valid}")
        logger.info(f"Dense forest pixels: {dense_count} ({dense_forest_pct}%)")
        logger.info(f"Light forest pixels: {light_count} ({light_forest_pct}%)")
        logger.info(f"Deforested pixels: {deforested_count} ({deforested_pct}%)")
        
        return {
            'dense_forest': dense_count,
            'light_forest': light_count,
            'deforested': deforested_count,
            'total': total_valid
        }
    except Exception as e:
        logger.error(f"Error classifying forest: {str(e)}")
        raise

# Generate report
def generate_report(classification):
    try:
        report_path = os.path.join(output_dir, "forest_analysis.txt")
        
        with open(report_path, 'w') as f:
            f.write("Sentinel-2 Forest Cover Analysis Report\n")
            f.write("======================================\n\n")
            
            f.write(f"Total analyzed area: {classification['total']} pixels\n\n")
            
            f.write("Forest Classification:\n")
            f.write(f"- Dense Forest: {classification['dense_forest']} pixels ")
            f.write(f"({dense_forest_pct}%)\n")
            
            f.write(f"- Light Forest: {classification['light_forest']} pixels ")
            f.write(f"({light_forest_pct}%)\n")
            
            f.write(f"- Deforested: {classification['deforested']} pixels ")
            f.write(f"({deforested_pct}%)\n")
        
        logger.info(f"Report generated: {report_path}")
        return report_path
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise

# Create visualization
def create_visualization(classification):
    try:
        chart_path = os.path.join(output_dir, "forest_classification.png")
        
        # Create pie chart
        labels = ['Dense Forest', 'Light Forest', 'Deforested']
        sizes = [dense_forest_pct, light_forest_pct, deforested_pct]  # Use predefined percentages
        colors = ['darkgreen', 'lightgreen', 'brown']
        explode = (0, 0, 0.1)  # explode the deforested slice
        
        plt.figure(figsize=(10, 7))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Forest Cover Classification')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Pie chart saved successfully!")
        return chart_path
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        raise

# Test basic email connectivity
def test_email_connection():
    try:
        logger.info(f"Testing email connection from {EMAIL_SENDER} to {EMAIL_RECIPIENT}")
        
        # Create a simple message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = "Test Email Connection"
        
        # Simple body
        msg.attach(MIMEText("This is a test email to verify SMTP connection.", 'plain'))
        
        # Connect to Gmail's SMTP server
        logger.info("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        
        # Login to account
        logger.info(f"Logging in as {EMAIL_SENDER}...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Send email
        logger.info("Sending test email...")
        server.send_message(msg)
        
        # Close connection
        server.quit()
        
        logger.info("Test email sent successfully!")
        return True
    except Exception as e:
        logger.error(f"Error sending test email: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# Send email with report and visualization
def send_email(report_path, chart_path):
    try:
        logger.info(f"Preparing to send email from {EMAIL_SENDER} to {EMAIL_RECIPIENT}")

        # Check if files exist and log their sizes
        max_size = 20 * 1024 * 1024  # 20 MB
        for file_path, label in [(report_path, 'Report'), (chart_path, 'Chart')]:
            if not os.path.exists(file_path):
                logger.error(f"{label} file does not exist: {file_path}")
                return
            size = os.path.getsize(file_path)
            logger.info(f"{label} file size: {size / 1024:.2f} KB")
            if size > max_size:
                logger.error(f"{label} file is too large to send via email: {size / (1024*1024):.2f} MB")
                return

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = EMAIL_SUBJECT

        # Email body
        body = """
Hello,

Attached is the latest Sentinel-2 forest cover analysis report and visualization.

Best regards,
Forest Monitoring System
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach report file
        logger.info(f"Attaching report: {report_path}")
        with open(report_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(report_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
            msg.attach(part)

        # Attach chart
        logger.info(f"Attaching chart: {chart_path}")
        with open(chart_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(chart_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(chart_path)}"'
            msg.attach(part)

        # Connect to Gmail's SMTP server - trying multiple methods
        try:
            # Method 1: SMTP_SSL (preferred for Gmail)
            logger.info("Connecting to Gmail SMTP server using SSL...")
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
            logger.info(f"Logging in as {EMAIL_SENDER}...")
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            logger.info("Sending email...")
            server.send_message(msg)
            server.quit()
            logger.info("Email sent successfully using SSL!")
        except Exception as ssl_error:
            logger.warning(f"SSL method failed: {str(ssl_error)}")
            logger.info("Trying alternative method with STARTTLS...")
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            logger.info("Email sent successfully using STARTTLS!")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# Main function
def main():
    try:
        # Test email connection first
        if not test_email_connection():
            logger.warning("Email test failed. Continuing with processing but email may not be sent.")
        
        # Load bands
        band_red, band_nir = load_bands()
        
        # Calculate NDVI
        ndvi = calculate_ndvi(band_red, band_nir)
        
        # Classify forest using predefined percentages
        classification = classify_forest(ndvi)
        
        # Generate report
        report_path = generate_report(classification)
        
        # Create visualization
        chart_path = create_visualization(classification)
        
        # Send email
        send_email(report_path, chart_path)
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import sys
import logging
import threading
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Store the latest process results
latest_results = {
    "status": "idle",
    "messages": [],
    "report_path": "static/sentinel_output/forest_analysis.txt",
    "chart_path": "static/sentinel_output/forest_classification.png",
    "timestamp": None,
    "email_sent": False
}

def clear_results():
    """Reset the results to default state"""
    latest_results.update({
        "status": "idle",
        "messages": [],
        "timestamp": None,
        "email_sent": False
    })

def send_mock_email():
    """Simulate sending an email"""
    time.sleep(2)  # Simulate email delay
    latest_results["messages"].append("✅ Email sent successfully!")
    latest_results["email_sent"] = True

def run_sentinel_analysis():
    """Run the Sentinel-2 analysis in a separate thread"""
    try:
        latest_results["status"] = "running"
        latest_results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_results["messages"].append("Starting Sentinel-2 forest analysis...")

        # Import the main script - this is your existing Anni_code.py
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        import Anni_code

        # Run the main function from Anni_code
        latest_results["messages"].append("Loading and processing Sentinel-2 bands...")
        band_red, band_nir = Anni_code.load_bands()
        
        latest_results["messages"].append("Calculating NDVI...")
        ndvi = Anni_code.calculate_ndvi(band_red, band_nir)
        
        latest_results["messages"].append("Classifying forest cover...")
        classification = Anni_code.classify_forest(ndvi)
        
        latest_results["messages"].append("Generating report...")
        report_path = Anni_code.generate_report(classification)
        
        latest_results["messages"].append("Creating visualization...")
        chart_path = Anni_code.create_visualization(classification)
        
        latest_results["messages"].append("Sending email report...")
        Anni_code.send_email(report_path, chart_path)

        latest_results["status"] = "completed"
        latest_results["messages"].append("✅ Process completed successfully!")
        latest_results["email_sent"] = True

    except Exception as e:
        latest_results["status"] = "error"
        latest_results["messages"].append(f"❌ Error: {str(e)}")
        logger.error(f"Error running analysis: {str(e)}", exc_info=True)


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/run-analysis', methods=['POST'])
def start_analysis():
    """Start the analysis process"""
    clear_results()
    
    # Start analysis in a background thread
    thread = threading.Thread(target=run_sentinel_analysis)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/status')
def get_status():
    """Get the current status of the analysis"""
    return jsonify(latest_results)

@app.route('/report')
def get_report():
    """Get the content of the report file"""
    report_path = os.path.join(app.root_path, latest_results["report_path"])
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            content = f.read()
        return jsonify({"content": content})
    return jsonify({"content": "Report not available"})

@app.route('/chart')
def get_chart():
    """Get the latest chart filename"""
    chart_path = os.path.join(app.root_path, latest_results["chart_path"])
    if os.path.exists(chart_path):
        return jsonify({"filename": os.path.basename(latest_results["chart_path"])})
    return jsonify({"error": "Chart not available"})

@app.route('/static/sentinel_output/<path:filename>')
def serve_sentinel_output(filename):
    """Serve files from sentinel_output directory"""
    return send_from_directory(os.path.join(app.root_path, 'static', 'sentinel_output'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

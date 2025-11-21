# Sentinel-2 Forest Analysis for Environmental Monitoring

## Project Overview

This project provides a comprehensive solution for monitoring deforestation and forest health using Sentinel-2 satellite imagery. It is a powerful tool for environmental agencies, researchers, and land managers to track changes in forest cover over time.

The system is designed to be accessible to both technical and non-technical users, offering both a simple web interface and a command-line tool for advanced users.

The core of the project is a sophisticated analysis pipeline that processes satellite data to identify and quantify forest areas. The results are delivered in a clear and concise report, complete with a visual map of the analyzed region, which is also sent to the user via email for convenience.

## Technology Stack

This project leverages a modern stack of technologies for data processing, analysis, and presentation:

*   **Backend:** Python
*   **Web Framework:** Flask
*   **Satellite Data Provider:** Google Earth Engine
*   **Geospatial Analysis:** Rasterio, NumPy
*   **Data Visualization:** Matplotlib
*   **Frontend:** HTML, CSS, JavaScript

## Key Features & Modules

*   **Automated Data Retrieval:** The system automatically fetches the latest Sentinel-2 satellite data from Google Earth Engine for any specified area of interest.
*   **Advanced Image Analysis:** It calculates the Normalized Difference Vegetation Index (NDVI), a key indicator of plant health, to classify the landscape into "Forest" and "Non-Forest" areas.
*   **Comprehensive Reporting:** A detailed report is generated that quantifies the total area of forest cover in square kilometers and as a percentage of the total area.
*   **Visual Mapping:** A high-quality map is produced, visually representing the classified forest and non-forest areas, making it easy to understand the results at a glance.
*   **Email Notifications:** The complete analysis, including the report and the visual map, is automatically sent to a specified email address, ensuring that stakeholders are always up-to-date.
*   **User-Friendly Web Interface:** A simple and intuitive web application allows users to easily define their area of interest and run the analysis with the click of a button.
*   **Command-Line Interface:** For power users and for integration into automated workflows, a command-line interface is available to run the analysis.

## Workflow

The project follows a simple yet powerful workflow:

1.  **Define Area of Interest:** The user specifies the geographical area to be analyzed, either through the web interface or as coordinates in the command-line tool.
2.  **Data Acquisition:** The system queries Google Earth Engine to download the relevant Sentinel-2 satellite images for the specified area and date range.
3.  **NDVI Calculation:** The raw satellite data is processed to calculate the NDVI for each pixel in the image.
4.  **Forest Classification:** Based on the calculated NDVI values, the system classifies each pixel as either "Forest" or "Non-Forest".
5.  **Report Generation:** A summary report is generated with key statistics on forest cover.
6.  **Visualization:** A map is created to visually represent the results of the classification.
7.  **Email Delivery:** The report and the map are sent to the user's email address.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/AI-14-cmd/Sentinel_2-Project.git
    cd Sentinel_2-Project
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. You will also need to authenticate with Google Earth Engine. You can use the `authenticate_gee.py` script for this, or follow the instructions at [https://developers.google.com/earth-engine/guides/python_install#authentication](https://developers.google.com/earth-engine/guides/python_install#authentication) to set up your credentials.

## Usage

You can run the analysis using either the command-line interface or the web application.

### Command-Line Interface

To run the analysis from the command line, execute the `main.py` script:

```bash
python main.py
```

The script will prompt you to enter the coordinates for the area of interest and the date range.

### Web Application

To use the web interface, start the Flask application:

```bash
python app.py
```

Then, open your web browser and navigate to `http://127.0.0.1:5000`. From the web page, you can start the analysis and view the results.

## Project Structure

*   `main.py`: The command-line entry point for the analysis.
*   `app.py`: The Flask web application.
*   `Anni_code.py`: Core functions for the analysis.
*   `gee_data_loader.py`: Functions for loading data from Google Earth Engine.
*   `area_selector.py`: Functions for getting user input for the area of interest.
*   `authenticate_gee.py`: Script to authenticate with Google Earth Engine.
*   `show_results.py`: Script to display the analysis results.
*   `Sentinel_2 web page/`: Contains an additional web application.
*   `Sentinel_api/`: Scripts and notebooks for interacting with the Sentinel API.
*   `requirements.txt`: The list of Python dependencies.
*   `templates/index.html`: The main HTML page for the web application.
*   `static/`: Static files for the web application (CSS, JS, images).
*   `sentinel_output/`: The directory where the output reports and charts are saved.
*   `S2B_MSIL2A_20250212T052839_N0511_R105_T43PCT_20250212T073349.SAFE/`: Example Sentinel-2 data.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
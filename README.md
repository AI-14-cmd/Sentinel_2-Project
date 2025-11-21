# Sentinel-2 Forest Analysis

This project analyzes Sentinel-2 satellite data to perform forest classification. It calculates the Normalized Difference Vegetation Index (NDVI) to classify forest cover, generates a report and a visualization of the results, and can be run both as a command-line tool and as a web application.

## Features

*   **Data Loading**: Loads Sentinel-2 bands from Google Earth Engine.
*   **NDVI Calculation**: Computes NDVI from the red and near-infrared bands.
*   **Forest Classification**: Classifies the area into forest and non-forest based on the NDVI values.
*   **Reporting**: Generates a text-based report of the analysis.
*   **Visualization**: Creates a PNG image visualizing the forest classification.
*   **Email Notification**: Sends an email with the report and visualization.
*   **Web Interface**: A Flask web application to run the analysis and view the results.
*   **Command-Line Interface**: A command-line script to run the analysis.

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

3. You will also need to authenticate with Google Earth Engine. Follow the instructions at [https://developers.google.com/earth-engine/guides/python_install#authentication](https://developers.google.com/earth-engine/guides/python_install#authentication) to set up your credentials.

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
*   `requirements.txt`: The list of Python dependencies.
*   `templates/index.html`: The main HTML page for the web application.
*   `static/`: Static files for the web application (CSS, JS, images).
*   `sentinel_output/`: The directory where the output reports and charts are saved.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License.
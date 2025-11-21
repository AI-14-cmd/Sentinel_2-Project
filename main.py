from Anni_code import *
from gee_data_loader import initialize_gee
from area_selector import get_coordinates_from_user, get_date_range

def main():
    # Get area and dates from user
    print("Select your area of interest...")
    LATITUDE, LONGITUDE = get_coordinates_from_user()
    START_DATE, END_DATE = get_date_range()
    
    print(f"Analyzing area: {LATITUDE}, {LONGITUDE}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    
    # Initialize Google Earth Engine and load data
    initialize_gee()
    red, nir = load_bands_gee(LATITUDE, LONGITUDE, START_DATE, END_DATE)
    
    # Calculate NDVI
    ndvi = calculate_ndvi(red, nir)
    
    # Classify forest
    classification = classify_forest(ndvi)
    
    # Generate outputs
    report_path = generate_report(classification)
    chart_path = create_visualization(classification)
    
    # Send email
    send_email(report_path, chart_path)
    
    # Show results
    from show_results import show_results
    show_results()
    
    print("Forest analysis completed!")

if __name__ == "__main__":
    main()
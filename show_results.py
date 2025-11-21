import os
import webbrowser
from PIL import Image
import matplotlib.pyplot as plt

def show_results():
    """Display analysis results"""
    
    output_dir = os.path.join(os.path.dirname(__file__), "static", "sentinel_output")
    report_path = os.path.join(output_dir, "forest_analysis.txt")
    chart_path = os.path.join(output_dir, "forest_classification.png")
    
    # Show text report
    if os.path.exists(report_path):
        print("\n" + "="*50)
        print("FOREST ANALYSIS REPORT")
        print("="*50)
        with open(report_path, 'r') as f:
            print(f.read())
    
    # Show chart
    if os.path.exists(chart_path):
        print(f"\nOpening chart: {chart_path}")
        
        # Try to open with default image viewer
        try:
            if os.name == 'nt':  # Windows
                os.startfile(chart_path)
            else:  # Mac/Linux
                webbrowser.open(f'file://{chart_path}')
        except:
            print("Could not open image automatically. Please check:")
            print(f"Chart saved at: {chart_path}")
    
    print(f"\nFiles saved in: {output_dir}")

if __name__ == "__main__":
    show_results()
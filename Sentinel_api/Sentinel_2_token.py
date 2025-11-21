import requests
import json

# Define the Sentinel Hub API URL
API_URL = "https://sh.dataspace.copernicus.eu/api/v1/process"

# Your access token
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVUh3VWZKaHVDVWo0X3k4ZF8xM0hxWXBYMFdwdDd2anhob2FPLUxzREZFIn0.eyJleHAiOjE3NDA3MTk0NDYsImlhdCI6MTc0MDcxODg0NiwianRpIjoiNDc2ZmY3MGItZmJhYi00OTRhLWJkNzctZjg3YzA2NDEwMDBlIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5kYXRhc3BhY2UuY29wZXJuaWN1cy5ldS9hdXRoL3JlYWxtcy9DRFNFIiwic3ViIjoiY2FhN2RhYzMtYmEzZC00ZTBlLTk0ZTMtOTQzMjI4NzVjMzkwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2gtNmQ1MWY3ZmYtMjBiNC00ODUxLWEwZmItMjQ1MTIzYTI3NjBjIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIHVzZXItY29udGV4dCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjE1Mi41OC4xOTUuMTIwIiwib3JnYW5pemF0aW9ucyI6WyJkZWZhdWx0LTRhNWI4ZTFkLTc3NzUtNDdjMC1iMmQ2LWM3NzVjZjkzM2ZhMCJdLCJ1c2VyX2NvbnRleHRfaWQiOiJiNzJkMzE0Yi1iMzIyLTQ1ODctYjAyMC0zNGZlZjM0ZjU0ZDMiLCJjb250ZXh0X3JvbGVzIjp7fSwiY29udGV4dF9ncm91cHMiOlsiL2FjY2Vzc19ncm91cHMvdXNlcl90eXBvbG9neS9jb3Blcm5pY3VzX2dlbmVyYWwvIiwiL29yZ2FuaXphdGlvbnMvZGVmYXVsdC00YTViOGUxZC03Nzc1LTQ3YzAtYjJkNi1jNzc1Y2Y5MzNmYTAvIl0sInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1zaC02ZDUxZjdmZi0yMGI0LTQ4NTEtYTBmYi0yNDUxMjNhMjc2MGMiLCJ1c2VyX2NvbnRleHQiOiJkZWZhdWx0LTRhNWI4ZTFkLTc3NzUtNDdjMC1iMmQ2LWM3NzVjZjkzM2ZhMCIsImNsaWVudEFkZHJlc3MiOiIxNTIuNTguMTk1LjEyMCIsImNsaWVudF9pZCI6InNoLTZkNTFmN2ZmLTIwYjQtNDg1MS1hMGZiLTI0NTEyM2EyNzYwYyJ9.ZQr62-9xj9MvLW5CULk4UZCT3tGo_ITpBarG4LtmiTkPSS6UcAbQ-25B_kVaPf-YGpoeuHY8hSzZl_7y21Ik0ipCuR8xNi1TqW9SvaXZL74jIEp3-_3fmqKYc_whV_y5zbBALBHmjdkt0lhJRMxLTgegIVfWGfnRDSzrE60rTANWZB3obWUh4nhd4dc2KlArIlF2WBjiVz0vHIbFTlXUNK3TN0dap5QpZ-i1atDFZ0QlWm-ZOgarnCFESo60E9DvSTrEZMcTER1BDkOn6_3aHDUlteBWjsZ8mizP5kgmdtxgKB1t9-Zto8htMKKU0mCX26CeckKn4YK2lYrXmay8rA"
# Define the evalscript (returns a true-color RGB image)
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B08", "B04"], // NIR and Red bands
    output: {
      id: "default",
      bands: 1,
      sampleType: "FLOAT32"
    }
  };
}

function evaluatePixel(sample) {
  let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04 + 0.0001);
  return [ndvi]; // Returns NDVI values
}
"""

# Define the request payload
payload = {
    "input": {
        "bounds": {
            "bbox": [8682920.28, 2875744.62, 8694052.23, 2888032.38],  # Update with actual coordinates
            "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/3857"} 
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2024-01-01T00:00:00Z",
                        "to": "2024-02-01T00:00:00Z"
                    },
                    "maxCloudCoverage": 20
                }
            }
        ]
    },
    "output": {
        "width": 512,
        "height": 512,
        "responses": [
            {"identifier": "default", "format": {"type": "image/tiff"}}
        ]
    },
    "evalscript": evalscript
}


# Send the request
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(API_URL, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    with open("sentinel_image.png", "wb") as f:
        f.write(response.content)
    print("✅ Image downloaded successfully: sentinel_image.png")
else:
    print("❌ Failed to fetch image:", response.text)

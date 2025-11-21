import requests

# Your access token
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVUh3VWZKaHVDVWo0X3k4ZF8xM0hxWXBYMFdwdDd2anhob2FPLUxzREZFIn0.eyJleHAiOjE3NDA3MTMwNjQsImlhdCI6MTc0MDcxMjQ2NCwianRpIjoiYWI0OTk0NDUtOTI2MC00M2RiLTgyOWMtNGI3MGZkZWNmYmU4IiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5kYXRhc3BhY2UuY29wZXJuaWN1cy5ldS9hdXRoL3JlYWxtcy9DRFNFIiwic3ViIjoiY2FhN2RhYzMtYmEzZC00ZTBlLTk0ZTMtOTQzMjI4NzVjMzkwIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2gtNmQ1MWY3ZmYtMjBiNC00ODUxLWEwZmItMjQ1MTIzYTI3NjBjIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIHVzZXItY29udGV4dCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjQ5LjQzLjI0MC4yMTkiLCJvcmdhbml6YXRpb25zIjpbImRlZmF1bHQtNGE1YjhlMWQtNzc3NS00N2MwLWIyZDYtYzc3NWNmOTMzZmEwIl0sInVzZXJfY29udGV4dF9pZCI6ImI3MmQzMTRiLWIzMjItNDU4Ny1iMDIwLTM0ZmVmMzRmNTRkMyIsImNvbnRleHRfcm9sZXMiOnt9LCJjb250ZXh0X2dyb3VwcyI6WyIvYWNjZXNzX2dyb3Vwcy91c2VyX3R5cG9sb2d5L2NvcGVybmljdXNfZ2VuZXJhbC8iLCIvb3JnYW5pemF0aW9ucy9kZWZhdWx0LTRhNWI4ZTFkLTc3NzUtNDdjMC1iMmQ2LWM3NzVjZjkzM2ZhMC8iXSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LXNoLTZkNTFmN2ZmLTIwYjQtNDg1MS1hMGZiLTI0NTEyM2EyNzYwYyIsInVzZXJfY29udGV4dCI6ImRlZmF1bHQtNGE1YjhlMWQtNzc3NS00N2MwLWIyZDYtYzc3NWNmOTMzZmEwIiwiY2xpZW50QWRkcmVzcyI6IjQ5LjQzLjI0MC4yMTkiLCJjbGllbnRfaWQiOiJzaC02ZDUxZjdmZi0yMGI0LTQ4NTEtYTBmYi0yNDUxMjNhMjc2MGMifQ.W1F9JavSyNsfgvTbdHV8B0la0h4eYyU7ysHjUoRjlSZe_XHfzIK29wPE7gOekPzTguiUvGOv-WtrV98iPl35bPF70P6R4W1broACR86iUqU7-BmUbfVv0sc76UFcxC3WVBPh2jKPMxVbZOTKihHAzzSQhMxi1tPXWqoNtEvt1r5SvNFY8_DEgNS2eFyly4QH1BzXyenGvMaVrPDxnrxhAUEP9k8ATzpBBOl6GWh0mFCbQne1zWM_8ILl1wp0_nBPIFri-AsE07ioewDQ95AatULPJRUDQomK3N4sdGbSbwxL7cKLIaXRqKAtPOTtA02L5bjt10OZLPp0WXgesHuW4g"
# Define the evalscript (returns a true-color RGB image)
url = "https://services.sentinel-hub.com/api/v1/process"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
payload = {
    "input": {
        "bounds": {
            "bbox" : [74.25, 15.45, 74.45, 15.64],  # Adjust your bounding box
            "crs": "EPSG:4326"
        },
        "data": [
            {
                "type": "S2L2A",  # Sentinel-2 Level 2A
                "dataFilter": {"timeRange": {"from": "2024-01-01", "to": "2024-02-01"}}
            }
        ]
    },
    "output": {
        "width": 512,
        "height": 512,
        "responses": [{"identifier": "default", "format": {"type": "image/png"}}]
    }
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    with open("sentinel_image.png", "wb") as file:
        file.write(response.content)
    print("✅ Image downloaded successfully: sentinel_image.png")
else:
    print(f"❌ Error: {response.text}")

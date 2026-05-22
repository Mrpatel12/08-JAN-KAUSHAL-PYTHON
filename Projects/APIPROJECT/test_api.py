import requests
import json

BASE_URL = "http://127.0.0.1:8000/"

def test_crud():
    # 1. POST - Create Data
    print("Testing POST...")
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "city": "NY"
    }
    response = requests.post(f"{BASE_URL}postdata/", json=data)
    print(f"POST Response: {response.status_code}, {response.json()}")
    
    if response.status_code == 201:
        obj_id = response.json().get('id')
        
        # 2. GET ALL
        print("\nTesting GET ALL...")
        response = requests.get(f"{BASE_URL}getall/")
        print(f"GET ALL Response: {response.status_code}, Found {len(response.json())} items")

        # 3. GET SINGLE
        print(f"\nTesting GET SINGLE (ID: {obj_id})...")
        response = requests.get(f"{BASE_URL}getsingle/{obj_id}/")
        print(f"GET SINGLE Response: {response.status_code}, {response.json()}")

        # 4. UPDATE (PUT)
        print(f"\nTesting UPDATE (ID: {obj_id})...")
        update_data = {"name": "John Updated", "email": "john@example.com", "city": "LA"}
        response = requests.put(f"{BASE_URL}updatedata/{obj_id}/", json=update_data)
        print(f"UPDATE Response: {response.status_code}, {response.json()}")

        # 5. DELETE
        print(f"\nTesting DELETE (ID: {obj_id})...")
        response = requests.delete(f"{BASE_URL}deletedata/{obj_id}/")
        print(f"DELETE Response: {response.status_code}")

if __name__ == "__main__":
    try:
        test_crud()
    except Exception as e:
        print(f"Error: {e}. Is your server running at {BASE_URL}?")

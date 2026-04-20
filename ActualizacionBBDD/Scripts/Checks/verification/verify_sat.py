import requests

def verify():
    try:
        r = requests.get('http://localhost:8000/api/v1/satellites')
        r.raise_for_status()
        data = r.json()
        print(f"Total satellites: {len(data)}")
        for s in data:
            name = s.get('name')
            desc_en = s.get('description_en')
            print(f"- {name}: {'OK' if desc_en else 'MISSING EN'}")
            if desc_en:
                print(f"  EN: {desc_en[:100]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify()

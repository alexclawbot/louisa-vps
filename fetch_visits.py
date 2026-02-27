import json
import sqlite3
import urllib.request
import time

API_BASE = "https://api.1503.affinect.prsl.cc"
API_KEY = "Lca5c8M1H0I13BHQBO9etE4hKDQZSvWNmyqBqvFdbyGO2y5aCvvtLw9vkjygHgtI"
TOTAL_PAGES = 165

def fetch_page(page_num):
    url = f"{API_BASE}/organization/v1/visits?page={page_num}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def main():
    print("📥 Fetching all visits from Affinect API...")
    print(f"Total pages: {TOTAL_PAGES}")
    print()
    
    # First, load contacts from DB to get gender mapping
    print("📇 Loading contacts from database...")
    conn = sqlite3.connect('affinect_contacts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, gender FROM contacts')
    contacts = {row[0]: {'name': row[1], 'gender': row[2]} for row in cursor.fetchall()}
    print(f"   Loaded {len(contacts):,} contacts")
    print()
    
    # Visit counts by contact_id
    visit_counts = {}
    last_visit_2025 = {}
    
    for page in range(1, TOTAL_PAGES + 1):
        try:
            data = fetch_page(page)
            items = data['data']['items']
            
            for visit in items:
                contact_id = visit['contact']['id']
                visit_datetime = visit['datetime']
                
                # Count visits
                visit_counts[contact_id] = visit_counts.get(contact_id, 0) + 1
                
                # Track last visit in 2025
                if visit_datetime.startswith('2025'):
                    if contact_id not in last_visit_2025 or visit_datetime > last_visit_2025[contact_id]:
                        last_visit_2025[contact_id] = visit_datetime
            
            if page % 20 == 0:
                print(f"✓ Page {page:3d}/{TOTAL_PAGES} (total visits: {sum(visit_counts.values()):6,})")
            time.sleep(0.05)
        except Exception as e:
            print(f"✗ Page {page} failed: {e}")
    
    print()
    print(f"✅ Total visits processed: {sum(visit_counts.values()):,}")
    print(f"   Unique contacts with visits: {len(visit_counts):,}")
    
    # Find men with >10 visits who visited in 2025
    print("\n🔍 Analyzing: Men with >10 visits in 2025...")
    
    results = []
    for contact_id, count in visit_counts.items():
        if count > 10 and contact_id in last_visit_2025 and contact_id in contacts:
            contact = contacts[contact_id]
            if contact['gender'] == 'Male':
                results.append({
                    'id': contact_id,
                    'name': contact['name'],
                    'visits': count,
                    'last_visit_2025': last_visit_2025[contact_id]
                })
    
    results.sort(key=lambda x: x['visits'], reverse=True)
    
    print(f"\n👨 Found {len(results)} men with >10 visits in 2025\n")
    
    # Save to CSV for easy export
    import csv
    with open('men_vip_2025.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Contact ID', 'Visits in 2025', 'Last Visit 2025'])
        for r in results:
            writer.writerow([r['name'], r['id'], r['visits'], r['last_visit_2025']])
    
    print(f"💾 Saved to: men_vip_2025.csv")
    print()
    
    # Display top results
    print(f"{'#':<4} {'Name':<35} {'Visits':<8} {'Last Visit 2025':<20}")
    print("-" * 75)
    for i, r in enumerate(results[:50], 1):
        last_visit = r['last_visit_2025'][:10] if r['last_visit_2025'] else 'N/A'
        print(f"{i:<4} {r['name']:<35} {r['visits']:<8} {last_visit:<20}")
    
    if len(results) > 50:
        print(f"\n... and {len(results) - 50} more")
    
    conn.close()
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()

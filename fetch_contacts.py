import json
import sqlite3
import urllib.request
import time

API_BASE = "https://api.1503.affinect.prsl.cc"
API_KEY = "Lca5c8M1H0I13BHQBO9etE4hKDQZSvWNmyqBqvFdbyGO2y5aCvvtLw9vkjygHgtI"
TOTAL_PAGES = 92

def fetch_page(page_num):
    url = f"{API_BASE}/organization/v1/contact-database?page={page_num}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def main():
    print("📥 Fetching all contacts from Affinect API...")
    print(f"Total pages: {TOTAL_PAGES}")
    print()
    
    all_contacts = []
    
    for page in range(1, TOTAL_PAGES + 1):
        try:
            data = fetch_page(page)
            items = data['data']['items']
            all_contacts.extend(items)
            print(f"✓ Page {page:3d}/{TOTAL_PAGES} - {len(items):3d} contacts (total: {len(all_contacts):5d})")
            time.sleep(0.05)
        except Exception as e:
            print(f"✗ Page {page} failed: {e}")
    
    print()
    print(f"✅ Total contacts fetched: {len(all_contacts)}")
    
    print("\n💾 Creating SQLite database...")
    conn = sqlite3.connect('affinect_contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''DROP TABLE IF EXISTS contacts''')
    cursor.execute('''
        CREATE TABLE contacts (
            id TEXT PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            full_name TEXT,
            gender TEXT,
            birth_day INTEGER,
            birth_month INTEGER,
            birth_year INTEGER,
            age INTEGER,
            email TEXT,
            phone TEXT,
            nationality TEXT,
            status TEXT,
            first_visit_datetime TEXT,
            first_visit_venue TEXT,
            last_visit_datetime TEXT,
            last_visit_venue TEXT,
            excluded_channels TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    for c in all_contacts:
        dob = c.get('date_of_birth') or {}
        first_visit = c.get('first_visit') or {}
        last_visit = c.get('last_visit') or {}
        excluded = c.get('excluded_channels') or []
        
        # Venue is a dict, not array
        fv_venue = first_visit.get('venue', {}) if isinstance(first_visit.get('venue'), dict) else {}
        lv_venue = last_visit.get('venue', {}) if isinstance(last_visit.get('venue'), dict) else {}
        
        cursor.execute('''
            INSERT OR REPLACE INTO contacts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            c.get('id'),
            c.get('firstname'),
            c.get('lastname'),
            c.get('full_name'),
            c.get('gender'),
            dob.get('day'),
            dob.get('month'),
            dob.get('year'),
            c.get('age'),
            c.get('email'),
            c.get('phone'),
            c.get('nationality'),
            c.get('status'),
            first_visit.get('datetime'),
            fv_venue.get('name'),
            last_visit.get('datetime'),
            lv_venue.get('name'),
            json.dumps(excluded),
            c.get('created_at'),
            c.get('updated_at')
        ))
    
    conn.commit()
    
    print("📇 Creating indexes...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_gender ON contacts(gender)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_birth_month ON contacts(birth_month)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_birth_day ON contacts(birth_day)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON contacts(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON contacts(full_name)')
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM contacts')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM contacts WHERE gender = "Female"')
    females = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM contacts WHERE gender = "Male"')
    males = cursor.fetchone()[0]
    
    print(f"\n✅ Database created: affinect_contacts.db")
    print(f"   📊 Total: {total:,}")
    print(f"   👩 Females: {females:,}")
    print(f"   👨 Males: {males:,}")
    print(f"   ❓ Other/Unknown: {total - females - males:,}")
    
    conn.close()
    print("\n🎉 Done!")

if __name__ == "__main__":
    main()

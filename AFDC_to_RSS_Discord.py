import requests
import json
from datetime import datetime, timedelta, timezone
from feedgen.feed import FeedGenerator

# Config - Long Island EV Community (update these!)
API_KEY = 'YOUR_NREL_API_KEY_HERE'
STATE = 'NY'
FUEL_TYPE = 'ELEC'
JSON_OUTPUT = 'recent_long_island_ev_stations.json'
RSS_OUTPUT = 'long_island_ev_updates.rss'
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL_HERE'
LONG_ISLAND_ZIP_PREFIXES = ['110', '111', '115', '117', '118', '119']

TODAY_UTC = datetime.now(timezone.utc)
PAST_MONTH = TODAY_UTC - timedelta(days=30)

print(f"Long Island EV Charger Update — {TODAY_UTC.strftime('%Y-%m-%d')} 🚀⚡")
print("Fetching latest data from AFDC...")

url = f'https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={API_KEY}&fuel_type={FUEL_TYPE}&state={STATE}&status=all&limit=all'
response = requests.get(url)
if response.status_code != 200:
    print(f"API error: {response.status_code} — {response.text}")
    exit(1)

stations = response.json().get('fuel_stations', [])
print(f"Downloaded {len(stations)} stations from New York")

def is_recent(station):
    def to_utc_aware(date_str):
        if not date_str:
            return None
        try:
            if 'T' in date_str or '+' in date_str or date_str.endswith('Z'):
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                return datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        except:
            return None

    for key in ['open_date', 'date_last_confirmed', 'updated_at']:
        dt = to_utc_aware(station.get(key))
        if dt and dt >= PAST_MONTH:
            return True
    return False

print("Filtering for Nassau/Suffolk and last 30 days...")
recent_li_stations = [
    s for s in stations
    if is_recent(s) and any(str(s.get('zip', '')).startswith(p) for p in LONG_ISLAND_ZIP_PREFIXES)
]

num_new = len(recent_li_stations)
print(f"Found {num_new} new/recently-updated chargers!")

if num_new == 0:
    print("No updates this run—skipping RSS/Discord.")
    exit(0)

with open(JSON_OUTPUT, 'w') as f:
    json.dump({'fuel_stations': recent_li_stations}, f, indent=2)
print(f"JSON saved to {JSON_OUTPUT}")

print("Generating RSS feed...")
fg = FeedGenerator()
fg.id('https://example.com/long-island-ev-updates')
fg.title('Long Island EV Charging Updates')
fg.link(href='https://example.com', rel='alternate')
fg.description('Fresh EV chargers in Nassau/Suffolk from AFDC - For Drive Electric Long Island!')
fg.language('en')

for station in recent_li_stations:
    fe = fg.add_entry()
    fe.id(str(station['id']))
    fe.title(station['station_name'])
    desc = f"Address: {station['street_address']}, {station['city']}, {station['zip']}\n"
    desc += f"Connectors: {', '.join(station.get('ev_connector_types', ['N/A']))}\n"
    date_used = station.get('open_date') or station.get('date_last_confirmed') or station['updated_at'][:10]
    desc += f"Added/Updated: {date_used}"
    fe.description(desc)
    fe.link(href=f"https://afdc.energy.gov/stations/#/{station['id']}", rel='alternate')
    fe.pubDate(to_utc_aware(date_used) or TODAY_UTC)

fg.rss_file(RSS_OUTPUT)
print(f"RSS saved to {RSS_OUTPUT}")

if DISCORD_WEBHOOK_URL:
    print("Posting updates to Discord...")
    for station in recent_li_stations:
        message = f"🚨 New EV Charger Alert! ⚡\n**{station['station_name']}**\n📍 {station['street_address']}, {station['city']}, {station['zip']}\n🔌 Connectors: {', '.join(station.get('ev_connector_types', ['N/A']))}\n🗓 Added/Updated: {date_used}\n🔗 https://afdc.energy.gov/stations/#/{station['id']}\n#LongIslandEV #DriveElectric"
        requests.post(DISCORD_WEBHOOK_URL, json={'content': message})
    print("Discord posts sent!")

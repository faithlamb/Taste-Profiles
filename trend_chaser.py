import io

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
MAPBOX_STYLE_ID = "flamb22/cmnetkc1u001f01s8dpsd8v2m"

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Dolores But You Can Call Me Lolita,"1000 S Miami Ave",Miami,FL,25.7642717,-80.1934058,"Dolores offers rooftop dining, bold fusion dishes, and a stylish atmosphere perfect for Miami's trend-driven dining scene. Its playful menu and photogenic cocktails make it a favorite for social nights out. The vibrant setting is ideal for diners who love being where the energy is.","https://lh3.googleusercontent.com/gps-cs-s/APNQkAHqDG0Y9HBz_W-1t-IMXNUzVGKe2VtgqSfA6xDL1EO1mKF1WOIwutNmhdah_JgojxL1eBMPX6vSm9bxRmOIRema2Y57pg6ATSko5pIM-msUsAetzh_iqtzgMDyIFa4-gs-CWH8H=s1360-w1360-h1020-rw"
Lindens,"2 Renwick St",New York,NY,40.7245348,-74.0084684,"Lindens is a sleek, design-forward American restaurant known for its raw bar, seasonal plates, and modern aesthetic. The space blends Scandinavian minimalism with downtown cool, making it a magnet for trend-minded diners. Its menu and atmosphere feel curated for the moment.","https://images.getbento.com/accounts/a5ff14ad24f6c69ec229b09ba0e6888f/media/images/92564LINDENSINTERIOR6.jpg?w=1200&fit=crop&auto=compress,format&cs=origin&h=600"
The Hampton Social,"1520 Main St",Dallas,TX,32.7805910,-96.7987025,"The Hampton Social brings coastal-chic interiors, rose-all-day energy, and Instagram-ready decor to the heart of Dallas. With bright, beach-inspired dishes and a lively crowd, it's a hotspot for stylish dining. The atmosphere is upbeat, airy, and perfect for trend seekers.","https://popmenucloud.com/cdn-cgi/image/width=1920,height=1920,format=auto,fit=scale-down/vwzyjpmb/4ce1c6c8-b421-4c5a-88de-b0cae9b406c4.jpg"
Mother Wolf,"2777 S Las Vegas Blvd",Las Vegas,NV,36.1377442,-115.1603586,"Mother Wolf delivers high-design Italian dining with dramatic interiors and a glamorous, see-and-be-seen vibe. Its Roman-inspired dishes and luxurious atmosphere make it one of Vegas's most stylish destinations. It's a perfect fit for diners who chase the newest and boldest openings.","https://platform.vegas.eater.com/wp-content/uploads/sites/24/chorus/uploads/chorus_asset/file/25019533/Peter_Luger_Steak_House_Las_Vegas_Dining.jpg"
Perch,"448 S Hill St",Los Angeles,CA,34.0489961,-118.2514107,"Perch is a rooftop French bistro offering sweeping skyline views and a chic, Parisian-inspired ambiance. With live music, craft cocktails, and a fashionable crowd, it's a quintessential LA hotspot. The setting is effortlessly photogenic and ideal for trend-driven diners.","https://images.squarespace-cdn.com/content/v1/5c4511380dbda3abea27229a/152e983f-4a9d-47d1-a36a-337ad95364f1/Perch+Rooftop+Daytime+Lunch.jpg"
"""


def build_popup(row: pd.Series) -> folium.Popup:
	popup_html = f"""
	<div style="width:280px; font-family: Arial, sans-serif;">
	  <h4 style="margin:0 0 6px 0;">{row['name']}</h4>
	  <p style="margin:0 0 6px 0;"><strong>{row['address']}</strong><br>{row['city']}, {row['state']}</p>
	  <img src="{row['image']}" alt="{row['name']}" style="width:100%; height:auto; border-radius:8px; margin:4px 0 8px 0;">
	  <p style="margin:0; font-size:13px; line-height:1.4;">{row['description']}</p>
	</div>
	"""
	return folium.Popup(popup_html, max_width=320)


def build_trend_chaser_map() -> folium.Map:
	data = pd.read_csv(io.StringIO(CSV_DATA))

	required_cols = {
		"name",
		"address",
		"city",
		"state",
		"latitude",
		"longitude",
		"description",
		"image",
	}
	missing = required_cols - set(data.columns)
	if missing:
		raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

	center_lat = data["latitude"].mean()
	center_lon = data["longitude"].mean()

	mapbox_tiles = (
		f"https://api.mapbox.com/styles/v1/{MAPBOX_STYLE_ID}/tiles/"
		"{z}/{x}/{y}?access_token=" + MAPBOX_TOKEN
	)

	m = folium.Map(
		location=[center_lat, center_lon],
		zoom_start=4,
		tiles=mapbox_tiles,
		attr="Mapbox",
	)

	for _, row in data.iterrows():
		marker = folium.Marker(
			location=[row["latitude"], row["longitude"]],
			tooltip=row["name"],
			popup=build_popup(row),
			icon=folium.Icon(color="orange", icon="cutlery", prefix="fa"),
		)
		marker.add_to(m)

	return m


if __name__ == "__main__":
	trend_map = build_trend_chaser_map()
	output_path = "trend-chaser-map.html"
	trend_map.save(output_path)
	print(f"Saved map to {output_path}")

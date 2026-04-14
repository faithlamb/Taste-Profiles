import io
import os

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
# Format: username/style_id, for example: flamb22/abc123xyz
MAPBOX_STYLE_ID = os.getenv("MAPBOX_STYLE_ID", "mapbox/streets-v12")

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Café Bastille Downtown Miami,"248 SE 1st St",Miami,FL,25.7733642,-80.1893597,"Café Bastille is a beloved local French café known for its cozy atmosphere and all-day brunch menu that draws a loyal neighborhood crowd. With comforting classics like croque madame, crepes, and omelets, it feels like a familiar weekend staple rather than a tourist stop. Its warm, bustling vibe makes it a true Miami favorite.","https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2f/76/85/0a/interior.jpg?w=1000&h=600&s=1"
Au Cheval,"33 Cortlandt Alley",New York,NY,40.7181205,-74.0017942,"Au Cheval brings elevated American diner fare to a quiet Tribeca alley, earning a cult following for its iconic burgers and nostalgic comfort dishes. The dim, intimate space feels like a hidden neighborhood gem despite its national reputation. It's the kind of spot locals swear by for a reliably great meal.","https://images.squarespace-cdn.com/content/v1/5d59e574ce74150001a10bd2/1726617879275-9UFV9MHE8AQMYF84U7NN/IMG_1660.jpeg"
Chet's,"208 N Market St",Dallas,TX,32.7804796,-96.8061740,"Chet's blends Irish-influenced comfort food with a laid-back, neighborhood-pub feel. With dishes like shepherd's pie, fish and chips, and hearty sandwiches, it's a go-to for locals seeking warmth and familiarity. The welcoming atmosphere makes it feel like a community staple.","https://popmenucloud.com/cdn-cgi/image/width=1920,height=1920,format=auto,fit=scale-down/ihuawbng/51073e19-0d88-49b0-ac76-f8130ad9f4fb.jpg"
7th & Carson,"616 E Carson Ave #110",Las Vegas,NV,36.1672888,-115.1392712,"7th & Carson is a downtown Las Vegas favorite known for its eclectic share plates and relaxed, local-centric vibe. The menu highlights fresh, approachable dishes that feel rooted in the community rather than the Strip. Its cozy patio and neighborhood energy make it a true local gem.","https://i0.wp.com/www.vegansbaby.com/wp-content/uploads/2018/10/20181011-2018-10-11_7th_and_Carson-2-1024x683.jpg?resize=800%2C534&ssl=1"
Eggslut,"317 S Broadway",Los Angeles,CA,34.0505885,-118.2486089,"Eggslut has become an LA institution thanks to its simple, comforting egg-centric sandwiches served with gourmet precision. Located inside Grand Central Market, it draws a loyal crowd of locals who crave its warm, satisfying flavors. Despite its fame, it maintains a casual, everyday feel.","https://dynamic-media-cdn.tripadvisor.com/media/photo-o/26/de/a1/ce/nice-buns.jpg?w=1100&h=1100&s=1"
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


def build_local_loyalist_map() -> folium.Map:
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

	# Use the configured Mapbox style via token.
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
			icon=folium.Icon(color="blue", icon="cutlery", prefix="fa"),
		)
		marker.add_to(m)

	return m


if __name__ == "__main__":
	local_map = build_local_loyalist_map()
	output_path = "local-loyalist-map.html"
	local_map.save(output_path)
	print(f"Saved map to {output_path}")
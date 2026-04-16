import io

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
MAPBOX_STYLE_ID = "flamb22/cmnetkc1u001f01s8dpsd8v2m"

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Crazy About You,"1155 Brickell Bay Dr PH101",Miami,FL,25.7620008,-80.1889886,"Crazy About You offers waterfront dining with a lively, social atmosphere perfect for groups. The eclectic menu spans Spanish, Italian, and American influences, making it ideal for sharing. Its upbeat energy makes it a go-to for social dining.","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIHgc9UC475v2swKFWlU9AJ0-qnawzQd7fGw&s"
abc cocina,"38 E 19th St",New York,NY,40.7379868,-73.9892758,"abc cocina serves vibrant Latin-inspired small plates in a stylish, energetic setting. The menu is designed for sharing, and the atmosphere is lively without being pretentious. It's a perfect fit for group dining and social nights out.","https://lh3.googleusercontent.com/gps-cs-s/APNQkAEuSiNrkWFUv6g0Z-M-QECXCLPiL21W9rWm2VICbvsX_pGCT1JzS3GqODaNcFxxh2lrsy-fYcj0_3KS5boDg5_Fbr8ytimoJVjRprvHgbSMzt7cRlphamgFcKC6o3PQl3vqn5Uxcf7rjgY=s1360-w1360-h1020-rw"
The Henry,"2301 N Akard St Suite 250",Dallas,TX,32.7892021,-96.8055857,"The Henry is a trendy, social American restaurant with a bright, welcoming atmosphere and a menu built for sharing. From cocktails to comfort-leaning plates, it's ideal for groups. The space is lively, modern, and always buzzing.","https://lh3.googleusercontent.com/p/AF1QipNYwKGaT8UWwbcs6R5CLVFLbdBbti0l-qLevZ8a=s1360-w1360-h1020-rw"
Carson Kitchen,"124 S 6th St #100",Las Vegas,NV,36.1695110,-115.1406860,"Carson Kitchen offers modern comfort food and creative small plates in a sleek, energetic downtown space. The rooftop patio and shareable menu make it perfect for social dining. It's a favorite for groups looking for great food in a fun setting.","https://usmenuguide.com/wp-content/uploads/2023/11/carsonkitchenlasvegas15-1024x683.jpeg"
Girl & the Goat LA,"555-3 Mateo St",Los Angeles,CA,34.0387800,-118.2324300,"Girl & the Goat brings bold, globally inspired share plates to a lively, industrial-chic dining room. The menu encourages exploration and sharing, making it ideal for groups. Its high-energy atmosphere makes every meal feel like an event.","https://www.wineandspiritsmagazine.com/wp-content/uploads/2022/01/2201-resto-girlandgoat-cred-anthony-tahlier-1024x768.jpg"
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


def build_social_foodie_map() -> folium.Map:
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
	social_map = build_social_foodie_map()
	output_path = "social-foodie-map.html"
	social_map.save(output_path)
	print(f"Saved map to {output_path}")

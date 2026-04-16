import io

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
MAPBOX_STYLE_ID = "flamb22/cmnetkc1u001f01s8dpsd8v2m"

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Claudie,"1101 Brickell Ave S-113",Miami,FL,25.7632665,-80.1910857,"Claudie offers refined French-Mediterranean cuisine with meticulous technique and elegant presentation. Its upscale atmosphere and chef-driven menu make it a destination for diners who value precision and craft. Every dish feels intentional and elevated.","https://images.squarespace-cdn.com/content/v1/653820f067951356ec09c800/8c11a7f5-49bf-4b99-b864-6e8a2aba3c1d/CLAUDIE_May_2025_0371-Enhanced-NR-Edit_4K.jpg"
Le Bernardin,"155 W 51st St",New York,NY,40.7614218,-73.9817558,"Le Bernardin is one of the world's most celebrated fine-dining restaurants, renowned for Eric Ripert's masterful seafood preparations. The service, technique, and execution are unmatched, creating a serene, luxurious dining experience. It's the pinnacle of culinary craftsmanship.","https://www.le-bernardinprive.com/images/fb.jpg"
Written by the Seasons,"380 Melba St",Dallas,TX,32.7471258,-96.8279412,"Written by the Seasons focuses on seasonal, chef-driven New American cuisine with beautifully composed plates. The intimate space and thoughtful menu highlight technique and ingredient quality. It's a standout for diners who appreciate culinary artistry.","https://14fc423a4c97ea6ac2e5.cdn6.editmysite.com/uploads/b/14fc423a4c97ea6ac2e5cfbbef2647d5a957f384248b668e610de4e39a1e345d/bishop%20arts_1740163973.png"
Sparrow + Wolf,"4480 Spring Mountain Rd #100",Las Vegas,NV,36.1265479,-115.2012681,"Sparrow + Wolf blends global influences with live-fire cooking to create inventive, boundary-pushing dishes. The menu is bold yet refined, showcasing serious technique and creativity. It's a favorite among culinary-minded locals and chefs.","https://venue-media.eventup.com/resized/venue/sparrow-wolf/c0ee.1920x1080.jpg"
Bestia,"2121 E 7th Pl",Los Angeles,CA,34.0338338,-118.2293287,"Bestia is an acclaimed Italian restaurant known for its handmade pastas, wood-fired dishes, and industrial-chic setting. The kitchen's precision and creativity have made it a cornerstone of LA dining. Every plate reflects deep technique and bold flavor.","https://bestiala.com/wp-content/uploads/2025/08/2025.08.05-Bestia_July_Joseph-Weaver_D122-copy.jpg"
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


def build_culinary_purist_map() -> folium.Map:
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
	purist_map = build_culinary_purist_map()
	output_path = "culinary-purist-map.html"
	purist_map.save(output_path)
	print(f"Saved map to {output_path}")

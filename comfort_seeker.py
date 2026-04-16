import io

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
MAPBOX_STYLE_ID = "flamb22/cmnetkc1u001f01s8dpsd8v2m"

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Yardbird Table & Bar,"1600 Lenox Ave",Miami Beach,FL,25.7890685,-80.1401579,"Yardbird is a Southern comfort classic, famous for its fried chicken, biscuits, and warm, rustic atmosphere. The menu is hearty and nostalgic, offering dishes that feel like home. It's cozy, welcoming, and perfect for comfort-driven diners.","https://www.droolius.com/wp-content/uploads/2012/04/Yardbird_MiamiBrunch_14.jpg"
Minetta Tavern,"113 MacDougal St",New York,NY,40.7299881,-74.0007016,"Minetta Tavern blends old-New-York charm with elevated comfort dishes like its iconic Black Label Burger. The dim lighting, vintage decor, and intimate booths create a warm, nostalgic atmosphere. It's a quintessential comfort-food destination.","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgD2jQ2CVTBnkKifAHmH_RN6quiFaLVzb74Q&s"
Fond,"1601 Elm St Suite 110",Dallas,TX,32.7822150,-96.7979407,"Fond serves homey, comforting dishes with a refined touch in a cozy, neighborhood-style setting. The menu features warm, familiar flavors elevated with thoughtful technique. It's a perfect retreat for diners seeking calm and comfort.","https://res.cloudinary.com/the-infatuation/image/upload/v1739927947/Fond_Dallas_Kathy_Tran_035_vv6lm2.jpg"
Main St. Provisions,"1214 S Main St",Las Vegas,NV,36.1568043,-115.1538393,"Main St. Provisions offers hearty comfort food with modern twists in a stylish yet inviting space. The open kitchen and warm service create a welcoming neighborhood feel. It's a standout for comforting, soulful dishes off the Strip.","https://npr.brightspotcdn.com/dims4/default/293d843/2147483647/strip/true/crop/1440%C3%971080+0+0/resize/880x660!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Fd1%2F1f%2F9ae6a860421f9e97b5b1f5189c3a%2F328995605-843800396685168-3316649993969494303-n.jpg"
Maccheroni Republic,"332 S Broadway",Los Angeles,CA,34.0500306,-118.2485361,"Maccheroni Republic is a beloved Italian spot known for its handmade pastas and homey, relaxed atmosphere. The BYO wine policy and cozy patio make it feel like a true neighborhood favorite. It's pure comfort in the heart of downtown LA.","https://dtlaexplorer.wordpress.com/wp-content/uploads/2015/04/img_8941.jpg"
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


def build_comfort_seeker_map() -> folium.Map:
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
	comfort_map = build_comfort_seeker_map()
	output_path = "comfort-seeker-map.html"
	comfort_map.save(output_path)
	print(f"Saved map to {output_path}")

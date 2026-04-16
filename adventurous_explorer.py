import io

import folium
import pandas as pd

MAPBOX_TOKEN = "pk.eyJ1IjoiZmxhbWIyMiIsImEiOiJjbWx0cXJzbGwwMzNsM2xwbmZqaWw2Zjk3In0.Lo4lEcg-rbCpdEAbAzyh2w"
MAPBOX_STYLE_ID = "flamb22/cmnetkc1u001f01s8dpsd8v2m"

CSV_DATA = """name,address,city,state,latitude,longitude,description,image
Tanuki River Landing,"1420 NW N River Dr",Miami,FL,25.7853295,-80.2196917,"Tanuki River Landing serves bold, eclectic Asian fusion dishes with vibrant flavors and creative presentations. The waterfront setting adds to the sense of adventure and discovery. It's ideal for diners seeking something unexpected.","https://images.squarespace-cdn.com/content/v1/640770e92dc69666974a8e37/62855f2d-b763-41cd-b7a0-a2f367e2ebcf/DSCF9296.jpg"
Le Coucou,"138 Lafayette St",New York,NY,40.7191167,-74.0001861,"Le Coucou offers refined French cuisine with adventurous dishes like rabbit, foie gras, and lobster prepared with classic technique. The airy, elegant dining room elevates the experience. It's perfect for diners who enjoy exploring sophisticated, daring flavors.","https://lecoucou.com/wp-content/uploads/sites/19/2023/12/L_Palmberg_LeCouCou_004-1024x683.jpg"
3Eleven Kitchen & Cocktails,"311 N Market St #100",Dallas,TX,32.7812264,-96.8070088,"3Eleven pairs scratch-made American dishes with inventive cocktails in a vibrant, modern space. The menu features creative twists on classics, making it ideal for curious diners. Its lively atmosphere adds to the sense of exploration.","https://assets.simpleviewinc.com/simpleview/image/upload/c_limit,q_75,w_1200/v1/crm/dallasites101/3eleven_3FBE1B79-5056-A36A-0A579887AF0AFCFD-3fbe19815056a36_3fbe2289-5056-a36a-0afb2a330fc4c2f0.jpg"
Sparrow + Wolf,"4480 Spring Mountain Rd #100",Las Vegas,NV,36.1265479,-115.2012681,"Sparrow + Wolf blends global influences with live-fire cooking to create inventive, boundary-pushing dishes. The menu is bold yet refined, showcasing serious technique and creativity. It's a favorite among culinary-minded locals and chefs.","https://www.gayot.com/images/reviews/sparrow-wolf-interior.jpg"
Holbox,"3655 S Grand Ave C9",Los Angeles,CA,34.0173560,-118.2784050,"Holbox specializes in Yucatan-style seafood with bold preparations like ceviches, aguachiles, and grilled whole fish. The flavors are vibrant, fresh, and deeply regional. It's a must-visit for diners seeking something truly unique.","https://offloadmedia.feverup.com/secretlosangeles.com/wp-content/uploads/2024/09/20160323/DSC09489-1024x683.jpg"
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


def build_adventurous_explorer_map() -> folium.Map:
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
	explorer_map = build_adventurous_explorer_map()
	output_path = "adventurous-explorer-map.html"
	explorer_map.save(output_path)
	print(f"Saved map to {output_path}")

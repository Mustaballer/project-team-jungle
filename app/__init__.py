from peewee import *
import datetime
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import folium
import json
from folium.plugins import FloatImage
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
data = open("app/static/data.json")
data = json.load(data)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"),
                     host=os.getenv("MYSQL_HOST"), port=3306)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


# routes send the loaded json object "data" to display personal information
@app.route("/")
def index():
    return render_template(
        "index.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/about")
def about():
    return render_template(
        "about.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/experience")
def experience():
    return render_template(
        "experience.html",
        title="Team Jungle Portfolio",
        url=os.getenv("URL"),
        data=data,
    )


@app.route("/map")
def map():
    return render_template(
        "map.html", title="Team Jungle Portfolio", url=os.getenv("URL"), data=data
    )


@app.route("/folium_map")
def folium_map():
    start_coords = (43.653, -79.383)
    folium_map = folium.Map(location=start_coords, zoom_start=3, tiles="Stamen Terrain")

    for i in range(0, len(data["locations"])):
        folium.Marker(
            location=[data["locations"][i]["latitude"], data["locations"][i]["longitude"]],
            popup=data["locations"][i]["name"],
            icon=folium.Icon(color=data["locations"][i]["color"]),
        ).add_to(folium_map)

    ## fix mobile view
    folium_map.get_root().header.add_child(
        folium.Element(
            '<meta name="viewport" content="width=device-width,'
            ' initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />'
        )
    )

    image_file = "/static/img/legend.jpg"
    FloatImage(image_file, bottom=0, left=0).add_to(folium_map)

    folium_map.save("app/templates/map.html")
    return render_template("mapindex.html")

@app.route('/timeline')
def timeline():
    return render_template("timeline.html", title="Timeline")


@app.route('/api/timeline_post', methods=["POST"])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<int:id>", methods=['DELETE'])
def delete_time_line_post(id):
    post_to_delete = TimelinePost.get(TimelinePost.id == id)
    post_to_delete.delete_instance()

    return "Successfully deleted"
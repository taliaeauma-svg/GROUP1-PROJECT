import math
import csv

class Point:
    def __init__(self, point_id, northing, easting, elevation=0):
        self.point_id = point_id
        self.northing = northing
        self.easting = easting
        self.elevation = elevation

class SurveyLine:
    def __init__(self, from_point, to_point, bearing, distance):
        self.from_point = from_point
        self.to_point = to_point
        self.bearing = bearing
        self.distance = distance

    def compute_new_point(self, new_point_id):
        bearing_rad = math.radians(self.bearing)
        delta_northing = self.distance * math.cos(bearing_rad)
        delta_easting = self.distance * math.sin(bearing_rad)
        new_northing = self.from_point.northing + delta_northing
        new_easting = self.from_point.easting + delta_easting
        return Point(new_point_id, new_northing, new_easting, self.from_point.elevation)
    
class SurveyManager:
    def __init__(self):
        self.points = {}
        self.survey_lines = []

    def export_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Point ID', 'Northing', 'Easting', 'Elevation'])
            for point in self.points.values():
                writer.writerow([point.point_id, point.northing, point.easting, point.elevation])

    def add_survey_line(self, survey_line):
        self.survey_lines.append(survey_line)

    def add_point(self, point):
        self.points[point.point_id] = point


start = Point("P1", 1000.0, 1000.0, 50.0)
Line = SurveyLine(start, None, 45.0, 100.0)
new_point = Line.compute_new_point("P2")

manager = SurveyManager()
manager.points[start.point_id] = start
manager.points[new_point.point_id] = new_point

manager.export_to_csv("survey_points.csv")

print(f"New Point ID: {new_point.point_id}, Northing: {new_point.northing}, Easting: {new_point.easting}, Elevation: {new_point.elevation}")

def calculate_bearing(pointA, pointB):
    delta_easting = pointB.easting - pointA.easting
    delta_northing = pointB.northing - pointA.northing
    bearing_rad = math.atan2(delta_easting, delta_northing)
    bearing_deg = math.degrees(bearing_rad)
    if bearing_deg < 0:
        bearing_deg += 360
    return bearing_deg
bearing = calculate_bearing(start, new_point)
print(f"Bearing from {start.point_id} to {new_point.point_id}: {bearing} degrees")
distance = math.sqrt((new_point.northing - start.northing) ** 2 + (new_point.easting - start.easting) ** 2)
print(f"Distance from {start.point_id} to {new_point.point_id}: {distance} units")

Line2 = SurveyLine(new_point, None, 135.0, 50.0)
new_point2 = Line2.compute_new_point("P3")

manager.points[new_point2.point_id] = new_point2
manager.export_to_csv("survey_points_updated.csv")
print(f"New Point ID: {new_point2.point_id}, Northing: {new_point2.northing}, Easting: {new_point2.easting}, Elevation: {new_point2.elevation}")
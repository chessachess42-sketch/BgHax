# Large detailed world map in terminal using Braille Unicode characters
# Pure Python + drawille (no heavy dependencies)

from drawille import Canvas
import math
import time
import sys
import os

def lonlat_to_xy(lon, lat, width, height):
    """Convert longitude/latitude to canvas x,y coordinates"""
    x = (lon + 180) / 360 * width
    y = (90 - lat) / 180 * height
    return int(x), int(y)

def draw_continent(c, points, char='⣿'):
    """Draw filled continent using points"""
    if not points:
        return
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x,y) in points:
                c.set(x, y)

def main():
    # Get terminal size for maximum size
    try:
        rows, cols = os.popen('stty size', 'r').read().split()
        height = int(rows) * 4 - 8   # Braille is 4x higher than normal chars
        width = int(cols) * 2 - 10
    except:
        height = 80 * 4   # Default large size
        width = 120 * 2
    
    height = max(60 * 4, height)   # At least decent size
    width = max(100 * 2, width)
    
    print(f"\nRendering large world map ({width}x{height} points)...")
    print("Braille mode - zoom out your font if too small! (Ctrl + mouse wheel)\n")
    
    c = Canvas(width, height)
    
    # Rough but fairly detailed continent outlines (lon, lat pairs)
    # You can add more points for better detail if you want
    
    # North America rough
    na_points = []
    for lon in range(-170, -50, 3):
        lat = 70 + math.sin((lon + 100) * 0.1) * 15
        na_points.append(lonlat_to_xy(lon, lat, width, height))
    for lon in range(-130, -60, 2):
        lat = 40 + math.cos((lon + 90) * 0.15) * 20
        na_points.append(lonlat_to_xy(lon, lat, width, height))
    
    # South America
    sa_points = []
    for lon in range(-80, -35, 3):
        lat = 0 - math.sin((lon + 60) * 0.12) * 30
        sa_points.append(lonlat_to_xy(lon, lat, width, height))
    
    # Europe + Africa
    eur_points = []
    for lon in range(-10, 40, 2):
        lat = 50 + math.sin(lon * 0.2) * 10
        eur_points.append(lonlat_to_xy(lon, lat, width, height))
    afr_points = []
    for lon in range(-20, 50, 3):
        lat = 20 - math.cos(lon * 0.1) * 30
        afr_points.append(lonlat_to_xy(lon, lat, width, height))
    
    # Asia + Australia
    asia_points = []
    for lon in range(30, 150, 4):
        lat = 40 + math.sin((lon - 80) * 0.08) * 25
        asia_points.append(lonlat_to_xy(lon, lat, width, height))
    aus_points = []
    for lon in range(110, 155, 3):
        lat = -25 + math.cos((lon - 130) * 0.2) * 10
        aus_points.append(lonlat_to_xy(lon, lat, width, height))
    
    # Antarctica rough
    ant_points = []
    for lon in range(-180, 180, 8):
        lat = -70 + math.sin(lon * 0.05) * 10
        ant_points.append(lonlat_to_xy(lon, lat, width, height))
    
    # Draw them!
    draw_continent(c, set(na_points), '⣿')
    draw_continent(c, set(sa_points), '⣿')
    draw_continent(c, set(eur_points + afr_points), '⣿')
    draw_continent(c, set(asia_points + aus_points), '⣿')
    draw_continent(c, set(ant_points), '⣿')
    
    # Add some oceans / extra detail with lighter chars
    for i in range(0, width, 15):
        for j in range(0, height, 15):
            if c.get(i, j) == 0:  # only on ocean
                c.set(i, j)  # light dot
    
    # Render the canvas!
    print(c.frame())
    
    print("\n" + "═" * 70)
    print("Pura world map braille style mein! (North upar, South neeche)")
    print("Continents filled with '⣿' - detailed enough for terminal")
    print("Press Ctrl+C to exit | Font chhota kar ke aur detail dekh sakta hai")
    print("═" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBhai map dekh liya? Ab nikal ja! 🌍😏")
    except Exception as e:
        print("Kuch gadbad ho gayi:", e)
        print("drawille install kar le: pip install drawille")
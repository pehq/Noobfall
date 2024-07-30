from PIL import Image
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os

def get_white_pixel_rectangles(image_path):
    # Open the image file
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure image is in RGB format

    width, height = img.size
    visited = [[False] * width for _ in range(height)]

    def is_white(x, y):
        if x >= width or y >= height:
            return False
        r, g, b = img.getpixel((x, y))
        return r == 255 and g == 255 and b == 255

    def find_rectangle(x, y):
        # Find the boundaries of the rectangle starting from (x, y)
        min_x, min_y = x, y
        max_x, max_y = x, y

        while True:
            expanded = False

            # Try to expand diagonally
            if max_x + 1 < width and max_y + 1 < height and is_white(max_x + 1, max_y + 1):
                if all(is_white(max_x + 1, k) and not visited[k][max_x + 1] for k in range(min_y, max_y + 1)) and \
                   all(is_white(k, max_y + 1) and not visited[max_y + 1][k] for k in range(min_x, max_x + 1)):
                    max_x += 1
                    max_y += 1
                    expanded = True

            # Try to expand to the right
            if max_x + 1 < width and all(is_white(max_x + 1, k) and not visited[k][max_x + 1] for k in range(min_y, max_y + 1)):
                max_x += 1
                expanded = True

            # Try to expand downwards
            if max_y + 1 < height and all(is_white(k, max_y + 1) and not visited[max_y + 1][k] for k in range(min_x, max_x + 1)):
                max_y += 1
                expanded = True

            if not expanded:
                break

        return min_x, min_y, max_x, max_y

    rectangles = []

    for y in range(height):
        for x in range(width):
            if is_white(x, y) and not visited[y][x]:
                min_x, min_y, max_x, max_y = find_rectangle(x, y)
                rectangles.append({
                    'x': min_x,
                    'y': min_y,
                    'w': max_x - min_x + 1,
                    'h': max_y - min_y + 1
                })
                # Mark the rectangle as visited
                for j in range(min_y, max_y + 1):
                    for i in range(min_x, max_x + 1):
                        visited[j][i] = True

    # Return compressed JSON
    return json.dumps(rectangles, separators=(',', ':'))

def main():
    # Initialize Tkinter and hide the root window
    root = Tk()
    root.withdraw()

    # Open a file dialog to select multiple image files
    file_paths = askopenfilenames(
        title="Select Image Files",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if file_paths:
        for file_path in file_paths:
            # Get white pixel rectangles
            rectangles_json = get_white_pixel_rectangles(file_path)
            
            # Define output file path
            output_file_path = os.path.splitext(file_path)[0] + '_white_pixel_rectangles.txt'
            
            # Write compressed JSON data to the text file
            with open(output_file_path, 'w') as file:
                file.write(rectangles_json)
            
            print(f"White pixel rectangles saved to {output_file_path}")
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()
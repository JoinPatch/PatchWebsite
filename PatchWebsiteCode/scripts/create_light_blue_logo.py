"""
Script to create a light blue version of the Patch logo for background use.
Converts white pixels to a light blue color suitable for subtle background patterns.
"""

from PIL import Image
import os

def create_light_blue_logo(input_path: str, output_path: str, target_color: tuple = (190, 219, 255)):
    """
    Convert a white logo to a light blue version.

    Args:
        input_path: Path to the input PNG image (white logo with transparency)
        output_path: Path to save the output PNG image
        target_color: RGB tuple for the target light blue color
    """
    # Open the image
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()

    width, height = img.size

    # Process each pixel
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # If the pixel has some opacity (not fully transparent)
            if a > 0:
                # Calculate the brightness of the original pixel
                brightness = (r + g + b) / (3 * 255)

                # Apply the target color with the original alpha and brightness
                new_r = int(target_color[0] * brightness)
                new_g = int(target_color[1] * brightness)
                new_b = int(target_color[2] * brightness)

                pixels[x, y] = (new_r, new_g, new_b, a)

    # Save the result
    img.save(output_path, 'PNG')
    print(f"Created light blue logo at: {output_path}")


def main():
    # Get the script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    public_dir = os.path.join(project_root, 'public')

    # Input and output paths
    input_logo = os.path.join(public_dir, 'WhiteLogoNoBackground.webp')
    output_logo = os.path.join(public_dir, 'LightBlueLogoNoBackground.webp')

    # Light blue color matching the site's blue palette
    # Using a very soft blue that will work well as a subtle background pattern
    light_blue = (160, 200, 240)  # Slightly darker blue

    if not os.path.exists(input_logo):
        print(f"Error: Input logo not found at {input_logo}")
        return

    create_light_blue_logo(input_logo, output_logo, light_blue)

    # Also create a very light version for even subtler use
    very_light_blue = (220, 235, 255)  # Even lighter for subtle background
    output_very_light = os.path.join(public_dir, 'VeryLightBlueLogoNoBackground.webp')
    create_light_blue_logo(input_logo, output_very_light, very_light_blue)
    print(f"Created very light blue logo at: {output_very_light}")


if __name__ == '__main__':
    main()

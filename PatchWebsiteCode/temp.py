from PIL import Image

img = Image.open("./public/FullLogoWhite.png").convert("RGBA")
pixels = img.getdata()

new_pixels = []
blue = (30, 64, 175)  # Tailwind blue-800

for r, g, b, a in pixels:
    if a > 0:  # non-transparent
        new_pixels.append((*blue, a))
    else:
        new_pixels.append((r, g, b, a))

img.putdata(new_pixels)
img.save("output.png")

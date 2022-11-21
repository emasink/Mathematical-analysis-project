import matplotlib
import matplotlib.pyplot as plt
import sys
from PIL import Image


def crop(im, width, height, image_tiles, image_text, img_width, img_height):
    for i in range(0, img_height, height):
        for j in range(0, img_width, width):
            tile = (j, i, j+width, i+height)
            a = im.crop(tile)
            # a.save(image_text+"column :"+str(j)+", row :"+str(i)+".png", format="png")
            image_tiles.append(a)


def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    color_scale = len(histogram)  # = brightness
    pixel_value_sum = 0
    for index in range(0, color_scale):
        pixel_value_sum += histogram[index]*index
    pixel_brightness = pixel_value_sum/(pixels * 255)
    return pixel_brightness


def get_length_list(image_tile_list):
    length = 0
    result_list = []
    for _ in image_tile_list:
        length += 1
        result_list.append(length)
    return result_list

#function to extend picture's measurements as needed
def append_length(columns, width):
    i = 0
    while ((width % columns != 0)):
        width = width + i
        i += 1
    return width

def get_tile_dimensions(image):
    width, height = image.size
    tile_width = int(width/columns) if (width % columns == 0) else int(append_length(columns, width)/columns)
    tile_height = int(height/rows) if (height % rows == 0) else int(append_length(rows, height)/rows)
    return (tile_width, tile_height)

# cropping variables
columns = 4
rows = 3

# Importing images from directory:
try:
    original_image = Image.open(str(sys.argv[1]))  # Image.open("img1.png")
    modified_image = Image.open(str(sys.argv[2]))  # Image.open("img2.png")
except IndexError:
    print("Incorrect command line arguments. Correct way: python3 project.py image1.png image2.png")
    sys.exit(1)

# Extracting pixel map:
pixel_map = original_image.load()


image_tiles = []
brightness_array_1 = []
tile_width, tile_height = get_tile_dimensions(original_image)
crop(original_image, tile_width, tile_height, image_tiles, "original", tile_width * columns, tile_height * rows)
for i in image_tiles:
    brightness_array_1.append(round(calculate_brightness(i), 4))
#    print(round(calculate_brightness(i), 4))
    
compare_image_tiles = []
brightness_array_2 = []
tile_width, tile_height = get_tile_dimensions(modified_image)
crop(modified_image, tile_width, tile_height, compare_image_tiles, "modified", tile_width * columns, tile_height * rows)
for i in compare_image_tiles:
    brightness_array_2.append(round(calculate_brightness(i), 4))
#    print(round(calculate_brightness(i), 4))

maxDistance = 0
for i in range(0, len(brightness_array_1)):
    distance = abs(brightness_array_1[i] - brightness_array_2[i])
    if distance > maxDistance:
        maxDistance = distance


print(maxDistance)
    # print(str(brightness_array_1[i]) + "     " + str(brightness_array_2[i]))


x_axis = get_length_list(image_tiles)
plt.plot(x_axis, brightness_array_1, "-b", label=sys.argv[1])
plt.plot(x_axis, brightness_array_2, "-r", label=sys.argv[2])
plt.legend(loc="best")
plt.title('Skaidinių ryškumų grafikai\n'+ "max atsilenkimas:" + str(maxDistance))
plt.show()




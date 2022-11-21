import matplotlib
import matplotlib.pyplot as plt
import sys
from PIL import Image


def crop(im, height, width, image_tiles, image_text):
    img_width, img_height = im.size
    for i in range(0, img_height, height):
        for j in range(0, img_width, width):
            tile = (j, i, j+width, i+height)
            a = im.crop(tile)
            a.save(image_text+"column :"+str(i)+", row :"+str(j)+".png", format="png")
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


# cropping variables
columns = 4
rows = 3

# Importing an images from directory:
try:
    original_image = Image.open(str(sys.argv[1]))  # Image.open("img1.png")
    modified_image = Image.open(str(sys.argv[2]))  # Image.open("img2.png")
except IndexError:
    print("Incorrect command line arguments. Correct way: python3 project.py image1.png image2.png")
    sys.exit(1)

# Extracting pixel map:
pixel_map = original_image.load()

width, height = original_image.size

chunk_width = width//columns
chunk_height = height//rows
image_tiles = []
brightness_array_1 = []
crop(original_image, chunk_width, chunk_height, image_tiles, "original")
for i in image_tiles:
    brightness_array_1.append(round(calculate_brightness(i), 4))
#    print(round(calculate_brightness(i), 4))
    
compare_image_tiles = []
brightness_array_2 = []
crop(modified_image, chunk_width, chunk_height, compare_image_tiles, "modified")
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
plt.plot(x_axis, brightness_array_1)
plt.plot(x_axis, brightness_array_2)
# matplotlib.rcParams['interactive'] == True
plt.show()




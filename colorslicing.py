import os
import cv2
import numpy as np

'''
Accepts a string input of the user's image path file 
and parses the '~' from the path to the user's root directory
'''
def user_img_input():
    path = input("Hello! Please enter the path to your image file:  ")
    img_path = os.path.expanduser(path)
    return img_path

'''
Verifies that a file exists at the path that has been parsed from the user input
'''
def path_validity(img_path):
    if os.path.isfile(img_path):
        print("\nFile path found at: " + str(img_path))
        return img_path
    else:
        print("File path not found. Path was: " + str(img_path))
        return None

'''
If the image exists, uses OpenCV to display the image in color
and waits one second before closing it. Returns the color image.
If image does not exist, returns none.
RaisesException: Depending on error in opening image
'''
def img_conversion(img_path):
    try:
        color_image = cv2.imread(img_path)
        if color_image is not None:
            cv2.imshow("Original Image", color_image)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            return color_image
        else:
            print("\nSorry, the image could not be loaded\n")
            return None
    except Exception as e:
        print("\nError encountered while opening image using OpenCV:  " + str(e) + '\n')
        return None

'''
Performs color slicing to enhance red and green colors and darken other colors
'''
def color_slicing(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for red color
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Define the range for green color
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Create masks for red and green colors
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = mask_red1 + mask_red2
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Enhance the red and green colors in the original image
    result_image = image.copy()
    result_image[red_mask > 0] = [0, 0, 255]  # Set the red channel to max
    result_image[green_mask > 0] = [0, 255, 0]  # Set the green channel to max

    # Darken the non-red and non-green areas
    combined_mask = red_mask + green_mask
    result_image[combined_mask == 0] = result_image[combined_mask == 0] // 2

    # Display the resulting image
    cv2.imshow("Color Sliced Image", result_image)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

    return result_image

def main():
    # Accept path to image
    image_path_user = user_img_input()

    # Verify that the path entered by the user is a valid one
    valid_path = path_validity(image_path_user)

    # Tries to open the image at the path in the OpenCV color mode
    if valid_path:
        color_img = img_conversion(image_path_user)
        
        if color_img is not None:
            # Apply color slicing
            color_sliced_img = color_slicing(color_img)

if __name__ == "__main__":
    main()

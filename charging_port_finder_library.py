# Contour outline library

import numpy as np
import cv2

#####
"""
These functions reformat the image.
"""

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    From Yong Da Li's github. He stole it from someone else. The 2nd-4th parameters are optional.
    """
    
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def external_rectangle(image):
    """
    image = [ [ [B G R], [...], ..., [] ], [], ..., [] ]
    """
    dy = 0 #55 for webcam.
    start_point = (0,dy)
    end_point = (len(image[0])-1, len(image)-1-dy)
    colour = (0,0,255)
    thickness = 1
    cv2.rectangle(image, start_point, end_point, colour, thickness)

    return image

#####

def max_contour_area(contours):
    """
    Definition:
    max_contour_area(contours)

    Inputs:
    1. contours = list of contours (edges of a coloured region)

    Functionality:
    1. Finds maximum contour area

    Outputs:
    1. max_area_index = index of maximum contour
    """

    max_area = 0
    max_area_index = 0
    
    for i in range(len(contours)):
        new_area = cv2.contourArea(contours[i])
        
        if new_area > max_area:
            max_area = new_area
            max_area_index = i

    # Return maximum area's index
    return max_area_index 

def find_max_inner_area(contours, hierarchy, max_area_index):
    """
    Definition:
    find_max_inner_area(contours, hierarchy, max_area_index)

    Inputs:
    1. contours = list of contours
    2. hierarchy = tree structure of inner contours
    3. max_area_index = which contour is the parent node

    Functionality:
    >>Runs through inner contours
    1. Find maximum contour
    <<

    Outputs:
    1. max_child_index = child contour with largest area

    Notes:
    hierarchy = [ [[Next, Previous, First_Child, Parent] ] ]
    We need to unpackage the hierarchy
    """

    # Select first inner area from largest area contour
    next_child = hierarchy[0][max_area_index][2]

    # Find max inner contour area
    max_area = 0
    max_child_index = 0

    while(next_child != -1):
    
        new_area = cv2.contourArea(contours[next_child])
        
        if new_area > max_area:
            
            max_area = new_area
            max_child_index = next_child

        next_child = hierarchy[0][next_child][0] # Select next child

    return max_child_index

def centre_finder(image, target_contour):
    """
    Definition:
    centre_finder(image, target_contour)

    Inputs:
    1. image
    2. target_contour

    Functionality:
    1. Compute x-, y-moments
    >>IF show_steps == TRUE:
    2. Draw rectangle around
    3. Draw dot in centre
    <<

    Outputs: [image, [cX, cY]]
    1. image = colour image with target drawn in the middle of the charging port
    2. [cX, cY] = x- and y-coordinates of the centre
    
    Source:
    1. https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
    """
    # Compute the center of the contour
    M = cv2.moments(target_contour)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    return [cX,cY]

def centre_target(image, target_contour, centre, show_steps=False, close_windows=False):
    [cX, cY] = centre
    # Draw RECTANGLE around image
    cv2.rectangle(image, cv2.boundingRect(target_contour), (0,0,255),5)

    # Draw DOT in the centre of the image
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, '('+str(cX)+','+str(cY)+')', (cX - 40, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if show_steps == True:

        # Show the image
        cv2.imshow('Centred Image', image)

        # Print centre coordinates
        print('Centre is at: ('+str(cX)+','+str(cY)+')')
        
    if close_windows == True:
        cv2.waitKey()
        cv2.destroyAllWindows()
    
    return image

#####

def contour_outline(image='test_port_0.jpg', method=0,show_final=False,show_steps=False,close_windows=False):
    """
    Definition:
    [image, contour] = contour_outline(image_name='test_port_0.jpg', method=0, steps_shown=False, close_windows=False)

    Inputs:
    1.

    Functionality:
    1. Retrieve image from file
    2. Resize image to correct size
    3. 
    7. Show (a) Original, (b) Grey-scale, (c) Threshold, (d) All contours, (e) Largest contour, (f) Largest inner contour

    Return:
    [im_resize, contours[max_child_index]]
    
    Outputs: 
    1. im_resize = resized image
    2. contours[max_child_index] = contour defining largest inner area

    Source:
    1. https://stackoverflow.com/questions/28677544/how-do-i-display-the-contours-of-an-image-using-opencv-python
    """

    if type(image) == str:
        # Open up file
        image = cv2.imread(image)
    else:
        # Assume it is a BGR list
        pass


    
    im_resize = ResizeWithAspectRatio(image.copy(), 600)

    im_border = external_rectangle(im_resize)
    """
    if show_steps == True:
        # Declare the images to display
        im_all_contours = im_resize.copy()
        im_max_contour = im_resize.copy()
        im_max_inner_contour = im_resize.copy()
    else:
        im_all_contours = im_resize
        im_max_contour = im_resize
        im_max_inner_contour = im_resize
    """
    im_all_contours = im_resize
    im_max_contour = im_resize
    im_max_inner_contour = im_resize
    # Convert to grey
    im_grey = cv2.cvtColor(im_border,cv2.COLOR_BGR2GRAY)
    
    if method == 1:
        # Mean
        im_grey = cv2.medianBlur(im_grey,5)
        im_thresh = cv2.adaptiveThreshold(im_grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    
    elif method == 2:
        im_grey = cv2.medianBlur(im_grey,5)
        im_thresh = cv2.adaptiveThreshold(im_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        
    else: # If method == 0 or else
        # Normal. Grey-scale the image
        ret,im_thresh = cv2.threshold(im_grey,127,255,0)

    # Find all contours
    contours, hierarchy = cv2.findContours(im_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Find maximum contour area!
    max_area_index = max_contour_area(contours)

    # Find maximum inner contour area
    max_child_index = find_max_inner_area(contours, hierarchy, max_area_index)

    if show_steps == True:
        cv2.imshow('Original', image) # Original colour image
        cv2.waitKey()
        cv2.imshow('Resized', im_resize) # Resized image
        cv2.waitKey()
        cv2.imshow('Grey scale', im_grey) # Grey-scale image
        cv2.waitKey()
        cv2.imshow('Threshold', im_thresh) # Thresholded image
        cv2.waitKey()
        # Draw contours
        cv2.drawContours(im_all_contours, contours, -1, (255,0,0), 1)
        cv2.imshow('All contours', im_all_contours) # All contours
        cv2.waitKey()

        # Draw maximum contour area!
        cv2.drawContours(im_max_contour, contours, max_area_index, (0,255,0),2) # This one works... I needed to put [] around the other one's 'contours'!!!
        cv2.imshow('Largest contour', im_max_contour) # Largest contour
        cv2.waitKey()
        
        # Draw maximum inner contour area
        cv2.drawContours(im_max_inner_contour, contours, max_child_index, (0,0,255),3) # This one works... I needed to put [] around the other one's 'contours'!!!
        cv2.imshow('Largest inner contour', im_max_inner_contour) # Largest inner contour

    elif show_final == True:
        cv2.drawContours(im_all_contours, contours, -1, (255,0,0), 1)
        cv2.drawContours(im_max_contour, contours, max_area_index, (0,255,0),2)
        cv2.drawContours(im_max_inner_contour, contours, max_child_index, (0,0,255),3)
        # I won't actually display the final...
        # cv2.imshow('Final', im_max_inner_contour)

    if close_windows == True:
        # Close all windows
        cv2.waitKey()
        cv2.destroyAllWindows()

    # Return image of max inner contour. Changed from im_resize
    return [im_max_inner_contour, contours[max_child_index]]

#contour_outline(image='test_port_0.jpg', method=0,show_steps=False,overlay=False,close_windows=False)

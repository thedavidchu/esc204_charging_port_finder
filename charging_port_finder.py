# Charging port finder

"""
Successfully finds hole in outline. Thank goodness <3! February 14, 2020
"""

import numpy as np
import cv2
from charging_port_finder_library import *

def charging_port_finder(image_name='test_port_2.jpg', method=0, show_final=False, show_steps=False, close_windows=False):
    """
    Definition:
    charging_port_finder(image_name='test_port_2.jpg', method=0, show_final=False, show_steps=False, close_windows=False)

    Inputs:
    1. image_name = a (valid) image file name
    2. method = whether the picture uses regular (0), Mean (1), or Gaussian (2)
    3. show_final = show final image
    4. steps_shown = whether the various contouring steps are shown (False=no show, True=show)
    5. close_windows = whether old windows should be closed

    Functionality: 
    1. Outputs centre of image
    >>IF steps are shown:
        2. Closes windows after each step
        3. Pauses for key input
    <<
    4. Shows final contour of charging port

    Returns:
    [image,[cX, cY]]

    Outputs:
    1. image = marked up image
    2. [cX, cY] = the centre of the charging port

    Common errors:
    1. Finds the port that you directly plug the charger into
        -> Fix -- same result
    2. Grey scaled image means that some borders blend in
        -> Fix with weighting colours?
    3. Invalid image name
        -> Fix with TRY, EXCEPT
    4. No contour detected
        -> Fix with TRY, EXCEPT
    5. No inner contour detected
        -> Fix with TRY, EXCEPT
    6. Incorrect contour detected
        -> Oops... Fix with
    7. Too large outline
    """
    
    # Input error testing
    """
    if type(image_name) != str:
        print('ERROR: type(image_name) != str\type(image_name)=' + str(type(image_name)))
        return -1
    elif image_name[-4:] != '.png' and image_name[-4:] != '.jpg':
        print('ERROR: image_name not .jpg or .png')
        return -1
    #elif image_name not in file:
    """
    if type(method) != int:
        print('ERROR: type(method) != int')
        return -1
    elif method<0 or method>2:
        print('ERROR: method<0 or method>2')
        return -1
    
    if type(show_steps) != bool or type(close_windows) != bool:
        print('ERROR: type(show_steps) != bool or type(close_windows) != bool')
        return -1

    [image, contour] = contour_outline(image_name, method, show_final, show_steps, close_windows)
    [cX, cY] = centre_finder(image, contour)

    if show_final == True:
        image=centre_target(image,contour,[cX,cY])

    return [image,[cX, cY]]

def camera_capture():
    """
    Source:
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
    """
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        try:
            [image, [cX, cY]] = charging_port_finder(frame,method=0, show_final=True, show_steps=False, close_windows=False)
        except:
            image = frame
            print("ERROR: Exception taken")
            pass
        
        # Display the resulting frame
        cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return 0

#[image, [cX, cY]] = charging_port_finder('test_port_2.jpg',0,True, True, True)
#cv2.imshow('image', image)
camera_capture()


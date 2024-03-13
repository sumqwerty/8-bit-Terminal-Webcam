#!/usr/bin/python3
import cv2
import curses
import sys
cap = ""
def start(stdscr):
    global cap
    try:
        cap = cv2.VideoCapture(int(sys.argv[1]))
    except:
        try:
            cap = cv2.VideoCapture(1)
        except:
            cap = cv2.VideoCapture(0)

    screen = curses.initscr()

    # Update the buffer, adding text at different locations
    num_rows, num_cols = screen.getmaxyx()

    black = [0,0,0]
    red = [0,0,255]
    green = [0,255,0]
    blue = [255,0,0]
    yellow = [0,255,255]
    magenta = [255,0,255]
    cyan = [255,255,0]
    white = [255,255,255]


    nBlack = 1
    nRed = 2
    nGreen = 3
    nBlue = 4
    nYellow = 5
    nMagenta = 6
    nCyan = 7
    nWhite = 8

    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_WHITE)



    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    try:
        curses.savetty()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (num_cols, num_rows))
            # Check if the frame is read successfully
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Get the height and width of the frame
            height, width, _ = frame.shape
            
            # Iterate over each pixel and set the red component to 255
            for y in range(num_rows-1):
                for x in range(num_cols-1):
                    r = int(frame[y, x, 2]);
                    g = int(frame[y, x, 1]);
                    b = int(frame[y, x, 0]);
                    br = (r+g+b)/3
                    if(br < 32):
                        screen.addch(y,x," ",curses.color_pair(nBlack) | curses.A_BOLD)
                    elif(br < 64):
                        screen.addch(y,x," ",curses.color_pair(nBlue) | curses.A_BOLD)
                    elif(br < 96):
                        screen.addch(y,x," ",curses.color_pair(nRed) | curses.A_BOLD)
                    elif(br < 128):
                        screen.addch(y,x," ",curses.color_pair(nBlue) | curses.A_BOLD)
                    elif(br < 160):
                        screen.addch(y,x," ",curses.color_pair(nGreen) | curses.A_BOLD)
                    elif(br < 192):
                        screen.addch(y,x," ",curses.color_pair(nYellow) | curses.A_BOLD)
                    elif(br < 224):
                        screen.addch(y,x," ",curses.color_pair(nCyan) | curses.A_BOLD)
                    else:
                        #screen.addch(y,x,"#")
                        screen.addch(y,x," ",curses.color_pair(nWhite) | curses.A_BOLD)

            # Draw the frame on a window
            if(len(sys.argv) > 2 and sys.argv[2] == 'd'):
                cv2.imshow('Webcam Frame', frame)
            screen.refresh()
            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        # Release the webcam when interrupted by the user (Ctrl+C)
        cap.release()
        cv2.destroyAllWindows()
        curses.endwin()
        print("Webcam released.")

    # Release the webcam when the script is done
    cap.release()
    cv2.destroyAllWindows()

curses.wrapper(start)

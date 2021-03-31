// C++ program for the above approach
#include <iostream>
#include <unistd.h>
#include <opencv2/opencv.hpp>
#include <time.h>
using namespace cv;
using namespace std;
  
// Driver code
int main(int argc, char** argv)
{
    // Read the image file as
    // imread("default.jpg");
    Mat image = imread("/home/awfulwaffle/out.ppm",
                       IMREAD_GRAYSCALE);
  
    // Error Handling
    if (image.empty()) {
        cout << "Image File "
             << "Not Found" << endl;
  
        // wait for any key press
        cin.get();
        return -1;
    }
  
    // Show Image inside a window with
    // the name provided
    // imshow("Window Name", image);  // not working
    // sleep(200);
  
    // Wait for any keystroke
    // waitKey(0);  // not working
    return 0;
}
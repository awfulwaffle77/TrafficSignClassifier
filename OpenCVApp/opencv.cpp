#include "opencv2/opencv.hpp"
#include "iostream"
#include "vector"

// #define DEFAULT_V4L_WIDTH  160
// #define DEFAULT_V4L_HEIGHT 120
#define MAX_VALS 25
#define WIDTH 160
#define HEIGHT 120

using namespace cv;

int main(int, char **)
{
    // Capture the Image from the webcam
    VideoCapture cap(0);

    cap.set(CV_CAP_PROP_FRAME_WIDTH, 160);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 120);
    cap.set(CV_CAP_PROP_CONVERT_RGB, false);
    // Get the frame
    Mat save_img, grey_img;
    cap >> save_img;
    
    cv::cvtColor(save_img, grey_img, CV_BGR2GRAY);

    if (save_img.empty())
    {
        std::cerr << "Something is wrong with the webcam, could not get frame." << std::endl;
    }

    int width, height;
    width = save_img.size[1];
    height = save_img.size[0];

    float* img = (float*)malloc(sizeof(float) * width * height);
    uchar* cimg = (uchar*)malloc(sizeof(uchar) * width * height);
    

    printf("RAW YUYV\n");
    int max = 0;
    for(int i = 0; i < height * width; i++){
        float x = (float)*(save_img.data + i);
        int z = (int)*(grey_img.data + i);
        // img[i] = (float)save_img.data[i]/255.0f;
        img[i] = x;
        cimg[i] = save_img.data[i];
        // printf("%f ", img[i]);
        printf("%d ", z);
        fflush(stdout);
        if(max == MAX_VALS){
            break;
        }
        max++;
    }
    // // save_img.data[height*width] = 0;
    // Mat _newPic(120,160,14,(void*)img);
    // Mat newPic(save_img);
    // newPic.data = cimg;
    // _newPic.data = (uchar*)img;
    // Save the frame into a file

    imwrite("newpic.jpg", save_img); // A JPG FILE IS BEING SAVED
    imwrite("newpic_grey.jpg", grey_img); // A JPG FILE IS BEING SAVED

    std::vector<uchar> diffBuffer;
    cv::imencode(".jpg",grey_img, diffBuffer);
    Mat ret = cv::imdecode(diffBuffer, 0);
    printf("Size: %d", diffBuffer.size());
    fflush(stdout);
    // cvEncodeImage(".jpg",)
    Mat image = imread("newpic_grey.jpg", IMREAD_GRAYSCALE); 
    cv::resize(image, image, cv::Size(WIDTH, HEIGHT));
    printf("\nJPG:\n");
    max = 0;
    for(int i = 0; i < MAX_VALS; i++){
        printf("%d:%d ", image.data[i], ret.data[i]);
        fflush(stdout);
    }
    // imwrite("_newpic.jpg", _newPic); // A JPG FILE IS BEING SAVED
}

#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

void followLine(string image_path) {
    Mat cap = imread(image_path);
    resize(cap, cap, Size(640, 480));
    Mat gray;
    cvtColor(cap, gray, COLOR_BGR2GRAY);

    int kernel_size = 5;
    Mat blur_gray;
    GaussianBlur(gray, blur_gray, Size(kernel_size, kernel_size), 0);

    int low_threshold = 50;
    int high_threshold = 150;
    Mat edges;
    Canny(blur_gray, edges, low_threshold, high_threshold);

    double rho = 1;
    double theta = CV_PI / 180;
    int threshold = 15;
    int min_line_length = 50;
    int max_line_gap = 20;
    Mat line_image = Mat::zeros(cap.size(), cap.type());

    vector<Vec4i> lines;
    HoughLinesP(edges, lines, rho, theta, threshold, min_line_length, max_line_gap);

    double sx1 = 0;
    double sx2 = 0;
    double sy1 = 0;
    double sy2 = 0;
    for (size_t i = 0; i < lines.size(); i++) {
        Vec4i l = lines[i];
        sx1 += l[0];
        sy1 += l[1];
        sx2 += l[2];
        sy2 += l[3];
    }
    sx1 /= lines.size();
    sx2 /= lines.size();
    sy1 /= lines.size();
    sy2 /= lines.size();
    line(line_image, Point(int(sx1), int(sy1)), Point(int(sx2), int(sy2)), Scalar(255, 0, 0), 5);

    Mat lines_edges;
    addWeighted(cap, 0.8, line_image, 1, 0, lines_edges);
    imshow("image", lines_edges);
    waitKey(0);
}

followLine("./test.jpg");
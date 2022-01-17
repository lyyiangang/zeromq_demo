#include <iostream>
#include <chrono>
#include <thread>
#include <opencv2/opencv.hpp>
#include <build/msg.pb.h>
#include <vector>

#include <zmq.hpp>

bool encode_buf = false;

int main(int argc, char *argv[])
{
    zmq::context_t context (1);
    zmq::socket_t publisher (context, ZMQ_PUB);
    publisher.set(zmq::sockopt::sndhwm, 2); // in case use too much memory, only cache 2 frame

    publisher.bind("tcp://127.0.0.1:5557");
    int i_frame (0);
    cv::Mat img_original = cv::imread("../cat.jpg");
    while(true) {
        char buff[255];
        sprintf(buff, "frame idx:%d", i_frame);
        cv::Mat img = img_original.clone();
        cv::putText(img, buff, cv::Point(0, 50), cv::FONT_HERSHEY_SCRIPT_COMPLEX, 1.0, cv::Scalar(255, 0, 0));

        RL::OcvMat serializableMat;
        if(encode_buf){
            // boost transpose
            std::vector<uchar> encoded_data;
            cv::imencode(".jpg", img, encoded_data);
            size_t dataSize = encoded_data.size();
            serializableMat.set_mat_data(encoded_data.data(), dataSize);
        }
        else{
            serializableMat.set_rows(img.rows);
            serializableMat.set_cols(img.cols);
            serializableMat.set_channels(img.channels());
            serializableMat.set_elt_type(img.type());
            serializableMat.set_elt_size((int)img.elemSize()); //channel = 3
            size_t dataSize = img.rows * img.cols * img.elemSize();
            serializableMat.set_mat_data(img.data, dataSize);
        }

        std::string encoded_msg;
        serializableMat.SerializeToString(&encoded_msg);
        //serializableMat.SerializeToOstream

        zmq::message_t zmq_msg(encoded_msg.size());
        memcpy ((void *) zmq_msg.data(), encoded_msg.c_str(), encoded_msg.size());
        publisher.send(zmq_msg);

        ++i_frame;
    }

    std::cout << "pub done" << std::endl;
    return 0;
}

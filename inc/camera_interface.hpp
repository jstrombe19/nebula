// WARNING::Auto-generated file; do not modify this file! 
// If change is necessary, update the corresponding yml and re-generate!
#pragma once

#ifndef _CAMERA_INTERFACE_H_
#define _CAMERA_INTERFACE_H_

class CameraInterface {
public:
     int x;
     double y;
     virtual int initialize(int a, int b) = 0;
     virtual int setExposure(int exposure) = 0;
     virtual int setGain(int gain) = 0;
};

#endif
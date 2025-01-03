#pragma once

#include "../inc/camera_interface.hpp"
#include "Spinnaker.h"
#include "SpinGenApi/SpinnakerGenApi.h"

class FLIR Blackfly S : public Camera Interface {
public:
    FLIR Blackfly S() = default;
    ~FLIR Blackfly S() override = default;

    int initialize(int a, int b) override;
    int setExposure(int exposure) override;
    int setGain(int gain) override;
};


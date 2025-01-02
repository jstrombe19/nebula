#ifndef FLIRBLACKFLYS_HPP
#define FLIRBLACKFLYS_HPP

#include "CameraInterface.hpp"

class FLIRBlackflyS : public CameraInterface {
public:
    FLIRBlackflyS() = default;
    ~FLIRBlackflyS() override = default;

    int initialize(int a, int b) override;
    int setExposure(int exposure) override;
    int setGain(int gain) override;
};

#endif // FLIRBLACKFLYS_HPP
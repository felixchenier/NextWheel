#ifndef _ADC_H_
#define _ADC_H_

#include <NextWheel.h>
#include <ADS8688.h>
#include "DataFrame.h"

class ADC
{
public:
    ADC();
    void begin();
    void update(ADCDataFrame& dataFrame);

private:
    ADS8688 m_ads8688;
};
#endif  // _ADC_H_

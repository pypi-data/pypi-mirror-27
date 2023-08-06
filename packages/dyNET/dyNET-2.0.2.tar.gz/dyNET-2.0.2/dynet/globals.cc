#include "dynet/globals.h"
#include "dynet/devices.h"
#include "dynet/timing.h"

namespace dynet {

std::mt19937* rndeng = nullptr;
Device* default_device = nullptr;
float weight_decay_lambda;
int autobatch_flag; 
int profiling_flag = 0;
NamedTimer timer;

}

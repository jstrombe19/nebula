#pragma once

#ifndef _MAIN_H_
#define _MAIN_H_

#include "../lib/third_party/zyre.cpp"


typedef struct NEBULA {
    int run_flag;
} Nebula;


int start_zyre_recv_thread(void);
void launch_zyre_recv(void);
int start_zyre_snd_thread(void);
void launch_zyre_snd(void);


#endif
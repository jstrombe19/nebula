#include <iostream>
#include <stdlib.h>
#include <stdbool.h>

#include "../inc/main.hpp"

int main(void) {
    std::cout << "hello, world!" << std::endl;

    NEBULA Nebula = {
        .run_flag = 0
    };

    // zyre_receive_thread();
    launch_zyre_recv();
    launch_zyre_snd();

    while(Nebula.run_flag == 0) {
        sleep(15);
    }

    sleep(15);
    return 0;
}


pthread_t zyre_recv_th, zyre_snd_th;

int start_zyre_recv_thread(void) {
    return pthread_create(&zyre_recv_th, NULL, zyre_receive_thread, NULL);
}

void launch_zyre_recv(void) {
    int zyre_recv_status = start_zyre_recv_thread();
    std::cout << "Launched zyre receive thread; status: " << zyre_recv_status << std::endl;
    return;
}

int start_zyre_snd_thread(void) {
    return pthread_create(&zyre_snd_th, NULL, zyre_send_thread, NULL);
}

void launch_zyre_snd(void) {
    int zyre_snd_status = start_zyre_snd_thread();
    std::cout << "Launched zyre receive thread; status: " << zyre_snd_status << std::endl;
    return;
}
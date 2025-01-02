#include <zyre.h>
#include <assert.h>
#include <string.h>
#include <iostream>

void* zyre_receive_thread(void* arg) {
    // Create a Zyre node
    zyre_t *node = zyre_new("receive-node");
    if (!node) {
        std::cerr << "Error creating Zyre receive node" << std::endl;
        // return 1;
        return arg;
    }

    // Set node name and start it
    zyre_set_header(node, "name", "Receive Node");
    int rc = zyre_start(node);
    if (rc != 0) {
        std::cerr << "Error starting Zyre node" << std::endl;
        // return 1;
        return arg;
    }

    // Join a group
    zyre_join(node, "my-group");

    // Send a message to the group
    // const char *msg = "Hello from C++";
    zyre_shouts(node, "my-group", "Hello from Receive Node!");

    // Receive messages
    while (true) {
        zmsg_t *msg = zyre_recv(node);
        if (!msg) {
            std::cerr << "Error receiving message" << std::endl;
            break;
        }

        char *group = zmsg_popstr(msg);
        char *sender = zmsg_popstr(msg);
        char *message = zmsg_popstr(msg);

        std::cout << "Received message from " << sender << " in group " << group << ": " << message << std::endl;

        zmsg_destroy(&msg);
        free(group);
        free(sender);
        free(message);

        sleep(1);
    }

    // Stop and destroy the node
    zyre_stop(node);
    zyre_destroy(&node);

    // return 0;
    return arg;
}

void* zyre_send_thread(void* arg) {
    // Create a Zyre node
    zyre_t *node = zyre_new("send-node");
    if (!node) {
        std::cerr << "Error creating Zyre send node" << std::endl;
        // return 1;
        return arg;
    }

    // Set node name and start it
    zyre_set_header(node, "name", "Send Node");
    int rc = zyre_start(node);
    if (rc != 0) {
        std::cerr << "Error starting Zyre send node" << std::endl;
        // return 1;
        return arg;
    }

    // Join a group
    zyre_join(node, "my-group");

    // Send a message to the group
    // const char *msg = "Hello from C++";
    zyre_shouts(node, "my-group", "Hello from Send Node!");

    // Receive messages
    while (true) {

        zyre_shouts(node, "my-group", "This is a message from the zyre send node!\n");

        zmsg_t *msg = zyre_recv(node);
        if (!msg) {
            std::cerr << "Error receiving message" << std::endl;
            break;
        }

        

        char *group = zmsg_popstr(msg);
        char *sender = zmsg_popstr(msg);
        char *message = zmsg_popstr(msg);

        std::cout << "Received message from " << sender << " in group " << group << ": " << message << std::endl;

        zmsg_destroy(&msg);
        free(group);
        free(sender);
        free(message);

        sleep(1);
    }

    // Stop and destroy the node
    zyre_stop(node);
    zyre_destroy(&node);

    // return 0;
    return arg;
}
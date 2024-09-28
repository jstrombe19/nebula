#include <zyre.h>
#include <string>
#include <iostream>

int main(void) {
    // Create a Zyre node
    zyre_t *node = zyre_new("my-node");
    if (!node) {
        std::cerr << "Error creating Zyre node" << std::endl;
        return 1;
    }

    // Set node name and start it
    zyre_set_header(node, "name", "C++ Node");
    int rc = zyre_start(node);
    if (rc != 0) {
        std::cerr << "Error starting Zyre node" << std::endl;
        return 1;
    }

    // Join a group
    zyre_join(node, "my-group");

    // Send a message to the group
    const char *msg = "Hello from C++";
    zyre_shout(node, "my-group", msg, strlen(msg));

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
    }

    // Stop and destroy the node
    zyre_stop(node);
    zyre_destroy(&node);

    return 0;
}
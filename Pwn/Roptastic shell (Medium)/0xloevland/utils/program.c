struct file_data {
    char buf[32];
    char path[64];
    uint32_t size;
};

static void fill_buffer(struct file_data *data) {
    char buf[512] = { 0 };
    printf("Data: ");
    ssize_t nread = read(STDIN_FILENO, buf, sizeof(buf) - 1);
    if (nread <= 0) {
        fprintf(stderr, "Failed read data: %s\n", strerror(errno));
        return;
    }

    memcpy(data->buf, buf, nread);
    printf("Done!\n\n");
}

static void buggy(void) {
    struct file_data data = { 0 };
    print_challenge_description();

    for (;;) {
        menu();
        int choice = get_int("> ");
        switch (choice) {
        case 1:
            fill_buffer(&data);
            break;
        case 2:
            print_stack_frame(&data);
            break;
        case 3:
            check_rop_chain();
            break;
        case 4:
            print_challenge_description();
            break;
        case 5:
            print_gadgets();
            break;
        case 6:
            lookup_symbol();
            break;
        case 7:
            add_string();
            break;
        case 8:
            return; /* quit */
        default:
            fprintf(stderr, "Invalid choice: %d\n", choice);
            break;
        }
    }
}

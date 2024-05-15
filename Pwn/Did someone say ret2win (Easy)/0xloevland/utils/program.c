struct file_data {
    char buf[32];
    char path[64];
    uint32_t size;
};

static void fill_buffer(struct file_data *data) {
    char buf[512] = { 0 };
    printf("Data: ");
    if (!fgets(buf, sizeof(buf), stdin)) {
        fprintf(stderr, "Failed read data: %s\n", strerror(errno));
        return;
    }

    // strip newline (if any)
    char *newline = strchr(buf, '\n');
    if (newline)
        *newline = '\0';

    strcpy(data->buf, buf);
    printf("Done!\n\n");
}

static void buggy(void) {
    struct file_data data = { 0 };

    data.size = 0x123;
    strcpy(data.path, "test.txt");

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
            /* trigger bug */
            break;
        case 4:
            return;
        default:
            fprintf(stderr, "Invalid choice: %d\n", choice);
            break;
        }
    }
}

static void win(void) {
    char *const args[] = {
        "sh",
        NULL,
    };
    printf("Great job! Spawning a shell...\n");
    execve("/bin/sh", args, environ);
    exit(EXIT_SUCCESS);
}

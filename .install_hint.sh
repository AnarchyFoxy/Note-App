#!/usr/bin/env bash

do_install() {
    # Check if 'make' command is available
    if ! command -v make >/dev/null 2>&1; then
        echo "Error: 'make' command not found. Please make sure 'make' is installed and in the PATH." >&2
        exit 1
    fi

    # Check if the 'Makefile' exists in the current directory
    if [[ ! -f "Makefile" ]]; then
        echo "Error: 'Makefile' not found in the current directory." >&2
        exit 1
    fi

    # Execute 'make install'
    make install

    # Check the return code of 'make' and print an error message if it fails
    if [[ $? -ne 0 ]]; then
        echo "Error: Installation failed. Please check the 'make install' command." >&2
        exit 1
    fi
}

# Call the 'do_install' function
do_install

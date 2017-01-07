# VulnServer

A buffer overfolow exploit for the crossfire Linux online multiplayer
RPG program. Note this is for a version compiled without stack smashing
protection support or Address Space Layout Randomization (ASLR) and
Data Execution Protection (DEP).

## Usage

    python main.py ip port payload

*   Optional parameters

    *   `-p`: send the given proof of concept buffer
    *   `-l int`: Send a buffer evenly divided in char numbers for binary tree search method
    *   `-u`: Send a unique string to determine the offset to the `EIP` register overwrite.
    *   `-t`: Test the offset to the `EIP` register.
    *   `-c`: Send a set of chars to test for bad characters.
    *   `-b`: Overwrite the `EIP` register with an address to a `JMP ESP` command and set a breakpoint on the entry to the shell code section.

*   No optional parameters will run the attack.

    *   Optionally specify an alternative payload with a relative address
    *   Payload format is msfvenom with the `-f python` flag

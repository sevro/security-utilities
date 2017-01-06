# SLMail Pwn

A script to execute a buffer overflow on SLMail 5.5 and get a reverse shell.
Also allows options to send a unique string `-u` which can be watched from a
debugger to demonstrate how the `EIP` was hijacked to redirect program
execution, and an option to send a test buffer `-t` that will overwite the
`EIP` with unique chars and everything on either side with identical bytes
for further demonstration.

## Usage

*   `-u`: Send a unique string to determine the offset to the `EIP` register overwrite.
*   `-t`: Test the offset to the `EIP` register.
*   `-c`: Send a set of chars to test for bad characters.
*   `-b`: Overwrite the `EIP` register with an address to a `JMP ESP` command and set a breakpoint on the entry to the shell code section.
*   No optional parameters will run the attack.

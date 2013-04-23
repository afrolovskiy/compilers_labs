#include <stdio.h>
#include <string.h>

#define UNKNOWN -1

struct context_type {
    int A, B, C, D;     // registers
    int CF, ZF;          // flags
};

struct vertex_type {
    int line_number;
    char cmd[4];
    void *operands;
    struct context_type* context;
    struct vertex_type** childs;
};

vertex_type* read_programm_graph(char* filename) {
   FILE *file = fopen (filename, "r" );
    if (file == NULL) {
        return NULL;
    }

    char line[32];
    int is_last = 0;
    vertex_type* vertex = (vertex_type*) malloc(sizeof(vertex_type));
    while(fgets(line, 32, file) ) {
        printf("%s",line);
        
        if (!is_last) {
            vertex->line_number = atoi(strtok(line, " \n"));
            strcpy(vertex->cmd, strtok(NULL, " \n"));
            if (strcmp(cmd, "MOV") == 0 || strcmp(cmd, "ADD") == 0 ||
                         strcmp(cmd, "ADC") == 0 || strcmp(cmd, "AND") == 0 ||
                         strcmp(cmd, "OR") == 0 || strcmp(cmd, "XOR") == 0 ||
                         strcmp(cmd, "LD") == 0) {
                char* operands = (char*) malloc(sizeof(char) * 2);
                operands[0] = strcpy(strtok(NULL, " ,\n"));
                if (strcmp(cmd, "LD") == 0) {
                    operands[1] = atoi(strtok(NULL, " ,\n"));
                } else {
                    operands[1] = strcpy(strtok(NULL, " ,\n"));
                }
                vertex->operands = operands;
            } else if (strcmp(cmd, "NEG") == 0 || strcmp(cmd, "INC") == 0 ||
                         strcmp(cmd, "DEC") == 0 ) {
                char* operands = (char*) malloc(sizeof(char) * 1);
                operands[0] = strcpy(strtok(NULL, " ,\n"));
                vertex->operands = operands;
            } else if (strcmp(cmd, "CLC") == 0 || strcmp(cmd, "STC") == 0) {
                printf("without operands\n");                                
            } else if (strcmp(cmd, "JUMP") == 0 || strcmp(cmd, "JZ") == 0 || 
                         strcmp(cmd, "JNZ") == 0  || strcmp(cmd, "JC") == 0  || 
                         strcmp(cmd, "JNC") == 0 || strcmp(cmd, "RET") == 0) {
                if (strcmp(cmd, "RET") == 0) {
                    is_last = 1;
                }             
               char* operands = (char*) malloc(sizeof(char) * 2);
                operands[0] = atoi(strtok(NULL, " \n"));
                vertex->operands = operands;
            } else {
                return NULL;          
            }
        } else {
            char *removed_count = strtok(line, " \n");
        }
    }


    return start_vertex;
}

    




int main() {
    vertex_type* v = read_programm_graph("input.txt");
    return 0;
}

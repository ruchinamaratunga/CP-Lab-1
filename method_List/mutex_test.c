#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <sys/time.h>

#define MAX 65535

struct node {
    int data;
    struct node *next;
};

int m = 0;
long number_of_thread;
struct node *root;

double m_fraction;
double i_fraction;
double d_fraction;

int m_opers;
int i_opers;
int d_opers;

struct timeval start, end;

int instructions[10000];

pthread_mutex_t mutex;

float time_diff(struct timeval *start,struct timeval *end) {
    return (end->tv_sec - start->tv_sec) + 1e-6*(end->tv_usec-start->tv_usec);
}

int Member(int value, struct node *linked_list) {
    struct node *current = linked_list;

    while (current != NULL && current->data < value) {
        current = current->next;
    }

    if (current == NULL || current->data >value) {
        return 0;
    } else {
        return 1;
    }
}

int Insert(int value, struct node **linked_list) {
    struct node *current_node = *linked_list;
    struct node *pred_p = NULL;
    struct node *temp_p;

    while (current_node != NULL && current_node->data < value) {
        pred_p = current_node;
        current_node = current_node->next;
    }

    if (current_node == NULL || current_node->data > value) {
        temp_p = (struct node*) malloc(sizeof(struct node));
        temp_p->data = value;
        temp_p->next = current_node;

        if (pred_p == NULL) {
            *linked_list = temp_p;
        } else {
            pred_p->next = temp_p;
        }
        return 1;
    } else {
        return 0;
    }
}

int Delete(int value, struct node **linked_list) {
    struct node *current = *linked_list;
    struct node *pred_p = NULL;

    while (current != NULL && current->data < value) {
        pred_p = current;
        current = current->next;
    }

    if (current != NULL && current->data == value) {
        if (pred_p == NULL) {
            *linked_list = current->next;
            free(current);
        } else {
            pred_p->next = current->next;
            free(current);
        }
        return 1;
    } else {
        return 0;
    }

}

void Print(struct node *root) {
    struct node *current = root;

    while(current->next !=NULL) {
        printf("(%d)\n |\n\\/\n",current->data);
        current = current->next;
    }
    printf("\n");
}

int Count(struct node *root) {
    struct node *current = root;
    int count = 0;
    while(current->next !=NULL) {
        current = current->next;
        count ++;
    }
    return count;
}

void getOperationCount(int* instructions, long* numOfThreads, int *m) {
    int me=0;
    int in=0;
    int d=0;
    int op;
    int opsForThread = (*m) / (*numOfThreads);

    for (size_t i = 0; i < (*numOfThreads); i++)
    {
            me=0;
            in=0;
            d=0;
        for (size_t j = 0; j < opsForThread; j++)
        {
            op = instructions[(opsForThread * i) + j];
            printf("operation Number is %d\n", op);
            if(op == 0){
                me++;
            } else if (op == 1) {
                in++;
            } else {
                d++;
            }
        }
        printf("For the %zu thread \n\tMember Count:- %d\n\tInsert Count:- %d\n\tDelete Count:- %d\n\t", i, me, in, d);
    }
    
}

void printInstruction(int* instructions, int* m) {
    for(int loop = 0; loop < (*m); loop++)
      printf("%d ", instructions[loop]);
}


void shuffle(int* instructions, int* m, int start, int end) {
    int temp, index;
    for (size_t i = start; i < end; i++)
    {
        index = rand() % (end - start);
        temp = instructions[index + start];
        instructions[index + start] = instructions[i];
        instructions[i] = temp;
    }
    // printInstruction(instructions, m);
}

void createInstructionList(int* instructions, int* m, double* m_f, double* i_f, double* d_f, long* thread_count) {
    m_opers = (*m) * (*m_f) / (*thread_count);
    i_opers = (*m) * (*i_f) / (*thread_count);
    d_opers = (*m) * (*d_f) / (*thread_count);
    int ops_for_thread = (*m) / (*thread_count);

    for (size_t k = 0; k < (*thread_count); k++) {
        for (size_t i = 0; i < m_opers; i++)
        {
            instructions[k*(ops_for_thread) + i] = 0;
        }

        for (size_t i = 0; i < i_opers; i++)
        {
            instructions[k*(ops_for_thread) + i + m_opers] = 1;
        }

        for (size_t i = 0; i < d_opers; i++)
        {
            instructions[k*(ops_for_thread) + i + i_opers + m_opers] = 2;
        }
        shuffle(instructions, m, k*(ops_for_thread), k*(ops_for_thread) + m_opers + i_opers + d_opers);
    }
}

void *execute(void *args) {
    int temp;
    int total = m/number_of_thread;
    long rank = (long) args;
    // printf("Thread Rank:- %ld\n", rank);

    for (size_t i = total * rank; i < total * rank + total; i++)
    {
        temp = rand() % MAX;
        if (instructions[i] == 0) {
            pthread_mutex_lock(&mutex);
            Member(temp, root);
            pthread_mutex_unlock(&mutex);
        } else if (instructions[i] == 1) {
            pthread_mutex_lock(&mutex);
            Insert(temp, &root);
            pthread_mutex_unlock(&mutex);
        } else {
            pthread_mutex_lock(&mutex);
            Delete(temp, &root);
            pthread_mutex_unlock(&mutex);
        }
    }
    return NULL;
}

int main(int argc, char *argv[]) {

    printf("Sequential Linked List Testing\n");
    
    number_of_thread = strtol(argv[1], NULL, 10);
    int n = atoi(argv[3]);
    m = atoi(argv[2]);
    // int instructions[m];

    m_fraction = atof(argv[4]);
    i_fraction = atof(argv[5]);
    d_fraction = atof(argv[6]);

    pthread_t thread_pool[number_of_thread];
    
    int random = rand() % MAX;
    root = (struct node*) malloc(sizeof(struct node));
    root->data = random;

    int i = 1;
    srand(time(NULL));
    while(i < n-1) {
        random = rand() % MAX; 
        if (Insert(random, &root) == 1) {
            i++;
        }
    }

    createInstructionList(instructions, &m, &m_fraction, &i_fraction, &d_fraction, &number_of_thread);
    // getOperationCount(instructions, &number_of_thread, &m);

    gettimeofday(&start,NULL);

    long thread;
    for (thread = 0; thread < number_of_thread; thread++) 
    {
        pthread_create(&thread_pool[thread], NULL, execute, (void *) thread);
    }

    for (thread = 0; thread < number_of_thread; thread++) {
        pthread_join(thread_pool[thread], NULL);
    }

    gettimeofday(&end,NULL);

    printf("Count : %d \n", Count(root));

    printf("Time : %0.6f\n", time_diff(&start, &end));

    return 0;
}

// gcc -pthread mutex_test.c -g -Wall -o mutex_test.out
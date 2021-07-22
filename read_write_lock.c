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

struct timeval start, end;

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

void *execute(void *args) {
    int total = m/number_of_thread;

    /**
     * 0 - member
     * 1 - insert
     * 2 - delete
    */
    int ops[3] = {0,1,2};

    int m_count = total*m_fraction;
    int i_count = total*i_fraction;
    int d_count = total*d_fraction;

    printf("m_count : %d\n",m_count);
    printf("i_count : %d\n",i_count);
    printf("d_count : %d\n",d_count);

    int selection = 0;
    int temp;

    while(m_count+i_count+d_count != 0) {
        selection = rand()%3;
        switch (ops[selection])
        {
        case 0:
            temp = rand() % MAX;
            if (m_count != 0) {
                Member(temp, root);
                m_count --;
            } else {
                ops[0] = -1;
            }
            break;

        case 1:
            temp = rand() % MAX;
            if (i_count != 0) {
                printf("%d\n",i_count);
                Insert(temp, &root);
                i_count --;
            } else {
                ops[1] = -1;
            }
            break;
        
        case 2:
            temp = rand() % MAX;
            if (d_count != 0) {
                Delete(temp, &root);
                d_count --;
            } else {
                ops[2] = -1;
            }
            break;        

        default:
            break;
        }
    }
    return NULL;
}

int main(int argc, char *argv[]) {

    printf("Sequential Linked List Testing\n");
    
    number_of_thread = strtol(argv[1], NULL, 10);
    int n = atoi(argv[2]);
    m = atoi(argv[3]);

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
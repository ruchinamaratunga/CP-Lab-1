# README

### Sequential

**build**
`gcc -pthread sequential_test.c -g -Wall -o sequential_test.out`

**run**

`./sequential.out <thread_num> <n> <m> <member_faction> <insert_fraction> <delete_fraction>`

### Mutex

**build**
`gcc -pthread mutex_test.c -g -Wall -o mutex_test.out`

**run**

`./mutex_test.out <thread_num> <n> <m> <member_faction> <insert_fraction> <delete_fraction>`

### Read Write Lock

**build**
`gcc -pthread read_write_lock.c -g -Wall -o read_write_lock.out`


**run**

`./read_write_lock.out <thread_num> <n> <m> <member_faction> <insert_fraction> <delete_fraction>`




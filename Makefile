target1: TARGET=sequential
target2: TARGET=mutex
target3: TARGET=rwlock

CC = g++
CPPFLAGS = -Wall 

sequential: sequential_test.o
	$(CC) $(CPPFLAGS) -o sequential_test.out sequential_test.o -lpthread

sequential_test.o: sequential_test.c
	$(CC) $(CPPFLAGS) -c sequential_test.c -lpthread

mutex: mutex_test.o
	$(CC) $(CPPFLAGS) -o mutex_test.out mutex_test.o -lpthread

mutex_test.o: mutex_test.c
	$(CC) $(CPPFLAGS) -c mutex_test.c -lpthread

clean:
	rm *.o *.out
CPPFLAGS = -g -fPIC -I.
LDFLAGS = -Wl,-rpath -Wl,.

all: libjson2pb.so test_json

clean:
	-rm -f *.o *.so *.a libjson2pb.so.* test test_pb2.py *.pyc

test_json: test_json.o test.pb.o libjson2pb.so -lprotobuf
test_json.o: test.pb.h

json2pb.o: bin2ascii.h

libjson2pb.so: json2pb.o
	$(CC) $(LDFLAGS) -o $@ $^ -Wl,-soname=$@ -Wl,-h -Wl,$@ -shared -L. -lcurl -lprotobuf -lstdc++ -ljansson

test.pb.h test.pb.cc: test.proto
	protoc --cpp_out=$(shell pwd) test.proto

test_pb2.py: test.proto
	protoc --python_out=$(shell pwd) test.proto

json2pb_python_unittest: test_pb2.py
	nosetests -v json2pb_unittest.py

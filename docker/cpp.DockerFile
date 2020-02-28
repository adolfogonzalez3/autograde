# A dockerfile for containers that can compile and run
# C++ programs.
from alpine

ENV test "#! \/usr\/bin\/env python3"
RUN apk add g++ python3
RUN pip3 install scons
RUN sed -i "1s/.*/$test/g" /usr/bin/scons
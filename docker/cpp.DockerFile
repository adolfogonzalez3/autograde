# A dockerfile for containers that can compile and run
# C++ programs.
from alpine

ENV test "#! \/usr\/bin\/env python3"
RUN apk add g++ python3 git unzip
RUN pip3 install scons
RUN sed -i "1s/.*/$test/g" /usr/bin/scons
RUN mkdir /build/

WORKDIR /home/
ADD https://github.com/adolfogonzalez3/autograde/archive/master.zip /home/
RUN unzip master.zip
WORKDIR /home/autograde-master/
RUN pip3 install .

WORKDIR /home/
COPY run.py .


ENTRYPOINT ["/usr/bin/python3", "run.py"]

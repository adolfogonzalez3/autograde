# A dockerfile for containers that can compile and run
# C++ programs.
from alpine

ENV test "#! \/usr\/bin\/env python3"
RUN apk add g++ python3 git
RUN pip3 install scons
RUN pip3 install git+https://github.com/adolfogonzalez3/autograde.git
RUN sed -i "1s/.*/$test/g" /usr/bin/scons
RUN mkdir /build/
WORKDIR /home/
COPY run.py .

#ENTRYPOINT ["/usr/bin/python3", "run.py"]

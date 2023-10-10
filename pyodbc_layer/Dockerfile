FROM lambci/lambda:build-python3.7
WORKDIR /root
RUN yum -y update
RUN curl ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.5.tar.gz -O && \
    tar xvzf unixODBC-2.3.5.tar.gz && \
    cd unixODBC-2.3.5 && \
    ./configure  --sysconfdir=/opt/python  --disable-gui --disable-drivers --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE --prefix=/home && \
    make install && \
    cd .. && \
    mv /home/* . && \
    mv unixODBC-2.3.5 unixODBC-2.3.5.tar.gz /tmp
RUN curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo && \
    yum -y install freetds e2fsprogs && \
    ACCEPT_EULA=Y yum -y install msodbcsql --disablerepo=amzn*
RUN export CFLAGS="-I/root/include" && \
    export LDFLAGS="-L/root/lib" && \
    pip install pyodbc requests "pymssql<3.0" adodbapi --upgrade -t .
RUN cp -r /opt/microsoft/msodbcsql .
RUN echo $'[ODBC Driver 13 for SQL Server]\n\
Driver      = ODBC Driver 13 for SQL Server\n\
Description = My ODBC Driver 13 for SQL Server\n\
Trace       = No'  > /root/odbc.ini
RUN echo $'[ODBC Driver 13 for SQL Server]\n\
Description = Microsoft ODBC Driver 13 for SQL Server\n\
Driver      = /opt/python/msodbcsql/lib64/libmsodbcsql-13.1.so.9.2\n\
UsageCount  = 1'  > /root/odbcinst.ini
RUN mkdir -p /opt/python && \
    cp /usr/lib64/libsybdb.so.5 /root/lib/libsybdb-89a09a88.so.5.1.0 && \
    cp -r /root/* /opt/python && \
    mv /opt/python/lib /opt && \
    mv /opt/python/bin /opt && \
    cd /opt && \
    rm -fr microsoft && \
    zip -r /python-odbc.zip .
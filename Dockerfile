FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y openjdk-8-jdk-headless python3 curl procps && rm -rf /var/lib/apt/lists/*
RUN curl -fL https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz | tar -xz -C /opt && mv /opt/hadoop-3.3.6 /opt/hadoop
ENV HADOOP_HOME=/opt/hadoop PATH=$PATH:/opt/hadoop/bin LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8
RUN echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>' > /opt/hadoop/etc/hadoop/core-site.xml
RUN echo '<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>' > /opt/hadoop/etc/hadoop/hdfs-site.xml
RUN echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
ENV HDFS_NAMENODE_USER=root HDFS_DATANODE_USER=root
CMD ["bash","-c","[ -d /tmp/hadoop-root/dfs/name ] || hdfs namenode -format -force; hdfs --daemon start namenode; hdfs --daemon start datanode; hdfs dfsadmin -safemode wait; tail -f /dev/null"]
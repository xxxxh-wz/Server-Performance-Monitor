# 使用Anaconda的官方Docker镜像
FROM --platform=linux/amd64 nvidia/cuda:11.3.1-base-ubuntu20.04


# 设置工作目录
WORKDIR /app

# 将当前目录下的文件复制到工作目录中
COPY . /app

# 安装Python和pip
RUN apt-get update && apt-get install -y python3 python3-pip

# 升级pip并安装psutil、Flask和nvitop（如果nvitop可通过pip安装）
RUN pip3 install --upgrade pip && pip3 install flask psutil nvitop Flask-HTTPAuth

# 暴露端口
EXPOSE 14120


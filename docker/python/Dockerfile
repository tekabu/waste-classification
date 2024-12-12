FROM python:3.9

ARG APP_PATH

RUN apt-get update && apt-get install -y \
    python3-rpi.gpio \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    python3-pip \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

COPY ./requirements.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN python -m pip install --upgrade pip

RUN pip install ultralytics==8.2.15 --default-timeout=600
RUN pip install opencv-python numpy
RUN pip install numpy

RUN pip install -r ./requirements.txt
     
RUN echo 'alias py="python"' >> ~/.bashrc
RUN echo 'alias ll="ls -l"' >> ~/.bashrc
RUN echo 'alias la="ls -la"' >> ~/.bashrc

WORKDIR /app

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["tail", "-f", "/dev/null"]

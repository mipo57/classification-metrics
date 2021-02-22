FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

USER ${USERNAME}
RUN mkdir /home/${USERNAME}/workspace 
WORKDIR /home/${USERNAME}/workspace

COPY metrics-classification/evaluate.py evaluate.py
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim as base

EXPOSE 8050

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y wget curl unzip gnupg
RUN apt-get update && apt-get install -y libgconf-2-4 libX11-xcb1 libXext6 libXss1 libxcb1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m spacy download en_core_web_md
WORKDIR /app
COPY . /app

FROM base as x86
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Install chromedriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver

FROM base as arm
RUN apt-get update

ARG TARGETPLATFORM

# Final stage that copies from the appropriate build stage
# FROM ${TARGETPLATFORM} as final
FROM x86 as x86-final
COPY --from=x86 /usr/bin/google-chrome-stable /usr/bin/google-chrome-stable
COPY --from=x86 /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 /usr/lib/x86_64-linux-gnu/libgconf-2.so.4
COPY --from=x86 /usr/lib/x86_64-linux-gnu/libX11.so.6 /usr/lib/x86_64-linux-gnu/libX11.so.6
COPY --from=x86 /usr/lib/x86_64-linux-gnu/libXext.so.6 /usr/lib/x86_64-linux-gnu/libXext.so.6
COPY --from=x86 /usr/lib/x86_64-linux-gnu/libXss.so.1 /usr/lib/x86_64-linux-gnu/libXss.so.1
COPY --from=x86 /usr/lib/x86_64-linux-gnu/libxcb.so.1 /usr/lib/x86_64-linux-gnu/libxcb.so.1

FROM arm as arm-final
COPY --from=base /app /app
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" root
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "embed.py"]

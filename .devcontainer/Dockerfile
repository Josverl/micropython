FROM mcr.microsoft.com/devcontainers/cpp:1-ubuntu-22.04
ENV apt-update='apt-get update -qq'
ENV apt-install='apt-get install -qq --no-install-recommends'

# Optionally install the cmake for vcpkg
ARG REINSTALL_CMAKE_VERSION_FROM_SOURCE="3.22.2"
COPY ./reinstall-cmake.sh /tmp/
RUN if [ "${REINSTALL_CMAKE_VERSION_FROM_SOURCE}" != "none" ]; then \
    chmod +x /tmp/reinstall-cmake.sh \
    && /tmp/reinstall-cmake.sh ${REINSTALL_CMAKE_VERSION_FROM_SOURCE}; \
    fi \
    && rm -f /tmp/reinstall-cmake.sh

# [Optional] Uncomment this section to install additional vcpkg ports.
# RUN su vscode -c "${VCPKG_ROOT}/vcpkg install <your-port-name-here>"

# Install additional packages.
RUN apt-get update -qq && \
    apt-get install -qq --no-install-recommends \
    build-essential \
    libffi-dev \
    pkg-config \
    python-pip \
    uncrustify=0.72.*

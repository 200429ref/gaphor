#!/bin/bash

set -euo pipefail

export MSYS2_FC_CACHE_SKIP=1

pacman --noconfirm --cachedir "/var/cache/pacman/pkg" -Suy

pacman --noconfirm --cachedir "/var/cache/pacman/pkg" -S --needed \
    git \
    make \
    mingw-w64-$MSYS2_ARCH-gcc \
    mingw-w64-$MSYS2_ARCH-gtk3 \
    mingw-w64-$MSYS2_ARCH-pkg-config \
    mingw-w64-$MSYS2_ARCH-cairo \
    mingw-w64-$MSYS2_ARCH-gobject-introspection \
    mingw-w64-$MSYS2_ARCH-python3 \
    mingw-w64-$MSYS2_ARCH-python3-gobject \
    mingw-w64-$MSYS2_ARCH-python3-cairo \
    mingw-w64-$MSYS2_ARCH-python3-pip \
    mingw-w64-$MSYS2_ARCH-python3-setuptools \
    p7zip dos2unix upx \
    mingw-w64-$MSYS2_ARCH-nsis \
    mingw-w64-$MSYS2_ARCH-wget

pip install poetry==1.0.3
poetry config virtualenvs.create false
poetry install
make translate
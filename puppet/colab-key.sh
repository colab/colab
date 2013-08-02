#!/bin/bash

mkdir -p ~colab/.ssh/ --mode=700
cp ~vagrant/.ssh/authorized_keys ~colab/.ssh/authorized_keys
chown -fR colab:colab ~colab/.ssh/

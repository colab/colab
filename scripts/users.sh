#!/bin/bash

# Make sure to create user colab and colabdev group
COLAB_USER=colab
COLAB_GROUP=colabdev

# Get user and group
COLAB_USER_EXISTS=`cat /etc/group | grep $COLAB_USER:`
COLAB_GROUP_EXISTS=`cat /etc/group | grep $COLAB_GROUP:`

# Errors
ERROR_NOT_ALLOWED=126
ERROR_ALREADY_EXIST=9

# Make sure colab user exist
if [ -e $COLAB_USER_EXISTS ]; then 
    sudo adduser $COLAB_USER; 
    LAST_CMD=`echo $?`
    if [ $LAST_CMD == $ERROR_NOT_ALLOWED ]; then
        echo "You don't have permission to create users"
        echo "Aborting installation"
        exit -1
    fi
fi

# Make sure colab group exist
if [ -e $COLAB_GROUP_EXISTS ]; then 
    sudo groupadd $COLAB_GROUP; 
    LAST_CMD=`echo $?`
    if [ $LAST_CMD == $ERROR_NOT_ALLOWED ]; then
        echo "You don't have permission to create groups"
        echo "Aborting installation"
        exit -1
    fi
fi



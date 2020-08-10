#!/bin/bash

ansible-playbook generate_data.yml
ansible-playbook revert.yml
rm host_vars/*
rm group_vars/switches.yml
# wal (web automation layer)

### The internet works for you.

[![Build Status](https://travis-ci.org/classmember/wal.svg?branch=master)](https://travis-ci.org/classmember/wal)

### Features:
* automate web tasks
* organize tasks
* easily control the tasks

### Installation:
```sh
pip install walscript
```

### Example script to list search results:
```wal
- go: duckduckgo.com
- click: q
- send_keys: test
- submit:
- save_screenshot:'screen.png
- foreach:
    - class: result__a
    - print_href: a
```

### Objectives:
* complete the yaml-based interpreter inspired by Saltstack, Ansible, and Fabric
* add json support
* add REST API
* organize scripts together into a repository
* create great support and documentation for DevOps platforms
* createa a micro-service server image to deploy as an application in enterprise networks

### Requirements:
* written in [python 3.6](https://www.python.org/)
* uses the [selenium](http://selenium-python.readthedocs.io/) web driver
* uses the [casperjs](http://phantomjs.org/) headless javascript based browser

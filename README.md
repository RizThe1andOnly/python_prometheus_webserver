# Python Prometheus Client and Web Server

This codebase will contain code and information I gather regarding python web servers using Flask as well as Prometheus. The objective here will be to set up a web-server using Flask that can be used by Prometheus to scrape some metrics. The other thing I will try to accomplish here is practice how to use the Prometheus client library for Python.

So far I know the Prometheus client libarary has means of creating a webserver built in but as a learning exercise I will attempt to set up my own Flask server to enable Prometheus to scrape metrics from some dummy source.

Will update this doc with info and knowledge as i go along.

---

Links to references:
- https://docs.microsoft.com/en-us/windows/python/web-frameworks
- https://flask.palletsprojects.com/en/2.0.x/
- 

---
## Goals

- Create a http endpoint using Flask and Gunicorn which will serve prometheus dummy metrics. 
    - The prometheus metrics will be forwarded to grafana for visualization.
        - Prometheus and Grafana will be run in Docker
            - Will have to figure out how to connect docker stuff to the non-docker stuff; easiest way to do it would be to use the ip address of the machine so containers can reach non-container applications.
            - Prometheus and Grafana will be run utilizing Docker Compose.
    - Prometheus metrics will be generated randomly though some python scripts running in background.
        - May utilize ThreadPoolExecutor if there are multi thread usage for this. Which there may be.
    - Flask and Gunicorn server will be run in WSL (Ubuntu).


### How to get there:
- Create and setup the dummy metrics reporter.
    - (11/20/2021) set up the multithreaded approach and test it.
- Set up Flask and Gunicorn server
    - (11/20/2021) have a demo on flask setup with gunicorn
        - Try to connect to server and get live (random) metrics from it.

---

## Starting up a Flask Server

Some components that are related to setting up a server:
- WSGI application:
    - Web Server Gateway Interfaces, specification that enables communication between wep applications and web servers. It just defines the standards on how software should be written so webservers can call it. Flask applications are WSGI applications that can be called by web-servers. 
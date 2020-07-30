# Python for Everyone

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mike-matera/python-for-everyone/main?urlpath=lab)

Learn Python with help and practice. These [Jupyter](https://jupyter.org/) notebooks support my [CIS-15](http://www.lifealgorithmic.com/cis-15a.html) class at [Cabrillo College](https://www.cabrillo.edu/). The notebooks teach the principles of programming with activities that give you practice and projects to challeng you.

## Using the Notebooks

It has never been easier to use this course content. Just click the "Binder" badge at the top of this page. The notebooks load with all of the lessons and labs ready to go. Binder sessions aren't saved but you can download individual notebooks to your computer and re-upload them to Binder next time. If you would like to take a deeper dive into the notebooks on your own computer the best way is to use the [Docker Hub](https://hub.docker.com/repository/docker/mikematera/python-for-everyone) images that are built from this repository. New to Docker? It's quite easy to get started! Follow the instructions to [install Docker](https://docs.docker.com/get-docker/). From the command line you can launch the Jupyter Lab server with this command: 

```bash 
$ docker run -it -p 8888:8888 mikematera/python-for-everyone
```

The result is just like starting a local Jupyter server and you will be able to connect to Jupyter using the `127.0.0.1` URL provided.

## Contributing

> This project is under active development. Please contact me if you want to collaborate. 

## License 

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

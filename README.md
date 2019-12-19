# Python for Everyone

Learn Python with help and practice. These [Jupyter](https://jupyter.org/) notebooks support my [CIS-15](http://www.lifealgorithmic.com/cis-15a.html) class at [Cabrillo College](https://www.cabrillo.edu/). The notebooks teach the principles of programming with activities that give you practice and projects to challeng you.

## Using the Notebooks

The notebooks have interconnected content and require installed modules. This section will show you how to get the notebooks running on your desktop. Before you begin you will need to have the following software installed:

- Python >= 3.6 (with `pip` and `venv`)
- [Bash](https://www.gnu.org/software/bash/), [zsh](https://www.gnu.org/software/bash/) or a compatible shell
- [Git](https://git-scm.com/)

Installing Python and Git will vary based on your OS. Linux, Mac and Windows are all supported. Bash or zsh are installed by default on Mac and Linux. On Windows you can get get Ubuntu from the [Microsoft Store](https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6). 

Clone the repository:
```
git clone https://github.com/mike-matera/python-for-everyone.git 
```

Create a virtual environment inside of the project directory:

```
cd python-for-everyone
python3 -m venv venv 
```

Activate the virtual environment:

```sh
. ./venv/bin/activate
```

Packages used by the notebooks are listed in `requirements.txt`. Update `pip` to the latest version then use pip to install the requirements:

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

The notebooks use `import` to access code in this project directory structure. In order for this to work the root directory of the repository should be in `$PYTHONPATH`.

```sh
PYTHONPATH=$(pwd) jupyter lab welcome.ipynb
```

Jupyter tries to open a new browser tab. If a browser doesn't appear after starting Jupyter open a tab manually and visit the URLs that are shown in Jupyter's output.

## Hosting

I use [AWS Cloud9](https://aws.amazon.com/cloud9/) in my course. Cloud9 is web based and users access the Jupyter server from the same browser that's connected to the Cloud9 instance. Cloud9 gives the class a uniform and predictable way to access their code and they never have to worry about losing files, but it costs money. I use `t2.micro` instances with `8GB` of storage (which is the default for Cloud9). The cost of an instance is:

- Runtime: $0.0116 per Hour ([prices](https://aws.amazon.com/ec2/pricing/on-demand/))
- Storage: $0.10 per GB-month of provisioned storage
 ([prices](https://aws.amazon.com/ebs/pricing/))

A student that uses the desktop for 10 hours a week (or 40 hours a month) will cost about $1.26 per month. Cloud9 stops the VM when a user is not connected. It's possible to disable that behavior and if a student does, the cost (based on 720 hours) will be about $9.15 per month. I get credit through [AWS Educate](https://aws.amazon.com/education/awseducate/) that covers the cost of my classes.

There are other Jupyter hosting solutions that I have not tried.

## Contributing

> This project is under active development. Please contact me if you want to collaborate. 

## License 

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

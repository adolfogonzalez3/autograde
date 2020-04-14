
Autograde is a tool for compiling and running code.

Autograde uses SCONS to manage compiling the code. The advantage of SCONS is that since its a python package, installing autograde installs SCONS. Autograde has the ability to look for source files in given build paths allowing for quick and easy compiling and running. 

Autograde can discover source files automatically using the method collect_source. This is used in the run.py and batch_run.py to simplify the process of compiling and running simple programming assignments.

Autograde can use the docker installation on your computer to run the compiling and running steps in a containerized environment. The advantages of this include:
* Faster build times (from what I've seen on my work machine)
* No leftover build files
* More secure (Docker has improved its security so far, preventing escalation within the container)

Install autograde using
```bash
pip install git+https://github.com/adolfogonzalez3/autograde.git
```

You can compile a folder with auto discovery using
```bash
python -m autograde.run <program-folder>
```

If you have docker then you can compile a folder using
```bash
python -m autograde.run --use_container <program-folder>
```
#!/usr/bin/env python
"""Run jupyter at CC-IN2P3, setup the LSST stack, and display it localy."""


import os
import sys
import subprocess
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import yaml
import numpy as np


DEFAULT_CONFIG = os.getenv("HOME") + "/.stackyter-config.yaml"


def string_to_list(a):
    """Transform a string with coma separated values to a list of values."""
    return a if isinstance(a, list) or a is None else a.split(",")


def get_default_config():
    """Get the stackyter default configuration file if it exists."""
    if os.getenv("STACKYTERCONFIG") is not None:  # set up by the user
        return yaml.load(open(os.getenv("STACKYTERCONFIG"), 'r'))
    elif os.path.exists(DEFAULT_CONFIG):  # default location
        print("INFO: Loading default configuration file from", DEFAULT_CONFIG)
        return yaml.load(open(DEFAULT_CONFIG, 'r'))
    else:
        return None


def read_config(config, key=None):
    """Read a config file and return the right configuration."""
    if key is not None:
        if key in config:
            print("INFO: Using configuration '%s'" % key)
            config = config[key]
        else:
            raise IOError("Configuration `%s` does not exist. Check your default file." % key)
    elif len(config) > 1:
        if 'default_config' in config:
            print("INFO: Using default configuration '%s'" % config['default_config'])
            config = config[config['default_config']]
        else:
            raise IOError("You must define a 'default_config' in you configuration file.")
    else:
        config = config[list(config)[0]]
    return config


def get_config(config, configfile):
    """Get the configuration for stackyter is any."""
    if configfile is not None:
        config = configfile
    if config is not None:
        if os.path.exists(config):
            # The user has given configuration file
            print("INFO: Using default configuration from", config)
            config = read_config(yaml.load(open(config, 'r')))
        else:
            default_config = get_default_config()
            if default_config is None:
                raise IOError("No default configuration file found. Check the doc.")
            # Get the selected configuration from the config file
            config = read_config(default_config, key=config)
    else:
        # Look for a default configuration file
        default_config = get_default_config()
        if default_config is not None:
            config = read_config(default_config)
    return config


if __name__ == '__main__':

    description = """Run Jupyter on CC-IN2P3, setup the LSST stack, and display it localy."""
    prog = "stackyter.py"
    usage = """%s [remote] [options]""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', default=None,
                        help='Name of the configuration to use, taken from your default '
                        'configuration file (~/.stackyter-config.yaml or $STACKYTERCONFIG). '
                        "Default if to use the 'default_config' defined in this file. "
                        'The content of the configuration file will be overwritten by any '
                        'given command line options.')
    parser.add_argument('-f', '--configfile', default=None,
                        help='Configuration file containing a set of option values. The content '
                        'of this file will be overwritten by any given command line options. '
                        'Mostly for testing your configuration file before making it the default.')
    parser.add_argument('-u', '--username',
                        help="Your CC-IN2P3 user name. If not given, ssh will try to "
                        "figure it out from you ~/.ssh/config or will use your local user name.")
    parser.add_argument('-H', "--host", default="cca7.in2p3.fr",
                        help="Name of the target host. This option may allow you to avoid potential"
                        " conflit with the definition of the same host in your $HOME/.ssh/config, "
                        "or to connect to an other host than the CC-IN2P3 ones (Jupyter must also "
                        "be available on these hosts). Default if to connect to CC-IN2P3.")
    parser.add_argument('-w', "--workdir", default=None,
                        help="Your working directory at CC-IN2P3")
    parser.add_argument('-j', "--jupyter", default="notebook",
                        help="Either launch a jupiter notebook or a jupyter lab.")
    parser.add_argument("--vstack", default='v14.0',
                        help="Version of the stack you want to set up."
                        " (E.g. v14.0, w_2017_43 or w_2017_43_py2)")
    parser.add_argument("--packages", default='lsst_distrib',
                        help="A list of packages you want to setup. Coma separated from command"
                        " line, or a list in the config file. You can use the `lsst_distrib` "
                        "package to set up all available packages from a given distrib.")
    parser.add_argument("--desc", action='store_true', default=False,
                        help="Setup a DESC environment giving you access to DESC catalogs "
                        "('proto-dc2_v2.0' is for now the only available catalog). This option "
                        "overwrites the '--vstack' and '--mysetup' options.")
    parser.add_argument("--mysetup", default=None,
                        help="Path to a setup file (at CC-IN2P3) that will be used to set up the "
                        "working environment. Be sure that a Python installation with Jupyter (and"
                        " jupyterlab) is available to make this work. The LSST stack won't be set "
                        "up in this mode. 'vstack', 'libs', 'bins' and 'labpath' options will be "
                        "ignored.")
    parser.add_argument("--libs", default=None,
                        help="Path(s) to local Python librairies. Will be added to your PYTHONPATH."
                        " Coma separated to add more than one paths, or a list in the config file."
                        " A default path for jupyter will be choose if not given.")
    parser.add_argument("--bins", default=None,
                        help="Path(s) to local binaries. Will be added to your PATH."
                        " Coma separated to add more than one paths, or a list in the config file."
                        " A default path for jupyter will be choose if not given.")
    parser.add_argument("--labpath", default=None,
                        help="You must provide the path in which jupyterlab has been installed"
                        " in case it differs from the (first) path you gave to the --libs option."
                        " A default path for jupyterlab will be choose if not given.")
    
    args = parser.parse_args()
        
    # Do we have a configuration file
    config = get_config(args.config, args.configfile)
    if config is not None:
        for opt, val in args._get_kwargs():
            # only keep option value from the config file
            # if the user has not set it up from command line
            if opt in config and '--' + opt not in sys.argv:
                setattr(args, opt, config[opt])

    # A valid username (and the corresponding password) is actually the only mandatory thing we need
    args.username = "" if args.username is None else args.username + "@"

    # Make sure that we have a list (even empty) for packages
    args.packages = string_to_list(args.packages)

    # A random port number is selected between 1025 and 65635 (included) for server side to
    # prevent from conflict between users.
    port = np.random.randint(1025, high=65635)

    # Start building the command line that will be launched at CC-IN2P3
    # Open the ssh tunnel to a CC-IN2P3 host
    cmd = "ssh -X -Y -tt -L 20001:localhost:%i %s%s << EOF\n" % \
          (port, args.username, args.host)

    # Print the hostname; for the record
    cmd += "hostname\n"

    # Add local libraries to the PATH and PYTHONPATH
    args.libs = string_to_list(args.libs)
    args.bins = string_to_list(args.bins)

    # Move to the working directory
    if args.workdir is not None:
        cmd += "if [[ ! -d %s ]]; then echo 'Error: directory %s does not exist'; exit 1; fi\n" % \
               (args.workdir, args.workdir)
        cmd += "cd %s\n" % args.workdir

    if args.mysetup is not None:
        # Use the setup file given by the user to set up the working environment (no LSST stack)
        cmd += "source %s\n" % args.mysetup
    elif args.desc:
        # Setup a DESC environment with an easy access to DESC catalogs
        desc_env = "/sps/lsst/dev/DESC/setup.sh"
        cmd += "source %s\n" % desc_env
    else:
        # Setup the lsst stack and packages if a version of the stack if given
        if args.vstack is not None:
            cmd += "source /sps/lsst/software/lsst_distrib/%s/loadLSST.bash\n" % args.vstack
        if args.packages is not None:
            cmd += ''.join(["setup %s\n" % package for package in args.packages])

        # First get the runing version of python
        if args.vstack == 'v13.0':
            cmd += "export VPY=2 \n"
            cmd += "export FVPY=2.7 \n"
        else:
            cmd += "export VPY=\`ls /sps/lsst/software/lsst_distrib/%s/python/"  % args.vstack + \
                   " | egrep -o 'miniconda[2,3]' | egrep -o '[2,3]'\`\n"
            cmd += "if [ \$VPY -eq 2 ]; then export FVPY=2.7; else export FVPY=3.6; fi\n"

        # Use default paths to make sure that jupyter is available
        jupybin = "/sps/lsst/dev/nchotard/demo/python\$VPY/bin"
        jupylib = "/sps/lsst/dev/nchotard/demo/python\$VPY/lib/python\$FVPY/site-packages"
        if args.libs is None:
            args.libs = [jupylib]
        else:
            args.libs.append(jupylib)
        if args.bins is None:
            args.bins = [jupybin]
        else:
            args.bins.append(jupybin)

        # Add ds9 to the PATH
        cmd += 'export PATH=\$PATH:/sps/lsst/dev/nchotard/local/bin\n'

        # We also need to add the following path to set up a jupyter lab
        if args.jupyter == 'lab':
            if args.labpath is not None:
                # Use the path given by the user
                cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % args.labpath
            elif args.labpath is None and args.libs is not None:
                # Take the first path of the --libs list
                cmd += 'export JUPYTERLAB_DIR="%s/share/jupyter/lab"\n' % \
                       args.libs[0].split('/lib')[0]
            elif args.labpath is None and args.libs is not None:
                # That should not happen
                raise IOError("Give me a path to the install directory of jupyterlab.")

    # Add local libraries to the PATH and PYTHONPATH
    if args.libs is not None:            
        for lib in args.libs:
            cmd += 'export PYTHONPATH="\$PYTHONPATH:%s"\n' % lib
    if args.bins is not None:
        for lbin in args.bins:
            cmd += 'export PATH="\$PATH::%s"\n' % lbin

    # Launch jupyter
    cmd += 'jupyter %s --no-browser --port=%i --ip=127.0.0.1 &\n' % (args.jupyter, port)

    # Get the token number and print out the right web page to open
    cmd += "export servers=\`jupyter notebook list\`\n"
    # If might have to wait a little bit until the server is actually running...
    cmd += "while [[ \$servers != *'127.0.0.1:%i'* ]]; " % port + \
           "do sleep 1; servers=\`jupyter notebook list\`; echo \$servers; done\n"
    cmd += "export servers=\`jupyter notebook list | grep '127.0.0.1:%i'\`\n" % port
    cmd += "export TOKEN=\`echo \$servers | sed 's/\//\\n/g' | " + \
           "grep token | sed 's/ /\\n/g' | grep token \`\n"
    cmd += "printf '\\n    Copy/paste this URL into your browser to run the notebook" + \
           " localy \n\\x1B[01;92m       'http://localhost:20001/\$TOKEN' \\x1B[0m\\n\\n'\n"

    # Go back to the jupyter server
    cmd += 'fg\n'

    # And make sure we can kill it properly
    cmd += "kill -9 `ps | grep jupyter | awk '{print $1}'`\n"

    # Close
    cmd += "EOF"

    # Run jupyter
    subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)

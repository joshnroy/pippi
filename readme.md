# Pippi: Computer music with python

This is pre-release software. I am working toward a stable 1.0 and would very much appreciate bug reports, feedback and pull requests!

## Installation

> Note: pippi is currently only compatible with Python 2.x

In order to build the C extensions that pippi uses for most DSP, you will need to install the Python development headers.

On debian (including ubuntu & raspbian) systems:

    apt-get install python-dev

On arch linux the headers are already installed along with the main `python2` package.

### To install last published version from pip:

    pip install pippi

### To install latest version from source:

Make sure you have `pip` installed on your system, since pippi uses the version of `setuptools` distributed with pip for installation.

To use the interactive features you will need to install `pyalsaaudio` (for ALSA support on linux) or `pyaudio` for experimental cross-platform audio support on OSX and Windows.

You may need to install the `libasound2-dev` package on debian systems with `apt-get` before you will be able to install `pyalsaaudio`.

If you're trying the experimental `pyaudio` support, you may need to install `portaudio` on your system first.

To use optional MIDI support with the interactive features you will need to install `pygame` via `pip`.

When you have the dependencies you selected installed, from the root of the pippi repository run:
    
    python setup.py install


### Now What?

Here's a simple 'Hello World!' style example you can try at the python console:

    >>> from pippi import dsp
    >>> out = dsp.tone(dsp.stf(5), freq=220, amp=0.2)
    >>> out = dsp.env(out, 'hann')
    >>> dsp.write(out, 'hello')
    'hello.wav'

Here's a slightly more interesting example:

    >>> from pippi import dsp
    >>> out = [ dsp.tone(dsp.stf(5), 55 * i, 'sine2pi', 0.2) for i in range(1, 5) ]
    >>> out = [ dsp.env(o, dsp.randchoose(['hann', 'tri', 'sine'])) for o in out ]
    >>> out = dsp.mix(out)
    >>> dsp.write(out, 'helloagain')
    'helloagain.wav'

[More documentation at Read The Docs.](http://pippi.readthedocs.org)


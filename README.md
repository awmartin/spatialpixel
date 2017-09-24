# Spatial Pixel Code

This repository hosts libraries and code featured at [Spatial Pixel](http://spatialpixel.com),
consisting of functionality for computational designers.

These sketches are written in Python and [Processing](http://processing.org) 3+, in both the Python and Java modes.

## Using These Libraries

_More to come..._

1. First, download a modified version of Python Mode for Processing that provides Python library support.
2. Create a `libraries_python` folder in your sketchbook.
3. Clone this repo into a new subfolder of that folder.

    $ cd libraries_python
    $ git clone https://github.com/awmartin/spatialpixel

The structure should look like this:

    YOUR SKETCHBOOK/
      |- ...
      |
      |- libraries/
      |- libraries_python/
      |   |- spatialpixel/
      |- modes/
      |   |- PythonMode
      |
      |- ...

Start Processing in Python Mode and you should be good to go.

## Available Libraries and Components

- data
  - kml
  - geojson
- google
  - directions
  - streetview
- mapping
  - slippymapper
- path
  - randomwalk
- ui
  - button
  - control
  - interface
  - panner
  - text
  - toggle
- util
  - lazyimages

## Using the code without the modified Python Mode

The problem with using the modified Python mode is that the Processing IDE will tempt you into upgrading when there are new "official" releases of Python mode. Until I can lobby to get the library support into the official code line, there are two ways to use the code.

1. Use the modified Python mode.
2. Copy/paste individual files into your sketches and import them.

With the second option, you might need to hack the import statements in the files according to your sketch's structure, which can be a bit tedious but shouldn't be too difficult. I recommend the first option.

## Contributing

If you'd like to contribute, please fork the repo, create a new branch, and send a pull request with a descriptive message. Screenshots are very helpful. :)

## License

MIT License. See [LICENSE.txt](LICENSE.txt).

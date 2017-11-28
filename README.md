# Spatial Pixel Code

This repository hosts libraries and code for computational designers featured at [Spatial Pixel](http://spatialpixel.com).

These sketches are written in Python and [Processing](http://processing.org) 3+, in both the Python and Java modes. Thanks to [Jonathan Feinberg](http://mrfeinberg.com) and his team for [processing.py](http://py.processing.org) and the [recent change to support site-packages](https://github.com/jdf/processing.py/commit/c8362cad7c1f565ea598b6b9d5f38d9ed3f8d45d).

## Using These Libraries

1. Ensure you have Python mode release 3027 or later.
2. It will create a `site-packages` folder in your `libraries` folder. This is where your Python dependencies can live (.py files) to be shared among all your Python mode sketches.
3. Download `spatialpixel.zip` from the [latest release](https://github.com/awmartin/spatialpixel/releases). Don't download the archives called "Source Code" as they won't include dependencies.

Alternatively for step 3, you can clone this repository:

    $ cd libraries/site-packages
    $ git clone https://github.com/awmartin/spatialpixel --recursive

The structure should look like this:

    YOUR SKETCHBOOK/
      |- ...
      |
      |- libraries/
      |   |- site-packages/
      |       |- spatialpixel/
      |       |- ...
      |
      |- ...

Start Processing in Python Mode and you should be able to import any of the modules included here. e.g. `import spatialpixel.mapping.slippymapper as slippymapper`

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

## Other ways to use the code

If you want to experiment with hacking at a library or component, one way is to copy/paste individual files into your sketches. You can also follow the contribution guidelines below and send pull requests.

## Contributing

If you'd like to contribute, please fork the repo, create a new branch, and send a pull request with a descriptive message. Screenshots are very helpful. :)

## License

MIT License for all the original code in this repo (see [LICENSE.txt](LICENSE.txt)). All dependencies maintain the licenses of their respective projects, all referenced in the `third_party` folder.

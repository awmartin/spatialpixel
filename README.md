# Spatial Pixel Code

This repository hosts libraries and code for computational designers featured at [Spatial Pixel](http://spatialpixel.com).

These sketches are written in Python and [Processing](http://processing.org) 3+, in both the Python and Java modes. Thanks to [Jonathan Feinberg](http://mrfeinberg.com) and his team for [processing.py](http://py.processing.org) and the [recent change to support site-packages](https://github.com/jdf/processing.py/commit/c8362cad7c1f565ea598b6b9d5f38d9ed3f8d45d).

## Using These Libraries

1. Ensure you have Python mode release 3027 or later.
2. It will create a `site-packages` folder in your `libraries` folder. This is where your Python dependencies can live (.py files) to be shared among all your Python mode sketches.
3. Clone this repo into a new subfolder of `site-packages`.


    $ cd libraries/site-packages
    $ git clone https://github.com/awmartin/spatialpixel

Alternatively, for step 3, you can download the archive of this repo and unzip it into `site-packages`. You'll have to come back periodically to download updates this way if you're not familiar with git.

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

## Other ways to use the code

If you want to experiment with hacking at a library or component, one way is to copy/paste individual files into your sketches. You can also follow the contribution guidelines below and send pull requests.

## Contributing

If you'd like to contribute, please fork the repo, create a new branch, and send a pull request with a descriptive message. Screenshots are very helpful. :)

## License

MIT License. See [LICENSE.txt](LICENSE.txt).

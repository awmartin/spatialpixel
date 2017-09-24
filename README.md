# Spatial Pixel Code

This repository hosts libraries and code featured at [Spatial Pixel](http://spatialpixel.com),
consisting of functionality for computational designers.

These sketches are written in Python and [Processing](http://processing.org) 3+, in both the Python and Java modes.

## Using These Libraries

1. Ensure you have Python mode release 3027 or later. (See note below if 3027 isn't yet available.)
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

### Before Version 3027 is officially released...

If 3027 hasn't been released yet, I've created an archive you can use in the meantime. [Download it here.](https://s3.amazonaws.com/spatialpixel/releases/PythonMode.zip)

To use, quit Processing and move any pre-existing PythonMode folder in the `modes` folder into a subfolder called `old`. This is just to back it up in case something goes wrong. Then unzip this zip file and place it into `modes`, effectively replacing the older folder.

    YOUR SKETCHBOOK/
      |- ...
      |
      |- libraries/
      |   |- site-packages/
      |       |- mylib.py
      |- modes/
      |   |- old/
      |   |- PythonMode/     <-- unzip the archive to live here
      |
      |- ...

Once you've restarted Processing, Python mode should create the `site-packages` folder for you. If it didn't, create the folder yourself.

To test, create a `mylib.py` file in the `site-packages` folder. Then in a Processing Python mode sketch, you should be able to `import mylib`.

Note that this particular build has been tested on macOS, but not Windows yet.


## Contributing

If you'd like to contribute, please fork the repo, create a new branch, and send a pull request with a descriptive message. Screenshots are very helpful. :)

## License

MIT License. See [LICENSE.txt](LICENSE.txt).

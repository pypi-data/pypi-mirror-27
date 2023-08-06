Wii.py
======

Wii.py from #Wii.py on EFNet is a GPL licensed Wii library written in and for Python. It provides editors and classes for many file types and files present on the Wii, especially files in banners. It was created as a replacement for the unreleased and never to be released pywii, written by marcan, but has since expanded in some areas that pywii did not cover and not completed others (such as Wii Optical Disc editing) that pywii has support for.

Derived from: http://wiibrew.org/wiki/Wii.py

Installation
------------

::

    pip install Wii.py

Features
--------

* Loading and easy editing of U8 archives
* Simple, easy classes for TMDs and Tickets, with methods to load from and save to files
* Simple Title object to hold information about a title
    * Can pack into a WAD
    * Can download from NUS
    * Can unpack into a directory structure
* Convert images to/from PNG and TPL
* Convert WAV sound the BNS sound (used in banners)
* Add IMET and IMD5 headers
* Load and extract files from Wii Optical Discs
* Create a fake 'NAND' that you can modify with a Python version of ES and ISFS from libogc
* Decompress LZ77 compressed files
* Work with these file types:
    * loc.dat
    * CCF
    * iplsave.bin
    * uid.sys
    * content.map
    * config.dat (network config)
    * setting.txt
    * Savegames

Dependencies
------------

* PyCrypto
* PIL (Python Imaging Library)
* wxPython (optional) if you want to use the toScreen() method of the TPL object

PyCrypto and PIL (Pillow fork) are part of the PyPI dependencies.  wxPython is not required if you're not doing GUI stuff.

Usage
-----

Unfortunately, there is no real documentation yet. For now, here's some short examples showing just how short your code can be.

Downloads the latest System Menu from NUS and packs it into a WAD::

    import Wii
    Wii.NUS.download(0x000000010000002).dumpFile("SystemMenu-latest.wad")

Downloads System Menu version 289, and replaces content index 0 with the file "patch.bin", changes the title id to 1-3, then saves to the WAD "patched.wad"::

    import Wii
    sysmenu = Wii.NUS.download(0x000000010000002, 289)
    sysmenu[0] = open("patch.bin", "rb").read()
    sysmenu.tmd.setTitleID(0x0000000100000003)
    sysmenu.tik.setTitleID(0x0000000100000003)
    sysmenu.dumpFile("patched.wad")

Unpacks the first command line argument WAD to the folder "inside"::

    import Wii, sys
    wadf = Wii.WAD.loadFile(sys.argv[1])
    wadf.dumpDir("inside")

Unpacks the first command line argument U8 archive to the folder "unpacked"::

    import Wii, sys
    u8archive = Wii.U8.loadFile(sys.argv[1])
    u8archive.dumpDir("unpacked")

Converts the png as the first argument to a TPL saved in "out.tpl"::

    import Wii, sys
    TPL(sys.argv[1]).toTPL("out.tpl")

Converts the Sound.wav to Sound.bns::

    import Wii, wave
    wav = wave.open("sound.wav", 'rb')
    channelnumber = wav.getnchannels()
    buffer = wav.readframes(wav.getnframes())
    samplerate = wav.getframerate()
    wav.close()
    bns = Wii.BNS()
    bns.create_bns(buffer, samplerate, channelnumber)
    bns.write("sound.bns")

Credits
-------

This library was written by Xuzz, SquidMan, megazig, Matt_P, Omega and The Lemon Man. It contains the LZ77 code written by marcan, with few modifications. Credit goes to Daeken for the Struct.py module.

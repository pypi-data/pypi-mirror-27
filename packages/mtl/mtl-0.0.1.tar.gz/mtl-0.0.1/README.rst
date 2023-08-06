mtl
===

``mtl`` (**m**\ oving **t**\ ime-**l**\ apse) is a ``python`` tool to create time lapse animation from photos taken not from a fixed camera (hence 'moving') with identifiable markers.

``mtl`` align time series photos with markers (3 or 4 markers) provided as .TPS file (digitized with `TPSDig software <http://life.bio.sunysb.edu/morph/soft-dataacq.html>`_), and output the aligned photos and time-lapse movie.

requires
--------
``mtl`` is based on `OpenCV <https://opencv.org/>`_'s implementation of affine transformation (with 3 markers provided) and perspective transformation (with 4 markers provided). A nice explanation on the transformation methods can be found `here <https://docs.opencv.org/3.2.0/da/d6e/tutorial_py_geometric_transformations.html>`_.

Output of time-lapse video is based on `ffmpeg <https://www.ffmpeg.org/>`_. To use ``mtl``, both ``OpenCV`` and ``ffmpeg`` are required.

how to use?
-----------
1. Use as a ``python`` package. 

2. Directly use the ``mtl.py`` ``python`` module, if you prefer. Download the `file <https://github.com/jinyung/mtl/blob/master/mtl/mtl.py>`_.

``mtl`` can be directly used as command line script, with the following arguments:

  -h, --help         show this help message and exit
  -t, --tps 	     path to tps file containing landmarks for alignments
  -i, --img	     path to the directory containing images to be aligned
  -s, --sep          separator between individual and time in image name.
                     NOTE: use single quote (') for special character in Unix
                     systems

Alternatively, ``mtl`` can be imported into ``python``:

  >>> from mtl import align

The main function of ``mtl`` is ``align``, which provides more options. For further details run:
 
  >>> help(align)

preparing images and markers file
---------------------------------
``mtl`` supports batch processing of multiple time series photos. Different time series (such as 'individuals') and time points should be indicated in the file name of the images. For examples, ``1-1.tif``, ``1-2.tif``, ..., ``1-100.tif`` and ``a-1.tif``, ``a-2.tif``, ..., ``a-100.tif`` will be processed as two different time series of '1' and 'a' with time points of 1, 2, ..., 100. These images should be placed in a single directory. A dash '-' is used to separate the time series and time points here so this should be instructed to the program. Only a single ``.TPS`` file is required for processing multiple time series photos, and it should contains markers for all images in the directory to be processed. 




Image extraction using a template. Uses homography and feature matching,
and stores results in a SQLite database for faster reprocessing. Usage:

.. code-block:: python

    from image_extract.extract import Extracter
    ex = Extracter()
    ex.crop_images(image_directory, crop_template, file_extension)

Successful crops are extracted to a directory called ``successful_crops``,
directly underneath ``image_directory``. Each template used creates a subdirectory, named after its
MD5:

.. code-block:: plain

    image_directory
        - img1.jpg
        - …
        - imgn.jpg
        - successful_crops
            - 2a1bdab44c5e81af34f47f3395a3da7e
                - img1_cropped.jpg

Call ``ex.summary(path)`` to see information on extracted crops for a given directory.

Call ``ex.delete(path[, template_md5])`` to delete extracted crops for a given template.
If no template value is given, all extracted crops in that directory are removed.

For best results, the template image should be of the same (or similar) resolution
as the image from which the crop is to be extracted.



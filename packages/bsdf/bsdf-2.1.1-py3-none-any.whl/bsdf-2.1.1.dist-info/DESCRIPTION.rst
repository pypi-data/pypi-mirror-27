Python implementation of the Binary Structured Data Format (BSDF).

BSDF is a binary format for serializing structured (scientific) data.
See http://bsdf.io for more information.

This is the reference implementation, which is relatively relatively
sophisticated, providing e.g. lazy loading of blobs and streamed
reading/writing. A simpler Python implementation is available as
``bsdf_lite.py``.

This module has no dependencies and works on Python 2.7 and 3.4+.

Note: on Legacy Python (Python 2.7), non-Unicode strings are encoded as bytes.


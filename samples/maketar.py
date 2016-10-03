################################################
# This file illustrates how to create a tar
# archive of a directory from your python code.
# This code will create a tar archive from the
# directory exdir which contains some files.
# The archive is called exdir.tar.
################################################

# The necessary header file
import tarfile

# Open the specified archive file (e.g. exdir.tar).
# If the archive does not already exit, create it.
tar = tarfile.open("exdir.tar", "w:gz")

# Add the exdir/ directory to the archive
tar.add("exdir/")

# Close the archive file
tar.close()


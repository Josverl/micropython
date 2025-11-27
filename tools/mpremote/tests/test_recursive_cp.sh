#!/bin/bash
set -e

echo -----
mkdir -p $TMP/a $TMP/a/b
touch $TMP/a/x.py $TMP/a/b/y.py
ls $TMP/a | sort
ls $TMP/a/b | sort

# TODO
echo -----
touch $TMP/y.py
ls $TMP | sort

# Recursive copy to a directory that doesn't exist. The source directory will
# be copied to the destination (i.e. bX will the same as a).
echo -----
cp -r $TMP/a $TMP/b1
cp -r $TMP/a/ $TMP/b2
cp -r $TMP/a $TMP/b3/
cp -r $TMP/a/ $TMP/b4/

# Recursive copy to a directory that does exist. The source directory will be
# copied into the destination (i.e. bX will contain a copy of a).
echo -----
mkdir $TMP/c{1,2,3,4}
cp -r $TMP/a $TMP/c1
cp -r $TMP/a/ $TMP/c2
cp -r $TMP/a $TMP/c3/
cp -r $TMP/a/ $TMP/c4/

echo -----
find $TMP | sort

echo -----
rm -rf $TMP/b{1,2,3,4} $TMP/c{1,2,3,4}



# Now replicate the same thing using `mpremote cp`.

# Recursive copy to a directory that doesn't exist. The source directory will
# be copied to the destination (i.e. bX will the same as a).
echo -----
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a $TMP/b1
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a/ $TMP/b2
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a $TMP/b3/
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a/ $TMP/b4/

# Recursive copy to a directory that does exist. The source directory will be
# copied into the destination (i.e. bX will contain a copy of a).
echo -----
mkdir $TMP/c{1,2,3,4}
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a $TMP/c1
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a/ $TMP/c2
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a $TMP/c3/
$MPREMOTE $MPREMOTE_FLAGS cp --no-verbose -r $TMP/a/ $TMP/c4/

echo -----
find $TMP | sort

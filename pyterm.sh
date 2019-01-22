#!/bin/bash

# GS
# Started: 16 Nov. 2018 
# Updated: 1 Dec. 2018 

# Get the directory of this script so I can cd into its directory so that when I run it, it will write its logs to the
# "logs" folder herein, relative to the dir of this script itself:
# - See: https://stackoverflow.com/a/246128/4561887
# - Make sure to have `#!/bin/bash` at the top of this script too!
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"

# Run this script.
# - Be sure to forward the incoming arguments on to the python script using the `"$@"` part. 
# - See: https://stackoverflow.com/a/14340879/4561887
cd $DIR
python3 ./pyterm.py "$@"

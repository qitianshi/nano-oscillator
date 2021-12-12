#! /bin/sh

# Checks OS, then activates Python venv.
case "$OSTYPE" in

    "darwin"*)
        echo "I'm a Mac."
        source env/bin/activate ;;

    "msys"*)
        echo "I'm a PC."
        .\venv\Scripts\activate ;;

    "linux-gnu"*)
        echo "I'm Linux."
        source env/bin/activate ;;

    *)
        echo "I'm confused: $OSTYPE"
        exit ;;

esac

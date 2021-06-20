# eXist-db Config
This repo contains eXist-db configuration files implementing [Production Use - Good Practice](https://exist-db.org/exist/apps/doc/production_good_practice). Configuration files are located in a subdirectory per eXist-db version (e.g. `./v5.1.1/`). Diffs to the original release files are kept to a minimum.

It also includes a python script that takes care of backing up and overwriting target files.

## Prepare
```
git clone https://github.com/eXistSolutions/existdb-config.git
cd existdb-config
```

## Usage (python - with backup)
```
./existdb-config.py -s ./v5.1.1/ -t ../exist-distribution-5.1.1/
```

This will
* create a timestamped backup tar file named `existdb-config_${timestamp}.tar` in the target folder `../exist-distribution-5.1.1/`
* copy over config fragments for a eXist-db 5.1.1

To undo the changes extract the backup tar archive at its location.
```
cd ../exist-distribution-5.1.1/
tar xf existdb-config_${timestamp}.tar
```

## Usage (manual - NO backup)
```
cp -a ./v5.1.1/ ../exist-distribution-5.1.1/
```

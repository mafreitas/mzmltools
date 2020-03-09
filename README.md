# MZMLTOOLS
## Python script to perform OpenMS transformations on MzML

```bash
usage: mzmltools.py [-h] -i filename -o filename [--ms1_threshold value]
                    [--ms2_threshold value]

mzmltools

optional arguments:
  -h, --help show this help message and exit
  -i filename, --input filename
  -o filename, --output filename
  --ms1_threshold value
  --ms2_threshold value
```

## Docker usage
A Dockerfile is also provided to assist with building and running the utility inside a docker container.

### To build the docker image

```
docker build -t mzmltools .
```

## To Run the docker image

```
docker run --rm -it -v $PWD:/share mzmltools
```

Change directories to /share inside the docket container and run the utility as described above.
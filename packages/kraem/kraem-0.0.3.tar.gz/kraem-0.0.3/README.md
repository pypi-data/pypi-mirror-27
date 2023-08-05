kraem (cram)
=

Kraem is a tool for compressing images in a folder recursively to a new folder which inherits the hierarchy from the source folder. You can also automatically upload the files to Google Cloud Storage bucket.  

This project is under development.

Installation and usage
---

```bash
$ pip install kraem
```

```bash
$ kraem -source uncompressed -destination compressed -quality 85 -gcs my-bucket-on-gcs
```

```bash
usage: kraem [-h] [-source SOURCE] [-destination DESTINATION]
              [-quality QUALITY] [-gcs GCS]

Compress images from a folder recursively to a new folder

optional arguments:
  -h, --help            show this help message and exit
  -source SOURCE        source directory
  -destination DESTINATION
                        destination directory
  -quality QUALITY      adjust image quality for compression
  -gcs GCS              Google Cloud Storage bucket
```

Missing
-
* Upload to Dropbox, Google Drive, AWS bucket and Azure
* Scaling
* Black and white filter
* Statistics (output in the CLI)

Google Cloud Storage
-
There are two possibilites to upload files to your GCS bucket. You can either:

1. use gcloud cli to handle the authentication
```bash
$ gcloud auth application-default login
```

2. add GOOGLE_APPLICATION_CREDENTIALS env variable to the zshrc/bashrc file
```bash
export GOOGLE_APPLICATION_CREDENTIALS='path/to/service-account.json'
```
How to get a service-account.json file https://developers.google.com/identity/protocols/application-default-credentials

###########
ELECTRICITY
###########

static file management

This provides an easier way to sync static files to the Amazon S3 and Rackspace CDN. It can upload an entire directory recursively applying public permissions.

It attempts to only sync files that have changed by comparing the MD5 hash.

#. you need a ~/.boto file to sync to amazon
#. rackspace cdn is not yet supported but is planned

Install from pip::

    pip install -e git+https://github.com/digitaldreamer/electricity.git#egg=electricity


This installs the electric package::

    # python
    from electricity.backends.amazon import AmazonCDN

    cdn = AmazonCDN(path, bucket)
    cdn.sync()

    cdn.flush()
    cdn.put()
    cdn.upload(filename, file_path)

    AmazonCDN.get_or_create_bucket(cdn, bucket_name)
    AmazonCDN.delete_bucket(cdn, bucket_name)


and makes the electric_sync bash script available::

    # bash
    electric_sync /path/to/directory <bucket name> -cdn <cdn type>

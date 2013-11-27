#!/usr/bin/env python
import argparse
import os
import sys

from electricity.backends.amazon import AmazonCDN


def amazon_sync(bucket, path):
    cdn = AmazonCDN(path, bucket)
    cdn.sync()


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', action='store', help="The path to the directory to sync")
    parser.add_argument('bucket', action='store', help="The bucket to sync into")
    parser.add_argument('-cdn', action='store', default='amazon', help="The CDN to sync to")
    results = parser.parse_args()

    if results.cdn == 'amazon':
        amazon_sync(results.bucket, results.directory)
    else:
        print 'ERROR: unsupported CDN:%s' % results.cdn

if __name__ == '__main__':
    main()

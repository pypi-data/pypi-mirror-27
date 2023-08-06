import io
import logging

import boto3
import botocore
from six.moves import http_cookiejar


logger = logging.getLogger(__name__)


class S3CookieJar(http_cookiejar.LWPCookieJar):
    bucket = None
    filename = None
    encryption_key = None

    def __init__(self, bucket=None, filename=None, encryption_key=None, *args, **kwargs):
        super(S3CookieJar, self).__init__(*args, **kwargs)
        self.bucket = bucket
        self.filename = filename
        self.encryption_key = encryption_key

    def save(self, filename=None, ignore_discard=False, ignore_expires=False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(http_cookiejar.MISSING_FILENAME_TEXT)

        logger.info("Saving cookiejar to s3://%s/%s" % (self.bucket, filename))

        session = boto3.Session()

        f = io.BytesIO()
        f.write(b"#LWP-Cookies-2.0\n")
        f.write(self.as_lwp_str(ignore_discard, ignore_expires).encode())
        f.seek(0)

        if self.encryption_key:
            kms = boto3.client("kms")
            r = kms.encrypt(KeyId=self.encryption_key, Plaintext=f.getvalue())

            f = io.BytesIO(r["CiphertextBlob"])

        s3 = session.resource("s3")
        bucket = s3.Bucket(self.bucket)
        bucket.upload_fileobj(f, filename)

    def load(self, filename=None, ignore_discard=False, ignore_expires=False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(http_cookiejar.MISSING_FILENAME_TEXT)

        logger.info("Loading cookiejar from s3://%s/%s" % (self.bucket, filename))
        f = io.BytesIO()

        session = boto3.Session()
        s3 = session.resource("s3")
        bucket = s3.Bucket(self.bucket)

        try:
            bucket.download_fileobj(filename, f)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                # Don't error if the cookiejar doesn't exist yet
                logger.info("Received 404 loading cookiejar, file doesn't exist yet")
                return
            raise

        if self.encryption_key:
            kms = boto3.client("kms")
            r = kms.decrypt(CiphertextBlob=f.getvalue())
            f = io.BytesIO(r["Plaintext"])

        f = io.StringIO(f.getvalue().decode())

        try:
            self._really_load(f, filename, ignore_discard, ignore_expires)
        finally:
            f.close()

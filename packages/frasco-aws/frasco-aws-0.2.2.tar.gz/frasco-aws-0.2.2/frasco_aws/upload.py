from frasco_upload.backends import StorageBackend, file_upload_backend
from frasco import current_app


@file_upload_backend
class S3StorageBackend(StorageBackend):
    name = 's3'

    def save(self, file, filename, force_sync=False):
        kwargs = dict(filename=filename, content_disposition_filename=file.filename,
            bucket=self.get_option('upload_bucket'), acl=self.get_option('upload_acl'),
            prefix=self.get_option('upload_filename_prefix'))

        if not force_sync and self.get_option('upload_async') and current_app.features.exists('tasks'):
            tmpname = current_app.features.upload.save_uploaded_file_temporarly(file, filename)
            current_app.features.tasks.enqueue('upload_file_to_s3',
                stream_or_filename=tmpname, mimetype=file.mimetype, delete_source=True, **kwargs)
        else:
            current_app.features.aws.upload_file_to_s3(file, filename, **kwargs)

    def url_for(self, filename, **kwargs):
        bucket = self.get_option('upload_bucket')
        if self.get_option('upload_signed_url'):
            b = current_app.features.aws.s3_connection.get_bucket(bucket)
            k = b.get_key(filename)
            kwargs.setdefault('expires_in', self.get_option('upload_s3_urls_ttl'))
            return k.generate_url(**kwargs)
        return 'https://%s.s3.amazonaws.com/%s' % (bucket, filename)

    def delete(self, filename, force_sync=False):
        if not force_sync and self.get_option('upload_async') and current_app.features.exists('tasks'):
            current_app.features.tasks.enqueue('delete_s3_file', filename=filename)
        else:
            current_app.features.aws.delete_s3_file(filename)

    def get_option(self, key):
        return self.options.get(key, current_app.features.aws.options.get(key))
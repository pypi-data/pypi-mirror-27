from frasco import Feature, action, cached_property
import boto
import os
from tempfile import NamedTemporaryFile


class AwsFeature(Feature):
    name = 'aws'
    ignore_attributes = ['s3_connection']
    defaults = {'upload_bucket': None,
                'upload_filename_prefix': '',
                'upload_acl': 'public-read',
                'upload_async': False,
                'upload_signed_url': False,
                'upload_s3_urls_ttl': 3600,
                'set_content_dispotion_header_with_filename': True,
                'charset': None,
                'use_sig_v4': False,
                'region_name': None,
                'connect_params': {},
                'set_contents_headers': {}}

    @cached_property
    def s3_connection(self):
        kwargs = {'aws_access_key_id': self.options.get('access_key'),
                  'aws_secret_access_key': self.options.get('secret_key')}

        if self.options['use_sig_v4']:
            if not boto.config.get('s3', 'use-sigv4'):
                boto.config.add_section('s3')
                boto.config.set('s3', 'use-sigv4', 'True')
            if self.options['region_name']:
                kwargs['host'] = 's3.%s.amazonaws.com' % self.options['region_name']
            else:
                kwargs['host'] = 's3.amazonaws.com'

        kwargs.update(self.options['connect_params'])
        if self.options['region_name']:
            return boto.s3.connect_to_region(self.options['region_name'], **kwargs)
        return boto.connect_s3(**kwargs)

    @action()
    def upload_file_to_s3(self, stream_or_filename, filename, bucket=None, prefix=None,
                          acl=None, mimetype=None, charset=None, delete_source=False,
                          content_disposition_filename=None):
        b = self.s3_connection.get_bucket(bucket or self.options['upload_bucket'])
        prefix = prefix or self.options.get('upload_filename_prefix', '')
        k = b.new_key(prefix + filename)
        acl = acl or self.options['upload_acl']
        headers = {}
        if self.options['set_content_dispotion_header_with_filename']:
            headers['Content-Disposition'] = 'attachment;filename="%s"' % (content_disposition_filename or filename)
        if mimetype:
            headers['Content-Type'] = mimetype
        if charset or self.options['charset']:
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'binary/octet-stream' # S3 default mimetype
            headers['Content-Type'] += '; charset=%s' % (charset or self.options['charset'])
        headers.update(self.options['set_contents_headers'])
        is_filename = isinstance(stream_or_filename, (str, unicode))
        if is_filename:
            k.set_contents_from_filename(stream_or_filename, headers, policy=acl)
        else:
            k.set_contents_from_string(stream_or_filename.read(), headers, policy=acl)
        if is_filename and delete_source:
            os.remove(stream_or_filename)

    @action(default_option='filename')
    def delete_s3_file(self, filename, bucket=None, prefix=None):
        b = self.s3_connection.get_bucket(bucket or self.options['upload_bucket'])
        prefix = prefix or self.options.get('upload_filename_prefix', '')
        b.delete_key(prefix + filename)


try:
    import upload
except ImportError:
    pass

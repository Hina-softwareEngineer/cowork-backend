
import os
import  mimetypes
import datetime
from supabase import create_client
from django.conf import settings
from storages.utils import clean_name, ReadBytesWrapper, is_seekable
from storages.backends.s3  import S3StaticStorage

class SupabaseStorage(S3StaticStorage):

    def __init__(self, **setting):

        self.gzip =  False
        self.gzip_content_types  =  (
                    "text/css",
                    "text/javascript",
                    "application/javascript",
                    "application/x-javascript",
                    "image/svg+xml",
                )
        self.supabase_url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.supabase = create_client(self.supabase_url, self.key)

    def  exists(self, name):
        return False

    def _normalize_name(self, name):
        return  name
    
    def _save(self, name, content):
        cleaned_name = clean_name(name) 
        current_time = datetime.datetime.now().isoformat()
        splitted_filename = cleaned_name.split(".")
        n = len(splitted_filename)
        cleaned_name  = "".join([splitted_filename[i] for i in range(n - 1)])
        cleaned_name = cleaned_name + current_time +  splitted_filename[n - 1]
        name = self._normalize_name(cleaned_name)
        params = self._get_write_parameters(name, content)

        if is_seekable(content):
            content.seek(0, os.SEEK_SET)

        file_data = content.read()
        
        result = self.supabase.storage.from_(settings.AWS_STORAGE_BUCKET_NAME).upload(file=file_data,path=cleaned_name, file_options=params)
        # if result.get('error'):
        #     raise Exception(f"Upload failed: {result['error']['message']}")

        return cleaned_name

    def url(self, name, parameters=None, expire=None, http_method=None):
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(clean_name(name))
        res = self.supabase.storage.from_(settings.AWS_STORAGE_BUCKET_NAME).get_public_url(name)
        return res
    
    def _get_write_parameters(self, name, content=None):
        params = {}

        if "ContentType" not in params:
            _type, encoding = mimetypes.guess_type(name)
            content_type = getattr(content, "content_type", None)
            content_type = content_type or _type or self.default_content_type

            params["content-type"] = content_type
            if encoding:
                params["ContentEncoding"] = encoding

        return params

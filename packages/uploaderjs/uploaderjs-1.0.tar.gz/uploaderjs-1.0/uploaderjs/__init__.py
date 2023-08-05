import os
import shutil

import requests


class UploaderJsError(Exception):
	pass


class UploaderJs(object):
	def __init__(self, token, version='v1', endpoint='https://api.uploaderjs'):
		self.token = token
		self.endpoint = '%s/%s' % (endpoint, version)

	def __call(self, url, **kwargs):
		r = requests.get('%s/%s' % (self.endpoint, url), auth=('Bearer', self.token), **kwargs)
		r.raise_for_status()
		return r

	def retrieve(self, form_id, destination, overwrite=False):
		files = self.list_files(form_id)
		for _file in files:
			self.save_file(_file.get('file_id'), os.path.join(destination, _file.get('file_filename')), overwrite)

	def list_files(self, form_id):
		r = self.__call('/forms/%s/files' % form_id)
		return r.json()

	def save_file(self, file_id, destination, overwrite=False):
		path = os.path.normpath(destination)

		if not os.path.exists(os.path.dirname(path)):
			raise UploaderJsError('Destination dir "%s" not exists.' % path)

		if not overwrite and os.path.exists(path):
			raise UploaderJsError('Destination file "%s" exists.' % path)

		r = self.__call('/files/%s' % file_id, stream=True)

		with open(destination, 'wb') as out_file:
			shutil.copyfileobj(r.raw, out_file)

		return True

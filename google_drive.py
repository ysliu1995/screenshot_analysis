from __future__ import print_function
import io
import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

class Drive:

	# If modifying these scopes, delete the file token.json.
	SCOPES = 'https://www.googleapis.com/auth/drive'

	def upload_download(self):
		"""Shows basic usage of the Drive v3 API.
		Prints the names and ids of the first 10 files the user has access to.
		"""
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('client_secret.json', self.SCOPES)
			creds = tools.run_flow(flow, store)
		service = build('drive', 'v3', http=creds.authorize(Http()))

		# 上傳成 Google 文件檔，讓 Google 雲端硬碟自動辨識文字
		CO2_sorted_file = self.get_file_name('input/CO2')
		PM25_sorted_file = self.get_file_name('input/PM25')
		CO2_res_list = [self.upload(service, 'CO2', '{}.jpg'.format(item)) for item in CO2_sorted_file]
		PM25_res_list = [self.upload(service, 'PM25', '{}.jpg'.format(item)) for item in PM25_sorted_file]

		# 下載辨識結果，儲存為文字檔案
		for index, item in enumerate(CO2_res_list):
			self.download(service, 'CO2', item, index)
		for index, item in enumerate(PM25_res_list):
			self.download(service, 'PM25', item, index)

	def get_file_name(self, dir):
		all_file = os.listdir(dir)
		s = sorted([int(f.strip('.jpg')) for f in all_file])
		return s

	def upload(self, service, dir, imgfile):
		mime = 'application/vnd.google-apps.document'
		res = service.files().create(
			body={
				'name': dir+'-'+imgfile,
				'mimeType': mime
			},
			media_body=MediaFileUpload(('input/{}/'.format(dir)+imgfile), mimetype=mime, resumable=True)
		).execute()

		return res 

	def download(self, service, dir, res, index):
		downloader = MediaIoBaseDownload(
			io.FileIO('output/{}/{}.txt'.format(dir, index+1), 'wb'),
			service.files().export_media(fileId=res['id'], mimeType="text/plain")
		)
		done = False
		while done is False:
			status, done = downloader.next_chunk()

		service.files().delete(fileId=res['id']).execute()
		
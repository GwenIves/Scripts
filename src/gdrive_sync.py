#!/bin/env python

#
# Synchronise local files with Google Drive
#

import oauth2client
import optparse
import httplib2
import os

from apiclient import discovery

FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
SCOPE = 'https://www.googleapis.com/auth/drive'
APPLICATION_NAME = 'Backup'
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIALS_DIR = ".credentials"
CREDENTIALS_FILE = APPLICATION_NAME.lower () + ".json"

def get_credentials():
    home_dir = os.path.expanduser ('~')
    credential_dir = os.path.join (home_dir, CREDENTIALS_DIR)

    if not os.path.exists (credential_dir):
        os.makedirs (credential_dir)

    credential_path = os.path.join (credential_dir, CREDENTIALS_FILE)

    store = oauth2client.file.Storage (credential_path)
    credentials = store.get ()

    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets (CLIENT_SECRET_FILE, SCOPE)
        flow.user_agent = APPLICATION_NAME

        credentials = oauth2client.tools.run (flow, store)

    return credentials

def get_files (service, title, parent_id = None, mime_type = None):
    query = "title = '{}'".format (title)

    if mime_type:
	    query += " and mimeType = '{}'".format (mime_type)

    if parent_id:
            query += "and '{}' in parents".format (parent_id)

    f = service.files().list (q = query).execute ()

    return f["items"]

def create_file (service, title, parent_id, source, mime_type):
    body = {
        "title" : title,
        "shared" : False,
        "mimeType" : mime_type,
	"parents" : [{"id" : parent_id}]
    }

    params = {
        "body" : body,
        "media_body" : source,
        "convert" : False,
        "useContentAsIndexableText" : False,
        "ocr" : False
    }

    files = get_files (service, title, parent_id)

    if not files:
        f = service.files().insert (**params).execute ()
    else:
	params["fileId"] = files[0]["id"]
        f = service.files().update (**params).execute ()

    return f

def get_folder_id (service, folder):
    if folder:
        folders = get_files (service, folder, "root", FOLDER_MIME_TYPE)

	if folders:
            folder_id = folders[0]["id"]
	else:
            folder = create_file (service, folder, "root", None, FOLDER_MIME_TYPE)
	    folder_id = folder["id"]
    else:
        folder_id = "root"

    return folder_id

def synchronize_file (filename, service, parent_id):
    basename = os.path.basename (filename)

    create_file (service, basename, parent_id, filename, None)

def synchronize_files (files, service, options):
    parent_id = get_folder_id (service, options.folder)

    for f in files:
        synchronize_file (f, service, parent_id)

def main():
    parser = optparse.OptionParser ()

    parser.add_option ("-d", "--directory", help = "Google Drive directory to upload to", dest = "folder", default = None)

    (opts, args) = parser.parse_args ()

    credentials = get_credentials ()
    http = credentials.authorize (httplib2.Http ())
    service = discovery.build ('drive', 'v2', http=http)

    synchronize_files (args, service, opts)

main ()

import csv
import os

from cStringIO import StringIO
from docopt import docopt
from boxsdk import JWTAuth, Client

from records import Database


def to_csv(field_names, collection):
    def get_att(model, att):
        att = getattr(model, att)
        att = att.encode('utf-8') if type(att) is unicode else att
        return ' '.join(str(att).split())

    def make_row(model):
        return {att: get_att(model, att) for att in field_names}

    def make_writer(sio):
        return csv.DictWriter(sio, field_names, dialect='excel',
                              quoting=csv.QUOTE_NONNUMERIC)

    # yield header
    sio = StringIO()
    w = make_writer(sio)
    w.writeheader()

    # yield rows
    for model in collection:
        row = make_row(model)
        w.writerow(row)

    return sio


class BoxClient(object):
    def __init__(self):
        self.client_id = os.environ['BOX_CLIENT_ID']
        self.client_secret = os.environ['BOX_CLIENT_SECRET']
        self.enterprise_id = os.environ['BOX_ENTERPRISE_ID']
        self.rsa_private_key_pass = os.environ['BOX_RSA_PRIVATE_KEY_PASS']
        self.rsa_private_key_path = os.environ['BOX_RSA_PRIVATE_KEY_PATH']
        self.jwt_key_id = os.environ['BOX_JWT_KEY_ID']
        self.folder_id = os.environ['BOX_FOLDER_ID']
        self.access_token = None
        self.refresh_token = None

        self.client = self.authenticate_box_client()

    def store_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token

    def authenticate_box_client(self):
        self.auth = JWTAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            enterprise_id=self.enterprise_id,
            jwt_key_id=self.jwt_key_id,
            rsa_private_key_passphrase=self.rsa_private_key_pass,
            rsa_private_key_file_sys_path=self.rsa_private_key_path,
            store_tokens=self.store_tokens
        )

        self.auth.authenticate_instance()
        return Client(self.auth)

    def upload(self, stream, filename):
        self.client.folder(folder_id=self.folder_id).upload_stream(stream,
                                                                   filename)


def cli():
    cli_docs = """Box Exporter: Take that data and put it in a box.
Usage:
  boxex <filepath> <filename> [--url=<url>] 
  boxex (-h | --help)

Options:
  -h --help      Show this screen
  --url=<url>    The database URL to use. Defaults to $DATABASE_URL

Notes:
  - While you may specify a database connection string with --url, box-exporter 
    will automatically default to the value of $DATABASE_URL, if available.
  - filepath is intended to be the path of a SQL file.
  - All box credentials are set via environmental variables. Make sure you have
    the following environment variables set or a KeyError will occur:
        $BOX_CLIENT_ID
        $BOX_CLIENT_SECRET
        $BOX_ENTERPRISE_ID
        $BOX_RSA_PRIVATE_KEY_PASS
        $BOX_RSA_PRIVATE_KEY_PATH
        $BOX_JWT_KEY_ID
        $BOX_FOLDER_ID
    """
    arguments = docopt(cli_docs)

    # Create the database object
    db = Database(arguments['--url'])

    # Authenticate the box client
    client = BoxClient()

    queryfile = arguments['<filepath>']
    filename = arguments['<filename>']

    # Execute the query, if it is found.
    if os.path.isfile(queryfile):
        rows = db.query_file(queryfile).all()

        if rows:
            # grab the first row and use keys as fieldnames
            fieldnames = rows[0].as_dict().keys()
            client.upload(to_csv(fieldnames, rows), filename)
    else:
        print('There was no query file that was found')


# Run the CLI when executed directly.
if __name__ == '__main__':
    cli()

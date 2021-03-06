#!/usr/bin/env python
#
# soaplib - Copyright (C) 2009 Aaron Bickell, Jamie Kirkpatrick
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#

from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String
from soaplib.serializers.binary import Attachment


from tempfile import mkstemp
import os


class DocumentArchiver(SimpleWSGISoapApp):

    @soapmethod(Attachment, _returns=String)
    def archive_document(self, document):
        '''
        This method accepts an Attachment object, and returns
        the filename of the archived file
        '''
        fd, fname = mkstemp()
        os.close(fd)

        document.fileName = fname
        document.save_to_file()

        return fname

    @soapmethod(String, _returns=Attachment)
    def get_archived_document(self, file_path):
        '''
        This method loads a document from the specified file path
        and returns it.  If the path isn't found, an exception is
        raised.
        '''
        if not os.path.exists(file_path):
            raise Exception("File [%s] not found"%file_path)

        document = Attachment(fileName=file_path)
        # the service automatically loads the data from the file.
        # alternatively, The data could be manually loaded into memory
        # and loaded into the Attachment like:
        #   document = Attachment(data=data_from_file)
        return document


def make_client():
    from soaplib.client import make_service_client
    client = make_service_client('http://localhost:7889/', DocumentArchiver())
    return client

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        server = make_server('localhost', 7889, DocumentArchiver())
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"

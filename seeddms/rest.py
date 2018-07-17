#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""rest.py - interface for the raw REST interfaces"""

import requests
import os
import re
import hashlib
import pprint
import json
import urllib
from .exceptions import SeedDMSException

class SeedDMSData(object):
    """class to store the results for a request object

    .. todo:: explain SeedDMS REST return structure.

    :param request_object: an object returned by :class:`request`
    :type request_object: class object

    Example::

        def return_data(self, url):
            req_obj = requests.get(url, cookies=self.cookies)
            return SeedDMSData(req_obj)

        obj = self.return_data(url)
        if obj.success:
            for x in obj:
                print x 
        else:
            print obj.message

    """

    def __init__(self, request_object):

        if request_object.status_code not in [200, 201]:
            content = None
            try:
                content = json.loads(request_object.content)
                message = content.get('message', '')
            except ValueError:
                message = content

            raise SeedDMSException("request to %s raised a %s error: %s" % (
                    request_object.url,
                    request_object.status_code, message))

        self.json_obj = request_object.json()

        self.count = 0
        self._data = self.json_obj

        if not isinstance(self._data, list):
            self._data = [self._data]
        self.data_max = len(self._data)

    @property
    def data(self):
        """return the first item in a the results

        sometimes the results are not iterable then the first element can be returned.

        :returns: results of the query
        :rtype: dict

        Example::

          import pprint

          obj = self.return_data(url)
          if obj.success:
              pprint.pprint(obj.data)
          else:
              print obj.message

        """
        return self._data[0]['data']

    def __iter__(self):
        return self

    def next(self):
        self.count += 1
        if self.count > self.data_max:
            raise StopIteration
        retv = self._data[self.count-1]
        # do something here?
        return retv

    @property
    def success(self):
        """return ``True`` if the query was successful.

        :returns: query success
        :rtype: bool

        """
        if self.json_obj.get('success'):
            return True
        else:
            return False

    @property
    def message(self):
        """return message content

        :returns: message
        :rtype: str

        """
        return self.json_obj.get('message', '')

class SeedDMS(object):
    """Raw REST interface for SeedDMS

    :param baseurl: url path to the rest api
    :param username: username to login with
    :param password: password to login with
    :param targetfolder: target folder to use on the DMS
    :type baseurl: str
    :type username: str
    :type password: str
    :type targetfolder: str

    .. note:: see :class:`seeddms.config.Config` for defaults.
    """
    def __init__(self, **kwargs):
        props = ('baseurl', 'username', 'password', 'targetfolder')
        self.baseurl = str()
        self.username = str()
        self.password = str()
        self.targetfolder = str()
        self.cookies = str()
        self.folderdict = dict()

        for prop in props:
            if prop in kwargs:
                setattr(self, prop, kwargs[prop])

# ------------------------------------------------------------------------------
# TRANSLATION FUNCTIONS
# ------------------------------------------------------------------------------

    def __tr_url(self, url, argdict=None):

        # FIXME: some url encoding??

        if argdict is None:
            argdict = {}

        retv = re.sub(r":(\w+)", r"%(\1)s", url)
        try:
            retv = retv % argdict
        except KeyError:
            raise SeedDMSException("incomplete argument list passed to %s" % retv)

        return "%s%s" % (self.baseurl, retv)

    def __tr_params(self, params):

        retv = dict()
        if params == None:
            return retv

        for keyname, keyvalue in params.iteritems():
            if keyvalue is None:
                retv[keyname] = ''
                continue

            if isinstance(keyvalue, bool):
                if keyvalue:
                    retv[keyname] = 'true'

                else:
                    retv[keyname] = 'false'
                continue

            if isinstance(keyvalue, int):
                retv[keyname] = str(keyvalue)
                continue

            if isinstance(keyvalue, str):
                retv[keyname] = keyvalue
                continue

            print "unhandled type %s for %s" % (type(keyvalue), keyname)

        return retv

# ------------------------------------------------------------------------------
# WRAPPERS FOR REST
# ------------------------------------------------------------------------------

    def rest_get(self, url, argdict=None, params=None, raw=False):
        """wrapper for :meth:`requests.get` to handle REST call and return a
        translated result.

        :param url: rest url
        :param argdict: dictionary with keyvalues pairs for the url
        :param params: dictionary of variables posted to the url
        :return: :class:`SeedDMSData` object
        """
        url = self.__tr_url(url, argdict)

        if params is None:
            req_obj = requests.get(url, cookies=self.cookies)

        else:
            params = self.__tr_params(params)
            req_obj = requests.get(url, params=params, cookies=self.cookies)

        if raw:
            print dir(req_obj)
            if req_obj.status_code == 200:
                return req_obj.content
        return SeedDMSData(req_obj)

    def rest_post(self, url, argdict=None, params=None):
        """wrapper for :meth:`requests.post` to handle REST call and return a
        translated result.

        :param url: rest url
        :param argdict: dictionary with keyvalues pairs for the url
        :param params: dictionary of variables posted to the url
        :return: :class:`SeedDMSData` object
        """
        url = self.__tr_url(url, argdict)

        if params is None:
            req_obj = requests.post(url, cookies=self.cookies)

        else:
            params = self.__tr_params(params)
            req_obj = requests.post(url, data=params, params=params, cookies=self.cookies)

        return SeedDMSData(req_obj)

    def rest_put(self, url, argdict=None, params=None):
        """wrapper for :meth:`requests.put` to handle REST call and return a
        translated result.

        :param url: rest url
        :param argdict: dictionary with keyvalues pairs for the url
        :param params: dictionary of variables posted to the url
        :return: :class:`SeedDMSData` object
        """
        url = self.__tr_url(url, argdict)

        if params is None:
            req_obj = requests.put(url, cookies=self.cookies)

        else:
            params = self.__tr_params(params)
            req_obj = requests.put(url, data=params, params=params, cookies=self.cookies)

        return SeedDMSData(req_obj)

    def rest_delete(self, url, argdict=None, params=None):
        """wrapper for :meth:`requests.delete` to handle REST call and return a
        translated result.

        :param url: rest url
        :param argdict: dictionary with keyvalues pairs for the url
        :param params: dictionary of variables posted to the url
        :return: :class:`SeedDMSData` object
        """
        url = self.__tr_url(url, argdict)

        if params is None:
            req_obj = requests.delete(url, cookies=self.cookies)
            params = self.__tr_params(params)

        else:
            params = self.__tr_params(params)
            req_obj = requests.delete(url, params=params, cookies=self.cookies)

        return SeedDMSData(req_obj)

# ------------------------------------------------------------------------------
# LOGIN/LOGOUT
# ------------------------------------------------------------------------------

    def do_login(self):
        """obtain a login cookie

        parameters:

        * `pass` :py:attr:`~password`
        * `user` :py:attr:`~username`

        """
        req_obj = requests.post(self.baseurl + "/login",
                                {'user': self.username, 'pass': self.password})
        json_obj = req_obj.json()

        if not json_obj.get('success'):
            raise SeedDMSException("Failed to login")

        self.cookies = req_obj.cookies

    def do_logout(self):
        """logout"""
        req_obj = requests.get(self.baseurl + "/logout")
        json_obj = req_obj.json()

        if not json_obj.get('success'):
            raise SeedDMSException("Failed to logout")


# ------------------------------------------------------------------------------
# ECHO
# ------------------------------------------------------------------------------

    def echo_data(self):
        """
        .. todo:: what does ``/echo`` do?

        """
        retv = str()
        req_obj = requests.get(self.baseurl + "/echo", cookies=self.cookies)
        if req_obj.status_code == 200:
            retv = req_obj.text
        return retv


# ------------------------------------------------------------------------------
# ACCOUNT
# ------------------------------------------------------------------------------

    def get_account(self):
        """Get information about the **current** account.

        :returns: dictionaty with user info
        :rtype: dict

        .. code-block:: python

           sdms.get_account()
           {u'comment': u'',
            u'disabled': False,
            u'email': u'address@server.com',
            u'hidden': False,
            u'id': 1,
            u'isadmin': True,
            u'isguest': False,
            u'language': u'en_GB',
            u'login': u'admin',
            u'name': u'Administrator',
            u'role': u'admin',
            u'theme': u'bootstrap',
            u'type': u'user'}

        """
        req_obj = self.rest_get("/account")
        if req_obj.success:
            return req_obj.data

    def get_locked_documents(self):
        """get a list of locked documents

        .. todo:: how do I lock a document in the interface?
        """
        req_obj = self.rest_get("/account/documents/locked")
        if req_obj.success:
            return req_obj.data


    def set_email(self, emailaddress):
        """set the email address for the logged in user.

        :param emailaddress: email address
        :type emailaddress: str

        .. note:: ``$id`` not used in function???

        .. note:: field ``fullname`` as email address???

        """
        req_obj = self.rest_put("/account/email", params={'fullname': emailaddress})
        if req_obj.success:
            return req_obj.data

    def set_full_name(self, fullname):
        """set the full name for the user.

        :param fullname: full name
        :type fullname: str

        """
        req_obj = self.rest_put("/account/fullname", params={'fullname': emailaddress})
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# ATTRIBUTEDEFINITIONS
# ------------------------------------------------------------------------------

    def get_attribute_definitions(self):
        """Get attribute definitions

        :returns: list of dictionaries with attribute definitions
        :rtype: list of dicts

        .. code-block:: python

           sdms.get_attribute_definitions()
           [{u'id': 1,
             u'max': 0,
             u'min': 0,
             u'multiple': False,
             u'name': u'foo_folder_attr',
             u'objtype': 1,
             u'type': 3,
             u'valueset': []}]

        """
        req_obj = self.rest_get("/attributedefinitions")
        if req_obj.success:
            return req_obj.data

    def change_attribute_definition_name(self, attribute_id, name):
        """Change a attribute definition name

        :param attribute_id: nummeric attribute id
        :type attribute_id: int
        :param name: new attribute definition name
        :type name: str

        """
        req_obj = self.rest_put("/attributedefinitions/:id/name",
                             argdict={'id': attribute_id},
                             params={'name': name})
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# CATEGORIES
# ------------------------------------------------------------------------------

    def get_categories(self):
        """get a list of categories.

        :returns: list of dictionaries with categories
        :rtype: list of dicts

        .. code-block:: python

           sdms.get_categories()
           [{u'id': 1, u'name': u'reference'},
            {u'id': 2, u'name': u'foo'},
            {u'id': 3, u'name': u'bar'},
            {u'id': 4, u'name': u'baz'}]

        """
        req_obj = self.rest_get("/categories")
        if req_obj.success:
            return req_obj.data

    def lookup_category_id(self, category_name):
        """get a nummeric value for ``category_name``.

        :param category_name: name of the category
        :type category_name: str
        :returns: category id
        :rtype: int or None
        """
        for row in self.get_categories():
            name = row.get('name')
            if category_name == name:
                return row.get('id')

    def get_category(self, category_id):
        """get category information for a category id.

        :param category_id: nummeric id of a category
        :returns: dictionary with category info
        :rtype: dict

        .. code-block:: python

           sdms.get_category(1)
           {u'id': 1, u'name': u'reference'}

        """
        req_obj = self.rest_get("/categories/:id", argdict={'id': category_id})
        if req_obj.success:
            return req_obj.data

    def create_category(self, category):
        """Create a new category.

        :param category: category name
        :type category: str

        .. code-block:: python

           sdms.create_category("games")
        """
        req_obj = self.rest_post("/categories", params={'category': category})
        if req_obj.success:
            return req_obj.data

    def change_category_name(self, category_id, newname):
        """Change a category name.

        :param category_id: nummeric category id
        :type category_id: str
        :param newname: new name of the category
        :type newname: str

        .. code-block:: python

           idn = sdms.lookup_category_id('reference')
           sdms.change_category_name(idn, 'oldstuff')

        """
        req_obj = self.rest_put("/categories/:id/name",
                                argdict={'id': category_id},
                                params={'name': newname})
        if req_obj.success:
            return req_obj.data

    def delete_category(self, category_id):
        """Delete a category.

        :param category_id: nummeric category id
        :type category_id: str

        .. code-block:: python

           idn = sdms.lookup_category_id('DJl0rd')
           sdms.delete_category(idn)
        """
        req_obj = self.rest_delete("/categories/:id", argdict={'id': category_id})
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# DOCUMENTS
# ------------------------------------------------------------------------------

    def get_document(self, document_id):
        """get a document

        :param document_id: nummeric document id
        :type document_id: int

        .. code-block:: python

           sdms.get_document(12).data
           {u'comment': u'',
            u'date': u'2018-07-09 19:06:00',
            u'id': 12,
            u'keywords': u'',
            u'mimetype': u'application/pdf',
            u'name': u'Grammar of the New Zealand Language',
            u'size': u'5044626',
            u'type': u'document',
            u'version': 1}


        """
        req_obj = self.rest_get("/document/:id", argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def get_document_attributes(self, document_id):
        """

        :param document_id: nummeric document id
        :type document_id: int

        .. code-block:: python

           sdms.get_document_attributes(12).data
           [{u'id': 1, u'name': u'language_reference', u'value': u'te reo maori'}]

        """
        req_obj = self.rest_get("/document/:id/attributes",
                                argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def get_document_content(self, document_id):
        """

        :param document_id: nummeric document id
        :type document_id: int

        .. code-block:: python

           filedata = sdms.get_document(docid)
           filepath = filedata.get('name')
           if filedata.get('mimetype') == 'application/pdf':
              filepath += '.pdf'

           with open(filepath, 'w') as ofh:
               ofh.write(sdms.get_document_content(docid))

        """
        req_obj = self.rest_get("/document/:id/content",
                                argdict={'id': document_id}, raw=True)
        return req_obj

    def get_document_file(self, document_id, fileid):
        """
        doesn't work???
        """
        req_obj = self.rest_get("/document/:id/file/:fileid",
                                argdict={'id': document_id,
                                         'fileid': fileid})
        if req_obj.success:
            return req_obj.data

    def get_document_files(self, document_id):
        """
        doesn't work???
        """
        req_obj = self.rest_get("/document/:id/files",
                                argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def get_document_links(self, document_id):
        """
        """
        req_obj = self.rest_get("/document/:id/links",
                                argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def get_document_preview(self, document_id, version=0, width=0):
        """
        """
        req_obj = self.rest_get("/document/:id/preview/:version/:width",
                                argdict={'id': document_id,
                                         'version': version,
                                         'width': width})
        if req_obj.success:
            return req_obj.data

    def get_document_version(self, document_id, version):
        """

        .. code-block:: python

           filedata = sdms.get_document_version(docid, 1)
           filepath = filedata.get('name')
           if filedata.get('mimetype') == 'application/pdf':
              filepath += '.pdf'

           with open(filepath, 'w') as ofh:
               ofh.write(sdms.get_document_content(docid))
        """
        return self.rest_get("/document/:id/version/:version",
                             argdict={'id': document_id, 'version': version}, raw=True)

    def get_document_versions(self, document_id):
        """get the various versions of the documents

        """
        req_obj = self.rest_get("/document/:id/versions",
                                argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def upload_document_file(self, document_id, **kwargs):
        """

        :param kwargs: dictionary of parameters
        :type kwargs: dict

        arguments passed to :meth:`rest_post`:

        * **comment**, 
        * **keywords**, 
        * **name**, 
        * **origfilename**, 
        * **public**, 
        * **version**, 
        """
        params = dict()
        for keyword in ['comment', 'keywords', 'name', 'origfilename',
                        'public', 'version']:
            params[keyword] = kwargs.get(keyword)

        req_obj = self.rest_post("/document/:id/attachment",
                                 argdict={'id': document_id}, params=params)
        if req_obj.success:
            return req_obj.data

    def move_document(self, document_id, folderid):
        """
        """
        req_obj = self.rest_post("/document/:id/move/:folderid",
                                 argdict={'id': document_id,
                                          'folderid': folderid})
        if req_obj.success:
            return req_obj.data

    def delete_document(self, document_id):
        """
        """
        req_obj = self.rest_delete("/document/:id", argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def remove_document_categories(self, document_id):
        """
        """
        req_obj = self.rest_delete("/document/:id/categories",
                                   argdict={'id': document_id})
        if req_obj.success:
            return req_obj.data

    def remove_document_category(self, document_id, category_id):
        """
        """
        req_obj = self.rest_delete("/document/:id/category/:categoryId",
                                   argdict={'id': document_id,
                                            'categoryId': category_id})
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# FOLDER
# ------------------------------------------------------------------------------

    def get_folder(self, folder_id=None, **kwargs):
        """

        :param kwargs: dictionary of parameters
        :type kwargs: dict

          arguments:
            - forcebyname
            - parentid

        .. code-block:: python

           sdms.get_folder("DMS")
           {u'attributes': [{u'id': 1, u'value': u'main'}],
            u'comment': u'DMS root',
            u'date': u'2017-02-22 12:36:22',
            u'id': 1,
            u'name': u'DMS',
            u'type': u'folder'}

        """
        argdict = {}
        url = '/folder'
        if folder_id is not None:
            url += '/:id'
            argdict['id'] = folder_id

        print "url: " + url
        print argdict
        print kwargs
        req_obj = self.rest_get(url, argdict=argdict, params=kwargs)
        if req_obj.success:
            return req_obj.data

    def get_folder_document_ids(self, folder_id):
        retv = list()
        for row in self.get_folder_children(folder_id):
            if row.get('type') ==  'document':
                retv.append(int(row.get('id')))
        return sorted(retv)

    def get_folder_folder_ids(self, folder_id):
        retv = list()
        for row in self.get_folder_children(folder_id):
            if row.get('type') ==  'folder':
                retv.append(int(row.get('id')))
        return sorted(retv)

    def get_folder_attributes(self, folder_id):
        """
        """
        req_obj = self.rest_get("/folder/:id/attributes",
                                argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def get_folder_children(self, folder_id):
        """
        """
        req_obj = self.rest_get("/folder/:id/children",
                                argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def get_folder_parent(self, folder_id):
        """
        """
        req_obj = self.rest_get("/folder/:id/parent", argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def get_folder_path(self, folder_id):
        """

        :param folder_id: nummeric folder id
        :type folder_id: int

        .. code-block:: python

           sdms.get_folder_path(2)
           [{u'id': u'1', u'name': u'DMS'}, {u'id': u'2', u'name': u'aotearoa'}]

        """
        req_obj = self.rest_get("/folder/:id/path", argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def get_folder_path_str(self, folder_id):
        """wrapper for :meth:`get_folder_path` returns a string.

        :param folder_id: nummeric folder id
        :type folder_id: int

        .. code-block:: python

           sdms.get_folder_path_str(2)
           u'DMS/aotearoa'
        """
        data = self.get_folder_path(folder_id)
        retv = "/".join([x.get('name') for x in data])
        return retv

    def create_folder(self, folder_id, **kwargs):
        """create a folder.

        :param folder_id: nummeric folder id of parent
        :type folder_id: int
        :param kwargs: dictionary of parameters
        :type kwargs: dict

        ``kwargs`` options:

        * **comment**
        * **name**
        * **attributes** NOT SUPPORTED YET

        .. todo: unclear on how to handle the attributes 
        """
        params = dict()
        for keyword in ['comment', 'name']:
            params[keyword] = kwargs.get(keyword)

        attributes = kwargs.get('attributes', {})

        req_obj = self.rest_post("/folder/:id/createfolder",
                                 argdict={'id': folder_id},
                                 params=params)
        if not req_obj.success:
            raise SeedDMSException("failed to create folder %(name)s" % kwargs)

        folder_id = req_obj.data.get('id')


    def upload_document(self, uploadfile, foldername=None):
        """
          arguments:
            - name
            - keywords
            - origfilename
            - foldername (opt)
        """
        # FIXME: dunno if this works
        datablob = open(uploadfile, "r").read()

        origfilename = os.path.basename(uploadfile)
        params['name'] = kwargs.get('origfilename', origfilename)
        params['origfilename'] = origfilename
        if 'keywords' in kwargs:
            params['keywords'] = kwargs.get('keywords')

        foldername = kwargs.get('foldername')

        params['foldername'] = kwargs.get('targetfolder', self.targetfolder)

        folder_id = self.get_folder_id(foldername)

        req_obj = self.rest_post("/folder/:id/document",
                                 argdict={'id': folder_id},
                                 data=datablob,
                                 params=params)
        if req_obj.success:
            return req_obj.data

    def upload_document_put(self, folder_id):
        """

            +----------+----------------------+
            | def      | upload_document_put  |
            +----------+----------------------+
            | function | uploadDocumentPut    |
            +----------+----------------------+
            | url      | /folder/:id/document |
            +----------+----------------------+
            | action   | put                  |
            +----------+----------------------+

          arguments:
            - name
            - origfilename
            - foldername (opt)
        """
        ##  # FIXME: dunno if this works
        ##  datablob = open(uploadfile, "r").read()
        ##  self.rest_put("/folder/:id/document",
        ##                           argdict={'id': folder_id},
        ##                           data=datablob,
        ##                           params=params)
        ##  if req_obj.success:
        ##      return req_obj.data
        pass

    def move_folder(self, folder_id, parent_folder_id):
        """
        """
        req_obj = self.rest_post("/folder/:id/move/:folderid",
                                 argdict={'id': folder_id,
                                          'folderid': parent_folder_id})
        if req_obj.success:
            return req_obj.data

    def clear_folder_access_list(self, folder_id):
        """
        """
        req_obj = self.rest_put("/folder/:id/access/clear",
                                 argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def add_group_access_to_folder(self, folder_id, group_id, mode):
        """

        :param folder_id: nummeric folder id
        :type folder_id: int
        :param group_id: nummeric group id
        :type group_id: int
        :param mode: mode string (read/readwrite/all)
        :type mode: str

        """
        req_obj = self.rest_put("/folder/:id/access/group/add",
                                 argdict={'id': folder_id},
                                 params={'id': group_id,
                                         'mode': mode})
        if req_obj.success:
            return req_obj.data

    def remove_group_access_from_folder(self, folder_id, group_id, mode):
        """

            +----------+---------------------------------+
            | def      | remove_group_access_from_folder |
            +----------+---------------------------------+
            | function | removeGroupAccessFromFolder     |
            +----------+---------------------------------+
            | url      | /folder/:id/access/group/remove |
            +----------+---------------------------------+
            | action   | put                             |
            +----------+---------------------------------+

          arguments:
            - id, user or group id input
            - mode, read/readwrite/all
        """
        pass

    def add_user_access_to_folder(self, folder_id):
        """

            +----------+-----------------------------+
            | def      | add_user_access_to_folder   |
            +----------+-----------------------------+
            | function | addUserAccessToFolder       |
            +----------+-----------------------------+
            | url      | /folder/:id/access/user/add |
            +----------+-----------------------------+
            | action   | put                         |
            +----------+-----------------------------+

          arguments:
            - id, user or group id input
            - mode, read/readwrite/all
        """
        pass

    def remove_user_access_from_folder(self, folder_id):
        """

            +----------+--------------------------------+
            | def      | remove_user_access_from_folder |
            +----------+--------------------------------+
            | function | removeUserAccessFromFolder     |
            +----------+--------------------------------+
            | url      | /folder/:id/access/user/remove |
            +----------+--------------------------------+
            | action   | put                            |
            +----------+--------------------------------+

          arguments:
            - id, user or group id input
            - mode, read/readwrite/all
        """
        pass


    def set_folder_inherits_access(self, folder_id):
        """

        :param folder_id: nummeric folder id
        :type folder_id: int

          arguments:
            - enable
        """
        req_obj = self.rest_get("/folder/:id/setInherit", argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def delete_folder(self, folder_id):
        """delete a folder

        :param folder_id: nummeric id or name of the folder
        :type folder_id: int or str
        """
        folder_id = self.get_folder_id(folder_id)
        req_obj = self.rest_delete("/folder/:id", argdict={'id': folder_id})
        if req_obj.success:
            return req_obj.data

    def get_folder_id(self, folder_id):
        """derived function; call `get_folder` but return the content of the
        `id` field.

        :param group_id: nummeric group id or group name
        :type group_id: int or str

        """
        return self.get_folder(folder_id)['id']

# ------------------------------------------------------------------------------
# GROUPS
# ------------------------------------------------------------------------------

    def get_group(self, group_id):
        """get the info matching a group

        :param group_id: nummeric group id or group name
        :type group_id: int or str

        .. code-block:: python

           sdms.get_group("aotearoa")
           {u'comment': u'',
            u'id': 3,
            u'name': u'aotearoa',
            u'type': u'group',
            u'users': []}

           sdms.get_group(3)
           {u'comment': u'',
            u'id': 3,
            u'name': u'aotearoa',
            u'type': u'group',
            u'users': []}

        """
        req_obj = self.rest_get("/groups/:id",
                                argdict={'id': group_id})
        if req_obj.success:
            return req_obj.data

    def create_group(self, **kwargs):
        """create a group

        :param kwargs: dictionary of parameters
        :type kwargs: dict

        ``kwargs`` names:

        * **name**, name of the group
        * **comment**, comment of the group

        .. code-block:: python

           sdms.create_group(name="aotearoa")
        """
        req_obj = self.rest_post("/groups",
                                params={'name': kwargs.get('name'),
                                        'comment': kwargs.get('comment', '')})
        if req_obj.success:
            return req_obj.data

    def add_user_to_group(self, group_id, user_id):
        """add a user to a group

        :param group_id: name or id of the group
        :type group_id: str or int
        :param user_id: user id
        :type user_id: int

        .. code-block:: python

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']

           sdms.add_user_to_group("aotearoa", user_id)

        """
        group_data = self.get_group(group_id)
        group_id = group_data.get('id')
        req_obj = self.rest_put("/groups/:id/addUser",
                                argdict={'id': group_id},
                                params={'userid': user_id})
        if req_obj.success:
            return req_obj.data

    def remove_user_from_group(self, group_id, user_id):
        """remove user from group

        :param group_id: name or id of the group
        :type group_id: str or int
        :param user_id: user id
        :type user_id: int

        .. code-block:: python

           group_data = sdms.get_group("aotearoa")
           group_id = group_data.get('id')

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']

           sdms.remove_user_from_group(group_id, user_id)

        """
        req_obj = self.rest_put("/groups/:id/removeUser",
                                argdict={'id': group_id},
                                params={'userid': user_id})
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------------------------

    def do_search(self, **kwargs):
        """search for documents

        :param kwargs: dictionary of parameters
        :type kwargs: dict

        ``kwargs`` names:

        * **query**, query string
        * **limit**, limit amount of results
        * **mode**,

        .. note:: what does ``typeahead`` do for ``mode`` ??

        .. code-block:: python

           sdms.do_search(query="2014")
           [{u'comment': u'',
             u'date': u'2018-07-09 11:47:19',
             u'id': 7,
             u'name': u'2014',
             u'type': u'folder'},
            {u'comment': u'',
             u'date': u'2018-07-09 18:15:53',
             u'id': 27,
             u'name': u'2014',
             u'type': u'folder'}]

        """
        params = dict()

        for keyn in ['limit', 'mode', 'query']:
            if keyn in kwargs:
                params[keyn] = kwargs.get(keyn)


        req_obj = self.rest_get("/search",
                                params=params)
        if req_obj.success:
            return req_obj.data

    def do_search_by_attr(self, **kwargs):
        """search for documents by attribute

        :param kwargs: dictionary of parameters
        :type kwargs: dict

        ``kwargs`` names:

        * **name**, attribute name
        * **value**, attribute value
        * **limit**, limit amount of results

        .. code-block:: python

           sdms.do_search_by_attr(name='foo_folder_attr', value='main')
           [{u'attributes': [{u'id': 1, u'value': u'main'}],
             u'comment': u'DMS root',
             u'date': u'2017-02-22 12:36:22',
             u'id': 1,
             u'name': u'DMS',
             u'type': u'folder'}]

        """
        params = dict()

        for keyn in ['limit', 'name', 'value']:
            if keyn in kwargs:
                params[keyn] = kwargs.get(keyn)

        req_obj = self.rest_get("/searchbyattr",
                                params=params)
        if req_obj.success:
            return req_obj.data

# ------------------------------------------------------------------------------
# USERS
# ------------------------------------------------------------------------------

    def get_users(self):
        """get a list of users

        .. code-block:: python

           sdms.get_users()
           [{u'comment': u'',
             u'disabled': False,
             u'email': u'address@server.com',
             u'hidden': False,
             u'id': 1,
             u'isadmin': True,
             u'isguest': False,
             u'language': u'en_GB',
             u'login': u'admin',
             u'name': u'Administrator',
             u'role': u'admin',
             u'theme': u'bootstrap',
             u'type': u'user'},
            {u'comment': u'',
             u'disabled': False,
             u'email': None,
             u'hidden': False,
             u'id': 2,
             u'isadmin': False,
             u'isguest': True,
             u'language': u'',
             u'login': u'guest',
             u'name': u'Guest User',
             u'role': u'guest',
             u'theme': u'',
             u'type': u'user'}]

        """
        req_obj = self.rest_get("/users")
        if req_obj.success:
            return req_obj.data

    def get_user_by_name(self, user_name):
        """get a users data by its user name/login. Calls :meth:`get_users` to
        get a list of users.

        :param user_name: username
        :type user_name: str

        .. code-block:: python

           sdms.get_user_by_name('admin')
           {u'comment': u'',
            u'disabled': False,
            u'email': u'address@server.com',
            u'hidden': False,
            u'id': 1,
            u'isadmin': True,
            u'isguest': False,
            u'language': u'en_GB',
            u'login': u'admin',
            u'name': u'Administrator',
            u'role': u'admin',
            u'theme': u'bootstrap',
            u'type': u'user'}

        """
        for req_obj in self.get_users():
            if req_obj['login'] == user_name:
                return req_obj

    def get_user_by_id(self, user_id):
        """get a users data by its user id.

        :param user_id: nummeric user id
        :type user_id: int

        .. code-block:: python

           sdms.get_user_by_id(1)
           {u'comment': u'',
            u'disabled': False,
            u'email': u'address@server.com',
            u'hidden': False,
            u'id': 1,
            u'isadmin': True,
            u'isguest': False,
            u'language': u'en_GB',
            u'login': u'admin',
            u'name': u'Administrator',
            u'role': u'admin',
            u'theme': u'bootstrap',
            u'type': u'user'}


        """
        req_obj = self.rest_get("/users/:id", argdict={'id': user_id})
        if req_obj.success:
            return req_obj.data

    def create_user(self, **kwargs):
        """

        ``kwargs`` names:

        * **user**
        * **pass**
        * **name**
        * **email**
        * **language**, default ``en_GB``
        * **theme**, default ``bootstrap``
        * **comment**
        * **role**, default ``guest``

        .. code-block:: python

           try:
               sdms.create_user(user='tangaroa',
                                password='redhat',
                                name='God of the Sea',
                                email='tangaroa@example.co.nz')
           except SeedDMSException as err:
               print err

        """

        data = dict()
        defaults = {'language': 'en_GB',
                    'theme': 'bootstrap',
                    'role': 'guest'}

        for keyname in ['user', 'pass', 'name', 'email', 'language', 'theme', 'comment', 'role']:
            data[keyname] = kwargs.get(keyname, defaults.get(keyname, ''))

        if 'password' in kwargs:
            data['pass'] = kwargs.get('password')

        if 'pass' in data:
            data['pass'] = self.encpasswd(data.get('pass'))

        return self.rest_post("/users", params=data)

    def set_disabled_user(self, user_id):
        """disable a user

        :param user_id: nummeric user id
        :type user_id: int

        .. code-block:: python

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']
           sdms.set_disabled_user(user_id)

        """
        req_obj = self.rest_put("/users/:id/disable", argdict={'id': user_id}, params={'disable': True})
        if req_obj.success:
            return req_obj.data

    def set_enabled_user(self, user_id):
        """enable a user

        :param user_id: nummeric user id
        :type user_id: int

        .. code-block:: python

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']
           sdms.set_enabled_user(user_id)

       """
        req_obj = self.rest_put("/users/:id/disable", argdict={'id': user_id}, params={'disable': False})
        if req_obj.success:
            return req_obj.data

    @staticmethod
    def encpasswd(password):
        """return the encrypted password

        :param password: plain text password
        :type password: str
        :return: password string
        :rtype: str

        .. note:: "encryption" is an md5 sum.
        """
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()

    def change_user_password(self, user_id, password):
        """change the users password

        :param user_id: nummeric user id
        :type user_id: int
        :param password: plaintext password
        :type password: str

        .. code-block:: python

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']
           sdms.change_user_password(user_id, 'redhat')

        """

        password = self.encpasswd(password)

        req_obj = self.rest_put("/users/:id/password", argdict={'id': user_id}, params={'password': password})
        if req_obj.success:
            return req_obj.data

    def delete_user(self, user_id):
        """delete a user by id

        :param user_id: user id
        :type user_id: int

        .. code-block:: python

           userdata = sdms.get_user_by_name('tangaroa')
           user_id = userdata['id']
           sdms.delete_user(user_id)

        """
        req_obj = self.rest_delete("/users/:id", argdict={'id': user_id})
        if req_obj.success:
            return req_obj.data


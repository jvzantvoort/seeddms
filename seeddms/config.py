#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""seeddms.config - $description
"""

import os
import ConfigParser

from .exceptions import SeedDMSException


class Config(object):
    """configuration handler for :class:`seeddms`.

    :param baseurl: url path to the rest api (default:
             ``http://localhost/seeddms/restapi/index.php``)
    :param username: username to login with (default: ``admin``)
    :param password: password to login with (default: ``admin``)
    :param targetfolder: target folder to use on the DMS (default: ``DMS``)
    :type baseurl: str
    :type username: str
    :type password: str
    :type targetfolder: str
    :return: return description
    :rtype: the return type description

    """

    def __init__(self, **kwargs):

        self.cfgopts = ('baseurl', 'username', 'password',  'targetfolder')
        self.configfile = os.path.expanduser("~/.seeddms-cli.conf")
        self.baseurl = 'http://localhost/seeddms/restapi/index.php'
        self.cookies = str()
        self.folderdict = dict()
        self.password = 'admin'
        self.targetfolder = 'DMS'
        self.username = 'admin'

        # load the config file
        self.configfile = kwargs.get('configfile', self.configfile)
        try:
            self.loadconfig()
        except SeedDMSException:
            pass

        # load the function arguments
        for prop in self.cfgopts:
            if prop in kwargs:
                setattr(self, prop, kwargs[prop])

    def loadconfig(self):
        """load the content from the configfile."""
        cfgfile = self.configfile

        if not os.path.exists(cfgfile):
            raise SeedDMSException("provided configfile %s does not exist\n" % cfgfile)

        config = ConfigParser.RawConfigParser()
        if not config.read(cfgfile):
            raise SeedDMSException("failed to read configfile %s\n" % cfgfile)

        if not config.has_section('main'):
            raise SeedDMSException("incomplete or corrupt configfile %s" % cfgfile)

        for pname in config.options('main'):
            if pname not in self.cfgopts:
                continue
            setattr(self, pname, config.get('main', pname))

    def writeconfig(self):
        """write the content to the configfile."""
        config = ConfigParser.RawConfigParser()
        config.add_section('main')
        config.set('main', 'baseurl', self.baseurl)
        config.set('main', 'username', self.username)
        config.set('main', 'password', self.password)
        config.set('main', 'targetfolder', self.targetfolder)

        with open(self.configfile, 'wb') as ofh:
            config.write(ofh)


if __name__ == '__main__':
    cfg = Config()

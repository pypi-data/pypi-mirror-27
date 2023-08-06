# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function


class Specials(object):
    """The Film Specials Base Class which renders iamges for use on the Dune UI
    """

    def __init__(self, Session, library):
        """Artwork __init__

            Args:
                | args (list): Passed through args from the command line.
                | Session (:obj:): sqlalchemy scoped_session. See zerrphix.db init.
                | config (:obj:): The config loaded (ConfigParser). See zerrphix.config.
                | config_root_dir (str): The directory from which the config file was loaded.

        """
        self.Session = Session
        self.library = library
        if hasattr(self, 'make_special_type_dict'):
            self.special_type_dict_by_special, self.special_type_dict_by_id = self.make_special_type_dict()

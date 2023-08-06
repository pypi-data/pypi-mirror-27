import os.path

from DatabaseLibrary import DatabaseLibrary
from Selenium2Library import Selenium2Library
from robot.libraries import DateTime
from robot.libraries import Dialogs
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.api import logger

__all__ = ('dia', 's2l', 'bi', 'dtl', 'osl', 'cl', 'at', 'get_configs_dir', 'get_actionmaps_dir', 'get_datafiles_dir', 'get_objectmaps_dir')

def get_configs_dir(delta_path=""):
    output_path = bi().get_variable_value("${EXECDIR}")
    output_path += "/configs/"
    output_path += delta_path
    output_path_normalized = validate_create_artifacts_dir(output_path)
    return output_path_normalized

def get_actionmaps_dir(delta_path=""):
    output_path = bi().get_variable_value("${EXECDIR}")
    output_path += "/actionmaps/"
    output_path += delta_path
    output_path_normalized = validate_create_artifacts_dir(output_path)
    return output_path_normalized

def get_datafiles_dir(delta_path=""):
    output_path = bi().get_variable_value("${EXECDIR}")
    output_path += "/datafiles/"
    output_path += delta_path
    output_path_normalized = validate_create_artifacts_dir(output_path)
    return output_path_normalized

def get_objectmaps_dir(delta_path=""):
    output_path = bi().get_variable_value("${EXECDIR}")
    output_path += "/objectmaps/"
    output_path += delta_path
    output_path_normalized = validate_create_artifacts_dir(output_path)
    return output_path_normalized

def validate_create_artifacts_dir(path):
    """
    As input take path return normalized path,
    create directory for this path
    :param path:
    :return path_normalized:
    """
    output_dir_normalized = os.path.dirname(os.path.abspath(os.path.normpath(path)))
    output_path_normalized = os.path.abspath(os.path.normpath(path))
    if not os.path.exists(output_dir_normalized):
        os.makedirs(output_dir_normalized)
    return output_path_normalized

def dia():
    """
        :rtype : Dialogs
        """
    dia_instance = BuiltIn().get_library_instance('Dialogs')
    assert isinstance(dia_instance, Dialogs)
    return dia_instance


def s2l():
    """
        :rtype : SeleniumLibrary
        """
    s2l_instance = BuiltIn().get_library_instance('Selenium2Library')
    assert isinstance(s2l_instance, Selenium2Library)
    return s2l_instance


def bi():
    """
        :rtype : BuiltIn
        """
    bi_instance = BuiltIn().get_library_instance('BuiltIn')
    assert isinstance(bi_instance, BuiltIn)
    return bi_instance


def dtl():
    """

        :rtype : DateTime
        """
    dt_instance = BuiltIn().get_library_instance('DateTime')
    assert isinstance(dt_instance, DateTime)
    return dt_instance


def osl():
    """

        :rtype : OperatingSystem
        """
    os_instance = BuiltIn().get_library_instance('OperatingSystem')
    assert isinstance(os_instance, OperatingSystem)
    return os_instance


def cl():
    """

        :rtype : Collections
        """
    c_instance = BuiltIn().get_library_instance('Collections')
    assert isinstance(c_instance, Collections)
    return c_instance


def dbl():
    """

        :rtype : DatabaseLibrary
        """
    c_instance = BuiltIn().get_library_instance('DatabaseLibrary')
    assert isinstance(c_instance, DatabaseLibrary)
    return c_instance


def at():
    """

        :rtype : AnimalTesting
        """
    c_instance = BuiltIn().get_library_instance('AnimalTesting')
    # assert isinstance(c_instance, AnimalTesting)
    return c_instance

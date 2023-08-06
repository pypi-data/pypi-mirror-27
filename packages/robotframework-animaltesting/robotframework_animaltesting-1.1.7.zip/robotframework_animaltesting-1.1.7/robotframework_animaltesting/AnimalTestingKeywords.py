#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ************************************************
# **** Copyright (c) 2016 The Yews Consulting ****
# ************************************************

import os
import os.path
import time

from robot.api import logger
from robot.libraries import DateTime
from robot.testdoc import TestDoc
from Selenium2Library.keywords import _SelectElementKeywords
from selenium.webdriver import FirefoxProfile, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By   #do not remove
from distutils import util
from AnimalTesting.robot_instances import validate_create_artifacts_dir
from robot_instances import *

try:
    # noinspection PyCompatibility
    from urlparse import urljoin
except ImportError:  # python3
    # noinspection PyCompatibility,PyUnresolvedReferences
    from urllib.parse import urljoin

import urllib
import datetime

class AnimalTestingKeywords(object):

    def __init__(self):
         super(AnimalTestingKeywords, self).__init__()
    def val(self,objlocator, objtype="", objdesc="", objtext=""):
        #Val(idate) , same as Rat(ify)
        self.rat(objlocator, objtype, objdesc, objtext)

    def val_not(self, objlocator, objtype="", objdesc="", objtext=""):
        # Val(idate) Not , same as Rat(ify) Not
        self.rat_not(objlocator, objtype, objdesc, objtext)

    def set(self,objlocator, objtype="", objdesc="", objtext=""):
        #Set , same as Cat(ch)
        self.bat(objlocator, objtype, objdesc, objtext)

    def get(self,objlocator, objtype="", objdesc="", objtext=""):
        self.cat(objlocator, objtype, objdesc, objtext)

    def rat(self,objlocator, objtype="", objdesc="", objtext=""):
        #Rat(ify) - validates object supplied
        if type(objtext) is int:
            objtext = str(objtext)
        if type(objdesc) is int:
            objdesc = str(objdesc)
        if type(objlocator) is int:
            objlocator = str(objlocator)
        if type(objtype) is int:
            objtype = str(objtype)
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        objtypelist = ["Number","Value", "Element", "Text", "TextField", "Textbox", "Link", "Page","URL", "Label", "Button", "Image", "Radio","Checkbox", "Combobox", "Combo", "Window", "Editbox"]
        if objlocator and objtype and objdesc and not cl().should_contain_match(objtypelist, objtype):

            if objtype == 'Page':
                logger.info("Verify [" +objdesc+ "] page exists and should be ["+objtext+"]", html=True, also_console=True)
                if not docflag:
                    bi().sleep(1) #Odd error in Firefox Marionette where it sometimes misses the title on the page
                    s2l().title_should_be(objtext)

            if objtype == 'Link':
                logger.info("Verify [" +objdesc+ "] Link exists and should be ["+objtext+"]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_link(objlocator)
                    if objtext:
                        s2l().element_should_contain(objlocator,objtext)

            if objtype == 'Image':
                logger.info("Verify [" +objdesc+ "] Image exists", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_image(objlocator)

            if objtype == 'Radio' or objtype == 'RadioButton':
                logger.info("Verify [" +objdesc+ "] Radio Button exists", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_radio_button(objlocator)

            if objtype == 'Checkbox':
                logger.info("Verify [" +objdesc+ "] Checkbox exists", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_checkbox(objlocator)

            if objtype == 'Combobox' or objtype == 'Combo':
                logger.info("Verify [" +objdesc+ "] Combobox exists", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_list(objlocator)

            if objtype == 'Editbox' or objtype == 'TextField' or objtype == 'Textbox':
                logger.info("Verify [" +objdesc+ "] [" + objtype + "] exists", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                if  objtext:
                    logger.info("Verify [" +objtext + "] exists in [" +objdesc+ "]", html=True, also_console=True)
                    if not docflag:
                        s2l().element_should_contain(objlocator,objtext)

            if objtype == 'Number' or objtype == 'Value':
                logger.info("Verify [" + objtext + "] exists in [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                if objtext:
                    if not docflag:
                        actual = s2l().get_value(objlocator)
                        if actual != objtext:
                            message = "The value of element '%s' should have been '%s' but " \
                                          "in fact it was '%s'." % (objdesc, objtext, actual)
                            raise AssertionError(message)

            if objtype == 'Text':
                logger.info("Verify [" + objtext + "] exists in [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                if objtext:
                    if not docflag:
                        actual = s2l().get_text(objlocator)
                        if actual != objtext:
                            message = "The text of '%s' should have been '%s' but " \
                                          "in fact it was '%s'." % (objdesc, objtext, actual)
                            raise AssertionError(message)

            if objtype == 'Element' or objtype == 'Label':
                logger.info("Verify [" +objdesc+ "] [" + objtype + "] exists and should be ["+objtext+"]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    gettext = s2l().get_text(objlocator)
                    if objtext:
                        s2l().element_should_contain(objlocator,objtext)
        else:
             # objlocator is equal to some text
             if objlocator and objtype == "" and objdesc == "" and objtext == "":
                 logger.info("Verify Page contains ["+objlocator+"]", html=True, also_console=True)
                 if not docflag:
                     s2l().page_should_contain(objlocator)

             if objlocator and objtype and objdesc == "" and objtext == "":
                 if objtype == 'URL':
                     logger.info("Verify URL contains ["+objlocator+"]", html=True, also_console=True)
                     if not docflag:
                         s2l().location_should_contain(objlocator)
                 else:
                     logger.info("Verify ["+objlocator+"] equals " +objtype, html=True, also_console=True)
                     if not docflag:
                        bi().should_be_equal_as_strings(objlocator, objtype)
             if objlocator and objtype and objdesc and cl().should_contain_match(objtypelist, objtype):
                 bi().fail("The Object Type [" + objtype + "] for [" + objlocator + "] doesnt exist as specified in Objectmap file")

    def rat_not(self,objlocator, objtype="", objdesc="", objtext=""):
        #Rat(ify) - validates object supplied does not exist
        if type(objtext) is int:
            objtext = str(objtext)
        if type(objdesc) is int:
            objdesc = str(objdesc)
        if type(objlocator) is int:
            objlocator = str(objlocator)
        if type(objtype) is int:
            objtype = str(objtype)
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        objtypelist = ["Number","Value", "Element", "TextField", "Textbox", "Link", "Label", "Button", "Image", "Radio","Checkbox", "Combobox", "Combo", "Window", "Editbox"]
        if objlocator and objtype and objdesc and not cl().should_contain_match(objtypelist, objtype):

            if objtype == 'Link':
                logger.info("Verify [" +objdesc+ "] Link does not exist and shouldn't be ["+objtext+"]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_link(objlocator)
                    if objtext:
                        s2l().element_should_not_contain(objlocator,objtext)

            if objtype == 'Image':
                logger.info("Verify [" +objdesc+ "] Image does not exist", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_imagee(objlocator)

            if objtype == 'Radio' or objtype == 'RadioButton':
                logger.info("Verify [" +objdesc+ "] Radio Button does not exist", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_radio_button(objlocator)

            if objtype == 'Checkbox':
                logger.info("Verify [" +objdesc+ "] Checkbox does not exist", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_checkbox(objlocator)

            if objtype == 'Combobox' or objtype == 'Combo':
                logger.info("Verify [" +objdesc+ "] Combobox does not exist", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_list(objlocator)

            if objtype == 'Editbox' or objtype == 'TextField' or objtype == 'Textbox':
                logger.info("Verify [" +objdesc+ "] [" + objtype + "] does not exist", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_element(objlocator)
                if  objtext:
                    logger.info("Verify [" +objtext + "] does not exist in [" +objdesc+ "]", html=True, also_console=True)
                    if not docflag:
                        s2l().element_should_not_contain(objlocator,objtext)

            if objtype == 'Number' or objtype == 'Value':
                logger.info("Verify [" + objtext + "] does not exist in [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_element(objlocator)
                if objtext:
                    if not docflag:
                        actual = s2l().get_value(objlocator)
                        if actual == objtext:
                            message = "The value of element '%s' shouldn't be '%s' but " \
                                          "should be '%s'." % (objdesc, objtext, actual)
                            raise AssertionError(message)

            if objtype == 'Text':
                logger.info("Verify [" + objtext + "] does not exist in [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_element(objlocator)
                if objtext:
                    if not docflag:
                        actual = s2l().get_text(objlocator)
                        if actual == objtext:
                            message = "The text of '%s' shouldn't be '%s' but " \
                                          "should be '%s'." % (objdesc, objtext, actual)
                            raise AssertionError(message)

            if objtype == 'Element' or objtype == 'Label':
                logger.info("Verify [" +objdesc+ "] [" + objtype + "] does not exist and shouldn't be ["+objtext+"]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_not_contain_element(objlocator)
                    gettext = s2l().get_text(objlocator)
                    if objtext:
                        s2l().element_should_not_contain(objlocator,objtext)
        else:
             # objlocator is equal to some text
             if objlocator and objtype == "" and objdesc == "" and objtext == "":
                 logger.info("Verify Page does not contain ["+objlocator+"]", html=True, also_console=True)
                 if not docflag:
                     s2l().page_should_not_contain(objlocator)

             if objlocator and objtype and objdesc and cl().should_contain_match(objtypelist, objtype):
                 bi().fail("The Object Type [" + objtype + "] for [" + objlocator + "] doesnt exist as specified in Objectmap file")


    def bat(self, objlocator, objtype="" , objdesc="", objtext=""):
        #bat(ch) - sets object from object map
        if type(objtext) is int:
            objtext = str(objtext)
        if type(objdesc) is int:
            objdesc = str(objdesc)
        if type(objlocator) is int:
            objlocator = str(objlocator)
        if type(objtype) is int:
            objtype = str(objtype)
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        objtypelist = ["Number", "Value", "Element","Text", "TextField", "Textbox", "Link", "Page","URL", "Label", "Button", "Image", "Radio", "Checkbox", "Combobox", "Combo", "Window", "Editbox"]
        if objlocator and objtype and objdesc and not cl().should_contain_match(objtypelist, objtype):
            if objtype == 'Element' or objtype == 'Label':
                logger.info("Click on [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    s2l().click_element(objlocator)
            if objtype == 'Page':
                logger.info("Log the page title [" + objdesc + " ", html=True, also_console=True)
                if not docflag:
                    s2l().title_should_be(objlocator)
                    s2l().log_title(objlocator)

            if objtype == 'URL':
                logger.info("Log the location [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().location_should_contain(objlocator)
                    s2l().log_location()

            if objtype == 'Link':
                logger.info("Click on the Link [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_link(objlocator)
                    s2l().click_link(objlocator)

            if objtype == 'Button':
                logger.info("Click the button [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_button(objlocator)
                    s2l().click_element(objlocator)

            if objtype == 'Radio' or objtype == 'RadioButton':
                logger.info("Click the Radio Button [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_radio_button(objlocator)
                    s2l().select_radio_button(objlocator)

            if objtype == 'Checkbox':
                logger.info("Check the Checkbox [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_checkbox(objlocator)
                    if s2l().checkbox_should_not_be_selected(objlocator):
                        s2l().select_checkbox(objlocator)

            if objtype == 'Combobox' or objtype == 'Combo':
                logger.info("Select fromn the list [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_list(objlocator)
                    s2l().select_from_list(objlocator,objtext)

            if objtype == 'Window':
                logger.info("Select the window [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    windowslist = s2l().get_window_titles()
                    if titleexists in windowslist:
                        s2l().select_window(objlocator)

            if objtype == 'Editbox' or objtype == 'TextField' or objtype == 'Textbox':
                logger.info("Input text [" + objtext + "] into [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    s2l().click_element(objlocator)
                    s2l().clear_element_text(objlocator)
                    s2l().input_text(objlocator,objtext)

            if objtype == 'Number' or objtype == 'Value':
                logger.info("Input number [" + objtext + "] into [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    s2l().click_element(objlocator)
                    s2l().clear_element_text(objlocator)
                    s2l().input_text(objlocator, objtext)
            if objtype == 'Image':
                logger.info("Click on the image [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_image(objlocator)
                    s2l().click_image(objlocator)

        else:
            if objlocator and objtype == "" and objdesc == "" and objtext == "":
                logger.info("Click on element [" + objlocator + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    s2l().click_element(objlocator)

            if objlocator and objtype and objdesc and cl().should_contain_match(objtypelist, objtype):
                bi().fail("The Object Type [" + objtype + "] for [" + objlocator + "] doesnt exist as specified in Objectmap file")

    def cat(self,objlocator, objtype="", objdesc="", objtext=""):
        #cat(ch) - gets an objects properties
        if type(objtext) is int:
            objtext = str(objtext)
        if type(objdesc) is int:
            objdesc = str(objdesc)
        if type(objlocator) is int:
            objlocator = str(objlocator)
        if type(objtype) is int:
            objtype = str(objtype)
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        objtypelist = ["Number","Value", "Element", "TextField", "Textbox", "Link", "Page""URL", "Label", "Button", "Image", "Radio","Checkbox", "Combobox", "Combo", "Window", "Editbox"]
        if objlocator and objtype and objdesc and not cl().should_contain_match(objtypelist, objtype):

            if objtype == 'Element' or objtype == 'Label' or objtype == 'Textfield' or objtype == 'Textbox' or objtype == 'Editbox':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    gettext = s2l().get_text(objlocator)
                    return gettext

            if objtype == 'Number' or objtype == 'Value':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_element(objlocator)
                    gettext = s2l().get_value(objlocator)
                    return gettext

            if objtype == 'Text':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain(objlocator)
                    gettext = s2l().get_text(objlocator)
                    return gettext

            if objtext:
                logger.info("Get [" + objtext + "]", html=True, also_console=True)
                if not docflag:
                    s2l().element_should_contain(objlocator, objtext)
                    return objtext

            if objtype == 'Page':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    getloc = s2l().get_location()
                    return getloc

            if objtype == 'Link':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_link(objlocator)
                    getattrib = s2l().get_element_attribute(objlocator + "@herf")
                    bi().set_test_message(getattrib)
                    return getattrib

            if objtype == 'Button':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_button(objlocator)
                    gettext = s2l().get_text(objlocator)
                    return gettext

            if objtype == 'Radio' or objtype == 'RadioButton':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_radio_button(objlocator)
                    getclicked = s2l().get_element_attribute(objlocator + "@clicked")
                    return getclicked

            if objtype == 'Checkbox':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_checkbox(objlocator)
                    getchecked = s2l().get_element_attribute(objlocator + "@checked")
                    return getchecked

            if objtype == 'Combobox' or objtype == 'Combo':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_list(objlocator)
                    getselected = s2l().get_element_attribute(objlocator + "@SelectedItem")
                    return getselected

            if objtype == 'Window':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    windowslist = s2l().get_window_titles()
                    return windowslist

            if objtype == 'Image':
                logger.info("Get [" + objdesc + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain_image(objlocator)
                    getattrib = s2l().get_element_attribute(objlocator + "@Alt")
                    return getattrib

        else:
            if objlocator and objtype == "" and objdesc == "" and objtext == "":
                logger.info("Get [" + str(objlocator) + "]", html=True, also_console=True)
                if not docflag:
                    s2l().page_should_contain(objlocator)
                    gettext = s2l().get_text(objlocator)
                    return gettext

            if objlocator and objtype and objdesc == None and objtext == None:
                logger.info("Compare [" + objlocator + "] [" + objtype + "]", html=True, also_console=True)
                if not docflag:
                    bi().should_be_equal_as_strings(objlocator, objtype)

            if objlocator and objtype and objdesc and cl().should_contain_match(objtypelist, objtype):
                bi().fail("The Object Type [" + objtype + "] for [" + objlocator + "] doesnt exist as specified in Objectmap file")

    def wait(self,objlocator, objtype="", objdesc="", objtext=""):
        #wait - waits for element
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        if type(objtext) is int:
            objtext = str(objtext)
        if type(objdesc) is int:
            objdesc = str(objdesc)
        if type(objlocator) is int:
            objlocator = str(objlocator)
        if type(objtype) is int:
            objtype = str(objtype)
        objtypelist = ["Number","Element","Text", "TextField", "Textbox", "Link", "Page","URL", "Label", "Button", "Image", "Radio",
                       "Checkbox", "Combobox", "Combo", "Window", "Editbox"]
        if objtype == "" or 'timeout=' in objtype:
            if not docflag:
                if 'timeout=' in objtype:
                    logger.info("Waiting for [" + objlocator + "] with a timeout of [" + timeout + "]", html=True,also_console=True)
                    timeout = objtype.split("timeout=",1)[1]
                    s2l().wait_until_page_contains(objlocator, timeout)
                else:
                    logger.info("Waiting for [" + objlocator + "]", html=True, also_console=True)
                    s2l().wait_until_page_contains(objlocator)
        else:
            if not cl().should_contain_match(objtypelist, objtype):
                bi().fail(
                    "The Object Type [" + objtype + "] for [" + objlocator+ "] doesnt exist as specified in Objectmap file")
            if not objdesc:
                bi().fail("The Object map item [" + objlocator+ "] is missing its docuemntion field")
            if objtype == 'Image' or objtype == 'Combobox' or objtype == 'Combo' or objtype == 'Checkbox' or objtype == 'Link' or objtype == 'Button' or objtype == 'Radio' or objtype == 'Element' or objtype == 'Label' or objtype == 'Textfield' or objtype == 'Textbox' or objtype == 'Editbox':
                logger.info("Waiting for [" + objtype + "]", html=True, also_console=True)
                if not docflag:
                    s2l().wait_until_page_contains_element(objlocator)
            if objtext or objtype == 'Page':
                logger.info("Waiting for [" + objtype + "]", html=True, also_console=True)
                if not docflag:
                    s2l().wait_until_page_contains(objtext)

    @staticmethod
    def save(self,objlocator="", objtype="", objdesc="", objtext=""):
        if objtype == "":
            objloc = "tempvar"
        else:
            objloc = objtype
        gettext = Selenium2LibraryKeywords.cat(objlocator, objtype, objdesc, objtext)
        bi().set_suite_variable('${objloc}', gettext)
        bi().set_test_message(objloc + ":" + gettext)
        return gettext

    @staticmethod
    def load(self,objlocator="", objtype="", objdesc="", objtext=""):
        if objtype == "":
            objloc = "tempvar"
        else:
            objloc = objlocator
        varvalue = bi().get_variable_value(objloc)
        return varvalue

    @staticmethod
    def Msg(self,message):
        if type(message) is int:
            message = str(message)
        logger.info("" +message, html=True, also_console=True)


    def page_should_contain_element(self,objlocator="", objtype="", objdesc="", objtext=""):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        logger.info("Verify [" + str(objdesc) + "] " + objlocator + " exists", html=True, also_console=True)
        if not docflag:
            s2l().page_should_contain_element(objlocator)

    def page_should_contain(self, objlocator="", objtype="", objdesc="", objtext=""):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        logger.info("Verify [" +objdesc+ "] [" + objlocator + "] exists", html=True, also_console=True)
        if not docflag:
            s2l().page_should_contain(objtype)

    def capture_screenshot(self, filename='selenium-screenshot-{index}.png'):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        if not docflag:
            s2l().capture_page_screenshot(filename)
        else:
            logger.info("Nothing to capture - Documentation Only Mode", html=True, also_console=True)

    def screenshot(self, filename='selenium-screenshot-{index}.png'):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        if not docflag:
            s2l().capture_page_screenshot(filename)
        else:
            logger.info("Nothing to capture - Documentation Only Mode", html=True, also_console=True)

    def set_selenium_implicit_wait(self, seconds):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        if not docflag:
            s2l().set_selenium_implicit_wait(seconds)

    def set_screenshot_directory(self, path, persist=False):
        docflag = util.strtobool(bi().get_variable_value("${DOCEXECONLY}"))
        logger.info(bi().get_variable_value("${OUTPUTDIR}"), html=True, also_console=True)
        if not docflag:
            s2l().set_screenshot_directory(path)

    def time_start(self,label):
        global starttime
        starttime = time.time()
        #logger.info(starttime, html=True, also_console=True)

    def time_stop(self, label):
        global stoptime
        stoptime = time.time()
        #logger.info(stoptime, html=True, also_console=True)
        elasped = round(stoptime - starttime, 2)
        #logger.info(elasped, html=True, also_console=True)
        return elasped




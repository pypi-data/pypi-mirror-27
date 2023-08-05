# -*- coding: utf-8 -*-

"""ICM Library: Interactive Command Modules (ICM) -- Cmnd methods of ICM classes are auto invokable at command line.

Command line parameters and arguments are passed to Icm.cmnd. ICMs are capable of communicating 
their full command line parameters and arguments syntax and expectations to ICM Players. 
"""

####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./iimMiniDist.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/iimMiniDist.py"
"""\
Part of ByStar Digital Ecosystem http://www.by-star.net.
This module's primary documentation is in  http://www.by-star.net/PLPC/180047

This Python module was developed in the 
    COMEEGA: Collaborative Org-Mode Enhanced Emacs Generalized Authorship
model and is intended to be maintained in that model. Reading and editing this module
is best done with emacs and org-mode. Do not edit unless you are familiar with dblock org-mode.
Do not modify anything within a "dblock" as they are meant to be overwritten.
"""
####+END:

"""
*  [[elisp:(org-cycle)][| ]]  Author        :: Author and Version Information [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| *Module-INFO:* |]]
"""
####+BEGINNOT: bx:dblock:global:iim:name-py :style "fileName"
__libName__ = "icm"
####+END:

####+BEGIN: bx:dblock:global:timestamp:version-py :style "date"
__version__ = "201712050236"
####+END:

__status__ = "Production"
__credits__ = [""]

# NOTYET dblk-begin
iicmInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'copyright':       "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]",
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]",],
    'contacts':        ["[[http://mohsen.1.banan.byname.net/contact]]",],
    'partOf':          ["[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]",]
}
# NOTYET dblk-end


"""
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
*      ================
*  /Controls/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]] 

####+END:
"""

"""
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/pythonWb.org"
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "pep8 %s" (bx:buf-fname))))][pep8]] | [[elisp:(python-check (format "flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]

####+END:
"""

"""
*      ================
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]] CONTENTS-LIST ################
*  [[elisp:(org-cycle)][| ]]  Notes         :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
*  [[elisp:(org-cycle)][| ]]  Info          :: *[Info]* General TODO List [[elisp:(org-cycle)][| ]]
**     ============ Essential Features TODO
*** TODO ======== Add the EH_ module.
*** TODO Common ICM Parameter -- Out Stream Consumer/Usage Context  --oUsage=icmPlayerBlee
"""


"""
*  [[elisp:(org-cycle)][| ]]  /Iif/                :: *Iif Main Class* [[elisp:(org-cycle)][| ]]
"""

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  Iif    [[elisp:(org-cycle)][| ]]
"""

class Iif(object):
    """	IIF docString. 	"""
    iifParamsMandatory = list()  # ['inFile']
    iifParamsOptional = list()   # ['perhaps']
    iifArgsLen = {'Min': 0, 'Max':0,}
    iifArgsSpec = dict()  # {1: []}  

    iifVisibility = ["all"]  # users, developers, internal
    iifUsers = []            # lsipusr
    iifGroups = []           # bystar
    iifImpact = []           # read, modify

    def __init__(self,
                 cmndLineInputOverRide=None,
                 iifOutcome = None,  
    ):
        self.cmndLineInputOverRide = cmndLineInputOverRide
        self.iifOutcome = iifOutcome       

    def docStrClass(self,):
        return self.__class__.__doc__

    def docStrIifMethod(self,):
        return self.iif.__doc__

    def paramsMandatory(self,):
        return self.__class__.iifParamsMandatory

    def paramsOptional(self,):
        return self.__class__.iifParamsOptional

    def argsLen(self,):
        return self.__class__.iifArgsLen

    def argsDesc(self,):
        return self.__class__.iifArgsSpec
    
    def users(self,):
        return self.__class__.iifUsers

    def groups(self,):
        return self.__class__.iifGroups

    def impact(self,):
        return self.__class__.iifImpact

    def visibility(self,):
        return self.__class__.iifVisibility

    def getOpOutcome(self):
        if self.iifOutcome:
            return self.iifOutcome
        return OpOutcome(invokerName=self.myName())

    def cmndLineValidate(
            self,
            outcome,
    ):
        if self.cmndLineInputOverRide:
            return True
            
        errorStr = self.iifArgsLenValidate()
        if errorStr:
            outcome.error = OpError.CmndLineUsageError
            outcome.errInfo = errorStr
            return False
        errorStr = self.iifParamsMandatoryValidate()
        if errorStr:
            outcome.error = OpError.CmndLineUsageError
            outcome.errInfo = errorStr
            return False
        errorStr = self.iifParamsOptionalValidate()
        if errorStr:
            outcome.error = OpError.CmndLineUsageError
            outcome.errInfo = errorStr
            return False
        return True

    def iifArgsLenValidate(self,
    ):
        """ If not as expected, return an error string, otherwise, None.

    expectedIifArgsLen is a dcitionary with 'Min' and 'Max' range.
    """
        iifArgsLen = len(IicmGlobalContext().iimRunArgsGet().iifArgs)
        expectedIifArgsLen = self.__class__.iifArgsLen

        def errStr():
            errorStr = "Bad Number Of iifArgs: iifArgs={iifArgs} --".format(iifArgs=iifArgsLen)
            if expectedIifArgsLen['Min'] == expectedIifArgsLen['Max']:
                errorStr = errorStr + "Expected {nu}".format(nu=expectedIifArgsLen['Min'])
            else:
                errorStr = errorStr + "Expected between {min} and {max}".format(
                    min=expectedIifArgsLen['Min'],
                    max=expectedIifArgsLen['Max']
                )
            return errorStr

        if iifArgsLen < expectedIifArgsLen['Min']:
            retVal = errStr()
        elif iifArgsLen > expectedIifArgsLen['Max']:
            retVal = errStr()
        else:
            retVal = None

        #parser=argparse.ArgumentParser()
        #parser.print_help()

        return(retVal)

    def iifParamsMandatoryValidate(self,
    ):
        """If not as expected, return an error string, otherwise, None.

    expectedIifArgsLen is a dcitionary with 'Min' and 'Max' range.
    """
        G = IicmGlobalContext()
        iicmRunArgs = G.iimRunArgsGet()
        iicmRunArgsDict = vars(iicmRunArgs)

        iifParamsMandatory = self.__class__.iifParamsMandatory

        for each in iifParamsMandatory:
            if each in iicmRunArgsDict.keys():
                continue
            else:
                return "Unexpected Mandatory Param: param={param} --".format(param=each)

        for each in iifParamsMandatory:
            if iicmRunArgsDict[each] == None:
                return "Missing Mandatory Param: param={param} --".format(param=each)                
            else:
                continue
        
        for each in iifParamsMandatory:
            exec(
                "G.usageParams.{paramName} = iicmRunArgs.{paramName}"
                .format(paramName=each)
            )
        return None

    def iifParamsOptionalValidate(self,
    ):
        """If not as expected, return an error string, otherwise, None.

    expectedIifArgsLen is a dcitionary with 'Min' and 'Max' range.
    """
        G = IicmGlobalContext()
        iicmRunArgs = G.iimRunArgsGet()
        iicmRunArgsDict = vars(iicmRunArgs)

        iifParamsOptional = self.__class__.iifParamsOptional

        for each in iifParamsOptional:
            if each in iicmRunArgsDict.keys():
                continue
            else:
                return "Unexpected Optional Param: param={param} --".format(param=each)
        
        for each in iifParamsOptional:
            #if iicmRunArgsDict[each] != None:
            exec(
                "G.usageParams.{paramName} = iicmRunArgs.{paramName}"
                .format(paramName=each)
            )
        return None

    
    def myName(self,):
        return self.__class__.__name__
            
    def iif(self, interactive=False):
        print "This is default Iif Class Definition -- It is expected to be overwritten. You should never see this."

        



"""
**     ============  IIM Model -- Obsoleted By: /libre/ByStar/InitialTemplates/activeDocs/bxRefModel/iim/fullUsagePanel-en.org
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  model    [[elisp:(org-cycle)][| ]]
"""

class model(Iif):
    """Print a summary of the IICM Model."""

    #@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=True,
    ):
        """Description of IICM Model."""
        
        description = """
** Python-IICM Overview: file:/libre/ByStar/InitialTemplates/activeDocs/bxRefModel/iim/fullUsagePanel-en.org

** Obtaining IIM
You can obtain IIM with:
 pip install bystar-iicm

** Some Simple Complete Examples For Using IIM-IIM
*** iimEmpty.py  -- A minimal iim module with no specific features but all common capabalities
*** iimBegin.py  -- A template for starting IIMs (Interactively Invokable Modules)
*** iimTargetBegin.py  -- A template for starting Target Oriented IIMs (Interactively Invokable Modules)

** Python-Iim-General Facilities:

*** Python-Iim-Logging
Python-Iim-Logging is based on [[http://docs.python.org/2/library/logging.html][the python logging library]]

*** Python-Iim-CallTracking
Two types of invokation tracking are widespread practice in hlip.
Both of these are controlable at IIM Interface
**** iim.do -- at the time of invokation
    Logging can be controlled at command-line by  "--callTrackings invoke+" / "--callTrackings invoke-"

**** @subjectToTracking  -- at the time of definition
    Amount of tracking is controlled with subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    Logging can be controlled at command-line by  "--callTrackings monitor+" / "--callTrackings monitor-"

** IIM Model -- (Python-Iim-IIM)  (Interactively Invokable Module):
An IIM is a collection of Interactively Invokable Facilities/Functions (IIF)

The module includes an abstract user interface. This Abstract User
Interface can then be bound to concrete and consistent user
interfaces. Four types of User Interfaces (IIM-UI)s are considered primary:

-- 1) Unix Command Line
-- 2) Web Based (Django) IIM
-- 3) Emacs IIM
-- 4) Module Dispatch Utilities (Eden-NET SON)

A particular IIM can be used with any IIM-UI.

Some IIMs in pratctice are only used on Command Line.

*** IIM and the Platform-UI Paradigm

- The module is cabapble of everything. The module does not exist in the
  context of a framework. The framework supports the module.
- The module is capable of producing its own user interface.

The Model of IIM can be based on IIM_Targets and IIM_Param which are in turn
based on FILE_TreeObject and FILE_Param.

*** FILE_TreeObject
Is an object, which is part of a tree of objects, residing on the file system.
**** _object: Specifies Object Type
**** _tree:   (node, leaf, ignore, ignoreNode, ignoreLeaf, auxNode, auxLeaf)
**** _treeProc:  specifies a processor at point which processes _object in _tree
*** FILE_Param
**** _object=FILE_Param subject to _tree processing
**** FILE_Param is pure information, it is to be manipulated. It is inherently persistent.
     The concept of a FILE_Param dates back to [[http://www.qmailwiki.org/Qmail-control-files][Qmail Control Files]] (at least).
     A FILE_Param is broader than that concept in two respects.
     1) A FILE_Param is represented as a directory on the file system. This FILE_Param
        permits the parameter to have attributes beyond just a value. Other attributes
        are themselves in the form of a traditional filename/value.
     2) The scope of usage of a FILE_Param is any parameter not just a control parameter.
*** FILE_ParamDict
**** Collection of FILE_Param s can be placed in FILE_ParamDict.
*** IIM_Param
**** Are Parameters in the context of IIM.
**** IIM_Params are created inside of IIM as part of Module Definition.
**** IIM_Params are meant to map on to argsparse.
**** IIM_Params are meant to map on to FILE_Param.
**** An IIM_Param is one of the following:
     - An IIM_TargetParameter
     - An IIM_ General Parameter
     - An IIF_ Specific Parameter

*** IIM_ParamDict
**** Collection of IIM_Param s can be placed in IIM_ParamDict.

*** RealWordEntities is Reality-Out-There that is abstracted as IIM_Target in the context of IIM.

*** TARGET_Elem in the context of IIM is abstraction of RealWordEntities.
IIM_Target is often a set of collections of FILE_Params.

**** IIM_TargetObjClass  -- Type Of Objects of TargetList (eg, Unix User Account)

**** IIM_TargetDomain    -- Domain of possible Targets

**** IIM_TargetSelectionProcess  -- The mechanism for choosing TargetList based on TargetDomain

**** TargetList  (Not TargetsList) -- List Of Tragets for TargetAction

**** TargetListParameters  -- A set of parameters specified for a given target

*** TARGET_Proxy_ is a set of facilities that establish relations between TARGET_Elem and RealWordEntities.
A TARGET_Proxy_ provides communication and mapping between either the entire
TARGET_Elem and RealWordEntities or pieces/aspects of it. In which case a
TARGET_Elem_Aspect is representation of TARGET_Elem_Aspect.

A TARGET_Proxy always have the following:

**** A reference to one TARGET_Elem
**** A context for applicable TARGET_Elem_Aspect
        A TARGET_Elem_Aspect is one set of parameters of a TARGET_Elem
**** A Get() facility for the TARGET_Elem_Aspect which gets the Aspect from RealWordEntity.
**** A Set() facility for the TARGET_Elem_Aspect which sets the Aspect to RealWordEntity.
**** A Pull() facility for the TARGET_Elem_Aspect which pulls the Aspect from RealWordEntity and updates Aspect.
**** A Push() facility for the TARGET_Elem_Aspect which pushes the Aspect to RealWordEntity.


**** A Verify() facility to check if the TARGET_Elem_Aspect is same as RealWordEntity.


*** IIF or TragetAction -- (Python-Iim-IIF)  (Interactive Invokable Functions):
An IIF/TargetAction is a python callable that conforms to the IIM model.

An IIF can receive:
   1- A set of IIM_Params and NO TargetList
   2- A set of IIM_Params and a TargetList
   3- A set of IIM_Params and TargetParams and a TaregtList
   4- An optional TargetParams and a TargetList

The IIF always receives:
    A- An IIM_FILE_Params
    B- A TargetParams List
    C- A TargetList

For 1)
  - A tmpTarget
  - An entry in TargetList
  - A Tmp IIM FILE_Param

**** TargetAction Options (--option spec)

**** TargetAction Arguments (follow --invoke iif)
**** EphemeraTarget Vs PersistentTarget
*** IIM-Context

**** iimRunArgs  (Arguments passed to IIM eg. on command line)

**** iimTargetList

**** iimTargetListParameters

*** IIM Function Types (Specified in callableEntryEnhancer)
**** IIF Function-Type
**** WithUsageArgs Function-Type
**** Unstated Function-Type

*** The Big Distributed File System (BDFS) Under IIM
**** We don't call it Hadoop -- Because Hadoop could well be just a
     first generation fad.
*** Target and TargetParameter Communication through the BDFS
**** See IimFileParams module
*** Python-Iim-IIM Common UI Features: (See iimHelp())
*** Python-Iim-IIUIs  (Interactively Invokable User Interfaces):
**** Command Line -- Native model of Executing IIMs
**** Web Based -- A Framework For specifying and executing IIMs
**** Emacs IIM --

** IIM Execution Phases
*** Module Specification
**** General Parameters Option Specification
**** TARGET_Elem Parameter Option Specification
**** IIF Specification
*** Target Parameters Specification
*** Target Selection
*** Module Execution
**** General Parameters Value Specification
**** TARGET_Elem Parameter Value Specification
*** Run-Time Params To FILE_ and TARGET_ Bindings
**** Run-Time Params To FILE_Param/ephemera Bindings
**** Run-Time Params To TARGET_Elem/ephemera Bindings
**** Run-Time Params To TARGET_Elem/perm Bindings (new)
*** IIF Invokation Based on FILE_ and TARGET_ Bindings
**** iifUsageArgsObtain() -- Potentially Cross UI
**** withUsageArgs function invokations
** IIF Execution Stages
*** Obatin iimRunArgs
*** Obtain TargetParamsList
*** Obtain TargetList
*** iifUsageArgsObtain() -- On a per iif basis gather args in G.usageArgs.argName
*** withUsageArgs is a /function type/ that can only be called after iifUsageArgsObtain()
** Structure Of Target Oriented Interactively Invokable Modules (TOIIM)

** Python-Iim-IIM Development Environment
You can develop you Python-Iim-IIM with any ide that you wish.
But power and beauty of Python-Iim-IIM only fully comes through Python-Blee

*** [[http://www.by-star.net/PLPC/180004][Python-Blee]]
Blee permits you to mix Python and [[http://www.org-mode.org][org-mode]].
This is how this module was developed and how it is best viewed.

Dynamic Blocks are used in the source code.
Do not modify anything within a "dblock" as they are meant to be overwritten.

        """
        if interactive: print description
        return description


"""
**     ============  IIM Help -- Common UI Features
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iicmHelp    [[elisp:(org-cycle)][| ]]
"""

class iicmHelp(Iif):
    """Print a summary of the IICM Model."""

    #@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=True,
    ):
        """Description of IICM Model."""
        
        description = """

** Python-Iim-IIM Common UI Features:

Command Line (User Interface based on options, arguments and sub-commands)
IIM is based on [[http:docs.python.org/dev/library/argparse.html][argsparse]] with a set of well defined pre-specified options.
The "-"/"--invoke" in particular permits rapid module development.

***  --help
***  -i iim.model
***  -i describe  (Applies to the G_ IIM)
***  -i examples
***  --customOpt -i iif arg1 arg2

** Logging Control
***  -v 1 or --verbosity 1  (logging level 1 to 50 -- 1 means most verbose)
***  --logFile /var/log/somefile    (Specifies destination LogFile for this run)

** Callable Monitor Logging Control
***  --callTrackings monitor+  (or: --callTrackings monitor-)

** Callable Invokation Logging Control
***  --callTrackings invoke+  (or: --callTrackings invoke-)

** Run Mode (dryRun vs fullRun)
*** --runMode dryRun (or: --runMode fullRun runDebug)

** Load Python code in Global Context from iim module
*** --load file1.py --load file2.py

** Extract (display) an IIF's docstring
*** --docstring -i iif
        """
        if interactive: print description
        return description

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Imports And Description -- describe()*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=        ::  Imports [[elisp:(org-cycle)][| ]]
"""

import sys
import os
import argparse
import inspect
from datetime import datetime
import time
import logging
#import pexpect
# Not using import pxssh -- because we need to custom manipulate the prompt
#import re

#import ast

import shlex
import subprocess

#from unisos.ucf import ucf
from unisos import ucf


"""
*  [[elisp:(org-cycle)][| ]]  /General/            :: *Common Utilities -- Constants, Variables* [[elisp:(org-cycle)][| ]]
"""


"""
*  [[elisp:(org-cycle)][| ]]  /Enumerations/       :: *Common Global Enumerations* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  ReturnCode -- Obsoleted   [[elisp:(org-cycle)][| ]]
"""

class ReturnCode():
    """ Argument Requirements: For Specification Of Required Keyword Arguments."""
    Success = 0
    Failure  = 1
    ExtractionSuccess = 11                                  
    UsageError = 201

    def __init__(self):
        pass


"""
*  [[elisp:(org-cycle)][| ]]  /Operations/       :: *Operation Results* [[elisp:(org-cycle)][| ]]
"""
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Constants        ::  OpError    [[elisp:(org-cycle)][| ]]
"""
    
OpError = ucf.Constants()
opErrorDesc = {}

OpError.Success = 0
opErrorDesc[OpError.Success] = "Successful Operation -- No Errors"
OpError.Failure = 1
opErrorDesc[OpError.Failure] = "Catchall for general errors",
OpError.ShellBuiltinMisuse = 2    
opErrorDesc[OpError.ShellBuiltinMisuse]= "Bash Problem"
OpError.ExtractionSuccess = 11
opErrorDesc[OpError.ExtractionSuccess] = "NOTYET"
OpError.PermissionProblem = 126
opErrorDesc[OpError.PermissionProblem] = "Command invoked cannot execute"
OpError.CommandNotFound = 127
OpError.ExitError = 128
OpError.Signal1 = 128+1
OpError.ControlC = 130
OpError.Signal9 = 128+9
# ByStar Base Error Starts at 155
OpError.UsageError = 201
OpError.CmndLineUsageError = 202
OpError.ExitStatusOutOfRange = 255


####+BEGIN: bx:dblock:python:func :funcName "notAsFailure" :funcType "succFail" :retType "bool" :deco "" :argsList "obj"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-succFail  :: /notAsFailure/ funcType=succFail retType=bool deco= argsList=(obj)  [[elisp:(org-cycle)][| ]]
"""
def notAsFailure(
    obj,
):
####+END:
    if not obj:
        return  OpError.Failure
    else:
        return  OpError.Success



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  opErrorDescGet -- return opErrorDesc[opError]   [[elisp:(org-cycle)][| ]]
"""
def opErrorDescGet(opError):
    """ OpError is defined as Constants. A basic textual description is provided with opErrorDescGet().

Usage:  opOutcome.error = None  -- opOutcome.error = OpError.UsageError
OpError, eventually maps to Unix sys.exit(error). Therefore, the range is 0-255.
64-to-78 Should be made consistent with /usr/include/sysexits.h.
There are also qmail errors starting at 100.
"""
    # NOTYET, catch exceptions
    return opErrorDesc[opError]



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  OpOutcome -- .log() .isProblematic()   [[elisp:(org-cycle)][| ]]
"""
class OpOutcome(object):
    """ Operation Outcome. Consisting Of Error and/or Result -- Operation Can Be Local Or Remote

** TODO Add exception and exceptionInfo For situations where try: is handled
** TODO Add opType as one of PyCallable -- SubProc, RemoteOp
** TODO Add a printer (repr) for OpOutcome

OpOutcome is a combination of OpError(SuccessOrError) and OpResults.
                                                         
Typical Usage is like this:

On Definition of f():
thisOutcome = OpOutcome()
thisOutcome.results = itemOrList
)
return(thisOutcome.set(
    opError=None,
    ))

Then on invocation:
thisOutcome = OpOutcome()
opOutcome = f()
if opOutcome.error: return(thisOutcome.set(opError=opOutcome.error))
opResults = opOutcome.results
"""
    def __init__(self,
                 invokerName=None,
                 opError=None,
                 opErrInfo=None,
                 opResults=None,
                 opStdout=None,
                 opStderr=None,
                 opStdcmnd=None,                                  
    ):
        '''Constructor'''
        self.invokerName = invokerName
        self.error = opError
        self.errInfo  = opErrInfo
        self.results = opResults
        self.stdout = opStdout
        self.stderr = opStderr
        self.stdcmnd = opStdcmnd      

    def set(self,
            invokerName=None,
            opError=None,
            opErrInfo=None,
            opResults=None,
            opStdout=None,
            opStderr=None,
            opStdcmnd=None,                        
    ):
        if invokerName != None:
            self.name = invokerName
        if opError != None:
            self.error = opError
        if opErrInfo != None:
            self.errInfo = opErrInfo
        if opResults != None:
            self.results = opResults
        if opStdout != None:
            self.stdout = opStdout
        if opStderr != None:
            self.stderr = opStderr
        if opStdcmnd != None:
            self.stdcmnd = opStdcmnd
            
        return self
    
    def isProblematic(self):
        if self.error:
            IicmGlobalContext().__class__.lastOpOutcome = self
            return True
        else:
            return False


    def log(self):
        G = IicmGlobalContext()
        LOG_here(G.iicmMyFullName() + ':' + str(self.invokerName) + ':' + ucf.stackFrameInfoGet(2))
        if self.stdcmnd: LOG_here("Stdcmnd: " +  self.stdcmnd)
        if self.stdout: LOG_here("Stdout: " +  self.stdout)        
        if self.stderr: LOG_here("Stderr: " +  self.stderr)
        return self


    def out(self):
        G = IicmGlobalContext()
        ANN_here(G.iicmMyFullName() + ':' + str(self.invokerName) + ':' + ucf.stackFrameInfoGet(2))
        if self.stdcmnd: ANN_write("Stdcmnd: \n" +  self.stdcmnd)
        if self.stdout: ANN_write("Stdout: ")
        if self.stdout: OUT_write(self.stdout)                
        if self.stderr: ANN_write("Stderr: \n" +  self.stderr)
        return self
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  opSuccess    [[elisp:(org-cycle)][| ]]
"""    
def opSuccess():
    """."""
    return (
        OpOutcome()
    )


class OpRemoteIif(object):
    """ Remote operation specification and invocation of an IIF through IICM command line.

Returns OpOutcome.

** TODO Developement Status: in-progress.
                                                         
Typical Usage:
performerIif = OpRemoteIif()
performerIif.performerInfo(
    remoteOpMethod="ssh",
    remoteOpSap=21,
    performerHost=ipAddrOrName,
    performerUser=lsipusr,
    performerCredentials=pubKey,
)
performerIif.cmndElems(
    iicmName="prog",
    iifName="iifName",
    iifMandatoryParams=listOfPars,
    iifOptionalParams=listOfOpts,
    iifArgs=listOfArgs,
    iicmParams=listOfCmndParams,
)
Or 
performerIif.cmndLine=cmndString

remoteOpOutcome = performerIif.perform()
"""
    def __init__(self,
                 remoteOpMethod=None,
                 remoteOpSap=None,
                 performerHost=None,
                 cmndLine=None,                 
    ):
        '''Constructor'''
        self.remoteOpMethod = remoteOpMethod
        self.cmndLine = cmndLine

    def performerInfo(self,
    ):
        return self

    def cmndElems(self,
    ):
        return self

    def perform(self,
    ):
        return self
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  ArgReq -- Obsoleted   [[elisp:(org-cycle)][| ]]
"""
#ArgReq = enum('Mandatory', 'Optional')   # Argument Requirements -- Mandatory Keyword Arguments
class ArgReq():
    """ Argument Requirements: For Specification Of Required Keyword Arguments.

    Example: ArgReq.Conditional -- to be used at declaration time.
    """
    Mandatory = "___Mandatory___"
    Optional = "___Optional___"
    Conditional = "___Conditional___"

    def __init__(self):
        pass

    def isMandatory(self, arg):
        """Predicate."""
        if arg == self.Mandatory:
            return True
        else:
            return False

    def mandatoryValidate(self, arg):
        """Predicate."""        
        if self.isMandatory(arg):
            EH_problem_info("Missing Mandatory Argument")
            # It is the caller's frame that is of significance
            raise ValueError("Missing Mandatory Argument: " + ucf.stackFrameInfoGet(2))
        return arg


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  Interactivity -- Obsoleted   [[elisp:(org-cycle)][| ]]
"""

class Interactivity():
    """ The interactive= keyword argument is specified as below and invoked as True or False."""
    Only = "___Only___"          # Should Only Be Invoked Interactively
    Both = "___Both___"          # Can Be Invoked Interactive Or Non-Interactively
    Not = "___Not___"            # Should Not Be Invoked Interactively

    def __init__(self):
        pass

    def interactiveInvokation(self, interactive):
        if interactive:
            return True
        else:
            return False



"""
*  [[elisp:(org-cycle)][| ]]  /General/            :: *Call Tracking (decorators)* [[elisp:(org-cycle)][| ]]
"""


"""
**  [[elisp:(org-cycle)][| ]]  Decorator     ::  Callable Tracking subjectToTracking()   [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  subjectToTracking    [[elisp:(org-cycle)][| ]]
"""

def subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True):
    """[DECORATOR-WITH-ARGS:]  Passes parameters to subSubjectToTracking. See subSubjectToTracking.
    """

    def subSubjectToTracking(fn):
        """[DECORATOR:] tracks calls to a function.

        Returns a decorated version of the input function which "tracks" calls
        made to it by writing out the function's name and the arguments it was
        called with.
        Do so subject to iimRunArgs_isCallTrackingMonitorOn and
        fnLoc, fnEntry, fnExit parameters.
        """

        import functools
        # Unpack function's arg count, arg names, arg defaults
        code = fn.func_code
        argcount = code.co_argcount
        argnames = code.co_varnames[:argcount]
        fn_defaults = fn.func_defaults or list()
        argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

        @functools.wraps(fn)
        def wrapped(*v, **k):
            if (fnLoc == False) and (fnEntry == False) and (fnExit == False):
                return fn(*v, **k)

            #if iimRunArgs_isCallTrackingMonitorOff():   # normally on, turns-off with monitor-
                #return fn(*v, **k)

            if not iimRunArgs_isCallTrackingMonitorOn(): # normally off, turns-on with monitor+
                return fn(*v, **k)

            # Collect function arguments by chaining together positional,
            # defaulted, extra positional and keyword arguments.
            positional = map(ucf.format_arg_value, zip(argnames, v))
            defaulted = [ucf.format_arg_value((a, argdefs[a]))
                         for a in argnames[len(v):] if a not in k]
            nameless = map(repr, v[argcount:])
            keyword = map(ucf.format_arg_value, k.items())
            args = positional + defaulted + nameless + keyword

            logControler = LOG_Control()
            logger = logControler.loggerGet()

            if fnLoc:
                depth = ucf.stackFrameDepth(2)
                indentation = ucf.STR_indentMultiples(multiple=depth)

                logger.debug(format('%s Monitoring(M-Call-%s): ' % (indentation, depth)) + ucf.stackFrameInfoGet(2))

            if fnEntry:
                logger.debug( "%s M-Enter-%s: %s(%s)" % (indentation, depth, fn.__name__, ", ".join(args)) )


            retVal = fn(*v, **k)

            if fnExit:
                logger.debug( "%s M-Return-%s(%s):  %s" % (indentation, depth, fn.__name__, retVal) )


            return retVal
        return wrapped
    return subSubjectToTracking


# def subjectToDryRun(fn):
#     """[DECORATOR] Subject the function to DryRun predicate.
#     """
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  callableEntryEnhancer    [[elisp:(org-cycle)][| ]]
"""

def callableEntryEnhancer(type='generic'):
    """\
    For now this is somewhat Complex,
    The Real parts are:
       - When requested, the callable's docstring is extracted.
         The request is either:
         --docString
         or type=describe
    The Imaginary parts are:
       - Callables are assigned --type (eg, iif)--, then
         list of all of a given type can be produced
         The iif type mimics Emacs' (interactive)
    """
    if iimRunArgs_isDocStringRequested():
        print( ucf.stackFrameInfoGet(2) )
        #print( stackFrameArgsGet(2) )
        print( ucf.stackFrameDocString(2) )

        raise StopIteration()

    if type == 'iif':
        # Tag it as Interactive
        pass
    elif type == 'describe':
        #print( stackFrameArgsGet(2) )
        print( ucf.stackFrameDocString(2) )
    elif type == 'iimUiSupport':
        pass
    elif type == 'generic':
        pass
    else:
        TM_here()
        raise StopIteration()


"""
**  [[elisp:(org-cycle)][| ]]  Func          ::  loadFile (based on execfile)   [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  loadFile    [[elisp:(org-cycle)][| ]]
"""
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def loadFile(file):
    """Load the specified python file."""

    global globdict
    globdict= globals()

    TM_here('IIM-Loading: ' + file)
    execfile(file, globdict)


"""
**  [[elisp:(org-cycle)][| ]]  Func          ::  Invokation Tracking do() and doLog()  [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  do    [[elisp:(org-cycle)][| ]]
"""
subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def do(fn, *v, **k):
    """Invokes fn with args (*v, **k) and logs the invocation and return based on invoke+/-.

    If invoke+ is set, invokation is logged. Otherwise it just invokes the function.
    Example Usage:
    instead of thisFunc(thatArg) in order to track thisFunc we:
    do(thisFunc, thatArg)
    """

    if iimRunArgs_isCallTrackingInvokeOff():
        return fn(*v, **k)

    #
    # Even though the call is identical because of stackFrameInfoGet(2)
    # in there, we are not going to --  return doLog(fn, *v, **k)
    # And instead we are duplicating the code.
    # Consider this an instance for why python should have macros.
    #

    # Unpack function's arg count, arg names, arg defaults
    code = fn.func_code
    argcount = code.co_argcount
    argnames = code.co_varnames[:argcount]
    fn_defaults = fn.func_defaults or list()
    argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

    # Collect function arguments by chaining together positional,
    # defaulted, extra positional and keyword arguments.
    positional = map(ucf.format_arg_value, zip(argnames, v))
    defaulted = [ucf.format_arg_value((a, argdefs[a]))
                 for a in argnames[len(v):] if a not in k]
    nameless = map(repr, v[argcount:])
    keyword = map(ucf.format_arg_value, k.items())
    args = positional + defaulted + nameless + keyword

    logControler = LOG_Control()
    logger = logControler.loggerGet()
    depth = ucf.stackFrameDepth(2)
    indentation = ucf.STR_indentMultiples(multiple=depth)

    logger.debug(format('%s Invoking(I-Call-%s): ' % (indentation, depth)) + ucf.stackFrameInfoGet(2))
    logger.debug( "%s I-Enter-%s: %s(%s)" % (indentation, depth, fn.__name__, ", ".join(args)) )
    retVal = fn(*v, **k)
    logger.debug( "%s I-Return-%s(%s):  %s" % (indentation, depth, fn.__name__, retVal) )
    return retVal


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  doLog    [[elisp:(org-cycle)][| ]]
"""
subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def doLog(fn, *v, **k):
    """Invokes fn with args (*v, **k) and logs the invocation and return.
    """

    # Unpack function's arg count, arg names, arg defaults
    code = fn.func_code
    argcount = code.co_argcount
    argnames = code.co_varnames[:argcount]
    fn_defaults = fn.func_defaults or list()
    argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

    # Collect function arguments by chaining together positional,
    # defaulted, extra positional and keyword arguments.
    positional = map(ucf.format_arg_value, zip(argnames, v))
    defaulted = [ucf.format_arg_value((a, argdefs[a]))
                 for a in argnames[len(v):] if a not in k]
    nameless = map(repr, v[argcount:])
    keyword = map(ucf.format_arg_value, k.items())
    args = positional + defaulted + nameless + keyword

    logControler = LOG_Control()
    logger = logControler.loggerGet()
    depth = ucf.stackFrameDepth(2)
    indentation = ucf.STR_indentMultiples(multiple=depth)

    logger.debug(format('Invoking(I-Call-%s): ' % (depth)) + ucf.stackFrameInfoGet(2))
    logger.debug( "%s I-Enter-%s: %s(%s)" % (indentation, depth, fn.__name__, ", ".join(args)) )
    retVal = fn(*v, **k)
    logger.debug( "%s I-Return-%s(%s):  %s" % (indentation, depth, fn.__name__, retVal) )
    return retVal


"""
*  [[elisp:(org-cycle)][| ]]  /subProc/            :: *SubProcess -- Bash or Command Syncronous invokations* [[elisp:(org-cycle)][| ]]
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  subProc_bash  -- subprocess.Popen()  [[elisp:(org-cycle)][| ]]
"""
subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def subProc_bash(
        cmndStr,
        stdin=None,
        outcome=None,
):
    """subprocess.Popen() -- shell=True, runs cmndStr in bash."""
    
    #
    if not outcome:
        outcome = OpOutcome()

    if not stdin:
        stdin = ""

    outcome.stdcmnd = cmndStr    
    try:
        process = subprocess.Popen(
            cmndStr,
            shell=True,
            executable="/bin/bash",            
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        outcome.error = OSError
    else: 
        outcome.stdout, outcome.stderr = process.communicate(input=format(stdin.encode()))
        process.stdin.close()

    process.wait()

    outcome.error = process.returncode
    
    return outcome



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  subProc_cmnd    [[elisp:(org-cycle)][| ]]
"""
subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def subProc_cmnd(
        cmndStr,
        stdin=None,
        outcome=None,
):
    """subprocess.Popen()
    """
    #
    if not outcome:
        outcome = OpOutcome()

    if not stdin:
        stdin = ""

    commandArgs=shlex.split(cmndStr)

    outcome.stdcmnd = cmndStr    
    try:
        process = subprocess.Popen(
            commandArgs,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        outcome.errInfo = OSError
    else: 
        outcome.stdout, outcome.stderr = process.communicate(input=format(stdin.encode()))
        process.stdin.close()

    process.wait()

    outcome.error = process.returncode
    
    return outcome


"""
*  [[elisp:(org-cycle)][| ]]  /General/            :: *Frame Marking and Tracking -- stackFrameInfoGet(frameNu)* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  frameNuFuncSetAuxInvokable -- Obsoleted   [[elisp:(org-cycle)][| ]]
"""

def frameNuFuncSetAuxInvokable(frameNu):
    """Should be called by funcName_auxInvokable. The set funcName.auxInvokable attr."""
    #print "kkkkk"
    callingName = ucf.stackFrameFuncGet(frameNu)
    #print callingName
    if not ucf.str_endsWith(callingName, "_auxInvokable"):
        EH_problem_usageError("")
        return False
    invokable=callingName[0:callingName.find("_auxInvokable")]
    #print invokable
    ucf.FUNC_strToFunc(invokable).auxInvokable = True

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  frameNuLibFuncSetAuxInvokable -- Obsoelted   [[elisp:(org-cycle)][| ]]
"""

def frameNuLibFuncSetAuxInvokable(frameNu):
    """Should be called by funcName_auxInvokable. The set funcName.auxInvokable attr."""
    #print "kkkkk"
    callingName = ucf.stackFrameFuncGet(frameNu)
    #print callingName
    if not ucf.str_endsWith(callingName, "_auxInvokable"):
        EH_problem_usageError("")
        return False
    invokable=callingName[0:callingName.find("_auxInvokable")]
    #print("iim." + invokable + "---ZZZ---")
    ucf.FUNC_strToFunc("iim." + invokable).auxInvokable = True


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  stackFrameDocStringNot    [[elisp:(org-cycle)][| ]]
"""

def stackFrameDocStringNot(frameNu):
    """
    """
    print "ZZZZ"
    try: frameNu = int(frameNu)
    except: pass
    print "AAAAZZZZ"    
    ANN_here()  
    callerframerecord = inspect.stack()[frameNu]      #
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print "BBBBZZZZ"       
    ANN_here()  
    func = ucf.FUNC_strToFunc( info.function )
    print "CCCZZZZ"        
    ANN_here()  
    #print "Called from module", info.f_globals['__name__']
    #print( getattr(info.filename, info.function) )
    #print( inspect.getdoc(getattr(info.function)) )
    return inspect.getdoc( func )
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  stackFrameArgsGetNot    [[elisp:(org-cycle)][| ]]
"""

def stackFrameArgsGetNot(frameNu):
    """
    """
    try: frameNu = int(frameNu)
    except: pass

    callerframerecord = inspect.stack()[frameNu]      #
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)

    fn = ucf.FUNC_strToFunc( info.function )

    # Unpack function's arg count, arg names, arg defaults
    code = fn.func_code
    argcount = code.co_argcount
    argnames = code.co_varnames[:argcount]
    fn_defaults = fn.func_defaults or list()
    argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

    print( info.function + ' -- '+ str(argcount) + str(argnames) + str(fn_defaults) + str(argdefs) )

    return


"""
*  [[elisp:(org-cycle)][| ]]  /Outputs Control/    :: *LOG_: IIM Logging Control -- On top of Standard of Python Logging* [[elisp:(org-cycle)][| ]]
"""

#LOGGER = 'Iim.Python.Logger'
LOGGER = 'Iim'
CONSL_LEVEL_RANGE = range(0, 51)
LOG_FILE = '/tmp/NOTYET.log'
#FORMAT_STR = '%(asctime)s %(levelname)s %(message)s'
FORMAT_STR = '%(levelname)s %(message)s -- %(asctime)s'

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  getConsoleLevel    [[elisp:(org-cycle)][| ]]
"""

def getConsoleLevel(args):
    level = args.verbosityLevel
    if level is None: return
    try: level = int(level)
    except: pass
    if level not in CONSL_LEVEL_RANGE:
        args.verbosityLevel = None
        print 'warning: console log level ', level, ' not in range 1..50.'
        return
    return level

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  LOG_Control  -- logging: debug(TM_), info(LOG_), warning(EH_), error(EH_), critical(EH_)   [[elisp:(org-cycle)][| ]]
"""

class LOG_Control():
    """IIM Logging on top of basic Logging.
    """

    args = None
    logger = None
    fh = None
    level = None

    def __init__(self):
        pass

    def loggerSet(self, args):
        """
        """

        #print( args )    #TEMP

        self.__class__.args = args

        logger = logging.getLogger(LOGGER)

        self.__class__.logger = logger

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT_STR)
        ## Add FileHandler
        fh = logging.FileHandler(LOG_FILE)
        fh.name = 'File Logger'
        fh.level = logging.WARNING
        fh.formatter = formatter
        logger.addHandler(fh)

        self.__class__.fh = fh

        ## Add (optionally) ConsoleHandler
        level = getConsoleLevel(args)

        self.__class__.level = level

        #print( 'level= ' + str(level) )  # TEMP

        if level is not None:
            #print( stackFrameInfoGet(1) )  # TEMP
            ch = logging.StreamHandler()
            ch.name = 'Console Logger'
            ch.level = level
            ch.formatter = formatter
            logger.addHandler(ch)
            #print( stackFrameInfoGet(1) )  # TEMP
        return logger

    def loggerSetLevel(self, level):
        """
        """

        #print( args )    #TEMP

        #self.__class__.args = args

        logger = logging.getLogger(LOGGER)

        self.__class__.logger = logger

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT_STR)
        ## Add FileHandler
        fh = logging.FileHandler(LOG_FILE)
        fh.name = 'File Logger'
        fh.level = logging.WARNING
        fh.formatter = formatter
        logger.addHandler(fh)

        self.__class__.fh = fh

        ## Add (optionally) ConsoleHandler
        #level = getConsoleLevel(args)

        self.__class__.level = level

        #print( 'level= ' + str(level) )  # TEMP

        if level is not None:
            #print( stackFrameInfoGet(1) )  # TEMP
            ch = logging.StreamHandler()
            ch.name = 'Console Logger'
            ch.level = level
            ch.formatter = formatter
            logger.addHandler(ch)
            #print( stackFrameInfoGet(1) )  # TEMP
        return logger

    def loggerReset(self):
        logger = self.__class__.logger
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT_STR)
        fh = self.__class__.fh
        fh.formatter = formatter

    def loggerGet(self):
        return self.__class__.logger

"""
*  [[elisp:(org-cycle)][| ]]  /TM_/                :: *TM_: Trackings Module (TM_)/Class -- Instrumented Tracing On Top Of IIM-Logging* [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  TM_note  -- logging.debug (10) -- bxf.tm.note() [[elisp:(org-cycle)][| ]]
"""

def TM_note(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.debug( 'TM_: ' + outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  TM_here  -- logging.debug (10) -- bxf.tm.here() [[elisp:(org-cycle)][| ]]
"""

def TM_here(*v, **k):
    """Mark file and line -- do the equivalent of a print statement.
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.debug('TM_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )



"""
*  [[elisp:(org-cycle)][| ]]  /LOG_/               :: *LOG_: Significant Event Which Is Not An Error* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  LOG_note  -- logging.info (20) -- bxf.info.note() -- bxf.info.op.note(outcome,).log()  [[elisp:(org-cycle)][| ]]
"""

def LOG_note(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.info( 'LOG_: ' + outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  LOG_here  -- logging.info (20) -- bxf.info.here() -- bxf.info.op.here(outcome,)  [[elisp:(org-cycle)][| ]]
"""

def LOG_here(*v, **k):
    """Mark file and line -- do the equivalent of a print statement.
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.info('LOG_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

    


"""
*  [[elisp:(org-cycle)][| ]]  /EH_/                :: *EH_: IIM Error Handling On Top Of Python Exceptions (EH_ Module)* [[elisp:(org-cycle)][| ]]
"""
"""
**  [[elisp:(org-cycle)][| ]]  Subject      ::== IifArgs Exceptions (EH_ Module) [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_iifArgsPositional  --   [[elisp:(org-cycle)][| ]]
"""

def EH_critical_iifArgsPositional(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    #raise RuntimeError()
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_iifArgsOptional    [[elisp:(org-cycle)][| ]]
"""

def EH_critical_iifArgsOptional(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    #raise RuntimeError()
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_usageError    [[elisp:(org-cycle)][| ]]
"""

def EH_critical_usageError(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_usageError: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    return(ReturnCode.UsageError)
    #raise RuntimeError()
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_problem_notyet    [[elisp:(org-cycle)][| ]]
"""

def EH_problem_notyet(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_NotYet: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    #raise RuntimeError()

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_problem_info    [[elisp:(org-cycle)][| ]]
"""

def EH_problem_info(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_Info: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_problem_usageError -- logger.error (40)  [[elisp:(org-cycle)][| ]]
"""

def EH_problem_usageError(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

    return (
        eh_problem_usageError(OpOutcome(), *v, **k)
    )
    
    #raise RuntimeError()

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  eh_problem_usageError -- Captured in Outcome  [[elisp:(org-cycle)][| ]]
"""
    

def eh_problem_usageError(outcome, *v, **k):
    """
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    errStr='EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2)
    return(outcome.set(
        opError=OpError.UsageError,
        opErrInfo=errStr,
    ))

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_unassigedError    [[elisp:(org-cycle)][| ]]
"""

def EH_critical_unassigedError(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    #raise RuntimeError()
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_problem_unassignedError    [[elisp:(org-cycle)][| ]]
"""

def EH_problem_unassignedError(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    #raise RuntimeError()

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_oops    [[elisp:(org-cycle)][| ]]
"""

def EH_critical_oops(*v, **k):
    """A Software Error has Occured.
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

    #raise RuntimeError()

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_critical_exception    [[elisp:(org-cycle)][| ]]
"""

def EH_critical_exception(e):
    """ Usage Example:
    try: m=2/0
    except Exception as e: iim.EH_critical_exception(e)
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    #fn = FUNC_currentGet()

    outString = format(e)
    
    logger.critical('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.critical(
        "EH_: {exc_type} {fname} {lineno}"
        .format(
            exc_type=exc_type,
            fname=fname,
            lineno=exc_tb.tb_lineno
        )
    )

    logging.exception(e)

    # Or any of the 
    #logger.error("EH_critical_exception", exc_info=True)
    #print(traceback.format_exc())


    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_badOutcome    [[elisp:(org-cycle)][| ]]
"""
def EH_badOutcome(outcome):
    print(
        "EH_badOutcome: InvokedBy {invokerName}, Operation Failed: Stdcmnd={stdcmnd} Error={status} -- {errInfo}".
        format(invokerName=outcome.invokerName,
               stdcmnd=outcome.stdcmnd,
               status=outcome.error,
               errInfo=outcome.errInfo,
        ))

    return outcome

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF              ::  EH_badLastOutcome    [[elisp:(org-cycle)][| ]]
"""
def EH_badLastOutcome():
    return (
        EH_badOutcome(
            IicmGlobalContext().lastOpOutcome
        ))

def eh_badLastOutcome():
    return (
            IicmGlobalContext().lastOpOutcome
    )

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  EH_runTime    [[elisp:(org-cycle)][| ]]
"""

def EH_runTime(*v, **k):
    """
    """
    logControler = LOG_Control()
    logger = logControler.loggerGet()

    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.error('EH_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )
    raise RuntimeError()


"""
*  [[elisp:(org-cycle)][| ]]  /ANN_/               :: *ANN_: Announcing Module (ANN_)/Class* [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  ANN_write  -- Same As print to stderr [[elisp:(org-cycle)][| ]]
"""

def ANN_write(*v, **k):
    """
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print( outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  ANN_note -- Prepends ANN_:     [[elisp:(org-cycle)][| ]]
"""

def ANN_note(*v, **k):
    """
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print( 'ANN_: ' + outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  ANN_here -- Prepends ANN_ and adds stackFrameInfoGet(2)   [[elisp:(org-cycle)][| ]]
"""

def ANN_here(*v, **k):
    """Mark file and line -- do the equivalent of a print statement.
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print('ANN_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )


"""
*  [[elisp:(org-cycle)][| ]]  /OUT_/               :: *OUT_: Output Module (OUT_)/Class* [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  OUT_write  -- Same As print to stderr [[elisp:(org-cycle)][| ]]
"""

def OUT_write(*v, **k):
    """
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print( outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  OUT_note -- Prepends OUT_:     [[elisp:(org-cycle)][| ]]
"""

def OUT_note(*v, **k):
    """
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print( 'OUT_: ' + outString )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  OUT_here -- Prepends OUT_ and adds stackFrameInfoGet(2)   [[elisp:(org-cycle)][| ]]
"""

def OUT_here(*v, **k):
    """Mark file and line -- do the equivalent of a print statement.
    """
    fn = ucf.FUNC_currentGet()
    argsLength =  ucf.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print('OUT_: ' + outString + ' -- ' + ucf.stackFrameInfoGet(2) )

    

    
"""
*  [[elisp:(org-cycle)][| ]]  /FV_/                :: *File Variables (FV_)* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FV_writeToFilePath    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FV_writeToFilePath(
        filePath,
        varValue,
):
    """
    """
    baseDir = os.path.dirname(filePath)
    if not os.path.isdir(baseDir):
        return None
    varName = os.path.basename(filePath)
    return(
        FV_writeToBaseDir(
            baseDir,
            varName,
            varValue,
        )
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FV_writeToFilePathAndCreate    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FV_writeToFilePathAndCreate(
        filePath,
        varValue,
):
    """
    """
    baseDir = os.path.dirname(filePath)
    varName = os.path.basename(filePath)
    return(
        FV_writeToBaseDirAndCreate(
            baseDir,
            varName,
            varValue,
        )
    )
 
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FV_writeToBaseDirAndCreate    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FV_writeToBaseDirAndCreate(
        baseDir,
        varName,
        varValue,
):
    """
    """
    if not os.path.isdir(baseDir):
        try: os.makedirs(baseDir, 0775)
        except OSError: pass

    return(
        FV_writeToBaseDir(
            baseDir,
            varName,
            varValue,
        )
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FV_writeToBaseDir    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FV_writeToBaseDir(
        baseDir,
        varName,
        varValue,
):
    """
    """
    if not os.path.isdir(baseDir):
        return None

    varValueFullPath = os.path.join(
        baseDir,
        varName
    )

    with open(varValueFullPath, "w") as valueFile:
        valueFile.write(str(varValue) +'\n')
        LOG_here("FILE_Param.writeTo path={path} value={value}".
                format(path=varValueFullPath, value=varValue))



"""
*  [[elisp:(org-cycle)][| ]]  /FILE_TreeObject/    :: *FILE_TreeObject: A Tree of Nodes and Leaves on Top Of file system* [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Subject      :: Facilitates building Tree hierarchies on the file system. [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Subject      :: Super Class for FILE_Param and IIM_Param [[elisp:(org-cycle)][| ]]
"""

FILE_TreeItemEnum = ucf.enum(
    'node',
    'leaf',
    'ignore',
    'ignoreLeaf',
    'ignoreNode'
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_TreeObject    [[elisp:(org-cycle)][| ]]
"""

class FILE_TreeObject(object):
    """Representation of a FILE_TreeObject in a file system directory (either a leaf or a node).

    This class is paralleled by /opt/public/osmt/bin/lcnObjectTree.libSh
    And is expected to be compatible with lcnObjectTree.libSh.

    A FILE_TreeObject is either a
       - FILE_TreeNode
       - FILE_TreeLeaf

    A FILE_TreeObject consists of:
       1) FileSysDir
       2) _tree_
       3) _treeProc_
       4) _objectType_

    _tree_  in bash  typeset -A treeItemEnum=(
    [node]=node                   # this dir is a node
    [leaf]=leaf                   # this dir is a leaf
    [ignore]=ignore               # ignore this and everything below it
    [ignoreLeaf]=ignoreLeaf       # ignore this leaf
    [ignoreNode]=ignoreNode       # ignore this node but continue traversing
)

    _objectTypes_  Known objectTypes are FILE_Param


    """

    def __init__(self,
                 fileSysPath,
                 ):
        '''Constructor'''
        self.__fileSysPath = fileSysPath

    def __str__(self):
        return  format(
            'value: ' + str(self.parValueGet()) +
            'read: ' + str(self.attrReadGet())
            )

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def nodeCreate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a node.
        """
        absFileSysPath = os.path.abspath(self.__fileSysPath)

        if not os.path.isdir(absFileSysPath):
            try: os.makedirs( absFileSysPath, 0777 )
            except OSError: pass

        thisFilePath= format(absFileSysPath + '/_tree_')
        with open(thisFilePath, "w") as thisFile:
             thisFile.write('node' +'\n')

    def leafCreate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """
        absFileSysPath = os.path.abspath(self.__fileSysPath)

        if not os.path.isdir(absFileSysPath):
            try: os.makedirs( absFileSysPath, 0777 )
            except OSError: pass

        thisFilePath= format(absFileSysPath + '/_tree_')
        with open(thisFilePath, "w") as thisFile:
             thisFile.write('leaf' +'\n')

    def validityPredicate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a verify that _tree_ is in place.
        """
        absFileSysPath = os.path.abspath(self.__fileSysPath)

        if not os.path.isdir(absFileSysPath):
            return 'NonExistent'

        filePathOf_tree_= format(absFileSysPath + '/_tree_')
        if not os.path.isfile(filePathOf_tree_):
            return 'NonExistent'

        lineString = open(filePathOf_tree_, 'r').read().strip()    # Making sure we get rid of \n on read()

        if lineString == 'node':
            return 'InPlace'
        else:
            EH_critical_usageError('lineString=' + lineString)
            return 'BadlyFormed'

    def nodePredicate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """
        print(self.__fileSysPath)

    def leafPredicate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """
        print(self.__fileSysPath)

    def nodeUpdate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """
        print(self.__fileSysPath)


    def leafUpdate(self, objectTypes=None, treeProc=None, ignore=None):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def nodesEffectiveList(self):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def leavesEffectiveList(self):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def nodesList(self):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def leavesList(self):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def treeObjectInfo(self):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """

    def treeRecurse(self, command):
        """At the fileSysPath of the FILE_TreeObject, create a leaf.
        """



"""
*  [[elisp:(org-cycle)][| ]]  /FILE_Param/         :: *FILE_Param: File Parameter (FILE_ParamBase, FILE_Param, FILE_ParamDict)* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_ParamBase    [[elisp:(org-cycle)][| ]]
"""
class FILE_ParamBase(FILE_TreeObject):
    """Representation of a FILE_TreeObject when _objectType_ is FILE_ParamBase (a node).
    """
    def baseCreate(self):
        """  """
        return self.nodeCreate()

    def baseValidityPredicate(self):
        """  """
        return self.validityPredicate()


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_Param    [[elisp:(org-cycle)][| ]]
"""

class FILE_Param(object):
    """Representation of One FILE_Parameter.

    A FILE_Param consists of 3 parts
       1) ParameterName
       2) ParameterValue
       3) ParameterAttributes

    On the file system:
      1- name of directory is ParameterName
      2- content of ParameterName/value is ParameterValue
      3- rest of the files in ParameterName/ are ParameterAttributes.

    The concept of a FILE_Param dates back to [[http://www.qmailwiki.org/Qmail-control-files][Qmail Control Files]] (at least).
    A FILE_Param is broader than that concept in two respects.
     1) A FILE_Param is represented as a directory on the file system. This FILE_Param
        permits the parameter to have attributes beyond just a value. Other attributes
        are themselves in the form of a traditional filename/value.
     2) The scope of usage of a FILE_Param is any parameter not just a control parameter.


    We are deliberately not using a python dictionary to represent a FILE_Param
    instead it is a full fledged python-object.
    """

    def __init__(self,
                 parName=None,
                 parValue=None,
                 storeBase=None,
                 storeRoot=None,
                 storeRel=None,
                 attrRead=None,
                 ):
        '''Constructor'''
        self.__parName = parName
        self.__parValue = parValue
        self.__storeBase = storeBase   # storeBase = storeRoot + storeRel
        self.__storeRoot = storeRoot
        self.__storeRel = storeRel
        self.__attrRead = attrRead


    def __str__(self):
        return  format(
            str(self.parNameGet()) + ": " + str(self.parValueGet())
            )

    def parNameGet(self):
        """  """
        return self.__parName

    def parValueGet(self):
        """        """
        return self.__parValue

    def parValueGetLines(self):
        """        """
        if self.__parValue == None:
            return None
        return self.__parValue.splitlines()

    def parValueSet(self, value):
        """        """
        self.__parValue = value

    def attrReadGet(self):
        """        """
        return self.__attrRead

    def attrReadSet(self, attrRead):
        """        """
        self.__attrRead = attrRead

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def readFrom(self, storeBase=None, parName=None):
        """Read into a FILE_param content of parBase/parName.

        Returns a FILE_param which was contailed in parBase/parName.
        """
        if self.__storeBase == None and storeBase == None:
            return EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return EH_problem_usageError("parName")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName

        self.__parName = parName

        parNameFullPath = os.path.join(self.__storeBase, parName)

        return self.readFromPath(parNameFullPath)

    # Undecorated because called before initialization
    #@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def readFromPath(self, parNameFullPath):
        """Read into a FILE_param content of parBase/parName.

        Returns a FILE_param which was contailed in parBase/parName.
        """

        if not os.path.isdir(parNameFullPath):
            #return EH_problem_usageError("parName: " + parNameFullPath)
            return None

        fileParam = self

        fileParam.__parName = os.path.basename(parNameFullPath)

        #
        # Now we will fill fileParam based on the directory content
        #
        for item in os.listdir(parNameFullPath):
            if item == "CVS":
                continue
            fileFullPath = os.path.join(parNameFullPath, item)
            if os.path.isfile(fileFullPath):
                if item == 'value':
                    lineString = open(fileFullPath, 'r').read().strip()    # Making sure we get rid of \n on read()
                    self.parValueSet(lineString)
                    continue

                # Rest of the files are expected to be attributes

                #lineString = open(fileFullPath, 'r').read()
                # NOTYET, check for exceptions
                #eval('self.attr' + str(item).title() + 'Set(lineString)')
            #else:
                #EH_problem_usageError("Unexpected Non-File: " + fileFullPath)

        return fileParam


    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeTo(self, storeBase=None, parName=None, parValue=None):
        """Write this FILE_Param to storeBase.

        """
        if self.__storeBase == None and storeBase == None:
            return EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return EH_problem_usageError("parName")

        if self.__parValue == None and parValue == None:
            return EH_problem_usageError("parValue")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName
        else:
            parName = self.__parName

        if parValue:
            self.__parValue = parValue
        else:
            parValue = self.__parValue

        parNameFullPath = os.path.join(self.__storeBase, parName)
        try: os.makedirs( parNameFullPath, 0777 )
        except OSError: pass

        fileTreeObject = FILE_TreeObject(parNameFullPath)

        fileTreeObject.leafCreate()

        parValueFullPath = os.path.join(parNameFullPath, 'value')
        with open(parValueFullPath, "w") as valueFile:
             valueFile.write(str(parValue) +'\n')
             LOG_here("FILE_Param.writeTo path={path} value={value}".
                      format(path=parValueFullPath, value=parValue))

        return parNameFullPath


    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeToPath(self, parNameFullPath=None, parValue=None):
        """Write this FILE_Param to storeBase.
        """

        return self.writeTo(storeBase=os.path.dirname(parNameFullPath),
                            parName=os.path.basename(parNameFullPath),
                            parValue=parValue)                 

        
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def writeToFromFile(self, storeBase=None, parName=None, parValueFile=None):
        """Write this FILE_Param to storeBase.

        """
        if self.__storeBase == None and storeBase == None:
            return EH_problem_usageError("storeBase")

        if self.__parName == None and parName == None:
            return EH_problem_usageError("parName")

        if parValueFile == None:
             return EH_problem_usageError("parValueFile")

        if storeBase:
            self.__storeBase = storeBase

        if parName:
            self.__parName = parName
        else:
            parName = self.__parName

        # if parValue:
        #     self.__parValue = parValue
        # else:
        #     parValue = self.__parValue

        parNameFullPath = os.path.join(self.__storeBase, parName)
        try: os.makedirs( parNameFullPath, 0777 )
        except OSError: pass

        fileTreeObject = FILE_TreeObject(parNameFullPath)

        fileTreeObject.leafCreate()

        parValueFullPath = os.path.join(parNameFullPath, 'value')
        with open(parValueFullPath, "w") as valueFile:
            with open(parValueFile, "r") as inFile:
                for line in inFile:
                    valueFile.write(line)

        return parNameFullPath


    def reCreationString(self):
        """Provide the string needed to recreate this object.

        """
        return

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteTo    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteTo(parRoot=None,
                      parName=None,
                      parValue=None,
                      ):
    """
    """

    thisFileParam = FILE_Param(parName=parName, parValue=parValue,)

    if thisFileParam == None:
        return EH_critical_usageError('')

    return thisFileParam.writeTo(storeBase=parRoot)

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteToPath    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteToPath(parNameFullPath=None,
                          parValue=None,
                          ):
    """
    """

    thisFileParam = FILE_Param()

    if thisFileParam == None:
        return EH_critical_usageError('')

    return thisFileParam.writeToPath(parNameFullPath=parNameFullPath,
                                     parValue=parValue)

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamWriteToFromFile    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamWriteToFromFile(parRoot=None,
                      parName=None,
                      parValueFile=None,
                      ):
    """
    """

    thisFileParam = FILE_Param(parName=parName)

    if thisFileParam == None:
        return EH_critical_usageError('')

    return thisFileParam.writeToFromFile(storeBase=parRoot, parValueFile=parValueFile)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamReadFrom    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return EH_critical_usageError('blank')

    filePar = blank.readFrom(storeBase=parRoot, parName=parName)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        raise IOError
        #return EH_critical_usageError('blank')
        return None

    return filePar

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamValueReadFrom    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamValueReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return EH_critical_usageError('blank')

    filePar = blank.readFrom(storeBase=parRoot, parName=parName)

    if filePar == None:
        print('Missing: ' + parRoot + parName)
        #raise IOError        
        #return EH_critical_usageError('blank')
        return None        

    return(filePar.parValueGet())


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamReadFromPath    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamReadFromPath(parRoot=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return EH_critical_usageError('blank')

    filePar = blank.readFromPath(parRoot)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        raise IOError
        #return EH_critical_usageError('blank')        

    return filePar


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamValueReadFromPath    [[elisp:(org-cycle)][| ]]
"""
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamValueReadFromPath(parRoot=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        return EH_critical_usageError('blank')

    filePar = blank.readFromPath(parRoot)

    if filePar == None:
        print('Missing: ' + parRoot)
        return EH_critical_usageError('blank')

    return(filePar.parValueGet())


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamVerWriteTo    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamVerWriteTo(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      parValue=None,
                      ):
    """ Given tiimoBase, Create parName, then assign parValue to parVerTag
    """

    parFullPath = os.path.join(parRoot, parName)
    try: os.makedirs( parFullPath, 0777 )
    except OSError: pass

    thisFileParam = FILE_Param(parName=parVerTag,
                                    parValue=parValue,
                                    )

    if thisFileParam == None:
        return EH_critical_usageError('')

    return thisFileParam.writeTo(storeBase=parFullPath)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_ParamVerReadFrom    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_ParamVerReadFrom(parRoot=None,
                      parName=None,
                      parVerTag=None,
                      ):
    blank = FILE_Param()

    if blank == None:
        try:  EH_critical_usageError('blank')
        except RuntimeError:  return

    parFullPath = os.path.join(parRoot, parName)
    try: os.makedirs( parFullPath, 0777 )
    except OSError: pass


    filePar = blank.readFrom(storeBase=parFullPath, parName=parVerTag)

    if filePar == None:
        #print('Missing: ' + parRoot + parName)
        return EH_critical_usageError('blank')

    #print(filePar.parValueGet())
    return filePar



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  FILE_ParamDict    [[elisp:(org-cycle)][| ]]
"""

class FILE_ParamDict(object):
    """Maintain a list of FILE_Params.

    NOTYET, nesting of dictionaries.
    """

    def __init__(self):
        self.__fileParamDict = dict()

    def parDictAdd(self, fileParam=None):
        """        """
        self.__fileParamDict.update({fileParam.parNameGet():fileParam})

    def parDictGet(self):
        """        """
        return self.__fileParamDict

    def parNameFind(self, parName=None):
        """        """
        return self.__fileParamDict[parName]

    def readFrom(self, path=None):
        """Read each file's content into a FLAT dictionary item with the filename as key.

        Returns a Dictionary of paramName:FILE_Param.
        """

        absolutePath = os.path.abspath(path)

        if not os.path.isdir(absolutePath):
            return None

        for item in os.listdir(absolutePath):
            fileFullPath = os.path.join(absolutePath, item)
            if os.path.isdir(fileFullPath):

                blank = FILE_Param()

                itemParam = blank.readFrom(storeBase=absolutePath, parName=item)

                self.parDictAdd(itemParam)

        return self.__fileParamDict

 
    
"""
*  [[elisp:(org-cycle)][| ]]  /FILE_paramDictRead/ :: *FILE_paramDictRead:* (IIF) [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_paramDictRead    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_paramDictRead(interactive=Interactivity.Both,
                      inPathList=None):
    """ Old Style IIF
    """
    try: callableEntryEnhancer(type='iif')
    except StopIteration:  return(ReturnCode.ExtractionSuccess)

    G = IicmGlobalContext()
    G.curFuncNameSet(ucf.FUNC_currentGet().__name__)

    if Interactivity().interactiveInvokation(interactive):
        iimRunArgs = G.iimRunArgsGet()
        if iifArgsLengthValidate(iifArgs=iimRunArgs.iifArgs, expected=0, comparison=int__gt):
            return(ReturnCode.UsageError)
    
        inPathList = []
        for thisPath in iimRunArgs.iifArgs:
            inPathList.append(thisPath)
    else:
        if inPathList == None:
            return EH_critical_usageError('inPathList is None and is Non-Interactive')                    

    for thisPath in inPathList:
        blankDict = FILE_ParamDict()
        thisParamDict = blankDict.readFrom(path=thisPath)
        TM_here('path=' + thisPath)

        if thisParamDict == None:
            continue

        for parName, filePar  in thisParamDict.iteritems():
            print('parName=' + parName)
            if filePar == None:
                continue
            thisValue=filePar.parValueGetLines()
            if thisValue == None:
                TM_here("Skipping: " + filePar.parNameGet())
                continue
            print(
                filePar.parNameGet() +
                '=' +
                thisValue[0])
    return

subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FP_readTreeAtBaseDir_fNOT(
        interactive=False,
        outcome=None,
        FPsDir=None,
):
    """Is also be exposed as an IIF."""
    if not outcome:
        outcome = OpOutcome()
    
    blankParDictObj  = FILE_ParamDict()
    thisParamDict = blankParDictObj.readFrom(path=FPsDir)
    TM_here('path=' + FPsDir)

    if thisParamDict == None:
        return eh_problem_usageError(
            outcome,
            "thisParamDict == None",
        )

    if interactive:
        ANN_write(FPsDir)
        FILE_paramDictPrint(thisParamDict)

    return outcome.set(
        opError=OpError.Success,
        opResults=thisParamDict,
    )

class FP_readTreeAtBaseDir(Iif):
    """Reads and recurses through all FPs"""
    
    iifParamsMandatory = ['FPsDir']
    iifParamsOptional = []       
    iifArgsLen = {'Min': 0, 'Max': 0,}


    subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        FPsDir=None,              # or IIF Parameter/Arg
    ):
        """When interactive, also prints out parValues as read."""

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :inIicm "true" :par "FPsDir"
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'FPsDir': FPsDir, }
        if not iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        FPsDir = callParamsDict['FPsDir']
####+END:

        #G = IicmGlobalContext()        

        # return FP_readTreeAtBaseDir_f(
        #     interactive=interactive,
        #     outcome = iifOutcome,          
        #     FPsDir=FPsDir,
        # )

        blankParDictObj  = FILE_ParamDict()
        thisParamDict = blankParDictObj.readFrom(path=FPsDir)
        TM_here('path=' + FPsDir)

        if thisParamDict == None:
            return eh_problem_usageError(
                iifOutcome,
                "thisParamDict == None",
            )

        if interactive:
            ANN_write(FPsDir)
            FILE_paramDictPrint(thisParamDict)

        return iifOutcome.set(
            opError=OpError.Success,
            opResults=thisParamDict,
        )


def iifCallParamsValidate(
        callParamDict,
        interactive,
        outcome=None,
        
):
    """Expected to be used in all IIFs.

Usage Pattern:

    if not iicm.iifCallParamValidate(FPsDir, interactive, outcome=iifOutcome):
       return iifOutcome
"""
    #G = IicmGlobalContext()
    #if type(callParamOrList) is not list: callParamOrList = [ callParamOrList ]

    if not outcome:
        outcome = OpOutcome()

    for key  in callParamDict:
        #print key
        if not callParamDict[key]:
            if not interactive:
                return eh_problem_usageError(
                    outcome,
                    "Missing Non-Interactive Arg {}".format(key),
                )
            exec("callParamDict[key] = IicmGlobalContext().usageParams." + key)
            
    return True

         

def FILE_paramDictPrint(fileParamDict):
    """ Returns a Dictionary of paramName:FILE_Param.        """
    for parName, filePar  in fileParamDict.iteritems():
        #print('parName=' + parName)
        if filePar == None:
            continue
        thisValue=filePar.parValueGetLines()
        if thisValue == None:
            TM_here("Skipping: " + filePar.parNameGet())
            continue
        if thisValue:
            print(
                filePar.parNameGet() +
                '=' +
                thisValue[0])
        else: # Empty list
            print(
                filePar.parNameGet() +
                '=')



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_paramDictReadDeep    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def FILE_paramDictReadDeep(interactive=Interactivity.Both,
                      inPathList=None):
    """
    """
    try: callableEntryEnhancer(type='iif')
    except StopIteration:  return(ReturnCode.ExtractionSuccess)

    G = IicmGlobalContext()
    G.curFuncNameSet(ucf.FUNC_currentGet().__name__)

    if Interactivity().interactiveInvokation(interactive):
        iimRunArgs = G.iimRunArgsGet()
        if iifArgsLengthValidate(iifArgs=iimRunArgs.iifArgs, expected=0, comparison=int__gt):
            return(ReturnCode.UsageError)
    
        inPathList = []
        for thisPath in iimRunArgs.iifArgs:
            inPathList.append(thisPath)
    else:
        if inPathList == None:
            return EH_critical_usageError('inPathList is None and is Non-Interactive')                    

    for thisPath in inPathList:
        #absolutePath = os.path.abspath(thisPath)

        if not os.path.isdir(thisPath):
            return EH_critical_usageError('Missing Directory: {thisPath}'.format(thisPath=thisPath))

        for root, dirs, files in os.walk(thisPath):
            #print("root={root}".format(root=root))
            #print ("dirs={dirs}".format(dirs=dirs))
            #print ("files={files}".format(files=files))

            thisFileParamValueFile = os.path.join(root, "value")
            if os.path.isfile(thisFileParamValueFile):
                try:
                    fileParam = FILE_ParamReadFromPath(parRoot=root)
                except IOError:
                    EH_problem_info("Missing " + root)
                    continue

                print(root + "=" + fileParam.parValueGet())

    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  FILE_parametersReadDeep_PlaceHolder    [[elisp:(org-cycle)][| ]]
"""

def FILE_parametersReadDeep_PlaceHolder(path=None):
    """Read each file's content into a DEEP dictionary item with the filename as key.

    Not Fully Implemeted YET.
    """
    retVal = None

    absolutePath = os.path.abspath(path)

    if not os.path.isdir(absolutePath):
        return retVal

    fileParamsDict = dict()

    for root, dirs, files in os.walk(absolutePath):
        # Each time that we see a dir we will create a new subDict
        print root
        print dirs
        print files

    return fileParamsDict




"""
*  [[elisp:(org-cycle)][| ]]  /IIM_Param/          :: *IIM_Param: IIM Parameter (IIM_Param, IIM_ParamDict)* [[elisp:(org-cycle)][| ]]
"""

     # (
     #     "routerIntSubnetAddr", # Name of the Parameter
     #     "Router Interface Subnet Address.", # Description
     #     ent.ENET_PARAM_TYPE_STRING, # Type of Data
     #     "255.255.255.0", # Default
     #     ["255.255.255.0"] # Range Of Values.
     # )

IIM_ParamScope = ucf.enum('TargetParam', 'IimGeneralParam', 'IifSpecificParam')
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  IIM_Param    [[elisp:(org-cycle)][| ]]
"""

class IIM_Param(object):
     """Representation of an Interactively Invokable Module Parameter (IIM_Param).

     An IIM Parameter is a superset of an argsparse parameter which also includes:
        - IIF relevance (Mandatory and Optional)
        - Maping onto FILE_Params


     IIM_Param is initially used to setup ArgParse and other user-interface parameter aspects.
     """

     def __init__(self,
                  parName=None,
                  parDescription=None,
                  parDataType=None,
                  parDefault=None,
                  parChoices=None,
                  parScope=None,
                  parMetavar=None,                  
                  parAction='store',                    # Same as argparse's action
                  parNargs=None,                        # Same as argparse's nargs
                  parIifApplicability=None,             # List of IIFs to which this IIM is applicable
                  argparseShortOpt=None,
                  argparseLongOpt=None,
                 ):
         '''Constructor'''
         self.__parName = parName
         self.__parValue = None
         self.__parIifApplicability = parIifApplicability
         self.__parDescription = parDescription
         self.__parDataType = parDataType
         self.__parDefault = parDefault
         self.__parChoices = parChoices
         self.__parMetavar = parMetavar         
         self.parActionSet(parAction)
         self.parNargsSet(parNargs)
         self.__argparseShortOpt =  argparseShortOpt
         self.__argparseLongOpt =  argparseLongOpt

     def __str__(self):
         return  format(
             'value: ' + str(self.parValueGet())
             )

     def parNameGet(self):
         """  """
         return self.__parName

     def parNameSet(self, parName):
         """        """
         self.__parName = parName

     def parValueGet(self):
         """        """
         return self.__parValue

     def parValueSet(self, value):
         """        """
         self.__parValue = value

     def parDescriptionGet(self):
         """        """
         return self.__parDescription

     def parDescriptionSet(self, parDescription):
         """        """
         self.__parDescription = parDescription

     def parDataTypeGet(self):
         """        """
         return self.__parDataType

     def parDataTypeSet(self, parDataType):
         """        """
         self.__parDataType = parDataType

     def parDefaultGet(self):
         """        """
         return self.__parDefault

     def parDefaultSet(self, parDefault):
         """        """
         self.__parDefault = parDefault

     def parChoicesGet(self):
         """        """
         return self.__parChoices

     def parChoicesSet(self, parChoices):
         """        """
         self.__parChoices = parChoices

     def parActionGet(self):
         """        """
         return self.__parAction

     def parActionSet(self, parAction):
         """        """
         self.__parAction = parAction

     def parNargsGet(self):
         """        """
         return self.__parNargs

     def parNargsSet(self, parNargs):
         """        """
         self.__parNargs = parNargs

     def argsparseShortOptGet(self):
         """        """
         return self.__argparseShortOpt

     def argsparseShortOptSet(self, argsparseShortOpt):
         """        """
         self.__argparseShortOpt = argsparseShortOpt

     def argsparseLongOptGet(self):
         """        """
         return self.__argparseLongOpt

     def argsparseLongOptSet(self, argsparseLongOpt):
         """        """
         self.__argparseLongOpt = argsparseLongOpt

     def readFrom(self, parRoot=None, parName=None):
         """Read into a FILE_param content of parBase/parName.

         Returns a FILE_param which was contailed in parBase/parName.
         """

         absoluteParRoot = os.path.abspath(parRoot)

         if not os.path.isdir(absoluteParRoot):
             return None

         absoluteParBase = os.path.join(absoluteParRoot, parName)

         if not os.path.isdir(absoluteParBase):
             return None

         fileParam = self

         self.__parName = parName

         #
         # Now we will fill fileParam based on the directory content
         #
         for item in os.listdir(absoluteParBase):
             fileFullPath = os.path.join(absoluteParBase, item)
             if os.path.isfile(fileFullPath):

                 if item == 'value':
                     lineString = open(fileFullPath, 'r').read()
                     self.parValueSet(lineString)
                     continue

                 # Rest of the files are expected to be attributes

                 lineString = open(fileFullPath, 'r').read()
                 # NOTYET, check for exceptions
                 eval('self.attr' + str(item).title() + 'Set(lineString)')

         return fileParam

     @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
     def writeAsFileParam(
             self,
             parRoot=None,
     ):
         """Writing a FILE_param content of self.

         Returns a FILE_param which was contailed in parBase/parName.
         """

         absoluteParRoot = os.path.abspath(parRoot)

         if not os.path.isdir(absoluteParRoot):
            try: os.makedirs( absoluteParRoot, 0775 )
            except OSError: pass
 
         #print absoluteParRoot

         #print 
         #print self.parValueGet()

         parValue = self.parValueGet()
         if not parValue:
             parValue = "unSet"
     
         FILE_ParamWriteTo(
             parRoot=absoluteParRoot,
             parName=self.parNameGet(),
             parValue=parValue,
         )

         varValueFullPath = os.path.join(
             absoluteParRoot,
             self.parNameGet(),
             'description'
         )

         FV_writeToFilePathAndCreate(
             filePath=varValueFullPath,
             varValue=self.parDescriptionGet(),
         )

         varValueBaseDir = os.path.join(
             absoluteParRoot,
             self.parNameGet(),
             'enums'
         )

         for thisChoice in self.parChoicesGet():
             FV_writeToBaseDirAndCreate(
                 baseDir=varValueBaseDir,
                 varName=thisChoice,
                 varValue="",
             )         
         
         
     
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  IIM_ParamDict    [[elisp:(org-cycle)][| ]]
"""

class IIM_ParamDict(object):
     """IIM Parameters Dictionary -- Collection of IIM_Param s can be placed in IIM_ParamDict

     From iimParamDict
     """

     def __init__(self):
         self.__iimParamDict = dict()

     def parDictAdd(self,
                    parName=None,
                    parDescription=None,
                    parDataType=None,
                    parMetavar=None,                                      
                    parDefault=None,
                    parChoices=None,
                    parScope=None,
                    parAction='store',
                    parNargs=None,
                    argparseShortOpt=None,
                    argparseLongOpt=None,
                   ):
         """        """
         thisParam = IIM_Param(parName=parName,
                               parDescription=parDescription,
                               parDataType=parDataType,
                               parMetavar=parMetavar,
                               parDefault=parDefault,
                               parChoices=parChoices,
                               parScope=parScope,
                               parAction=parAction,
                               parNargs=parNargs,
                               argparseShortOpt=argparseShortOpt,
                               argparseLongOpt=argparseLongOpt,
                               )

         self.parDictAppend(thisParam)

     def parDictAppend(self, iimParam=None):
         """        """
         self.__iimParamDict.update({iimParam.parNameGet():iimParam})


     def parDictGet(self):
         """        """
         return self.__iimParamDict

     def parNameFind(self, parName=None):
         """        """
         return self.__iimParamDict[parName]


     def iifApplicabilityUpdate(self,
                                iif=None,
                                mandatoryParams=None,
                                optionalParams=None,
                                ):
         """NOTYET -- Verify That Mandatory and Optional Params for this iif have been specified At Runtime."""

         # if iimRunArgs.perfSap:
         #     print(iimRunArgs.perfSap)

         # if iimRunArgs.wsdlUrl:
         #     print(iimRunArgs.wsdlUrl)

         return

"""
*  [[elisp:(org-cycle)][| ]]  /IIM Output/         :: *iimOutputBaseGet -- iimOutputXlsGetPath(fileBaseName)* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimOutputBaseGet    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iimOutputBaseGet():
    return "./"

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimOutputXlsGetPath    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iimOutputXlsGetPath(fileBaseName):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d%H%M%S')
    fileName = fileBaseName + st + ".xlsx"
    return os.path.join(iimOutputBaseGet(), fileName)

"""
*  [[elisp:(org-cycle)][| ]]  /IIM Lib/            :: *percentage, runOnceOnly, setAdjust*  [[elisp:(org-cycle)][| ]]
"""


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  /G_/                 :: *IimGlobalContext (G_) -- Class, IIM Singleton, provides global context* [[elisp:(org-cycle)][| ]]
"""


IIM_GroupingType = ucf.enum(
    'Pkged',
    'Grouped',
    'Scattered',
    'Unitary',
    'Standalone',
    'Other',
    'UnSet',    
)

IIM_PkgedModel = ucf.enum(
    'BasicPkg',
    'ToiimPkg',
    'EmpnaPkg',
    'UnSet',    
)

IIM_CmndParts = ucf.enum(
    'Common',
    'Param',
    'Target',
    'Bxo',
    'Bxsrf',        
    'UnSet',    
)

AuxInvokationContext = ucf.enum(
    'UnSet',        
    'IimRole',
    'IifParamsAndArgs',
    'DocString',
)
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class            ::  IicmGlobalContext    [[elisp:(org-cycle)][| ]]
"""

class IicmGlobalContext():
     """ Singleton: Interactively Invokable Module Global Context.
     """

     iicmArgsParser = None
     
     iimRunArgsThis = None
     iimParamDict = None       # IIM Specified Parameters in g_argsExtraSpecify()
     thisFuncName = None
     logger = None
     astModuleFunctionsList = None
     
     usageParams = ucf.Variables
     usageArgs = ucf.Variables

     # IIM-Profile Specifications
     iimGroupingType = IIM_GroupingType.UnSet
     iimPkgedModel = IIM_PkgedModel.UnSet
     iimCmndPartsList = [IIM_CmndParts.UnSet]

     _auxInvokationContext = AuxInvokationContext.UnSet
     _auxInvokationResults = None
     _iifNames = None # All 3 of the above have been obsoleted
     
     _iifFuncsDict = None
     _iifMethodsDict = None

     lastOpOutcome = None

     def __init__(self):
         pass

     def globalContextSet(self,
                          iimRunArgs=None,
                          iimParamDict=None
                          ):
         """
         """
         #if not iimRunArgs == None:
         self.__class__.iimRunArgsThis = iimRunArgs

         # NOTYET, 2017 -- Review This
         if iimParamDict == None:
             pass
             #self.__class__.iimParamDict = IIM_ParamDict()

         logger = logging.getLogger(LOGGER)
         self.__class__.logger = logger

         self.__class__.astModuleFunctionsList = ucf.ast_topLevelFunctionsInFile(
             self.iimMyFullName()
         )

     def iimRunArgsGet(self):
         return self.__class__.iimRunArgsThis

     def iimParamDictSet(self, iimParamDict):
         self.__class__.iimParamDict = iimParamDict

     def iimParamDictGet(self):
         return self.__class__.iimParamDict

     def iimMyFullName(self):
          return os.path.abspath(sys.argv[0])

     def iimMyName(self):
         return os.path.basename(sys.argv[0])

     def iicmMyFullName(self):
          return os.path.abspath(sys.argv[0])

     def iicmMyName(self):
         return os.path.basename(sys.argv[0])

     def iimModuleFunctionsList(self):
         return self.__class__.astModuleFunctionsList
     
     def curFuncNameSet(self, curFuncName):
         self.__class__.thisFuncName = curFuncName

     def curFuncName(self):
         return self.__class__.thisFuncName

     def auxInvokationContextSet(self, auxInvokationEnum):
         self.__class__._auxInvokationContext = auxInvokationEnum

     def auxInvokationContext(self):
         return self.__class__._auxInvokationContext

     def auxInvokationResultsSet(self, auxInvokationRes):
         self.__class__._auxInvokationResults = auxInvokationRes

     def auxInvokationResults(self):
         return self.__class__._auxInvokationResults

     def iifNamesSet(self, iifs):
         self.__class__._iifNames = iifs

     def iifNames(self):
         return self.__class__._iifNames

     def iifMethodsDictSet(self, iifs):
         self.__class__._iifMethodsDict = iifs

     def iifMethodsDict(self):
         return self.__class__._iifMethodsDict

     def iifFuncsDictSet(self, iifs):
         self.__class__._iifFuncsDict = iifs

     def iifFuncsDict(self):
         return self.__class__._iifFuncsDict


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  commonIicmParamsParser    [[elisp:(org-cycle)][| ]]
"""     
def commonIicmParamsParser(parser):
    """Module Common Command Line Parameters.

    NOTYET -- Needs To Be Called
    """
    iicmParams = commonIicmParamsPrep()

    argsparseBasedOnIimParams(parser, iicmParams)

    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  commonIicmParamsPrep    [[elisp:(org-cycle)][| ]]
"""
def commonIicmParamsPrep():
    """Module Common Command Line Parameters.
    """
    iicmParams = IIM_ParamDict()

    iicmParams.parDictAdd(
        parAction='append',
        parName='callTrackings',
        parDescription="Set monitoring of calls and selected invokes.",
        parDataType=None,
        parDefault=[],
        parChoices=['invoke+', 'invoke-', 'monitor+', 'monitor-'],
        parScope=IIM_ParamScope.TargetParam,
        argparseShortOpt='-t',
        argparseLongOpt='--callTrackings',
        )
       
    iicmParams.parDictAdd(
        parAction='store',
        parName='runMode',
        parDescription="Run Mode as fullRun or dryRun",
        parDataType=None,
        parDefault='fullRun',
        parChoices=['dryRun', 'fullRun', 'runDebug'],
        parScope=IIM_ParamScope.TargetParam,
        #argparseShortOpt='-r',
        argparseLongOpt='--runMode',
        )
       
    iicmParams.parDictAdd(
        parAction='store',
        parName='verbosity',
        parDescription='Adds a Console Logger for the level specified in the range 1..50',
        parDataType=None,
        parDefault='30',
        parMetavar='ARG',
        parChoices=['1', '10', '20', '30', '40', '50',],
        parScope=IIM_ParamScope.TargetParam,
        argparseShortOpt='-v',        
        argparseLongOpt='--verbosity',
        )
       
    iicmParams.parDictAdd(
        parAction='store',
        parName='logFile',
        parDescription='Specifies destination LogFile for this run',
        parDataType=None,
        parDefault=None,
        parMetavar='ARG',
        parChoices=[],
        parScope=IIM_ParamScope.TargetParam,
        #argparseShortOpt='-v',        
        argparseLongOpt='--logFile',
        )

    iicmParams.parDictAdd(
        parAction='store',
        parName='logFileLevel',
        parDescription='Specifies destination LogFile for this run',
        parDataType=None,
        parDefault=None,
        parMetavar='ARG',
        parChoices=[],
        parScope=IIM_ParamScope.TargetParam,
        #argparseShortOpt='-v',        
        argparseLongOpt='--logFileLevel',
        )

    iicmParams.parDictAdd(
        parAction='store_true',
        parName='docstring',
        parDescription='Docstring',
        parDataType=None,
        parDefault=None,
        parMetavar='ARG',
        parChoices=[],
        parScope=IIM_ParamScope.TargetParam,
        #argparseShortOpt='-v',        
        argparseLongOpt='--logFileLevel',
        )
    
    # iicmParams.parDictAdd(
    #     parAction='store',
    #     parName='iifArgs',
    #     parDescription='Docstring',
    #     parDataType=None,
    #     parDefault=None,
    #     parMetavar='ARG',
    #     parChoices=None,
    #     parScope=IIM_ParamScope.TargetParam,
    #     #argparseShortOpt='-v',        
    #     argparseLongOpt='--logFileLevel',
    #     )
    

    iicmParams.parDictAdd(
        parAction='append',
        parName='loadfiles',
        parDescription='Load Files',
        parDataType=None,
        parDefault=None,
        parMetavar='ARG',
        parChoices=[],
        parScope=IIM_ParamScope.TargetParam,
        #argparseShortOpt='-l',        
        argparseLongOpt='--load',
        )
    
    return iicmParams

     
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  argsCommonProc -- Obsoleted By commonIicmParamsPrep??   [[elisp:(org-cycle)][| ]]
"""
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def argsCommonProc(parser):

     parser.add_argument(
         '-i',
         '--invokes',
         dest='invokes',
         action='append'
         )

     parser.add_argument(
         '-t',
         '--callTrackings',
         dest='callTrackings',
         action='append',
         choices=['invoke+', 'invoke-', 'monitor+', 'monitor-'],
         default=[]
         )

     parser.add_argument(
         '--runMode',
         dest='runMode',
         action='store',
         choices=['dryRun', 'fullRun', 'runDebug'],
         default='fullRun'
         )

     parser.add_argument(
         '-v',
         '--verbosity',
         dest='verbosityLevel',
         metavar='ARG',
         action='store',
         default=None,
         help='Adds a Console Logger for the level specified in the range 1..50'
         )

     parser.add_argument(
         '--logFile',
         dest='logFile',
         metavar='ARG',
         action='store',
         default=None,
         help='Specifies destination LogFile for this run'
         )

     parser.add_argument(
         '--logFileLevel',
         dest='logFileLevel',
         metavar='ARG',
         action='store',
         default=None,
         help=''
         )

     parser.add_argument(
         '--docstring',
         action='store_true',
         dest="docstring"
         )

     parser.add_argument(
         'iifArgs',
     #dest='iifArgs',   #
         metavar='IIF',
         nargs='*',
         action='store',
         help='Interactively Invokable Function Arguments'
         )

     parser.add_argument(
         '--load',
         dest='loadFiles',
         action='append',
         default=[]
         )

     return

"""
*  [[elisp:(org-cycle)][| ]]  getopt.args   :: Arguments Parsing -- G_argsProc based on argparse [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  G_argsProc    [[elisp:(org-cycle)][| ]]
"""
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def G_argsProc(arguments, extraArgs):
     """IIM-IIM Argument Parser.

     extraArgs resides in the G_ module.
     """

     parser = argparse.ArgumentParser(
         description=__doc__
         )

     argsCommonProc(parser)
     #commonIicmParamsPrep()
     
     extraArgs(parser)

     #
     # The logic below breaks multiple --invokes.
     # Perhaps a distinction between --invoke and --invokes is an answer.
     #
     # We are inserting "--" after -i cmnd
     # to get things like -i run pip install --verbose
     #
     #
     index = 0
     for each in arguments:
         if each == "-i":
             arguments.insert(index+2, "--")
             break
         if each == "--invokes":            
             arguments.insert(index+2, "--")
             break
         index = index + 1

     args = parser.parse_args(arguments)

     return args, parser


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  argsparseBasedOnIimParams    [[elisp:(org-cycle)][| ]]
"""
#subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def argsparseBasedOnIimParams(parser, iimParams):
     """Convert iimParams to parser
**  [[elisp:(org-cycle)][| ]]  Subject      :: type= is missing -- [[elisp:(org-cycle)][| ]]
     """


     for key, iimParam in iimParams.parDictGet().iteritems():
         if ( iimParam.argsparseShortOptGet() == None )  and ( iimParam.argsparseLongOptGet() == None ):
             break

         if not iimParam.argsparseShortOptGet() == None:
             parser.add_argument(
                 iimParam.argsparseShortOptGet(),
                 iimParam.argsparseLongOptGet(),
                 dest = iimParam.parNameGet(),
                 nargs = iimParam.parNargsGet(),
                 action=iimParam.parActionGet(),
                 default = iimParam.parDefaultGet(),
                 help=iimParam.parDescriptionGet()
                 )
         else:
             parser.add_argument(
                iimParam.argsparseLongOptGet(),
                dest = iimParam.parNameGet(),
                nargs = iimParam.parNargsGet(),
                metavar = 'ARG',
                action=iimParam.parActionGet(),
                default = iimParam.parDefaultGet(),
                help=iimParam.parDescriptionGet()
                )

     return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimParamsToFileParamsUpdate    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iimParamsToFileParamsUpdate(
        parRoot,
        iimParams,
):
     """Convert iimParams to parser
**  [[elisp:(org-cycle)][| ]]  Subject      :: type= is missing -- [[elisp:(org-cycle)][| ]]
     """

     LOG_here("Updating iimParams at: {parRoot}".format(parRoot=parRoot))
     
     for key, iimParam in iimParams.parDictGet().iteritems():
         if ( iimParam.argsparseShortOptGet() == None )  and ( iimParam.argsparseLongOptGet() == None ):
             break
         
         iimParam.writeAsFileParam(
             parRoot=parRoot,
         )
         
     return
 
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifParamsMandatoryAssert    [[elisp:(org-cycle)][| ]]
"""

def iifParamsMandatoryAssert(paramsList):
        for key, value in paramsList.iteritems():
            if value == None: return(EH_critical_usageError(key))
            

"""
*  [[elisp:(org-cycle)][| ]]  /G_ examples/        :: *G_commonExamples -- Common features included in G_examples() + devExamples(), etc* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  commonExamples    [[elisp:(org-cycle)][| ]]
"""
class commonExamples(Iif):
    """Print common IICM examples."""

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=True,
    ):
        """Provide a menu of common iicm examples.
"""
        G_myFullName = sys.argv[0]
        G_myName = os.path.basename(G_myFullName)

        iifExampleMenuChapter('/Intercatively Invokable Module (IIM) General Usage Model/')

        print( G_myName + " --help" )
        print( G_myName + " -i model" )
        print( G_myName + " -i iicmHelp" )
        print( G_myName + " -i iicmOptionsExamples" )
        print( G_myName + " -i iicmInfo" )
        print( G_myName + " -i iicmInUpdate ./var" )        
        print( G_myName + " -i iifInfo iifName" )
        print( G_myName + " -i iifInfo iifInfo" )                
        print( G_myName + " -i devExamples" )
        print( G_myName + " -i describe" )
        print( G_myName + " -i describe" + " |" + " emlVisit")
        print( G_myName + " -i examples" )
        print( G_myName + " -i examples" + " |" + " iimToEmlVisit")

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  G_commonBriefExamples    [[elisp:(org-cycle)][| ]]
"""
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def G_commonBriefExamples(interactive=False):

     G_myFullName = sys.argv[0]
     G_myName = os.path.basename(G_myFullName)

     iifExampleMenuChapter('/Intercatively Invokable Module (IIM) Brief Usage Model/')

     print( G_myName + " -i commonExamples" + "    # Help, Model, iimOptionsExample")
     print( G_myName + " -i describe" + " |" + " emlVisit")
     print( G_myName + " -i examples" + " |" + " iimToEmlVisit")
     print( G_myName + " -i visit")     
     print( """emlVisit -v -n showRun -i gotoPanel """ + G_myFullName)

     iifExampleMenuChapter('*IICM Blee Player Invokations*')
     ANN_write("iicmPlayer.sh -h -v -n showRun -i grouped {G_myName}".format(G_myName=G_myName))     

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  devExamples    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def devExamples(interactive=False):

     G_myName = sys.argv[0]

     print("======== Development =========")

     print("python -m trace -l " + G_myName + " | egrep -v " + '\'/python2.7/|\<string\>\'')
     print("python -m trace -l " + G_myName)
     print("python -m trace -t " + G_myName)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimOptionsExamples    [[elisp:(org-cycle)][| ]]
"""

class iicmOptionsExamples(Iif):
    """Print a summary of the IICM Model."""

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=True,
    ):
 
        G_myFullName = sys.argv[0]
        G_myName = os.path.basename(G_myFullName)

        print("==== iifEx Built-In Feature Examples =====")

        print( G_myName + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " -v 20" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " -v 1" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " --runMode dryRun" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " -v 1" + " --callTrackings monitor-" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " -v 1" + " --callTrackings monitor+" + " --callTrackings invoke+" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " -v 1" + " --callTrackings monitor-" + " --callTrackings invoke-" + " -i iim.iifExample arg1 arg2" )
        print( G_myName + " --docstring" + " -i describe" )



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimExampleMyName    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iimExampleMyName(myName, myFullName):
    """
    """
    print("#######  " + '  *' + myName + '*  ' + "  ##########")
    print("=======  " + myFullName + "  ===========")

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  ex_gCommon    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def ex_gCommon():
    """."""
    G = IicmGlobalContext()
    iimExampleMyName(G.iicmMyName(), G.iicmMyFullName())
    G_commonBriefExamples()    
    #G_commonExamples()

"""
*  [[elisp:(org-cycle)][| ]]  /example Seps/       :: *iifExample -- Simple Usage Example -- Seperators* [[elisp:(org-cycle)][| ]]
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExample    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExample():
     """Example of using built-in features of an IIF in an IIM.

     - The iim.callableEntryEnhancer() must be included to enable --docstring.
     - Decorator @iim.subjectToTracking() enables Call Monitoring.
     - iim.do() enables invokation monitoring
     - iim.TM_ enables tracking/tracing using the LOG_ facility.
     """

     try: callableEntryEnhancer(type='iif')
     except StopIteration:  return

     G = IicmGlobalContext()
     iimRunArgs = G.iimRunArgsGet()

     logger = LOG_Control().loggerGet()

     logger.debug('Raw Logging' + ucf.stackFrameInfoGet(1) )
     TM_here('Here' + ' Tracking')
     TM_note('UnHere Tracking')

     for thisArg in iimRunArgs.iifArgs:
         print ('iifExample() received iifArg=' + thisArg)

     do( intrusiveFunc, ' With Some Parameter' )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExampleMenuChapter    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExampleMenuChapter(title):
    """
    """
    print("#######  " + title + "  ##########")


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExampleMenuSection    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExampleMenuSection(title):
     """
     """
     print("=======  " + title + "  ==========")


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExampleMenuSubSection    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExampleMenuSubSection(title):
     """  """
     print("%%%%%%%  " + title + "  %%%%%%%%%%%")


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExampleMenuItem    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExampleMenuItem(
        commandLine,
        icmName=None,          # Defaults to G_myName
        verbosity='basic',
        comment='none',
        icmWrapper=None,
):
    """ vebosity is one of: 'none', 'little', 'some',  'full'
    """
    G_myFullName = sys.argv[0]
    G_myName = os.path.basename(G_myFullName)

    if comment == 'none':
        fullCommandLine = commandLine
    else:
        fullCommandLine = commandLine + '         ' + comment

    if icmName:
        G_myName = icmName
        
    if icmWrapper:
        G_myName = icmWrapper + " " + G_myName

    if verbosity == 'none':
        #print( G_myName + " -v 30" + " " + fullCommandLine)
        print( G_myName + " " + fullCommandLine)        
    elif verbosity == 'basic':
        print( G_myName + " -v 1"  + " " + fullCommandLine )
    elif verbosity == 'little':
        print( G_myName + " -v 20" + " " + fullCommandLine )
    elif verbosity == 'some':
        print( G_myName + " -v 1"  + " --callTrackings monitor-" + " --callTrackings invoke-" + " " + fullCommandLine )
    elif verbosity == 'full':
        print( G_myName + " -v 1"  + " --callTrackings monitor+" + " --callTrackings invoke+" + " " + fullCommandLine )
    else:
        return EH_critical_oops('')

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  ex_gCmndMenuItem    [[elisp:(org-cycle)][| ]]
"""    
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def ex_gCmndMenuItem(
        cmndName,    # String
        cmndPars,    # Dictionary
        cmndArgs,    # String
        verbosity='basic',
        comment='none',
        icmWrapper=None,
        icmName=None,
):
    """ vebosity is one of: 'none', 'little', 'some',  'full'
    """

    cmndParsStr = ""
    for key in cmndPars:
        cmndParsStr += """--{parName}="{parValue}" """.format(parName=key, parValue=cmndPars[key])
    
    cmndLine = """{cmndParsStr} -i {cmndName} {cmndArgs}""".format(
        cmndName=cmndName, cmndParsStr=cmndParsStr, cmndArgs=cmndArgs
    )

    iifExampleMenuItem(
        commandLine=cmndLine,
        verbosity=verbosity,
        comment=comment,
        icmWrapper=icmWrapper,
        icmName=icmName,
    )    

####+BEGIN: bx:dblock:python:func :funcName "ex_gExecMenuItem" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "execLine wrapper=None comment='none'"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-anyOrNone :: /ex_gExecMenuItem/ funcType=anyOrNone retType=bool deco= argsList=(execLine wrapper=None comment='none')  [[elisp:(org-cycle)][| ]]
"""
def ex_gExecMenuItem(
    execLine,
    wrapper=None,
    comment='none',
):
####+END:
    """
** Output an Non-ICM menu line.
"""
    if comment == 'none':
        fullCommandLine = execLine
    else:
        fullCommandLine = execLine + '         ' + comment
        
    if wrapper:
        fullCommandLine = wrapper + fullCommandLine

    print fullCommandLine
    

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifExampleExternalCmndItem    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifExampleExternalCmndItem(commandLine,
                               verbosity='basic',
                               comment='none'
                               ):
    """ vebosity is one of: 'none', 'little', 'some',  'full'
                               """
    #G_myFullName = sys.argv[0]
    #G_myName = os.path.basename(G_myFullName)

    if comment == 'none':
        fullCommandLine = commandLine
    else:
        fullCommandLine = commandLine + '         ' + comment

    print( fullCommandLine )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifArgsLengthIsNotValid    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifArgsLengthIsNotValid(iifArgs=ArgReq.Mandatory,
                        expected=ArgReq.Mandatory,
                        comparison=ArgReq.Mandatory,
                       ):
    iifArgsLen=len(iifArgs)
    if comparison(iifArgsLen, expected):
        EH_critical_usageError("Bad Number Of iifArgs: iifArgs={iifArgs}"
                                 .format(iifArgs=iifArgs))
        return(True)
    return(False)
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifArgsLengthValidate    [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def iifArgsLengthValidate(iifArgs=ArgReq.Mandatory,
                        expected=ArgReq.Mandatory,
                        comparison=ArgReq.Mandatory,
                       ):
    iifArgsLen=len(iifArgs)
    if comparison(iifArgsLen, expected):
        EH_critical_usageError("Bad Number Of iifArgs: iifArgs={iifArgs}"
                                 .format(iifArgs=iifArgs))
        return(1)
    return(0)
        
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  int__gt    [[elisp:(org-cycle)][| ]]
"""

def int__gt(nuOfArgs,  expected):
    if nuOfArgs > expected:
        return True
    else:
        return False

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  intrusiveFunc  -- Put this in the examples  [[elisp:(org-cycle)][| ]]
"""
@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def intrusiveFunc(arg):
    """Example of an intrusive function that can be subject to dryRun.
    Could also be done with @subjectToDryRun
    """
    if iimRunArgs_isRunModeDryRun():
        print( "Skipping This Intrusive Function" + arg )
        return

    print( "Performing Some Intrusive Action" + arg )


"""
*  [[elisp:(org-cycle)][| ]]  /iimRunArgs/         :: *IimRunArgs_ -- In support of Run Time IIM Options --  iimRunArgs_isOptionXxSet()* [[elisp:(org-cycle)][| ]]
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_isCallTrackingMonitorOff    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_isCallTrackingMonitorOff():
    """Activated with --callTrackings monitor-.
    """

    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()
    retVal = False

    for this in iimRunArgs.callTrackings:
        if this == 'monitor-':
            retVal = True

    return retVal
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_isCallTrackingMonitorOn    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_isCallTrackingMonitorOn():
    """Activated with --callTrackings monitor-.
    """

    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()
    retVal = False

    try:
        callTrackings = iimRunArgs.callTrackings
    except AttributeError:
        callTrackings = []
        

    for this in callTrackings:
        if this == 'monitor+':
            retVal = True

    return retVal
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_isCallTrackingInvokeOff    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_isCallTrackingInvokeOff():
    """Activated with --callTrackings monitor-.
    """
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    retVal = False

    for this in iimRunArgs.callTrackings:
        if this == 'invoke-':
            retVal = True

    return retVal

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_isRunModeDryRun    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_isRunModeDryRun():
    """Activated with --runMode dryRun.
    """
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    retVal = False

    if iimRunArgs.runMode == 'dryRun':
        retVal = True

    return retVal

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_isDocStringRequested    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_isDocStringRequested():
    """Activated with -i docString.
    """
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    retVal = False

    if iimRunArgs.docstring:
        retVal = True

    return retVal

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_loadFiles    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_loadFiles():
    """Load the python files specified with --load."""
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    for this in iimRunArgs.loadFiles:
        loadFile(this)

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iimRunArgs_evalFiles    [[elisp:(org-cycle)][| ]]
"""

def iimRunArgs_evalFiles():
    """Eval Files -- Unused But Perhaps Usefull."""
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    for this in iimRunArgs.loadFiles:
        TM_here('Loading: ' + this)
        f = open(this)
        eval(f.read()) # Caution: you must be sure of what's in that file
        f.close()


"""
*  [[elisp:(org-cycle)][| ]]  /G_main/             :: *G_main -- Invoked from IIM, calls invokesProc* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  G_main    [[elisp:(org-cycle)][| ]]
"""
# DO NOT DECORATE THIS FUNCTION
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)   # Log module has not been setup, we can't track this
def G_main(inArgv,
           G_examples,
           extraArgs,
           invokesProc,
           mainEntry=None,
):
    """This is the main entry point for Python.Iim.Iim (InteractiveInvokationModules)
    """

    #
    # The order is important here,
    # 1) Parse The Command Line -- 2) LOG_ usese the command line -- 3) G. setup
    #
    iimRunArgs, iicmArgsParser = G_argsProc(inArgv, extraArgs)

    logControler = LOG_Control()
    logControler.loggerSet(iimRunArgs)

    logger = logControler.loggerGet()

    logger.info('Main Started: ' + ucf.stackFrameInfoGet(1) )

    G = IicmGlobalContext()
    G.globalContextSet( iimRunArgs=iimRunArgs )
    G.iicmArgsParser = iicmArgsParser

    iimRunArgs_loadFiles()

    if len( inArgv ) == 0:
        if G_examples:
            G_examples()
            return

    if iimRunArgs.invokes:
        invokesProc()
    else:
        if mainEntry:
            mainEntry()

    return 0


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  G_mainWithClass    [[elisp:(org-cycle)][| ]]
"""
# DO NOT DECORATE THIS FUNCTION
#@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)   # Log module has not been setup, we can't track this
def G_mainWithClass(
        inArgv,
        G_examples,
        extraArgs,
        classedIifsDict,
        funcedIifsDict,
        mainEntry=None,
):
    """This is the main entry point for Python.Iim.Iim (InteractiveInvokationModules)
    """

    iimRunArgs, iicmArgsParser = G_argsProc(inArgv, extraArgs)    

    logControler = LOG_Control()
    logControler.loggerSet(iimRunArgs)

    logger = logControler.loggerGet()

    logger.info('Main Started: ' + ucf.stackFrameInfoGet(1) )

    G = IicmGlobalContext()
    G.globalContextSet( iimRunArgs=iimRunArgs )
    G.iicmArgsParser = iicmArgsParser    
    G.iifMethodsDictSet(classedIifsDict)
    G.iifFuncsDictSet(funcedIifsDict)

    iimRunArgs_loadFiles()

    if len( inArgv ) == 0:
        if G_examples:
            G_examples().iif()
            return

    if iimRunArgs.invokes:
        thisIifName=iimRunArgs.invokes[0]        
        outcome = invokesProcAllClassedAndFunced(
            classedIifsDict,
            funcedIifsDict,            
        )

        if not outcome:
            return

        try:
            outcomeError = outcome.error
        except AttributeError:
            ANN_here("Consider returning an outcome. iif={iif}".format(iif=thisIifName))
            return
        
        if outcomeError: 
            if outcome.error != OpError.Success:
                if outcome.error == OpError.CmndLineUsageError:
                    sys.stderr.write(
                        "{myName}.{iifName} Command Line Failed: Error={status} -- {errInfo}\n".
                        format(myName=G.iicmMyName(),
                               iifName=thisIifName,
                               status=outcome.error,
                               errInfo=outcome.errInfo,
                    ))
                    print "------------------"
                    G.iicmArgsParser.print_help()
                    print "------------------"
                    print "Run -i usage for more details."
                else:
                    sys.stderr.write(
                        "{myName}.{iifName} Failed: Error={status} -- {errInfo}\n".
                        format(myName=G.iicmMyName(),
                               iifName=thisIifName,
                               status=outcome.error,
                               errInfo=outcome.errInfo,
                    ))
            else:
                #sys.stderr.write("{myName}.{iifName} Completed Successfully: status={status}\n"
                logger.info(
                    "{myName}.{iifName} Completed Successfully: status={status}".
                    format(myName=G.iicmMyName(),
                           iifName=thisIifName,
                           status=outcome.error
                ))
        else:
            #sys.stderr.write("{myName}.{iifName} Completed Successfully: status={status}\n"
            logger.info(                
                "{myName}.{iifName} Completed Successfully: status={status}".                
                format(myName=G.iicmMyName(),
                       iifName=thisIifName,
                       status=outcome.error
            ))
        return outcome.error
    else:
        if mainEntry:
            mainEntry()

    return 0

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  invokesProcWithClass    [[elisp:(org-cycle)][| ]]
"""
def invokesProcAllClassedAndFunced(
        classedIifsDict,
        funcedIifsDict,        
):
    """Process all invokations applicable to all (classed+funced of mains+libs) IIFs."""
    G = IicmGlobalContext()
    iimRunArgs = G.iimRunArgsGet()

    ucf.perhapsInvokeHook('g_iicmPreIifs', funcedIifsDict)

    #print classedIifsDict

    #print "ZZ"

    #print funcedIifsDict
    
    for invoke in iimRunArgs.invokes:
        #
        # First we try iifList_mainsMethods()
        #
        try:
            classedIif = classedIifsDict[invoke]
        except  KeyError:
            #print "TM_"
            pass
        else:
            outcome = classedIif().iif(
                interactive=True, 
            )
            continue

        #
        # Next we try iifList_libsMethods()
        #
        callDict = dict()
        for eachIif in iifList_libsMethods().iif(interactive=False):
            try:
                callDict[eachIif] = eval("{eachIif}".format(eachIif=eachIif))
            except NameError:
                print("EH_problem -- Skipping eval({eachIif})".format(eachIif=eachIif))
                continue

        try:
            classedIif = callDict[invoke]
        except  KeyError:
            pass
        else:
            outcome =  classedIif().iif(
                interactive=True, 
            )
            continue

        #
        # Next we try iifList_mainsFuncs() which is in funcedIifsDict
        #
        try:
            funcedIif = funcedIifsDict[invoke]
        except  KeyError:
            EH_problem_info("invoke={}".format(invoke))
            pass
        else:
            outcome =  funcedIif(
                interactive=True, 
            )
            continue

        #
        # We tried everything and could not find any
        #

        # BUG, NOTYET, EH_problem goes to -v 20
        EH_problem_info("Invalid Action: {invoke}"
                        .format(invoke=invoke))            

        print("Invalid Action: {invoke}"
                        .format(invoke=invoke))

        outcome = OpOutcome()
        outcome.error = OpError.CmndLineUsageError
        outcome.errInfo = "Invalid Action: {invoke}".format(invoke=invoke)

    ucf.perhapsInvokeHook('g_iicmPostIifs', funcedIifsDict)
    
    return(outcome)


"""
*  [[elisp:(org-cycle)][| ]]  /Player Support/      :: *Framework iifs That are expected by the IICM-Player* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iimLanguage    [[elisp:(org-cycle)][| ]]
"""
class iimLanguage(Iif):
    """Returns python"""

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
    ):
        """Part of iicm framework."""
        thisOutcome = OpOutcome()
        if interactive:
            print "python"

        return thisOutcome.set(
            opError=OpError.Success,
            opResults="python"
        )


    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iimCmndPartIncludes    [[elisp:(org-cycle)][| ]]
"""
class iimCmndPartIncludes(Iif):
    """NOTYET Returns True"""

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
    ):
        """Part of iicm framework."""

        #if interactive:
            #print "python"

        return True
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iicmInUpdate -- Update    [[elisp:(org-cycle)][| ]]
"""    
class iicmInUpdate(Iif):
    """Given a baseDir, update iicmIn"""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
            iicmsBase=None,  # iifArgs[0]
    ):
        """Part of iicm framework."""

        if interactive:
            G = IicmGlobalContext()
            iimRunArgs = G.iimRunArgsGet()
            iicmsBase = iimRunArgs.iifArgs[0]
        else:
            if not iicmsBase:
                EH_problem_usageError("")
                return

        G_myFullName = sys.argv[0]
        G_myName = os.path.basename(G_myFullName)

        iicmInBase = iicmsBase + "/" + G_myName + "/iicmIn"
        
        print "{iicmInBase}".format(iicmInBase=iicmInBase)
            
        iimParamsToFileParamsUpdate(
            parRoot="{iicmInBase}/paramsFp".format(iicmInBase=iicmInBase),
            iimParams=G.iimParamDictGet(),
        )

        iimParamsToFileParamsUpdate(
            parRoot="{iicmInBase}/commonParamsFp".format(iicmInBase=iicmInBase),
            iimParams=commonIicmParamsPrep(),
        )

        iifMainsMethodsToFileParamsUpdate(
            parRoot="{iicmInBase}/iifMainsFp".format(iicmInBase=iicmInBase),
        )

        iifLibsMethodsToFileParamsUpdate(
            parRoot="{iicmInBase}/iifLibsFp".format(iicmInBase=iicmInBase),
        )
        
        return 


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iicmInfo    [[elisp:(org-cycle)][| ]]
"""    
class iicmInfo(Iif):
    """Given a baseDir, update iicmIn"""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]

    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
    ):
        """Part of iicm framework."""

        # if interactive:
        G = IicmGlobalContext()
        #     iimRunArgs = G.iimRunArgsGet()
        #     iicmInBase = iimRunArgs.iifArgs[0]
        # else:
        #     if not iicmInBase:
        #         EH_problem_usageError("")
        #         return

        print("* IICM Specified Parameters")

        iimParams = G.iimParamDictGet()

        for key, iimParam in iimParams.parDictGet().iteritems():
            if ( iimParam.argsparseShortOptGet() == None )  and ( iimParam.argsparseLongOptGet() == None ):
                break

            print "** " + key
            print "*** " + str(iimParam)

        print("* IICM Common Parameters")            

        iimParams = commonIicmParamsPrep()

        for key, iimParam in iimParams.parDictGet().iteritems():
            if ( iimParam.argsparseShortOptGet() == None )  and ( iimParam.argsparseLongOptGet() == None ):
                break

            print "** " + key
            print "*** " + str(iimParam)
            
        print("* IICM Mains Methods")
            
        mainsMethods = iifList_mainsMethods().iif(interactive=False)         
        for each in mainsMethods:
            iifInfo().iif(
                interactive=True,
                orgLevel=2,
                iifName=each,
            )

        print("* IICM Libs Methods")
            
        libsMethods = iifList_libsMethods().iif(interactive=False)
        for each in libsMethods:
            iifInfo().iif(
                interactive=True,
                orgLevel=2,
                iifName=each,
            )
       
        return 
 


"""
####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF       ::  version    [[elisp:(org-cycle)][| ]]
*       [[elisp:(org-cycle)][| *Version:* | ]]
####+END:
"""
class version(Iif):
    """IICM version number."""

    iifArgsLen={'Min': 0, 'Max':0,}
    
    #@iicm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Version number is obtained from."""
        if interactive:
            print("* IIM-Version: {ver}".format(ver=str( __version__ )))
            return
        else:
            return(format(str(__version__)))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  visit    [[elisp:(org-cycle)][| ]]
"""
class visit(Iif):
    """Visit The IICM Module."""

    iifArgsLen = {'Min': 0, 'Max':0,}
    
    subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Use emacs client to visit the IICM module."""
        
        myName=self.myName()
        G = IicmGlobalContext()
        thisOutcome = OpOutcome(invokerName=myName)
        
        thisOutcome = subProc_bash(
            """emlVisit -v -n showRun -i gotoPanel {myFullName}"""
            .format(myFullName=G.iicmMyFullName()),
            stdin=None, outcome=thisOutcome,
        ).out()
        
        if thisOutcome.isProblematic():
            return(EH_badOutcome(thisOutcome))
        
        return thisOutcome
        

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifInfo    [[elisp:(org-cycle)][| ]]
"""    
class iifInfo(Iif):
    """Returns a human oriented string for the specified iifName's expected pars/args usage."""

    iifArgsLen={'Min': 1, 'Max':1,}    
    iifArgsSpec = {1: ["iifName"]}
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
            iifName=None,  # iifArgs[0]             
            orgLevel=2,
    ):
        """Used by IICM Players to inform user of a given iifName capabilities."""

        myName=self.myName()
        G = IicmGlobalContext()
        thisOutcome = OpOutcome(invokerName=myName)

        if not iifName:
            if not interactive:
                EH_problem_usageError("")
                return
            iifName = G.iimRunArgsGet().iifArgs[0]

        iifClass = iifNameToClass(iifName)
        if not iifClass: return

        outString = list()

        def orgIndentStr(subLevel): return "*" * (orgLevel + subLevel)

        outString.append("{baseOrgStr} {iifName}\n".format(
            baseOrgStr=orgIndentStr(0),
            iifName=iifName,
        ))
        outString.append("{baseOrgStr} iifShortDocStr={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifDocStrShort().iif(
                interactive=False,
                iifName=iifName,
        )))
        outString.append("{baseOrgStr} iifFullDocStr={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifDocStrFull().iif(
                interactive=False,
                iifName=iifName,
        )))
        outString.append("{baseOrgStr} iifParamsMandatory={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().paramsMandatory(),           
        ))
        outString.append("{baseOrgStr} iifParamsOptional={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().paramsOptional(),           
        ))
        outString.append("{baseOrgStr} iifArgsLen={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().argsLen(),           
        ))
        outString.append("{baseOrgStr} iifArgsSpec={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().argsDesc(),           
        ))
        outString.append("{baseOrgStr} iifUsers={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().users(),           
        ))
        outString.append("{baseOrgStr} iifGroups={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().groups(),           
        ))
        outString.append("{baseOrgStr} iifImapct={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().impact(),           
        ))
        outString.append("{baseOrgStr} iifVisibility={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().visibility(),           
        ))

        if interactive:
            # print adds an extra line at the end in Python 2.X
            sys.stdout.write("".join(outString))

        return thisOutcome.set(
            opError=OpError.Success,
            opResults="".join(outString)
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifInfoEssential    [[elisp:(org-cycle)][| ]]
"""    
class iifInfoEssential(Iif):
    """Returns a human oriented string for the specified iifName's expected pars/args usage."""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]
    iifArgsSpec = ["iifName"]
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)     
    def iif(self,
            interactive=False,
            iifName=None,  # iifArgs[0]            
            orgLevel=2,
    ):
        """Used by IICM Players to inform user of a given iifName capabilities."""

        myName=self.myName()
        G = IicmGlobalContext()
        thisOutcome = OpOutcome(invokerName=myName)

        if not iifName:
            if not interactive:
                EH_problem_usageError("")
                return
            iifName = G.iimRunArgsGet().iifArgs[0]

        iifClass = iifNameToClass(iifName)
        if not iifClass: return

        outString = list()

        def orgIndentStr(subLevel): return "*" * (orgLevel + subLevel)

        outString.append("{baseOrgStr} iifFullDocStr={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifDocStrFull().iif(
                interactive=False,
                iifName=iifName,
        )))
        outString.append("{baseOrgStr} iifParamsMandatory={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().paramsMandatory(),           
        ))
        outString.append("{baseOrgStr} iifParamsOptional={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().paramsOptional(),           
        ))
        outString.append("{baseOrgStr} iifArgsLen={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().argsLen(),           
        ))
        outString.append("{baseOrgStr} iifArgsSpec={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().argsDesc(),           
        ))
        outString.append("{baseOrgStr} iifUsers={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().users(),           
        ))
        outString.append("{baseOrgStr} iifGroups={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().groups(),           
        ))
        outString.append("{baseOrgStr} iifImapct={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().impact(),           
        ))
        outString.append("{baseOrgStr} iifVisibility={str}\n".format(
            baseOrgStr=orgIndentStr(1),
            str=iifClass().visibility(),           
        ))

        if interactive:
            # print adds an extra line at the end in Python 2.X
            sys.stdout.write("".join(outString))

        return thisOutcome.set(
            opError=OpError.Success,
            opResults="".join(outString)
        )
    
    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifNameToClass    [[elisp:(org-cycle)][| ]]
"""
def iifNameToClass(
        iifName,
):
    """Given iifName, return iifClass."""

    G = IicmGlobalContext()
    classedIifsDict = G.iifMethodsDict()

    try:
        classedIif = classedIifsDict[iifName]
    except  KeyError:
        #print "TM_"
        pass
    else:
        return classedIif
    
    try:
        iifClass = eval("{iifName}".format(iifName=iifName))
    except NameError:
        return None

    if iifName in iifSubclassesNames():
        return iifClass
    else:
        return None
    

"""
*  [[elisp:(org-cycle)][| ]]  /iifsList_/          :: *iifsList_ -- List C-IIFs and F-IIFs in a given file and in iicm library* [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_allMethods    [[elisp:(org-cycle)][| ]]
"""
class iifList_allMethods(Iif):
    """List All Classed-IIFs."""

    #Do Not Decorate with  @subjectToTracking    
    def iif(self,
            interactive=True,
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it and return the list.
"""
        allClassedIifNames = iifSubclassesNames()

        if interactive:
            ucf.listPrintItems(allClassedIifNames)

        return allClassedIifNames

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_allFuncs    [[elisp:(org-cycle)][| ]]
"""
class iifList_allFuncs(Iif):
    """List All Classed-IIFs."""

    #Do Not Decorate with  @subjectToTracking
    def iif(self,
            interactive=True,
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it and return the list.
"""
        allFuncedIifNames = iifSubclassesNames()

        if interactive:
            ucf.listPrintItems(allFuncedIifNames)

        return allFuncedIifNames

    
mainsClassedIifsGlobal = None    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_mainsMethods    [[elisp:(org-cycle)][| ]]
"""
class iifList_mainsMethods(Iif):
    """List All C-IIFs of the Module."""

    #Do Not Decorate with  @subjectToTracking    
    def iif(self,
            interactive=False,
            importedIifs={}
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it and return the list.
"""

        global mainsClassedIifsGlobal

        allClassedIifNames = iifSubclassesNames()

        mainClasses = ucf.ast_topLevelClassNamesInFile(
            sys.argv[0]
        )

        relevantClasses = mainClasses
        for key, modPath in importedIifs.iteritems():
            if modPath.endswith('.pyc') and os.path.exists(modPath[:-1]):
                modPath = modPath[:-1]
            relevantClasses += ucf.ast_topLevelClassNamesInFile(modPath)

        mainsClassedIifs = set.intersection(
            set(allClassedIifNames),
            set(relevantClasses),
        )
        
        if interactive:
            ucf.listPrintItems(mainsClassedIifs)

        mainsClassedIifsGlobal = mainsClassedIifs

        return mainsClassedIifs

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_mainsFuncs    [[elisp:(org-cycle)][| ]]
"""
class iifList_mainsFuncs(Iif):
    """List All F-IIFs of the Module."""

    #Do Not Decorate with  @subjectToTracking    
    def iif(self,
            interactive=False,
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it.
"""

        astMainModulesFunctionsList = ucf.ast_topLevelFunctionNamesInFile(
             sys.argv[0]
        )

        #print astMainModulesFunctionsList
        
        if interactive:
            print "print the list here"   

        return astMainModulesFunctionsList

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_libsMethods    [[elisp:(org-cycle)][| ]]
"""         
class iifList_libsMethods(Iif):
    """List All NAMES of C-IIFs of the Libs Module."""

    #@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it.
"""

        global mainsClassedIifsGlobal
        
        allClassedIifNames = iifSubclassesNames()

        #mainClasses = ucf.ast_topLevelClassNamesInFile(
        #    sys.argv[0]
        #)

        #print allClassedIifNames
        #print mainClasses
        #libsClassedIifs = set(allClassedIifNames) - set(mainClasses)
        libsClassedIifs = set(allClassedIifNames) - set(mainsClassedIifsGlobal)

        if interactive:
            ucf.listPrintItems(libsClassedIifs)

        return libsClassedIifs

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifList_libsFuncs    [[elisp:(org-cycle)][| ]]
"""
class iifList_libsFuncs(Iif):
    """List All C-IIFs of the Module."""

    #@subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
    ):
        """Is based on subclasses of Iif and which are in the main module.
When interactive is false, return the list and when true print it.
"""
        if interactive:
            return
        else:
             print "print the list here"   
             return

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifClassDocStr    [[elisp:(org-cycle)][| ]]
"""
class iifClassDocStr(Iif):
    """Given a list of iifs as Args, for each return the the class docStr."""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
            iifName=None,
    ):
        """The Iif class from which this is drived, includes docStr extractors.\
"""
        G = IicmGlobalContext()
        if not iifName:
            if not interactive:
                EH_problem_usageError("")
                return None
            iifName = G.iimRunArgsGet().iifArgs[0]

        iifClass = iifNameToClass(iifName)
        if not iifClass: return None
            
        docStr = iifClass().docStrClass()

        if interactive: print docStr

        return docStr

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifFuncDocStr    [[elisp:(org-cycle)][| ]]
"""
class iifMethodDocStr(Iif):
    """Given a list of iifs as Args, for each return the iif() funcs docStr."""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
            iifName=None,            
    ):
        """The Iif class from which this is drived, includes docStr extractors.\
"""
        G = IicmGlobalContext()
        if not iifName:
            if not interactive:
                EH_problem_usageError("")
                return
            iifName = G.iimRunArgsGet().iifArgs[0]

        iifClass = iifNameToClass(iifName)
        if not iifClass: return 
            
        docStr = iifClass().docStrIifMethod()

        if interactive:
            print docStr

        return docStr


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifDocStrShort    [[elisp:(org-cycle)][| ]]
"""
class iifDocStrShort(Iif):
    """Given a list of iifs as Args, for each return the the class docStr."""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
            iifName=None,
    ):
        """The Iif class from which this is drived, includes docStr extractors.\
"""
        classDocStr = iifClassDocStr().iif(
                interactive=False,
                iifName=iifName,
        )
        if not classDocStr: return None

        shortDocStr = ucf.STR_getFirstLine(classDocStr)
        
        if interactive: print shortDocStr
        return shortDocStr

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF        ::  iifDocStrLong    [[elisp:(org-cycle)][| ]]
"""
class iifDocStrFull(Iif):
    """Given a list of iifs as Args, for each return the iif() funcs docStr."""
    iifParamsMandatory = None
    iifParamsOptional = None
    iifArgsLen = ["1"]
    
    @subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,
            iifName=None,            
    ):
        """The Iif class from which this is drived, includes docStr extractors.\
"""
        classDocStr = iifClassDocStr().iif(
                interactive=False,
                iifName=iifName,
        )
        if not classDocStr: return None

        methodDocStr = iifMethodDocStr().iif(
                interactive=False,
                iifName=iifName,
        )
        if not methodDocStr: return None

        longDocStr = classDocStr + "\n" + methodDocStr
        
        if interactive: print longDocStr
        return longDocStr


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifSubclassesNames    [[elisp:(org-cycle)][| ]]
"""
def iifSubclassesNames():
    """Not using generators by choice."""
    # return [each.__name__ for each in Iif.__subclasses__()]
    iifsNames = list()
    for eachClass in Iif.__subclasses__():
        iifsNames.append(eachClass.__name__)
    return iifsNames

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifMainsMethodsToFileParamsUpdate    [[elisp:(org-cycle)][| ]]
"""
def iifMainsMethodsToFileParamsUpdate(
        parRoot,
):
    """ """
    mainsIifMethods = iifList_mainsMethods().iif()
    for each in mainsIifMethods:
        iifToFileParamsUpdate(
            iifName=each,
            parRoot=parRoot,
        )
    return

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifLibsMethodsToFileParamsUpdate    [[elisp:(org-cycle)][| ]]
"""
def iifLibsMethodsToFileParamsUpdate(
        parRoot,
):
    """ """
    libsIifMethods = iifList_libsMethods().iif()
    for each in libsIifMethods:
        iifToFileParamsUpdate(
            iifName=each,
            parRoot=parRoot,
        )
    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  iifToFileParamsUpdate    [[elisp:(org-cycle)][| ]]
"""
def iifToFileParamsUpdate(
        iifName,
        parRoot,
):
    "Write iif as fileParam"
    
    absoluteParRoot = os.path.abspath(parRoot)

    if not os.path.isdir(absoluteParRoot):
        try: os.makedirs( absoluteParRoot, 0775 )
        except OSError: pass

    parValue = "unSet"

    FILE_ParamWriteTo(
        parRoot=absoluteParRoot,
        parName=iifName,
        parValue=parValue,
    )
    
    def writeIifAttrFV(
            iifName,
            attrName,
            attrValue,
    ):
        varValueFullPath = os.path.join(
            absoluteParRoot,
            iifName,
            attrName,
        )
        FV_writeToFilePathAndCreate(
            filePath=varValueFullPath,
            varValue=attrValue,
        )

        
    docStr = iifDocStrShort().iif(
        iifName=iifName,
    )
    writeIifAttrFV(
        iifName=iifName,
        attrName='description',
        attrValue=docStr,
    )
        
    docStr = iifDocStrFull().iif(
        iifName=iifName,
    )
    writeIifAttrFV(
        iifName=iifName,
        attrName='fullDesc',
        attrValue=docStr,
    )

    iifClass = iifNameToClass(iifName)
    if not iifClass: return 
    
    writeIifAttrFV(
        iifName=iifName,
        attrName='paramsMandatory',
        attrValue=iifClass().paramsMandatory(),
    )
    writeIifAttrFV(
        iifName=iifName,
        attrName='paramsOptional',
        attrValue=iifClass().paramsOptional(),
    )
    writeIifAttrFV(
        iifName=iifName,
        attrName='iifInfo',
        attrValue=iifInfoEssential().iif(
            interactive=False,
            orgLevel=2,
            iifName=iifName,
        )
    )
    
    return


        
"""
*  [[elisp:(org-cycle)][| ]]  /General-Misc/       :: *Common-Misc Utilities -- FUNC_* [[elisp:(org-cycle)][| ]]
"""


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *End Of Editable Text*
"""

"""
*  [[elisp:(org-cycle)][| ]]  COMMON        :: /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
"""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall

####+END:

#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  Given a mailFile, Let this IICM do its processing
"""
"""
####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
* 
*  An Interactively Invokable Command Module (IICM) :: Best Used With Blee-IICM-Players in Emacs -- Part Of ByStar
####+END:
"""
"""
*  [[elisp:(org-cycle)][| *IICM-INFO:* |]]
"""
####+BEGINNOT: bx:dblock:global:iim:name-py :style "fileName"
__iicmName__ = "mboxRetrieve"
####+END:

####+BEGIN: bx:dblock:global:timestamp:version-py :style "date"
__version__ = "201706241205"
####+END:

# NOTYET dblk-begin
__status__ = "Production"
# NOTYET dblk-end

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
####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
#*      ================
*  [[elisp:(org-cycle)][|/Controls/| ]] ::  [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]] 
*** /More Panels Access ::
####+END:
"""

"""
# NOTYET, Can be dblock
*      ================
*  #################### CONTENTS-LIST ################
#*      ================
"""

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Imports*
"""
####+BEGINNOT: bx:dblock:global:file-insert :file "" Add Path As ParameterNOTYET
"""
*  [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  insertPathForImports    [[elisp:(org-cycle)][| ]]
"""
def insertPathForImports(path):
    import os
    import sys
    absolutePath = os.path.abspath(path)    
    if os.path.isdir(absolutePath):
        sys.path.insert(1, absolutePath)

insertPathForImports("../lib/python/")

####+END:

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=    ::  Imports [[elisp:(org-cycle)][| ]]
"""

import sys
import os
#import time


####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "ucf" :file "ucf"
# Development Workaround  For JediWorkaround
import ucf
####+END:

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "icm" :file "icm"
# External Usage
from unisos.icm import icm
####+END:

#import shlex
#import subprocess

#from datetime import datetime

#import re
#import pprint

import email
#import mailbox
#import smtplib

#import flufl.bounce

from email.mime.text import MIMEText
#from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

from bxMsg import msgOut
from bxMsg import msgIn
#from bxMsg import msgLib

import marmeAcctsLib
import marmeSendLib

import collections


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Framework IIFs*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  describe    [[elisp:(org-cycle)][| ]]
"""
class describe(icm.Iif):
    """IICM basic description."""

    iifArgsLen={'Min': 0, 'Max':0,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Provides basic description of this IICM."""

        moduleDescription="""
*       [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**       Functional Specification :Overview:
**       *[End-Of-Description]*
"""
        if interactive:
            print( str( __doc__ ) )  # This is the Summary: from the top doc-string
            print(moduleDescription)

        return("Version: " + format(str(__version__)) + format(str(__doc__) + moduleDescription))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  usage    [[elisp:(org-cycle)][| ]]
"""
class usage(icm.Iif):
    """IICM basic usage information."""

    iifArgsLen={'Min': 0, 'Max':0,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Provides basic usage information for this IICM."""

        moduleDescription="""
*       [[elisp:(org-cycle)][| *Usage:* | ]]

**       See-Also:
***      iicm -i describe
***      iicm -i version
**      *[End-Of-Usage]*
"""
        if interactive:
            print( str( __doc__ ) )  # This is the Summary: from the top doc-string
            #version(interactive=True)
            print(moduleDescription)

        return(format(str(__doc__)+moduleDescription))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  status    [[elisp:(org-cycle)][| ]]
"""
class status(icm.Iif):
    """IICM current development status."""

    iifArgsLen={'Min': 0, 'Max':0,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Provides information about current development status of the module including todo and scheduled action items."""

        moduleDescription="""
*       [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Current         :: Just getting started [[elisp:(org-cycle)][| ]]

**      *[End-Of-Status]*
"""
        if interactive:
            print( str( __doc__ ) )  # This is the Summary: from the top doc-string
            #version(interactive=True)
            print(moduleDescription)

        return(format(str(__doc__)+moduleDescription))
        


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-Info  ::  g_iicmChars -- IICM Characteristic Definitions (Grouped/CmndParts)   [[elisp:(org-cycle)][| ]]
"""

def g_iicmChars():
    iicmInfo['panel'] = "G_myName}-Panel.org"
    iicmInfo['groupingType'] = "IimGroupingType-pkged"
    iicmInfo['cmndParts'] = "IimCmndParts[common] IimCmndParts[param]"

g_iicmChars()
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-Func  ::  g_iicmPreIifs Hook  [[elisp:(org-cycle)][| ]]
"""

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def g_iicmPreIifs():
    #print "PREHOOK"
    pass
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-Func  ::  g_iicmPostIifs Hook   [[elisp:(org-cycle)][| ]]
"""

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def g_iicmPostIifs():
    #print "POSTHOOK"    
    pass

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Options, Arguments and Examples Specifications*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =ArgsSpec=   ::  g_argsExtraSpecify    [[elisp:(org-cycle)][| ]]
"""
# Do not decorate with @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def g_argsExtraSpecify(parser):
    """Module Specific Command Line Parameters.
    g_argsExtraSpecify is passed to G_main and is executed before argsSetup (can not be decorated)
    """
    G = icm.IicmGlobalContext()
    iicmParams = icm.IIM_ParamDict()

    #enabledMailAcct = marmeAcctsLib.enabledMailAcctObtain()

    marmeAcctsLib.commonParamsSpecify(iicmParams)

    iicmParams.parDictAdd(
        parName='moduleVersion',
        parDescription="Module Version",
        parDataType=None,
        parDefault=None,
        parChoices=list(),
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--version',
    )

    iicmParams.parDictAdd(
        parName='inFile',
        parDescription="Input File",
        parDataType=None,
        # ../control/outMail/common/template/bynameUtf8.mail
        parDefault=os.path.join(
            marmeAcctsLib.outMailCommonDirGet(),
            "template/bynameUtf8.mail"
        ),            
        parChoices=["someFile", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--inFile',
        )
    
    iicmParams.parDictAdd(
        parName='fromLine',
        parDescription="From Line",
        parDataType=None,
        parDefault="someFrom@example.com",
        parChoices=["from@example.com", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--fromLine',
        )
    
    iicmParams.parDictAdd(
        parName='toLine',
        parDescription="To Line",
        parDataType=None,
        parDefault="someTo@example.com",
        parChoices=["to@example.com", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--toLine',
        )
    
       
    icm.argsparseBasedOnIimParams(parser, iicmParams)

    # So that it can be processed later as well.
    G.iimParamDictSet(iicmParams)
    
    return


####+BEGINNOT: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/G_examplesIim.top.py"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  examples    [[elisp:(org-cycle)][| ]]
"""
####+END:
class examples(icm.Iif):
    """Framework compliant examples IIF."""

    iifArgsLen={'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par ""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {}
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
####+END:

        icm.ex_gCommon()

        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  General Dev and Testing IIFs [[elisp:(org-cycle)][| ]]
"""
        icm.iifExampleMenuChapter('*General Dev and Testing IIFs*')   

        cmndName = "unitTest" ; cmndArgs = "" ; cps = collections.OrderedDict()        
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        
        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  Default Mail From Complete File [[elisp:(org-cycle)][| ]]
"""
        icm.iifExampleMenuChapter("""*Mail From Complete File -- Default ControlProfile={controlProfile} Acct={mailAcct}*""".format(
                controlProfile=marmeAcctsLib.enabledControlProfileObtain(), mailAcct=marmeAcctsLib.enabledMailAcctObtain(),))

        cmndName = "sendCompleteMessage" ; cmndArgs = "" ;

        icm.iifExampleMenuSection("""*Mail File fromValid/toValid -- Default ControlProfile={controlProfile} Acct={mailAcct}*""".format(
                controlProfile=marmeAcctsLib.enabledControlProfileObtain(), mailAcct=marmeAcctsLib.enabledMailAcctObtain(),))

        inFileExample = '''{fileName}'''.format(
            fileName=os.path.join(marmeAcctsLib.outMailCommonDirGet(),
                                  "template/plain/fromValid/toValid/default.mail"))

        cps = collections.OrderedDict() ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        cps = collections.OrderedDict() ; cps['runMode'] = "runDebug" ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

        cps = collections.OrderedDict() ; cps['runMode'] = "runDebug" ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='little')

        cps = collections.OrderedDict() ; cps['runMode'] = "dryRun" ; cps['inFile'] = inFileExample 
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

        icm.iifExampleMenuSection("""*Mail File fromValid/toBad -- Default ControlProfile={controlProfile} Acct={mailAcct}*""".format(
                controlProfile=marmeAcctsLib.enabledControlProfileObtain(), mailAcct=marmeAcctsLib.enabledMailAcctObtain(),))

        inFileExample = '''{fileName}'''.format(
            fileName=os.path.join(marmeAcctsLib.outMailCommonDirGet(),
                                  "template/plain/fromValid/toBad/default.mail"))

        cps = collections.OrderedDict() ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        cps = collections.OrderedDict() ; cps['runMode'] = "runDebug" ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

        cps = collections.OrderedDict() ; cps['runMode'] = "runDebug" ; cps['inFile'] = inFileExample
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='little')

        cps = collections.OrderedDict() ; cps['runMode'] = "dryRun" ; cps['inFile'] = inFileExample 
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
        
        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  Mail From Partial File -- Qmail Inject [[elisp:(org-cycle)][| ]]
"""
        
        icm.iifExampleMenuChapter('*Mail From Partial File -- Qmail Inject*')

        inFileExample = '''{fileName}'''.format(
            fileName=os.path.join(
                marmeAcctsLib.outMailCommonDirGet(),
                "template/bynameUtf8.mail"
            ))

        cmndName = "sendFromPartialFileWithPars" ; cmndArgs = "" ; cps = collections.OrderedDict()        
        cps['submissionMethod'] = "inject" ; cps['inFile'] = inFileExample
        cps['runMode']="dryRun"
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  Basic Mail Sending  [[elisp:(org-cycle)][| ]]
"""
        
        
        icm.iifExampleMenuChapter('*Basic Mail Sending*')

        cmndName = "msgSend_basic" ; cmndArgs = "" ; cps = collections.OrderedDict()        
        cps['fromLine']="office@mohsen.1.banan.byname.net" ; cps['toLine']="test@mohsen.banan.1.byname.net"
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        cmndName = "msgSend_basic" ; cmndArgs = "" ; cps = collections.OrderedDict()
        cps['verbosity']="20" ; cps['runMode']="runDebug"        
        cps['fromLine']="office@mohsen.1.banan.byname.net" ; cps['toLine']="test@mohsen.banan.1.byname.net"
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        cmndName = "msgSend_basic" ; cmndArgs = "" ; cps = collections.OrderedDict()
        cps['verbosity']="20" ; cps['runMode']="dryRun"        
        cps['fromLine']="office@mohsen.1.banan.byname.net" ; cps['toLine']="test@mohsen.banan.1.byname.net"
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')
        

        cmndName = "msgSend_tracked" ; cmndArgs = "" ; cps = collections.OrderedDict()        
        cps['fromLine']="office@mohsen.1.banan.byname.net" ; cps['toLine']="test@mohsen.banan.1.byname.net"
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

        
        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  From  marmeAcctsLib.py   [[elisp:(org-cycle)][| ]]
"""

        marmeAcctsLib.examples_marmeAcctsLibControls()
   
        marmeAcctsLib.examples_outMailAcctAccessPars()
        
        return(iifOutcome)

    
####+BEGIN: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/G_examples.bottom.py"
    # Intentionally Left Blank -- previously: lhip.G_devExamples(G_myName)

####+END:

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Specific Interactively Invokable Functions (IICM-IIF)*
"""

"""
*  [[elisp:(org-show-subtree)][=|=]] [[elisp:(org-cycle)][| ]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] || Class-IIF         ::  unitTest    [[elisp:(org-cycle)][| ]]
"""
class unitTest(icm.Iif):
    """
** Place holder for IICM's experimental or test code. 
    """
    iifArgsLen = {'Min': 0, 'Max': 0,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """Use this IIF for rapid prototyping and testing of newly developed functions.

** TODO Needs to be added to examples.
"""
        
        myName=self.myName()
        #G = icm.IicmGlobalContext()        
        thisOutcome = icm.OpOutcome(invokerName=myName)

        print (icm.__file__)
        print sys.path

        import imp
        print(imp.find_module('iicm'))

        @ucf.runOnceOnly
        def echo(str):
            print str
            
        echo("first")
        echo("second")  # Should not run

        # Install the import hook.
        #from macros import custom_loop
        #with custom_loop(10):
        #   print "I'm looping!"

        SomeEnum = icm.Enum(
            inject='injectZZ',
            submit='submit',
        )

        print SomeEnum.inject

        return


        print msgOut.InjectionMethod.inject

        print eval("msgOut.InjectionMethod.inject")

        print vars(msgOut.InjectionMethod)

        print msgOut.enumFromStrWhenValid("InjectionMethod", msgOut.InjectionMethod.submit)

        orderedDict2 =icm.oDict(arg1="value1", arg2="value2")

        print orderedDict2

        print orderedDict2['arg1']

        SomeEnum = icm.Enum(
            inject='inject',
            submit='submit',
        )

        print SomeEnum.inject
        
        #global add
        return thisOutcome
        #print(type(add))
        #add(1,2)
        #return 

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Support Functions For MsgProcs*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  sendFromPartialFileWithPars    [[elisp:(org-cycle)][| ]]
"""
class sendFromPartialFileWithPars(icm.Iif):
    """
** Submit a message using inFile and pars: outMailAcct, submissionMethod. 
** Augment with delivery/non-delivery requests and track.
"""
    
    iifParamsMandatory = []
    iifParamsOptional = ['outMailAcct', 'inFile', 'submissionMethod']        
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "outMailAcct inFile sendingMethod" :asFunc "msg"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        outMailAcct=None,         # or Cmnd-Input
        inFile=None,         # or Cmnd-Input
        sendingMethod=None,         # or Cmnd-Input
        msg=None,         # asFunc when interactive==False
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'outMailAcct': outMailAcct, 'inFile': inFile, 'sendingMethod': sendingMethod, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        outMailAcct = callParamsDict['outMailAcct']
        inFile = callParamsDict['inFile']
        sendingMethod = callParamsDict['sendingMethod']
####+END:
        
        G = icm.IicmGlobalContext()

        if not msg:
            if inFile:
                msg = msgIn.getMsgFromFile(inFile)
            else:
                # Stdin then
                msg = msgIn.getMsgFromStdin()

        icm.LOG_here(msgOut.strLogMessage(
            "Msg As Input:", msg,))

        if not sendingMethod:
            sendingMethod = msgOut.SendingMethod.submit
        if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
            return msgOut.sendingMethodSet(msg, sendingMethod)

        print G.usageParams.runMode
        
        if msgOut.sendingRunControlSet(msg, G.usageParams.runMode).isProblematic():
            return msgOut.sendingRunControlSet(msg, G.usageParams.runMode)
        

        envelopeAddr = msg['From']
        recipientsList = msg['To']
        
        msgOut.envelopeAddrSet(
            msg,
            mailBoxAddr=envelopeAddr,  # Mandatory
        )

        msgOut.crossRefInfo(
            msg,
            crossRefInfo="XrefForStatusNotifications"  # Mandatory
        )
        msgOut.nonDeliveryNotificationRequetsForTo(
            msg,
            recipientsList=recipientsList,        
            notifyTo=envelopeAddr,
        )
        msgOut.nonDeliveryNotificationActions(
            msg,
            coRecipientsList=recipientsList,
        )
        msgOut.deliveryNotificationRequetsForTo(
            msg,
            recipientsList=recipientsList,
            notifyTo=envelopeAddr,
        )
        msgOut.dispositionNotificationRequetsForTo(
            msg,
            recipientsList=recipientsList,
            notifyTo=envelopeAddr,
        )

        if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
            return icm.EH_badLastOutcome()
            
        if not marmeSendLib.bx822Set_sendWithEnabledAcct(msg, sendingMethod):
            return icm.EH_badOutcome(iifOutcome)

        iifOutcome = marmeSendLib.sendCompleteMessage().iif(
            interactive=False,
            msg=msg,
        )

        return iifOutcome


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  msgSend_basic    [[elisp:(org-cycle)][| ]]
"""
class msgSend_basic(icm.Iif):
    """
** Send a very basic simple message sendCompleteMessage().iif(msg)
"""

    iifParamsMandatory = ['fromLine', 'toLine']
    iifParamsOptional = ['sendingMethod']      
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "fromLine toLine sendingMethod"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        fromLine=None,         # or Cmnd-Input
        toLine=None,         # or Cmnd-Input
        # sendingMethod=msgOut.SendingMethod.inject,         # or Cmnd-Input
        sendingMethod=None,
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'fromLine': fromLine, 'toLine': toLine, 'sendingMethod': sendingMethod, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        fromLine = callParamsDict['fromLine']
        toLine = callParamsDict['toLine']
        sendingMethod = callParamsDict['sendingMethod']
####+END:

        if not sendingMethod:
            sendingMethod = msgOut.SendingMethod.submit

        msg = MIMEMultipart()

        msg['From'] = fromLine
        msg['To'] = toLine

        msg['Subject'] = """Example Of A Simple And Untracked Message"""

        msg.preamble = 'Multipart massage.\n'

        part = MIMEText(
            """ 
This is a simple example message with a simple attachment
being sent using the current enabled controlledProfile and mailAcct.

On the sending end, use mailAcctsManage.py with 
-i enabledControlProfileSet and -i enabledMailAcctSet
to select the outgoing profile. The current settings are:
    ControlProfile={controlProfile}  -- MailAcct={mailAcct}

This message is then submitted for sending with sendCompleteMessage().iif(msg)

Please find example of an attached file\n
            """.format(
                controlProfile=marmeAcctsLib.enabledControlProfileObtain(),
                mailAcct=marmeAcctsLib.enabledMailAcctObtain()
            )
        )
        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("/etc/resolv.conf", "rb").read())
        Encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="/etc/resolv.conf"')

        msg.attach(part)

        if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
            return icm.EH_badLastOutcome()
            
        if not marmeSendLib.bx822Set_sendWithEnabledAcct(msg, sendingMethod):
            return icm.EH_badOutcome(iifOutcome)

        iifOutcome = marmeSendLib.sendCompleteMessage().iif(
            
            interactive=False,
            msg=msg,
        )
        
        return iifOutcome

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  msgSend_tracked    [[elisp:(org-cycle)][| ]]
"""
class msgSend_tracked(icm.Iif):
    """
** Send a very basic simple message sendCompleteMessage().iif(msg)
"""

    iifParamsMandatory = ['fromLine', 'toLine']
    iifParamsOptional = ['sendingMethod']      
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "fromLine toLine sendingMethod"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        fromLine=None,         # or Cmnd-Input
        toLine=None,         # or Cmnd-Input
        # sendingMethod=msgOut.SendingMethod.inject,         # or Cmnd-Input
        sendingMethod=None,
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'fromLine': fromLine, 'toLine': toLine, 'sendingMethod': sendingMethod, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        fromLine = callParamsDict['fromLine']
        toLine = callParamsDict['toLine']
        sendingMethod = callParamsDict['sendingMethod']
####+END:
        #G = icm.IicmGlobalContext()

        if not sendingMethod:
            sendingMethod = msgOut.SendingMethod.submit

        msg = email.message.Message()  #msg = MIMEText() # MIMEMultipart() 

        msg['From'] = fromLine
        msg['To'] = toLine

        msg['Subject'] = """Example Of A Simple And Tracked Message"""

        envelopeAddr = fromLine

        if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
            return msgOut.sendingMethodSet(msg, sendingMethod)
        
        msg.add_header('Content-Type', 'text')
        msg.set_payload(
            """ 
This is a simple example message with a simple attachment
being sent using the current enabled controlledProfile and mailAcct.

On the sending end, use mailAcctsManage.py with 
-i enabledControlProfileSet and -i enabledMailAcctSet
to select the outgoing profile. The current settings are:
    ControlProfile={controlProfile}  -- MailAcct={mailAcct}

This message is then submitted for sending with sendCompleteMessage().iif(msg)

            """.format(
                controlProfile=marmeAcctsLib.enabledControlProfileObtain(),
                mailAcct=marmeAcctsLib.enabledMailAcctObtain()
            )
        )


        #
        ###########################
        #
        # Above is the real content of the email.
        #
        # We now augment the message with:
        #   - explicit envelope address -- To be used for Delivery-Status-Notifications (DSN)
        #   - The email is be tagged for crossReferencing when DSN is received (e.g. with peepid)    
        #   - Request that non-delivery-reports be acted upon and sent to co-recipients
        #   - Explicit delivery-reports are requested
        #   - Explicit read-receipts are requested
        #   - Injection/Submission parameters are specified
        # The message is then sent out
        #

        msgOut.envelopeAddrSet(
            msg,
            mailBoxAddr=envelopeAddr,  # Mandatory
        )

        #
        # peepId will be used to crossRef StatusNotifications
        #
        msgOut.crossRefInfo(
            msg,
            crossRefInfo="XrefForStatusNotifications"  # Mandatory
        )

        #
        # Delivery Status Notifications will be sent to notifyTo=envelopeAddr
        #
        msgOut.nonDeliveryNotificationRequetsForTo(
            msg,
            notifyTo=envelopeAddr,
        )

        #
        # In case of Non-Delivery, coRecipientsList will be informed
        #
        msgOut.nonDeliveryNotificationActions(
            msg,
            coRecipientsList=[toLine],        
        )

        #
        # Explicit Delivery Report is requested
        #
        msgOut.deliveryNotificationRequetsForTo(
            msg,
            recipientsList=[toLine],
            notifyTo=envelopeAddr,
        )

        #
        # Explicit Read Receipt is requested
        #    
        msgOut.dispositionNotificationRequetsForTo(
            msg,
            recipientsList=[toLine],        
            notifyTo=envelopeAddr,
        )

        if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
            return icm.EH_badLastOutcome()
            
        if not marmeSendLib.bx822Set_sendWithEnabledAcct(msg, sendingMethod):
            return icm.EH_badOutcome(iifOutcome)

        iifOutcome = marmeSendLib.sendCompleteMessage().iif(
            
            interactive=False,
            msg=msg,
        )
        
        return


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *G_main -- Instead Of IICM-IIF Dispatcher-Example*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  G_main -- icm.argsparse bypass  [[elisp:(org-cycle)][| ]]
"""

def G_main():
    """ For use instead of IIF dispatcher. Unused unless examples is None."""
    print sys.argv
    #argc = len(sys.argv)
    return



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Framework Model Selection And Entry --*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Configure    ::  g_ iicm Mode Specification    [[elisp:(org-cycle)][| ]]
"""

g_examples = examples     # or None -- When None, G_main is invoked
g_mainEntry = G_main      # or None -- Unused unless examples is None
g_importedIifs = {        # Enumerate modules from which IIFs become invokable
   'marmeAcctsLib': marmeAcctsLib.__file__,
   'marmeSendLib': marmeSendLib.__file__,    
}


"""
#*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Python Main*
"""

####+BEGINNOT: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/icm.G_main.py"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || /Dblk-Begin/ ::  g_iicmMain Func  (Python Main)   [[elisp:(org-cycle)][| ]]
"""

def classedIifsDict():
    """Should be done here, can not be done in iicm library."""
    callDict = dict()
    for eachIif in icm.iifList_mainsMethods().iif(
            interactive=False,
            importedIifs=g_importedIifs,
    ):
        try:
            callDict[eachIif] = eval("{}".format(eachIif))
            continue
        except NameError:
            pass
        
        for mod in g_importedIifs:
            try:
                eval("{mod}.{iif}".format(mod=mod, iif=eachIif))
            except AttributeError:
                continue
            try:                
                callDict[eachIif] = eval("{mod}.{iif}".format(mod=mod, iif=eachIif))
                break
            except NameError:
                pass
    return callDict


def funcedIifsDict():
    """Should be done here, can not be done iicm library."""
    callDict = dict()
    for eachIif in icm.iifList_mainsFuncs().iif(interactive=False):
        try:
            callDict[eachIif] = eval("{eachIif}".format(eachIif=eachIif))
        except NameError:
            pass
    return callDict

iicmInfo['iicmName'] = __iicmName__
iicmInfo['version'] = __version__
iicmInfo['status'] = __status__
iicmInfo['credits'] = __credits__
# NOTYET, pass along iicmInfo

def g_iicmMain():
    """This IICM's specific information is passed to G_mainWithClass"""
    sys.exit(
        icm.G_mainWithClass(
            inArgv=sys.argv[1:],                 # Mandatory
            extraArgs=g_argsExtraSpecify,        # Mandatory
            G_examples=g_examples,               # Mandatory            
            classedIifsDict=classedIifsDict(),   # Mandatory
            funcedIifsDict=funcedIifsDict(),     # Mandatory
            mainEntry=g_mainEntry,
        )
    )

g_iicmMain()

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || /Dblk-End/   ::   [[elisp:(org-cycle)][| ]]
"""
####+END:

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Unused Facilities -- Temporary Junk Yard*
"""

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *End Of Editable Text*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [COMMON]      :: /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
"""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall

####+END:

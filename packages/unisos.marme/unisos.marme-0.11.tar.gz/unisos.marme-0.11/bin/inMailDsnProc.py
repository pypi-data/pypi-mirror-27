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
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  insertPathForImports    [[elisp:(org-cycle)][| ]]
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

import iicm

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "ucf" :file "ucf"
# Development Workaround  For JediWorkaround
import ucf
####+END:

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "icm" :file "icm"
# External Usage
from unisos.icm import icm
####+END:

from bxMsg import msgOut
#from bxMsg import msgIn
#from bxMsg import msgLib


import marmeAcctsLib
import marmeSendLib
import marmeTrackingLib

import re

import email
import mailbox

import flufl.bounce

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase

import collections

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Framework IIFs*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  describe    [[elisp:(org-cycle)][| ]]
"""
class describe(icm.Iif):
    """IICM basic description."""

    iifArgsLen={'Min': 0, 'Max': 0,}
    
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
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-Func  ::  g_iicmPreIifs    [[elisp:(org-cycle)][| ]]
"""

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def g_iicmPreIifs():
    #print "PREHOOK"
    pass
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-Func  ::  g_iicmPostIifs    [[elisp:(org-cycle)][| ]]
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
        parDefault=None,
        parChoices=["someFile", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--inFile',
        )
    
       
    icm.argsparseBasedOnIimParams(parser, iicmParams)

    # So that it can be processed later as well.
    G.iimParamDictSet(iicmParams)
    
    return


####+BEGINNOT: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/G_examplesIim.top.py"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || FrmWrk-IIF   ::  examples    [[elisp:(org-shifttab 2))][|=]] [[elisp:(org-cycle)][| ]]
"""
####+END:
class examples(icm.Iif):
    """Framework compliant examples IIF."""

    iifArgsLen={'Min': 1, 'Max':2,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
            firstArg=None,            # iifArgs[0]
    ):
        """iif of SomeIif function longer docString."""
        myName=self.myName()
        #G = icm.IicmGlobalContext()        
        thisOutcome = icm.OpOutcome(invokerName=myName)

        #defaultMailDom = marmeAcctsLib.defaultMailDomGet()
        
        G_myFullName = sys.argv[0]
        G_myName = os.path.basename(G_myFullName)
        icm.iimExampleMyName(G_myName, os.path.abspath(G_myFullName))
        icm.G_commonBriefExamples()    
        #iim.G_commonExamples()
        #g_curFuncName = iim.FUNC_currentGet().__name__
        logControler = icm.LOG_Control()
        logControler.loggerSetLevel(20)

        #iifThis = icm.FUNC_currentGet().__name__

        logControler = icm.LOG_Control()
        logControler.loggerSetLevel(20)

        #verboseDebug = " -v  1"
        #verboseWarning = " -v 30"        
        #verboseError = " -v 30"
        
        #enabledControlProfile = marmeAcctsLib.enabledControlProfileObtain()
        #enabledMailAcct = marmeAcctsLib.enabledMailAcctObtain()        
        #inMailAcct = enabledMailAcct
        #inMboxStatic="Inbox"
        #inMbox = marmeAcctsLib.enabledMailBoxObtain()

        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  General Dev and Testing IIFs    [[elisp:(org-cycle)][| ]]
"""
        
        icm.iifExampleMenuChapter('*General Dev and Testing IIFs*')   

        iifAction = " -i unitTest" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
        icm.iifExampleMenuItem(menuLine, verbosity='full')

        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  Real Invokations --    [[elisp:(org-cycle)][| ]]
"""

        icm.iifExampleMenuChapter('*Real Invokations*')

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnProcessAndRefile"
        cps = collections.OrderedDict() # ; cps['runMode'] = 'dryRun' COMMENTED-OUT
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')

        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='full')        

        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  Testing -- /DryRun/ -- devTest -- Maildir Apply To Message Processor  [[elisp:(org-cycle)][| ]]
"""
        
        icm.iifExampleMenuChapter('*Testing -- /DryRun/ -- devTest -- Maildir Apply To Message Processor*')

        # menuLine = """--runMode dryRun --inMailAcct={inMailAcct} --inMbox={inMbox} {iifAction} {iifArgs}""".format(
        #    inMailAcct=inMailAcct, inMbox=inMbox, iifAction=iifAction, iifArgs=iifArgs)

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "msgDisect"
        cps = collections.OrderedDict() ; #cps['controlProfile'] = enabledControlProfile ; cps['inMailAcct'] = enabledMailAcct
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnReportLong"
        cps = collections.OrderedDict() ; #cps['controlProfile'] = enabledControlProfile ; cps['inMailAcct'] = enabledMailAcct
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnProcessAndRefile"
        cps = collections.OrderedDict() ; cps['runMode'] = 'dryRun'
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')
        
        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnTestSendToCoRecipients"
        cps = collections.OrderedDict() ; cps['runMode'] = 'dryRun'
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnTestSendToCoRecipients"
        cps = collections.OrderedDict() ; cps['runMode'] = 'runDebug'
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')

        cmndName = "maildirApplyToMsg"        
        cmndArgs = "dsnTestSendToCoRecipients"
        cps = collections.OrderedDict() ; cps['runMode'] = 'fullRun'
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper=None, verbosity='little')
        
        
        """
**  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Examples   ::  From  marmeAcctsLib.py   [[elisp:(org-cycle)][| ]]
"""
        

        marmeAcctsLib.examples_controlProfileManage()

        marmeAcctsLib.examples_marmeAcctsLibControls()

        marmeAcctsLib.examples_select_mailBox()        

        marmeAcctsLib.examples_inMailAcctAccessPars()

        marmeAcctsLib.examples_outMailAcctAccessPars()        
        
        
        return(thisOutcome)

    
####+BEGIN: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/G_examples.bottom.py"
    # Intentionally Left Blank -- previously: lhip.G_devExamples(G_myName)

####+END:

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Specific Interactively Invokable Functions (IICM-IIF)*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  unitTest    [[elisp:(org-cycle)][| ]]
"""
class unitTest(icm.Iif):
    """Place holder for IICM's experimental or test code. """

    iifArgsLen = {'Min': 0, 'Max':0,}
    
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
    
        return thisOutcome

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  maildirApplyToMsg    [[elisp:(org-cycle)][| ]]
"""
class maildirApplyToMsg(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct', 'inMbox']       
    iifArgsLen = {'Min': 1, 'Max':1000,}
    iifArgsSpec = {0: ['msgDisect', 'coRecepientNdr']}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def argsSpec(self):
        """ """
        # iifArgs = iicm.IIF_args()

        # iifArgObj = iifArgs.obtainObj(
        #     argName='inMsgProcessor',
        #     argObjType='Any',
        #     argDescription="A function that accepts an inMsg and processes it.",
        #     argDataType=None,
        #     argDefault=None,
        #     argChoices=list(),
        # ).append(iifArgs)

        # iifArgs.append(iifArgObj)

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct inMbox"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
        inMbox=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, 'inMbox': inMbox, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
        inMbox = callParamsDict['inMbox']
####+END:

        G = icm.IicmGlobalContext()

        
        inMailDir = marmeAcctsLib.getPathForAcctMbox(controlProfile, inMailAcct, inMbox)

        icm.LOG_here(inMailDir)

        mbox = mailbox.Maildir(
            inMailDir,
            factory=None,  # important!! default does not work
        )

        iimRunArgs = G.iimRunArgsGet()
        for msgProc in iimRunArgs.iifArgs:
            #iim.ANN_here("thisArg={thisArg}".format(thisArg=msgProc))

            #for msg in mbox:
            for key in mbox.iterkeys():
                try:
                    msg = mbox[key]
                except email.errors.MessageParseError:
                    icm.EH_problem_info(msg)
                    continue                # The message is malformed. Just leave it.
          
            
                try:
                    eval(msgProc + '(inMailDir, mbox, key, msg)')
                except Exception as e:
                    icm.EH_critical_exception(e)
                    icm.EH_problem_info("Invalid Action: {msgProc}"
                                        .format(msgProc=msgProc))            
                    raise   # NOTYET, in production, the raise should be commented out
        
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Apply    ::  msgDisect    [[elisp:(org-cycle)][| ]]
"""

@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def msgDisect(
        maildir,
        mbox,
        key,
        inMsg,
):
    """ """
    for part in inMsg.walk():
        print part.get_content_type()

    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Apply    ::  dsnReportLong    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnReportLong(
        maildir,        
        mbox,
        key,
        inMsg,
):
    """ """
    tempFailedRecipients, permFailedRecipients = flufl.bounce.all_failures(inMsg)

    failedMsg = fromNonDeliveryReportGetFailedMsg(
        inMsg,
        tempFailedRecipients,
        permFailedRecipients,
    )

    coRecipients = fromFailedMsgGetCoRecipients(
        failedMsg,
        tempFailedRecipients,
        permFailedRecipients,
    )

    dsnType = msgDsnTypeDetect(
        inMsg,
        failedMsg,
        tempFailedRecipients,
        permFailedRecipients,
        coRecipients,
    )

    dsnTypeReports(inMsg, dsnType, "long")

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Apply    ::  dsnTestSendToCoRecipients    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnTestSendToCoRecipients(
        maildir,        
        mbox,
        key,
        inMsg,
):
    """ 
** inMsg is analyzed to see if it contains a bounce. based on that it is catgorized as one of the following:
"""
    dsnProcessAndRefileWithGivenActions(
        maildir,        
        mbox,
        key,
        inMsg,
        action_deliveryReport=None,
        action_receiptNotification=None,
        action_ndrNoCoRecipients=None,
        action_ndrWithCoRecipients=msgSend_test_permanentNdrToCoRecipients,
        action_tmpNonDeliveryReport=None,
        action_notADsn=None,
    )
      


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Apply    ::  dsnProcessAndRefile    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnProcessAndRefile(
    maildir,        
    mbox,
    key,
    inMsg,
):
    """ 
** inMsg is analyzed to see if it contains a bounce. based on that it is catgorized as one of the following:
"""
    dsnProcessAndRefileWithGivenActions(
        maildir,        
        mbox,
        key,
        inMsg,
        action_deliveryReport=None,
        action_receiptNotification=None,
        action_ndrNoCoRecipients=None,
        action_ndrWithCoRecipients=msgSend_test_permanentNdrToCoRecipients,
        action_tmpNonDeliveryReport=None,
        action_notADsn=None,
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  dsnProcessAndRefileWithGivenActions    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnProcessAndRefileWithGivenActions(
        maildir,        
        mbox,
        key,
        inMsg,
        action_deliveryReport=None,
        action_receiptNotification=None,
        action_ndrNoCoRecipients=None,
        action_ndrWithCoRecipients=None,
        action_tmpNonDeliveryReport=None,
        action_notADsn=None,
):
    """ 
** inMsg is analyzed to see if it contains a bounce. based on that it is catgorized as one of the following:
*** envNotADsn: If it is not a Delivery Status Notification (DSN) it is filed 
*** envTmpNdr:  A temporary Non-Delivery Report (NDR)
*** envNdrNoCoRecip:  A permanent Non-Delivery Report without any co-recipients
*** envNdrWithCoRecipNotified: A permanent NDR with co-recipients that were notified
*** envNdrWithCoRecip: A permanent NDR with co-recipients that were not notified
*** envDr:  A Delivery Report
*** envRn: A Recipt Notification
"""
    G = icm.IicmGlobalContext()
    runMode = G.iimRunArgsGet().runMode
    
    tempFailedRecipients, permFailedRecipients = flufl.bounce.all_failures(inMsg)

    failedMsg = fromNonDeliveryReportGetFailedMsg(
        inMsg,
        tempFailedRecipients,
        permFailedRecipients,
    )

    coRecipients = fromFailedMsgGetCoRecipients(
        failedMsg,
        tempFailedRecipients,
        permFailedRecipients,
    )

    dsnType = msgDsnTypeDetect(
        inMsg,
        failedMsg,
        tempFailedRecipients,
        permFailedRecipients,
        coRecipients,
    )

    dsnTypeReports(inMsg, dsnType, "short")

    
    if dsnType == DsnType.deliveryReport:
        if action_deliveryReport:
            action_deliveryReport(
                inMsg,
                failedMsg,
                tempFailedRecipients,
                permFailedRecipients,
                coRecipients,
                dsnType,
            )
      
    elif dsnType == DsnType.receiptNotification:
        if action_receiptNotification:
            action_receiptNotification(
                inMsg,
                failedMsg,
                tempFailedRecipients,
                permFailedRecipients,
                coRecipients,
                dsnType,
            )
    
    elif dsnType == DsnType.ndrNoCoRecipients:
        if runMode == 'dryRun':
            pass
        elif runMode == 'runDebug':
            pass
        elif  runMode == 'fullRun':
            if action_ndrNoCoRecipients:
                action_ndrNoCoRecipients(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )

            msgMoveToFolder("envNdrNoCoRecip", maildir, mbox, key, inMsg,)
            marmeTrackingLib.trackEnvPermNdr(inMsg)
        else:
            icm.EH_critical_oops()

        
    elif dsnType == DsnType.ndrWithCoRecipients:
        if runMode == 'dryRun':
            pass
        elif runMode == 'runDebug':
            if action_ndrWithCoRecipients:
                action_ndrWithCoRecipients(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
        elif  runMode == 'fullRun':
            if action_ndrWithCoRecipients:
                action_ndrWithCoRecipients(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
            msgMoveToFolder("envNdrWithCoRecipNotified", maildir, mbox, key, inMsg,)            
            marmeTrackingLib.trackSentCoRecipient(inMsg)

        else:
            icm.EH_critical_oops()

    elif dsnType == DsnType.tmpNonDeliveryReport:
        if runMode == 'dryRun':
            pass
        elif runMode == 'runDebug':
            if action_tmpNonDeliveryReport:
                action_tmpNonDeliveryReport(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
        elif  runMode == 'fullRun':
            if action_tmpNonDeliveryReport:
                action_tmpNonDeliveryReport(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
            msgMoveToFolder("envTmpNdr", maildir, mbox, key, inMsg,)
            marmeTrackingLib.trackEnvTmpNdr(inMsg)

        else:
            icm.EH_critical_oops()
            
        
    elif dsnType == DsnType.notADsn:
        if runMode == 'dryRun':
            pass
        elif runMode == 'runDebug':
            if action_notADsn:
                action_notADsn(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
        elif  runMode == 'fullRun':
            if action_notADsn:
                action_notADsn(
                    inMsg,
                    failedMsg,
                    tempFailedRecipients,
                    permFailedRecipients,
                    coRecipients,
                    dsnType,
                )
            msgMoveToFolder("envNotADsn", maildir, mbox, key, inMsg,)

    else:
        icm.EH_critical_oops()
        


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *DSN (Delivery Status Notification) Type Processors*
"""
        

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Enum         ::  DsnType    [[elisp:(org-cycle)][| ]]
"""
DsnType = icm.Enum(
    deliveryReport='deliveryReport',
    receiptNotification='receiptNotification',
    ndrNoCoRecipients='ndrNoCoRecipients',
    ndrWithCoRecipients='ndrWithCoRecipients',
    tmpNonDeliveryReport='tmpNonDeliveryReport',
    notADsn='notADsn',
)


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  msgDsnTypeDetect    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def msgDsnTypeDetect(
    inMsg,
    failedMsg,
    tempFailedRecipients,
    permFailedRecipients,
    coRecipients,        
):        
    """ 
** Returns a DsnType.
"""
    if tempFailedRecipients:
        return DsnType.tmpNonDeliveryReport
 
    elif permFailedRecipients:
        if coRecipients:
            return DsnType.ndrWithCoRecipients
        else:
            return DsnType.ndrNoCoRecipients

    # Delivery Report Needs To Be Detected

    # Receipt Notification Needs To Be Detected
    
    elif inMsg['subject'] == "Delivery delay notification":
        return DsnType.tmpNonDeliveryReport
        
    else:
        return DsnType.notADsn

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  dsnTypeShortReport    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnTypeShortReport(
        inMsg,
        typeStr,
):
    icm.ANN_note("""{typeStr:15}:: {msgId}""".format(
        typeStr=typeStr, msgId=str(inMsg['message-id']),))

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  dsnTypeLongReport    [[elisp:(org-cycle)][| ]]
"""    
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnTypeLongReport(
        inMsg,
        typeStr,
):
    icm.ANN_note("""{typeStr:20}:: {msgId} -- {date} -- {subject}""".format(
        typeStr=typeStr, msgId=str(inMsg['message-id']),
        date=str(inMsg['date']), subject=str(inMsg['subject']),
        ))
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  dsnTypeReports    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def dsnTypeReports(
    inMsg,
    dsnType,
    reportType,
):

    def dsnTypeStrReport(
            inMsg,
            typeStr,
            reportType,
    ):
        if reportType == "short":
            dsnTypeShortReport(inMsg, typeStr,)
        elif reportType == "long":
            dsnTypeLongReport(inMsg, typeStr,)
        else:
            icm.EH_critical_oops()

    if dsnType == DsnType.deliveryReport:
        dsnTypeStrReport(inMsg, "Delivery Report", reportType,)
        
    elif dsnType == DsnType.receiptNotification:
        dsnTypeStrReport(inMsg, "Receipt Notification", reportType,)
    
    elif dsnType == DsnType.ndrNoCoRecipients:
        dsnTypeStrReport(inMsg, "ndrNoCoRecipients", reportType,)

    elif dsnType == DsnType.ndrWithCoRecipients:
        dsnTypeStrReport(inMsg, "ndrWithCoRecipients", reportType,)
 
    elif dsnType == DsnType.tmpNonDeliveryReport:
        dsnTypeStrReport(inMsg, "tmpNonDeliveryReport", reportType,)        

    elif dsnType == DsnType.notADsn:
        dsnTypeStrReport(inMsg, "Not A DSN", reportType,)        

    else:
        icm.EH_critical_oops()



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Support Functions For MsgProcs*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  fromNonDeliveryReportGetFailedMsg    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def fromNonDeliveryReportGetFailedMsg(
    nonDeliveryReportMsg,        
    tempFailedRecipients,
    permFailedRecipients,
):
    """ 
** returns the extracted failed message from the non-delivery-report. Or None.
"""

    if not (tempFailedRecipients or permFailedRecipients):
        # This is NOT a nonDeliveryReport
        return None

    #
    # Get the failed message as an attachement
    # 
    for part in nonDeliveryReportMsg.walk():
        if part.get_content_type() == 'message/rfc822':
            failedMsgList = part.get_payload()
            if failedMsgList:
                #for failedMsg in failedMsgList:
                nuOfFailedMsgs = len(failedMsgList)
                if nuOfFailedMsgs != 1:
                    icm.EH_problem_info("More Then One -- Expected One")
                    return None
                else:
                    return failedMsgList[0]

    #
    # So,the failed message was not included and is part of the body.
    #
    
    #scre = re.compile(b'mail to the following recipients could not be delivered')
    scre = re.compile(b'-- The header and top 20 lines of the message follows --')

    msg = nonDeliveryReportMsg
    failedMsgStr = ""
    found = False
    for line in msg.get_payload(decode=True).splitlines():
        if scre.search(line):
            found = "gotIt"
            continue
        if found == "gotIt":  # This consumes an empty line
            found = True
            continue
        if found == True:
            failedMsgStr = failedMsgStr + line + '\n'

    if found:
        return email.message_from_string(failedMsgStr)
    else:
        return None

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  fromFailedMsgGetCoRecipients    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def fromFailedMsgGetCoRecipients(
    failedMsg,
    tempFailedRecipients,
    permFailedRecipients,
):
    """ 
** Return list of CoRecipients or None
"""
    if not (tempFailedRecipients or permFailedRecipients):
        # This is NOT a nonDeliveryReport
        return None

    if not failedMsg:
        icm.EH_critical_unassigedError("UnFound FailedMsg")
        return None
   
    allRecipients= None

    tos = failedMsg.get_all('to', [])
    ccs = failedMsg.get_all('cc', [])
    resent_tos = failedMsg.get_all('resent-to', [])
    resent_ccs = failedMsg.get_all('resent-cc', [])
    allRecipients = email.utils.getaddresses(tos + ccs + resent_tos + resent_ccs)
                
    if not allRecipients:
        icm.EH_problem_unassignedError("allRecipients is None")
        return None

    allRecipientsSet = set()
    for thisRecipient in allRecipients:
        allRecipientsSet.add(thisRecipient[1])

    failedRecipients = tempFailedRecipients | permFailedRecipients
        
    coRecipientsSet = allRecipientsSet - failedRecipients

    if coRecipientsSet:
        return coRecipientsSet
    else:
        return None


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Msg ReFiling*
"""
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  msgMoveToFolder    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def msgMoveToFolder(
        destFolder,
        srcMaildir,        
        srcMbox,
        srcKey,
        srcMsg,
):
    """ 
** Given a srcMbox and a srcMsg, move it to the specified  destination.
"""
    srcMailBase = os.path.dirname(srcMaildir)

    destMbox = mailbox.Maildir(
            os.path.join(srcMailBase, destFolder),
            factory=None,  # important!! default does not work
    )

    # Write copy to disk before removing original.
    # If there's a crash, you might duplicate a message, but
    # that's better than losing a message completely.
    destMbox.lock()
    destMbox.add(srcMsg)
    destMbox.flush()
    destMbox.unlock()

    # Remove original message
    srcMbox.lock()
    srcMbox.discard(srcKey)
    srcMbox.flush()
    srcMbox.unlock()

    destMbox.close()

    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Msg Sending*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Send     ::  msgSend_test_permanentNdrToCoRecepiets    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def msgSend_test_permanentNdrToCoRecipients(
    inMsg,
    failedMsg,
    tempFailedRecipients,
    permFailedRecipients,
    coRecipients,
    dsnType,
):
    """ Given a nonDeliveryReportMsg, We focus on the failedMsg
    """

    testToLine = "test@mohsen.banan.1.byname.net"


    failedRecipients = tempFailedRecipients | permFailedRecipients

    failedFromLine = failedMsg['From']
    failedSubjectLine = failedMsg['Subject']
    failedDateLine = failedMsg['date']                                              

    msg = MIMEMultipart()    

    msg['Date'] = email.utils.formatdate(localtime = 1)
    msg['Message-ID'] = email.utils.make_msgid()
    
    msg['Subject'] = """Co-Recipient Non-Delivery-Report  -- Was: {failedSubjectLine}""".format(
        failedSubjectLine=failedSubjectLine)

    msg['From'] = failedFromLine

    toLine = ""
    
    for thisRecipient in coRecipients:
        if toLine:
            toLine = toLine + ', ' + thisRecipient
        else:
            toLine = thisRecipient            

    msg['To'] = testToLine
        
    
    msg.preamble = 'Multipart massage.\n'

    #pp = pprint.PrettyPrinter(indent=4)

    mailBodyStr = """\

Real To Line: {toLine}

A previous message 
    Dated: {failedDateLine}
    To: {failedRecipients} 
for which you were also a recipient, failed. 

This is to let you know that we have received a non-delivery-report (bounce message)
for that email and since you were also a recepient of that email, we are letting you 
know that {failedRecipients} did not recieve that email.

A full copy of the non-delivery-report that we received is attached.

This is a machine generated email and is purely informational.


    """.format(
        failedDateLine=failedDateLine,
        toLine=toLine,
        failedRecipients=" ".join(failedRecipients),
    )

    part = MIMEText(mailBodyStr)
    msg.attach(part)

    part = MIMEBase('message', "rfc822")
    part.set_payload(inMsg.as_string())
    #Encoders.encode_base64(part)

    msg.attach(part)

    sendingMethod = msgOut.SendingMethod.submit
        
    if msgOut.sendingMethodSet(msg, sendingMethod).isProblematic():
        return icm.EH_badLastOutcome()

    if not marmeSendLib.bx822Set_sendWithEnabledAcct(msg, sendingMethod):
        return icm.EH_problem_info("")

    iifOutcome = marmeSendLib.sendCompleteMessage().iif(
        interactive=False,
        msg=msg,
    )

    return iifOutcome




"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Msg-Send     ::  msgSend_permanentNdrToCoRecepiets    [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def msgSend_permanentNdrToCoRecepietsObsoleted(
        failedRecipients,
        nonDeliveryReportMsg,
):
    """ Given a nonDeliveryReportMsg, We focus on the failedMsg
    """

 

    allRecipients= None

    failedMsgWasFound = False

    for part in nonDeliveryReportMsg.walk():
        if part.get_content_type() == 'message/rfc822':
            failedMsgList = part.get_payload()
            failedMsgWasFound = True
            for failedMsg in failedMsgList:
                tos = failedMsg.get_all('to', [])
                ccs = failedMsg.get_all('cc', [])
                resent_tos = failedMsg.get_all('resent-to', [])
                resent_ccs = failedMsg.get_all('resent-cc', [])
                allRecipients = email.utils.getaddresses(tos + ccs + resent_tos + resent_ccs)
                failedFromLine = failedMsg['From']
                failedSubjectLine = failedMsg['Subject']
                failedDateLine = failedMsg['date']                                              
                
            break

    if failedMsgWasFound is False:
        #icm.EH_problem_unassignedError("Failed Message Was UnFound")
        return

    if not allRecipients:
        icm.EH_problem_unassignedError("Failed Message Is Missing All Recipients")
        return

    allRecipientsSet = set()
    for thisRecipient in allRecipients:
        allRecipientsSet.add(thisRecipient[1])
 
    coRecipientsSet = allRecipientsSet - failedRecipients

    msg = MIMEMultipart()    

    msg['Date'] = email.utils.formatdate(localtime = 1)
    msg['Message-ID'] = email.utils.make_msgid()
    
    msg['Subject'] = """Co-Recipient Non-Delivery-Report  -- Was: {failedSubjectLine}""".format(
        failedSubjectLine=failedSubjectLine)

    msg['From'] = failedFromLine

    toLine = ""
    
    for thisRecipient in coRecipientsSet:
        if toLine:
            toLine = toLine + ', ' + thisRecipient
        else:
            toLine = thisRecipient            

    msg['To'] = "test@mohsen.banan.1.byname.net"
        
    
    msg.preamble = 'Multipart massage.\n'

    #pp = pprint.PrettyPrinter(indent=4)

    mailBodyStr = """\

Real To Line: {toLine}

A previous message 
    Dated: {failedDateLine}
    To: {failedRecipients} 
for which you were also a recipient, failed. 

This is to let you know that we have received a non-delivery-report (bounce message)
for that email and since you were also a recepient of that email, we are letting you 
know that {failedRecipients} did not recieve that email.

A full copy of the non-delivery-report that we received is attached.

This is a machine generated email and is purely informational.


    """.format(
        failedDateLine=failedDateLine,
        toLine=toLine,
        failedRecipients=" ".join(failedRecipients),
    )

    part = MIMEText(mailBodyStr)
    msg.attach(part)

    part = MIMEBase('message', "rfc822")
    part.set_payload(failedMsg.as_string())
    #Encoders.encode_base64(part)

    #part.add_header('Content-Disposition', 'attachment; filename="/etc/resolv.conf"')

    msg.attach(part)

    # msgSend_submitWith_byName_sa20000(
    #     msg=msg,
    #     envelopeAddr="test@mohsen.banan.1.byname.net",
    #     recipients=["test@mohsen.banan.1.byname.net"],
    # )

    return



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Supporting Classes And Functions*
* /None/
"""
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common/Generic Facilities -- Library Candidates*
* /None/
"""

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *G_main -- Instead Of IICM-IIF Dispatcher-Example*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  G_main -- icm.argsparse bypass  [[elisp:(org-cycle)][| ]]
"""

def G_main():
    """ For use instead of IIF dispatcher."""
    print sys.argv
    #argc = len(sys.argv)
    return


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *IICM Framework Model Selection And Entry /Dblked/ --*
"""


####+BEGINNOT: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/icm.G_main.py"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || /Dblk-Begin/ ::  g_ iicm Mode Specification    [[elisp:(org-cycle)][| ]]
"""

g_examples = examples  # or None 
g_mainEntry = G_main # or None
g_importedIifs = {        # Enumerate modules from which IIFs become invokable
   'marmeAcctsLib': marmeAcctsLib.__file__,
}


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || /Dblk-End/   ::   [[elisp:(org-cycle)][| ]]
"""
####+END:

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
    """ """
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

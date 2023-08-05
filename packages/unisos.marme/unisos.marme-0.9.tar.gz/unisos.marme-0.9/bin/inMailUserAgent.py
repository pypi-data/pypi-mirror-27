#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  A set of basic examples that show iicm_ usage and which can be used as a starting point.
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
#import time
import shutil

import icmsPkgLib
import marmeAcctsLib
import iicm


####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "ucf" :file "ucf"
# Development Workaround  For JediWorkaround
import ucf
####+END:

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "icm" :file "icm"
# External Usage
from unisos.icm import icm
####+END:


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
   
    marmeAcctsLib.commonParamsSpecify(iicmParams)
       
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

    iifArgsLen={'Min': 0, 'Max':0,}
    
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)    
    def iif(self,
            interactive=False,        # Can also be called non-interactively
    ):
        """iif of SomeIif function longer docString."""
        myName=self.myName()
        #G = icm.IicmGlobalContext()        
        thisOutcome = icm.OpOutcome(invokerName=myName)

        defaultMailDom = marmeAcctsLib.enabledMailAcctObtain()        
        
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

        icm.iifExampleMenuChapter('*General Dev and Testing IIFs*')   

        thisIifAction= " -i unitTest"
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='none'
        )
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='full'
        )

        icm.iifExampleMenuChapter('*Config File Creation Facilities*')

        icm.iifExampleMenuSection('*Automated Config File Creation Facilities*')           

        thisIifAction= " -i notmuchConfigUpdate"
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='none'
        )
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='full'
        )

        thisIifAction= " -i notmuchConfigStdout"
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='none'
        )
        icm.iifExampleMenuItem(
            format(""  + thisIifAction),
            verbosity='full'
        )

        configFile = withInMailDomGetNotmuchConfigPath(defaultMailDom)
        
        icm.ANN_write(
            """ls -l {}""".format(configFile)
        )
        icm.ANN_write(
            """cat  {} """.format(configFile)
        )

        icm.iifExampleMenuSection('*Interactive Config File Creation Facilities*')           

        thisIifAction = " -i runNotmuch"        
        iifArgs = '''setup  # Creates/Edits notmuch-config'''
        icm.iifExampleMenuItem(
            """{thisIifAction} {iifArgs}"""
            .format(thisIifAction=thisIifAction, iifArgs=iifArgs),
            verbosity='none'
        )        

        icm.iifExampleMenuSection('*Show/List Config Parameter Settings*')   

        iifArgs = '''config list  # Shows Key aspects of notmuch-config'''
        icm.iifExampleMenuItem(
            """{thisIifAction} {iifArgs}"""
            .format(thisIifAction=thisIifAction, iifArgs=iifArgs),
            verbosity='none'
        )

        icm.iifExampleMenuChapter('*Run notmuch -- new, Search*')   

        iifArgs = '''new # Refresh the index'''
        icm.iifExampleMenuItem(
            """{thisIifAction} {iifArgs}"""
            .format(thisIifAction=thisIifAction, iifArgs=iifArgs),
            verbosity='none'
        )        

        thisIifAction = " -i runNotmuch"
        iifArgs = '''-- search --format=text --output=files "from:"'''
        icm.iifExampleMenuItem(
            """{thisIifAction} {iifArgs}"""
            .format(thisIifAction=thisIifAction, iifArgs=iifArgs),
            icmWrapper="",
            verbosity='none',
        )        
        icm.iifExampleMenuItem(
            """{thisIifAction} {iifArgs}"""
            .format(thisIifAction=thisIifAction, iifArgs=iifArgs),
            icmWrapper="echo",
            verbosity='none',
        )        

        
        iifAction = " -i runNotmuch" ; iifArgs = '''-- search --output=files "to: isit442"'''
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')

        marmeAcctsLib.examples_marmeAcctsLibControls()

        marmeAcctsLib.examples_inMailAcctAccessPars()

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
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  notmuchConfigUpdate    [[elisp:(org-cycle)][| ]]
"""    
class notmuchConfigUpdate(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct']       
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
####+END:

        outcome = notmuchConfigStdout().iif(
            interactive=False,
            controlProfile=controlProfile,
            inMailAcct=inMailAcct,
        )
        if outcome.isProblematic(): return(icm.EH_badOutcome(outcome))

        configFileStr = outcome.stdout

        configFilePath = withInMailDomGetNotmuchConfigPath(inMailAcct)

        rcFileFromControl = "{controlProfileBaseDir}/inMail/{inMailAcct}/conf/_notmuch-config".format(
            # ../control/inMail/example.com/conf/_notmuch-config
            controlProfileBaseDir=marmeAcctsLib.controlProfileBaseDirGet(controlProfile),
            inMailAcct=inMailAcct,
        )
        
        if os.path.isfile(rcFileFromControl):
            shutil.copyfile(rcFileFromControl, configFilePath)
        else:
            with open(configFilePath, "w") as thisFile:
                thisFile.write(configFileStr + '\n')

        if interactive:
            icm.ANN_here("configFilePath={val}".format(val=configFilePath))
        
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  withInMailDomGetNotmuchConfigPath    [[elisp:(org-cycle)][| ]]
"""
def withInMailDomGetNotmuchConfigPath(
        inMailAcct,
):
    inMailAcctConfBase = os.path.abspath(
        "{configBaseDir}/{inMailAcct}"
        .format(configBaseDir=marmeAcctsLib.configBaseDirGet() ,inMailAcct=inMailAcct)
    )

    try: 
        os.makedirs(inMailAcctConfBase)
    except OSError:
        if not os.path.isdir(inMailAcctConfBase):
            raise

    filePath = os.path.join(
        inMailAcctConfBase,
        "_notmuch-config"
    )
    return filePath

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  notmuchConfigStdout    [[elisp:(org-cycle)][| ]]
"""    
class notmuchConfigStdout(icm.Iif):
    """
** Applies results of inMailAcctAccessParsGet() to offlineimaprcTemplate().
"""
    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct'] 
    iifArgsLen = {'Min': 0, 'Max': 0,}
    
####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
####+END:

        templateFile = os.path.join(
            icmsPkgLib.pkgInputsBaseDir_obtain(),
            "notmuch/_notmuch-config.template"
        )

        outcome = icm.subProc_bash(
            """\
cat {templateFile} | \
	sed \
	    -e "s@%mailDirPath%@{mailDirPath}@g" \
	    -e "s@%firstName%@{firstName}@g" \
	    -e "s@%lastName%@{lastName}@g" 
"""
            .format(
                templateFile=templateFile,
                # ../var/inMail/example/maildir/Inbox
                mailDirPath=marmeAcctsLib.getPathForAcctMaildir(
                   controlProfile, inMailAcct),
                firstName="FirstName",
                lastName="LastName",
            )
        )#.log()
        if outcome.isProblematic(): return(icm.EH_badOutcome(outcome))

        if interactive:
            icm.ANN_write(outcome.stdout)
        
        return outcome.set(
            opError=icm.OpError.Success,
            #opResults=outcome.stdout
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  runNotmuch    [[elisp:(org-cycle)][| ]]
"""    
class runNotmuch(icm.Iif):
    """Passes cmndArgs to notmuch --config xx"""

    iifParamsMandatory = []
    iifParamsOptional = ['inMailAcct'] 
    iifArgsLen = {'Min': 0, 'Max': 1000,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "inMailAcct"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        inMailAcct=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'inMailAcct': inMailAcct, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        inMailAcct = callParamsDict['inMailAcct']
####+END:

        G = icm.IicmGlobalContext()
        iicmRunArgs = G.iimRunArgsGet()
        joinedArgs = icm.str_joinedArgs(iicmRunArgs.iifArgs)

        defaultMailDom = marmeAcctsLib.enabledMailAcctObtain()                
        configFile = withInMailDomGetNotmuchConfigPath(defaultMailDom)

        outcome = icm.subProc_bash(
            """notmuch --config={configFile} {joinedArgs}"""
            .format(
                configFile=configFile,
                joinedArgs=joinedArgs,
            )
        ).out()
        if outcome.isProblematic(): return(icm.EH_badOutcome(outcome))

        if interactive:
            pass
        
        return outcome.set(
            opError=icm.OpError.Success,
            #opResults=outcome.stdout
        )

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Supporting Classes And Functions*
*   /None/  [[elisp:(org-cycle)][| ]]
"""
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common/Generic Facilities -- Library Candidates*
*   /None/  [[elisp:(org-cycle)][| ]]
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

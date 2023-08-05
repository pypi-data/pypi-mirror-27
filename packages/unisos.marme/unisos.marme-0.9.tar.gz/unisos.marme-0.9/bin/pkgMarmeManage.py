#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  Install dependencies of ICMs-Pkgs.
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

import platform

#import iicm

import collections

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "ucf" :file "ucf"
# Ordinary Usage
from unisos.ucf import ucf
####+END:

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "icm" :file "icm"
# Ordinary Usage
from unisos.icm import icm
####+END:

from unisos.marme import icmsPkgLib


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =ModSpecs=   ::  canon_pythonPkgsSpec    [[elisp:(org-cycle)][| ]]
"""
def canon_pythonPkgsSpec():
    pkgs = collections.OrderedDict()
    pkgs["notmuch"] = None
    pkgs["flufl.bounce"] = "2.3"
    return pkgs


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =ModSpecs=   ::  canon_linuxPkgsSpec    [[elisp:(org-cycle)][| ]]
"""
def canon_linuxPkgsSpec():
    pkgs = collections.OrderedDict()
    pkgs["offlineimap"] = None
    return pkgs
   
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

    icmsPkgLib.commonParamsSpecify(iicmParams)
       
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

        iifAction = " -i unitTest" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
        icm.iifExampleMenuItem(menuLine, verbosity='full')        

        icm.iifExampleMenuChapter('*BinsPreps*')

        iifAction = " -i binsPreps" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')

        iifAction = " -i binsPrepsCurInfo" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')

        icm.iifExampleMenuSection('*Install ICMs Needed Linux Packages*')
        
        iifAction = " -i canon_linuxPkgInstall" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')

        icm.iifExampleMenuSection('*Install ICMs Needed Python Packages*')
        
        iifAction = " -i canon_pythonPkgInstall" ; iifArgs = ""
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
        
        #
        # ICMs PKG Information
        #

        icmsPkgLib.examples_pkgInfoParsFull(
            icmsPkgNameSpecification(),
            icmsPkgControlBaseDir=icmsPkgControlBaseDirDefault(),
            icmsPkgRunBaseDir=icmsPkgRunBaseDirDefault(),
        )

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
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  icmsPkgNameSpecification    [[elisp:(org-cycle)][| ]]
"""
def icmsPkgNameSpecification():    return "marme.dev"

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  icmsPkgControlBaseDirDefault    [[elisp:(org-cycle)][| ]]
"""
def icmsPkgControlBaseDirDefault():    return os.path.abspath("../../marme.control")

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  icmsPkgRunBaseDirDefault    [[elisp:(org-cycle)][| ]]
"""
def icmsPkgRunBaseDirDefault():    return os.path.expanduser("~/byStarRunEnv")


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  binsPreps    [[elisp:(org-cycle)][| ]]
"""
class binsPreps(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 0, 'Max': 0,}


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

        pkgsList = canon_pythonPkgsSpec()
        for pkgName in pkgsList:
            pkgVersion = pkgsList[pkgName]
            canon_pythonPkgInstall(pkgName, pkgVersion)

        pkgsList = canon_linuxPkgsSpec()
        for pkgName in pkgsList:
            pkgVersion = pkgsList[pkgName]
            canon_linuxPkgInstall(pkgName, pkgVersion)
            
        
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  binsPrepsCurInfo    [[elisp:(org-cycle)][| ]]
"""    
class binsPrepsCurInfo(icm.Iif):
    """
** Retrieve current version and settings of PythonPkgs and LinuxPkgs.
"""

    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 0, 'Max': 0,}

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
        #G = icm.IicmGlobalContext()
        #g_runArgs = G.iimRunArgsGet()

        #
        # Python Packages
        #
        pkgsList = canon_pythonPkgsSpec()
        for pkgName in pkgsList:
            # Not all packages ahve __version__ so this is not reliable
            #exec("import {pyModule}".format(pyModule=each))
            #exec("print {pyModule}.__version__".format(pyModule=each))

            installedVer = pythonPkg_versionGet(pkgName)

            installedLoc = pythonPkg_locationGet(pkgName)
            
            icm.ANN_write(
                "Python:: pkgName={pkgName} -- expectedVer={expectedVer} -- installedVer={installedVer} -- installedLoc={installedLoc}"
                .format(pkgName=pkgName,
                        expectedVer=pkgsList[pkgName],
                        installedVer=installedVer,
                        installedLoc=installedLoc,
                ))
            
        #
        # Linux Packages
        #
        pkgsList = canon_linuxPkgsSpec()
        for pkgName in pkgsList:

            installedVer = linuxPkg_versionGet(pkgName)
            
            icm.ANN_write(
                "Linux::  pkgName={pkgName} -- expectedVer={expectedVer} -- installedVer={installedVer}"
                .format(pkgName=pkgName,
                        expectedVer=pkgsList[pkgName],
                        installedVer=installedVer,
                ))
            
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Supporting Classes And Functions*
*       /None/  [[elisp:(org-cycle)][| ]]
"""
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common/Generic Facilities -- Library Candidates*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  canon_linuxPkgInstall    [[elisp:(org-cycle)][| ]]
"""
def canon_linuxPkgInstall(
        pkgName,
        pkgVersion,
):
    """
** Install a given Linux pkg based on its canonical name and version.
"""
    distroName = platform.linux_distribution()[0]
    
    if  distroName == "Ubuntu":
        return linuxPkgInstall_aptGet(pkgName, pkgVersion)
    elif distroName == "Redhat":
        return linuxPkgInstall_yum(pkgName, pkgVersion)
    else:
        icm.EH_problem_info("Unsupported Distribution == {}".format(distroName))
        return

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  linuxPkgInstall_ubuntu    [[elisp:(org-cycle)][| ]]
"""
def linuxPkgInstall_aptGet(
        pkgName,
        pkgVersion,
):
    """
** Install a given linux pkg with apt-get based on its canonical name and version.
"""
    installedVersion = linuxPkg_versionGet(pkgName)
    if pkgVersion:
        if installedVersion == pkgVersion:
            icm.ANN_write("Linux::  {pkgName} ver={ver} (as expected) is already installed -- skipped".format(
                pkgName=pkgName, ver=installedVersion))
            return
        else:
            outcome = icm.subProc_bash(
                """echo NOTYET pip install {pkgName}=={pkgVersion}"""
                .format(pkgName=pkgName, pkgVersion=pkgVersion)
            ).log()
            if outcome.isProblematic(): return icm.EH_badOutcome(outcome)
            resultStr = outcome.stdout.strip()
            icm.ANN_write(resultStr)
            return

    installedVersion = linuxPkg_versionGet(pkgName)
    if installedVersion:
        icm.ANN_write("Linux::  {pkgName} ver={ver} (as any) is already installed -- skipped".format(
            pkgName=pkgName, ver=installedVersion))
        return
    else:
        outcome = icm.subProc_bash(
            """sudo apt-get install {pkgName}"""
            .format(pkgName=pkgName)
        ).log()
        if outcome.isProblematic(): return icm.EH_badOutcome(outcome)
        resultStr = outcome.stdout.strip()
        icm.ANN_write(resultStr)
        return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  linuxPkgInstall_redhat    [[elisp:(org-cycle)][| ]]
"""
def linuxPkgInstall_yum(
        pkgName,
        pkgVersion,
):
    """
** Install a given linux pkg with yum based on its canonical name and version.
"""

    outcome = icm.subProc_bash(
        """sudo yum install {pkgName}"""
        .format(pkgName=pkgName)
    ).log()
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)
    resultStr = outcome.stdout.strip()
    icm.ANN_write(resultStr)
    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  linuxPkg_versionGet    [[elisp:(org-cycle)][| ]]
"""
def linuxPkg_versionGet(
        pkgName,
):
    """
** Return version as string if Python pkgName is installed
** Return None if Python pkgName is not installed
"""
    dpkgQueryOpts = """dpkg-query --show --showformat='${db:Status-Status}\n'"""
    outcome = icm.subProc_bash(
        """{dpkgQueryOpts} {pkgName}"""
        .format(dpkgQueryOpts=dpkgQueryOpts, pkgName=pkgName)
    ).log()
    if outcome.isProblematic():
        icm.EH_badOutcome(outcome)
        return None

    resultStr = outcome.stdout.strip()
    if resultStr == "":
        return None
    
    dpkgQueryOpts = """dpkg-query --show --showformat='${Version}\n'"""
    outcome = icm.subProc_bash(
        """{dpkgQueryOpts} {pkgName}"""
        .format(dpkgQueryOpts=dpkgQueryOpts, pkgName=pkgName)
    ).log()
    if outcome.isProblematic():
        icm.EH_badOutcome(outcome)
        return None
    
    resultStr = outcome.stdout.strip()
    if resultStr == "":
        return None
    else:
        return resultStr



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  canon_pythonPkgInstall    [[elisp:(org-cycle)][| ]]
"""
def canon_pythonPkgInstall(
        pkgName,
        pkgVersion,
):
    """
** Install a given Python pkg based on its canonical name and version.
"""
    return pythonPkg_install_pip(pkgName, pkgVersion)    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  pythonPkg_install_ubuntu    [[elisp:(org-cycle)][| ]]
"""
def pythonPkg_install_pip(
        pkgName,
        pkgVersion,
):
    """
** Install a given Python pkg based on its canonical name and version.
If version is specified,  the package is installed or updated to that version.
If version is None, 
    if package is already installed no action is taken
    if package is not installed, the latest is installed
"""
    installedVersion = pythonPkg_versionGet(pkgName)
    if pkgVersion:
        if installedVersion == pkgVersion:
            icm.ANN_write("Python:: {pkgName} ver={ver} (as expected) is already installed -- skipped".format(
                pkgName=pkgName, ver=installedVersion))
            return
        else:
            outcome = icm.subProc_bash(
                """echo pip install {pkgName}=={pkgVersion}"""
                .format(pkgName=pkgName, pkgVersion=pkgVersion)
            ).log()
            if outcome.isProblematic(): return icm.EH_badOutcome(outcome)
            resultStr = outcome.stdout.strip()
            icm.ANN_write(resultStr)
            return

    installedVersion = pythonPkg_versionGet(pkgName)
    if installedVersion:
        icm.ANN_write("Python:: {pkgName} ver={ver} (as any) is already installed -- skipped".format(
            pkgName=pkgName, ver=installedVersion))
        return
    else:
        outcome = icm.subProc_bash(
            """echo pip install {pkgName}"""
            .format(pkgName=pkgName)
        ).log()
        if outcome.isProblematic(): return icm.EH_badOutcome(outcome)
        resultStr = outcome.stdout.strip()
        icm.ANN_write(resultStr)
        return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  pythonPkg_versionGet    [[elisp:(org-cycle)][| ]]
"""
def pythonPkg_versionGet(
        pkgName,
):
    """
** Return version as string if Python pkgName is installed
** Return None if Python pkgName is not installed
"""
    outcome = icm.subProc_bash(
        """pip show {pkg} | egrep '^Version' | cut -d ':' -f 2"""
        .format(pkg=pkgName)
    ).log()
    if outcome.isProblematic():
        icm.EH_badOutcome(outcome)
        return None
    
    resultStr = outcome.stdout.strip()
    if resultStr == "":
        return None
    else:
        return resultStr

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  pythonPkg_locationGet    [[elisp:(org-cycle)][| ]]
"""    
def pythonPkg_locationGet(
        pkgName,
):
    """
** Return location as string if Python pkgName is installed
** Return None if Python pkgName is not installed
"""
    outcome = icm.subProc_bash(
        """pip show {pkg} | egrep '^Location' | cut -d ':' -f 2"""
        .format(pkg=pkgName)
    ).log()
    if outcome.isProblematic():
        icm.EH_badOutcome(outcome)
        return None
    
    resultStr = outcome.stdout.strip()
    if resultStr == "":
        return None
    else:
        return resultStr
    
    
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
   'icmsPkgLib': icmsPkgLib.__file__,
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

#import iicm

def classedIifsDict():
    """Should be done here, can not be done in iicm library."""
    callDict = dict()
    for eachIif in icm.iifList_mainsMethods().iif(
            interactive=False,
            importedIifs=g_importedIifs,
    ):
        #print eachIif
        try:
            callDict[eachIif] = eval("{}".format(eachIif))
            continue
        except NameError:
            pass

        #print "ZZLL"
        for mod in g_importedIifs:
            #print mod
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

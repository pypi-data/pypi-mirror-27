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
__version__ = "201706283912"
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
    """
** Extends Python imports path with  ../lib/python
"""
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

#import sys
import os
#import time

import iicm
import icmsPkgLib

import collections


####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "ucf" :file "ucf"
# Development Workaround  For JediWorkaround
import ucf
####+END:

####+BEGIN: bx:dblock:python:import:jediWorkAround :namespace "unisos" :module "icm" :file "icm"
# External Usage
from unisos.icm import icm
####+END:


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Base Directory Locations*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  mailAcctsBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def mailAcctsBaseDirGet():
    return(
        icmsPkgLib.pkgBaseDir_obtain()
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  controlBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def controlBaseDirGet():
    return(
        icmsPkgLib.controlBaseDir_obtain()
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  varBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def varBaseDirGet():
    return(
        icmsPkgLib.varBaseDir_obtain()
    )

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  configBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def configBaseDirGet():
    return(
        icmsPkgLib.varConfigBaseDir_obtain()
    )

    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  tmpBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def tmpBaseDirGet():
    return(
        icmsPkgLib.tmpBaseDir_obtain()
    )

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Control From  FP Obtain*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  enabledControlProfileObtain    [[elisp:(org-cycle)][| ]]
"""
def enabledControlProfileObtain():
    """Returns as a string fp value read."""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            controlBaseDirGet(),
            "common",
            "selections",
            "fp",
        ),
        parName="enabledControlProfile",
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  availableControlProfilesObtain    [[elisp:(org-cycle)][| ]]
"""
def availableControlProfilesObtain():
    """
Returns a list
"""
    availablesList = list()
    controlBaseDir = controlBaseDirGet()
    for each in  os.listdir(controlBaseDir):
        if each == "CVS":
            continue
        if each == "common":
            continue
        eachFullPath = os.path.join(controlBaseDir, each)
        if not os.path.isdir(eachFullPath):
            continue
        availablesList.append(each)
    return availablesList


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  enabledMailAcctObtainObsoleted    [[elisp:(org-cycle)][| ]]
"""
def enabledMailAcctObtainObsoleted():
    """
** Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            controlBaseDirGet(),
            "common",
            "selections",
            "fp",
        ),
        parName="enabledMailAcct",          
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  enabledInMailAcctObtain    [[elisp:(org-cycle)][| ]]
"""
def enabledInMailAcctObtain():
    """
** Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            controlBaseDirGet(),
            "common",
            "selections",
            "fp",
        ),
        parName="enabledInMailAcct",          
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  availableInMailAcctObtain    [[elisp:(org-cycle)][| ]]
"""
def availableInMailAcctObtain():
    """
Returns a list
"""
    availablesList = list()
    baseDir = os.path.join(
           controlProfileBaseDirGet(enabledControlProfileObtain(),),
            "inMail",
    )

    for each in  os.listdir(baseDir):
        if each == "CVS":
            continue
        if each == "common":
            continue
        eachFullPath = os.path.join(baseDir, each)
        if not os.path.isdir(eachFullPath):
            continue
        availablesList.append(each)
    return availablesList


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  enabledOutMailAcctObtain    [[elisp:(org-cycle)][| ]]
"""
def enabledOutMailAcctObtain():
    """
** Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            controlBaseDirGet(),
            "common",
            "selections",
            "fp",
        ),
        parName="enabledOutMailAcct",          
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  availableOutMailAcctObtain    [[elisp:(org-cycle)][| ]]
"""
def availableOutMailAcctObtain():
    """
Returns a list
"""
    availablesList = list()
    baseDir = os.path.join(
           controlProfileBaseDirGet(enabledControlProfileObtain(),),
            "outMail",
    )

    for each in  os.listdir(baseDir):
        if each == "CVS":
            continue
        if each == "common":
            continue
        eachFullPath = os.path.join(baseDir, each)
        if not os.path.isdir(eachFullPath):
            continue
        availablesList.append(each)
    return availablesList



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  enabledMailBoxObtain    [[elisp:(org-cycle)][| ]]
"""
def enabledMailBoxObtain():
    """
** Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            controlBaseDirGet(),
            "common",
            "selections",
            "fp",
        ),
        parName="enabledMailBox",          
    )


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Control Base Directory From FP Get*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  controlProfileBaseDirGet    [[elisp:(org-cycle)][| ]]
"""
def controlProfileBaseDirGet (controlProfile):
    """
** Joins controlBaseDirGet() and enabledControlProfileObtain()
"""
    if not controlProfile:
        controlProfile = enabledControlProfileObtain()
    return os.path.abspath(
        os.path.join(
            controlBaseDirGet(),
            controlProfile,
    ))

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  outMailAcctDirGet    [[elisp:(org-cycle)][| ]]
"""

def outMailAcctDirGet(controlProfile, outMailAcct):
    return os.path.abspath(
        os.path.join(
           controlProfileBaseDirGet(controlProfile),
            "outMail",
            outMailAcct,
            "fp",
    ))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  outMailCommonDirGet    [[elisp:(org-cycle)][| ]]
"""
def outMailCommonDirGet(controlProfile):
    if not controlProfile:
        controlProfile = enabledControlProfileObtain()
    return os.path.abspath(
        os.path.join(
            controlProfileBaseDirGet(controlProfile),
            "outMail",
            "common",
            #"fp",         # NOTYET, Needs to be revisited
    ))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  inMailAcctDirGet    [[elisp:(org-cycle)][| ]]
"""
def inMailAcctDirGet(controlProfile, inMailAcct):
    if not controlProfile:
        controlProfile = enabledControlProfileObtain()
    return os.path.abspath(
        os.path.join(
            controlProfileBaseDirGet(controlProfile),             
            "inMail",
            inMailAcct,
            "fp",

    ))


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  inMailCommonDirGet    [[elisp:(org-cycle)][| ]]
"""
def inMailCommonDirGet(controlProfile,):
    if not controlProfile:
        controlProfile = enabledControlProfileObtain()
    return (
        os.path.abspath(
            os.path.join(
                controlProfileBaseDirGet(controlProfile,),
                "inMail"
                "common"
                "fp"            
            )))


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *VAR Base Directory Get*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  getPathForAcctMaildir    [[elisp:(org-cycle)][| ]]
"""
def getPathForAcctMaildir(
    controlProfile,
    mailAcct,
):
    """
** NOTYET, controlProfile is not being used.
"""
    return (
        os.path.join(
            varBaseDirGet(),
            "inMail",
            controlProfile,
            mailAcct,
            "maildir"
        ))

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  getPathForAcctMbox    [[elisp:(org-cycle)][| ]]
"""
def getPathForAcctMbox(
    controlProfile,     
    mailAcct,
    mbox,
):
    #if not controlProfile:
        #controlProfile = enabledControlProfileObtain()

    if not mailAcct:
        mailAcct = enabledInMailAcctObtain()

    if not mbox:
        mbox = enabledMailBoxObtain()

    return (
        os.path.join(
            varBaseDirGet(),
            "inMail",
            controlProfile,            
            mailAcct,
            "maildir",
            mbox,
        ))

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  getPathForInMailConfig    [[elisp:(org-cycle)][| ]]
"""
def getPathForInMailConfig(
    controlProfile,     
    inMailAcct,
):

    return (
        os.path.join(
            configBaseDirGet(),
            "inMail",
            controlProfile,            
            inMailAcct,
        ))

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  getPathForOutMailConfig    [[elisp:(org-cycle)][| ]]
"""
def getPathForOutMailConfig(
    controlProfile,     
    outMailAcct,
):

    return (
        os.path.join(
            configBaseDirGet(),
            "outMail",
            controlProfile,            
            outMailAcct,
        ))



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common Arguments Specification*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  commonParamsSpecify    [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
        iicmParams,
):
    enabledControlProfile = enabledControlProfileObtain()    
    #enabledMailAcct = enabledMailAcctObtain()
    enabledInMailAcct = enabledInMailAcctObtain()
    enabledOutMailAcct = enabledOutMailAcctObtain()        

    iicmParams.parDictAdd(
        parName='controlProfile',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault="{default}".format(default=enabledControlProfile),
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--controlProfile',
    )

    iicmParams.parDictAdd(
        parName='inMailAcct',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault="{default}".format(default=enabledInMailAcct),
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--inMailAcct',
    )
    
    iicmParams.parDictAdd(
        parName='outMailAcct',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault="{default}".format(default=enabledOutMailAcct),
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--outMailAcct',
    )
    
    iicmParams.parDictAdd(
        parName='firstName',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--firstName',
    )
    
    iicmParams.parDictAdd(
        parName='lastName',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--lastName',
    )

    iicmParams.parDictAdd(
        parName='userName',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--userName',
    )

    iicmParams.parDictAdd(
        parName='userPasswd',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--userPasswd',
    )
    
    iicmParams.parDictAdd(
        parName='mtaRemHost',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--mtaRemHost',
    )

    iicmParams.parDictAdd(
        parName='mtaRemProtocol',
        parDescription="Base for Domain/Site/Source of incoming Mail",
        parDataType=None,
        parDefault=None,
        parChoices=["someOptionalPar", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--mtaRemProtocol',
    )
    
    
    # iicmParams.parDictAdd(
    #     parName='imapServer',
    #     parDescription="Base for Domain/Site/Source of incoming Mail",
    #     parDataType=None,
    #     parDefault=None,
    #     parChoices=["someOptionalPar", "UserInput"],
    #     parScope=icm.IIM_ParamScope.TargetParam,
    #     argparseShortOpt=None,
    #     argparseLongOpt='--imapServer',
    # )

    iicmParams.parDictAdd(
        parName='inMailAcctMboxesPath',
        parDescription="Base Directory Of Maildir where msgs are retrieved to.",
        parDataType=None,
        parDefault=None,        
        #parDefault="../var/inMail/{default}/maildir/".format(default=enabledMailAcct),
        parChoices=["someFile", "UserInput"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--inMailAcctMboxesPath',
    )
    
    iicmParams.parDictAdd(
        parName='inMbox',
        parDescription="Name of MailBox to be joined with inMailAcctMboxesPath.",
        parDataType=None,
        parDefault=None,
        parChoices=["envelope", "Tmp"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--inMbox',
    )

    iicmParams.parDictAdd(
        parName='mboxesList',
        parDescription="Name of MailBox to be joined with inMailAcctMboxesPath.",
        parDataType=None,
        parDefault=None,
        parChoices=["envelope", "Tmp"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--mboxesList',
    )

    iicmParams.parDictAdd(
        parName='ssl',
        parDescription="Name of MailBox to be joined with inMailAcctMboxesPath.",
        parDataType=None,
        parDefault=None,
        parChoices=["no", "on"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--ssl',
    )
    
    iicmParams.parDictAdd(
        parName='sendingMethod',
        parDescription="sending method for outgoing email",
        parDataType=None,
        parDefault=None,
        parChoices=["inject", "authSmtp"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--sendingMethod',
    )

    iicmParams.parDictAdd(
        parName='envelopeAddr',
        parDescription="Envelope Address Of Outgoing Email",
        parDataType=None,
        parDefault=None,
        parChoices=["envelop@example.com"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--envelopeAddr',
    )

    # iicmParams.parDictAdd(
    #     parName='parGroup',
    #     parDescription="Temporary till args dblock processing gets fixed",
    #     parDataType=None,
    #     parDefault=None,
    #     parChoices=["access", ],
    #     parScope=icm.IIM_ParamScope.TargetParam,
    #     argparseShortOpt=None,
    #     argparseLongOpt='--parGroup',
    # )
    


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common Examples Sections*
"""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_controlProfileManage    [[elisp:(org-cycle)][| ]]
"""
def examples_controlProfileManage():
    """."""
    icm.iifExampleMenuChapter('* =Selection=  Control Profiles -- /{}/ --*'.format(enabledControlProfileObtain()))

    thisIifAction= " -i enabledControlProfileGet"
    icm.iifExampleMenuItem(
        format(""  + thisIifAction),
        verbosity='none'
    )

    iifAction = "  -i enabledControlProfileSet"

    for each in availableControlProfilesObtain():
        iifArgs = " {controlProfile}".format(controlProfile=each)
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_enabledInMailAcctConfig    [[elisp:(org-cycle)][| ]]
"""    
def examples_enabledInMailAcctConfig():
    """
** Select Enabled Mail Account Config. Read/Writeen to control/common/selections/fp
"""
    icm.iifExampleMenuChapter('* =Selection=  InMailAccts -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledInMailAcctObtain()))

    thisIifAction= " -i enabledInMailAcctGet"
    icm.iifExampleMenuItem(
        format(""  + thisIifAction),
        verbosity='none'
    )

    iifAction = "  -i enabledInMailAcctSet"


    for each in availableInMailAcctObtain():
        iifArgs = " {}".format(each)
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
    return



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_enabledOutMailAcctConfig    [[elisp:(org-cycle)][| ]]
"""
def examples_enabledOutMailAcctConfig():
    """
** Select Enabled Mail Account Config. Read/Writeen to control/common/selections/fp
"""
    icm.iifExampleMenuChapter('* =Selection=  OutMailAccts -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))

    thisIifAction= " -i enabledOutMailAcctGet"
    icm.iifExampleMenuItem(
        format(""  + thisIifAction),
        verbosity='none'
    )

    iifAction = "  -i enabledOutMailAcctSet"

    for each in availableOutMailAcctObtain():
        iifArgs = " {}".format(each)
        menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
        icm.iifExampleMenuItem(menuLine, verbosity='none')
    return
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_select_mailBox    [[elisp:(org-cycle)][| ]]
"""
def examples_select_mailBox():
    """."""
    icm.iifExampleMenuChapter('* =Selection=  MailBox -- /{controlProfile}+{mailAcct}+{mBox}/ --*'.format(
        controlProfile=enabledControlProfileObtain(),
        mailAcct=enabledInMailAcctObtain(),
        mBox=enabledMailBoxGet().iif().results,
        ))

    thisIifAction= " -i enabledMailBoxGet"
    icm.iifExampleMenuItem(
        format(""  + thisIifAction),
        verbosity='none'
    )

    iifAction = "  -i enabledMailBoxSet"
    #iifArgs = " {enabledMailAcct}".format(enabledMailAcct=enabledMailAcctObtain())
    
    # ../../marme.control
    iifArgs = " Inbox"
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, verbosity='none')
    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_inMailAcctAccessPars    [[elisp:(org-cycle)][| ]]
"""
def examples_inMailAcctAccessPars():
    """
** Auxiliary examples to be commonly used.
"""
    icm.iifExampleMenuChapter('* =FP Values=  inMail Controls -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledInMailAcctObtain()))
    

    iifAction = " -i inMailAcctParsGet" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, verbosity='none')

    menuLine = """"""
    icm.iifExampleMenuItem(menuLine, icmName="marmeAcctsManage.py", verbosity='none')    


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_inMailAcctAccessParsFull    [[elisp:(org-cycle)][| ]]
"""    
def examples_inMailAcctAccessParsFull():
    """
** Auxiliary examples to be commonly used.
"""
    icm.iifExampleMenuChapter('* =FP Values=  inMail Controls -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledInMailAcctObtain()))

    iifAction = " -i inMailAcctParsGet" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, verbosity='none')

    icm.iifExampleMenuSection('*inMail /Access/ ParsSet -- /defaulMailAcct={}/ --*'.format(enabledInMailAcctObtain()))    

    iifAction = " -i inMailAcctAccessParsSet" ; iifArgs = ""
    menuLine = """--userName="UserName" --userPasswd="UserPasswd" --imapServer="ImapServer" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')
    
    iifAction = " -i inMailAcctAccessParsSet" ; iifArgs = ""
    menuLine = """--userName="UserName" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    icm.iifExampleMenuSection('*inMail /ControllerInfo/ ParsSet -- /defaulMailAcct={}/ --*'.format(enabledInMailAcctObtain()))    

    iifAction = " -i inMailAcctControllerInfoParsSet" ; iifArgs = ""
    menuLine = """--firstName="FirstName" --lastName="LastName" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')
    
    iifAction = " -i inMailAcctControllerInfoParsSet" ; iifArgs = ""
    menuLine = """--firstName="FirstName" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    icm.iifExampleMenuSection('*inMail /Retrieval/ ParsSet -- /defaulMailAcct={}/ --*'.format(enabledInMailAcctObtain()))    

    iifAction = " -i inMailAcctRetrievalParsSet" ; iifArgs = ""
    menuLine = """--inMailAcctMboxesPath="MaildirPath" --mboxesList="" --ssl="on" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    
    iifAction = " -i inMailAcctRetrievalParsSet" ; iifArgs = ""
    #mailDirPath = os.path.join(varBaseDirGet(), "inMail", enabledMailAcctObtain(), "mailDir")
    mailDirPath = getPathForAcctMaildir(enabledControlProfileObtain(), enabledInMailAcctObtain())
    menuLine = """--inMailAcctMboxesPath={mailDirPath} {iifAction} {iifArgs}""".format(
        mailDirPath=mailDirPath, iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    iifAction = " -i inMailAcctRetrievalParsSet" ; iifArgs = ""
    menuLine = """--ssl=on {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')
    
    
    iifAction = " -i inMailAcctRetrievalParsSet" ; iifArgs = ""
    menuLine = """--mboxesList="Inbox" --ssl="on" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')
    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_outMailAcctAccessPars    [[elisp:(org-cycle)][| ]]
"""
def examples_outMailAcctAccessPars():
    """."""
    icm.iifExampleMenuChapter('* =FP Values=  outMail Controls -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))
    

    cmndName = "outMailAcctParsGet" ; cmndArgs = "" ; cps = collections.OrderedDict()        
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

    menuLine = """"""
    icm.iifExampleMenuItem(menuLine, icmName="marmeAcctsManage.py", verbosity='none')    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_outMailAcctAccessParsFull    [[elisp:(org-cycle)][| ]]
"""    
def examples_outMailAcctAccessParsFull():
    """."""
    icm.iifExampleMenuChapter('* =FP Values=  outMail Controls -- /{controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))

    cmndName = "outMailAcctParsGet" ; cmndArgs = "" ; cps = collections.OrderedDict()        
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none')

    icm.iifExampleMenuSection('*outMail /Access/ ParsSet -- /enabledMailAcct={controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))        

    cmndName = "outMailAcctParsSet" ; cmndArgs = "access" ; cps = collections.OrderedDict()        
    cps['userName']="TBS" ; cps['userPasswd']="TBS" ; cps['mtaRemHost']="TBS" ; cps['mtaRemProtocol']="smtp_ssl/smtp_tls/smtp"     
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='none')

    icm.iifExampleMenuSection('*outMail /ControllerInfo/ ParsSet -- /enabledMailAcct={controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))        

    cmndName = "outMailAcctParsSet" ; cmndArgs = "controllerInfo" ; cps = collections.OrderedDict()        
    cps['firstName']="TBS" ; cps['lastName']="TBS"
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='none')

    icm.iifExampleMenuSection('*outMail /Submission/ ParsSet -- /enabledMailAcct={controlProfile}+{mailAcct}/ --*'.format(
        controlProfile=enabledControlProfileObtain(), mailAcct=enabledOutMailAcctObtain()))                

    cmndName = "outMailAcctParsSet" ; cmndArgs = "submission" ; cps = collections.OrderedDict()        
    cps['sendingMethod']="inject/submit" ; cps['envelopeAddr']="TBS"
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, icmWrapper="echo", verbosity='none')

    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *File Parameters Get/Set -- Commands*
"""

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  FP_readTreeAtBaseDir_CmndOutput    [[elisp:(org-cycle)][| ]]
"""
def FP_readTreeAtBaseDir_CmndOutput(
        interactive,
        fpBaseDir,
        iifOutcome,
):
    """Invokes FP_readTreeAtBaseDir.iif as interactive-output only."""
    #
    # Interactive-Output + Chained-Outcome Command Invokation
    #
    FP_readTreeAtBaseDir = icm.FP_readTreeAtBaseDir()
    FP_readTreeAtBaseDir.cmndLineInputOverRide = True
    FP_readTreeAtBaseDir.iifOutcome = iifOutcome
        
    return FP_readTreeAtBaseDir.iif(
        interactive=interactive,
        FPsDir=fpBaseDir,
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledControlProfileGet    [[elisp:(org-cycle)][| ]]
"""
class enabledControlProfileGet(icm.Iif):
    """
** Output the current from -- NOTYET -- Should write at {varBase}/selections/fp
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
    
        enabledMailAcct = enabledControlProfileObtain()
 
        if interactive:
            icm.ANN_write(enabledMailAcct)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=enabledMailAcct,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledControlProfileSet    [[elisp:(org-cycle)][| ]]
"""    
class enabledControlProfileSet(icm.Iif):
    """
** Write as a FP the enabledControlProfile.
"""

    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 1, 'Max': 1,}
    
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

        G = icm.IicmGlobalContext()        

        iicmRunArgs = G.iimRunArgsGet()
        for each in iicmRunArgs.iifArgs:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(
                    controlBaseDirGet(),
                    "common",
                    "selections",
                    "fp",
                    "enabledControlProfile",
                ),
                parValue=each,
            )

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=each,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailAcctGet    [[elisp:(org-cycle)][| ]]
"""
class enabledInMailAcctGet(icm.Iif):
    """
** Output the current enabledMailAcct
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
    
        enabledInMailAcct = enabledInMailAcctObtain()
 
        if interactive:
            icm.ANN_write(enabledInMailAcct)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=enabledInMailAcct,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailAcctSet    [[elisp:(org-cycle)][| ]]
"""
class enabledInMailAcctSet(icm.Iif):
    """
** Write as a FP  the enabledMailAcct.
"""
    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 1, 'Max': 1,}
    
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

        G = icm.IicmGlobalContext()        

        iicmRunArgs = G.iimRunArgsGet()
        for each in iicmRunArgs.iifArgs:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(
                    controlBaseDirGet(),
                    "common",
                    "selections",
                    "fp",
                    "enabledInMailAcct",
                ),
                parValue=each,
            )

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=each,
        )



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailAcctGet    [[elisp:(org-cycle)][| ]]
"""
class enabledOutMailAcctGet(icm.Iif):
    """
** Output the current enabledMailAcct
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
    
        enabledOutMailAcct = enabledOutMailAcctObtain()
 
        if interactive:
            icm.ANN_write(enabledOutMailAcct)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=enabledOutMailAcct,
        )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailAcctSet    [[elisp:(org-cycle)][| ]]
"""
class enabledOutMailAcctSet(icm.Iif):
    """
** Write as a FP  the enabledMailAcct.
"""
    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 1, 'Max': 1,}
    
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

        G = icm.IicmGlobalContext()        

        iicmRunArgs = G.iimRunArgsGet()
        for each in iicmRunArgs.iifArgs:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(
                    controlBaseDirGet(),
                    "common",
                    "selections",
                    "fp",
                    "enabledOutMailAcct",
                ),
                parValue=each,
            )

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=each,
        )


    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailBoxGet    [[elisp:(org-cycle)][| ]]
"""
class enabledMailBoxGet(icm.Iif):
    """
** Output the current enabledMailBox
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
    
        enabledMailBox = enabledMailBoxObtain()
 
        if interactive:
            icm.ANN_write(enabledMailBox)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=enabledMailBox,
        )
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  enabledMailBoxSet    [[elisp:(org-cycle)][| ]]
"""
class enabledMailBoxSet(icm.Iif):
    """
** Write as a FP  the enabledMailBox.
"""
    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 1, 'Max': 1,}
    
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

        G = icm.IicmGlobalContext()        

        iicmRunArgs = G.iimRunArgsGet()
        for each in iicmRunArgs.iifArgs:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(
                    controlBaseDirGet(),
                    "common",
                    "selections",
                    "fp",
                    "enabledMailBox",
                ),
                parValue=each,
            )

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=each,
        )
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  inMailAcctAccessParsGet    [[elisp:(org-cycle)][| ]]
"""
class inMailAcctParsGet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct']       
    iifArgsLen = {'Min': 0, 'Max': 3,}
    iifArgsSpec = {0: ['access', 'controllerInfo', 'retrieval']}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct" :args "parTypes"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
        parTypes=None,         # or Args-Input
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

        G = icm.IicmGlobalContext()

        validParTypes = self.__class__.iifArgsSpec[0]

        if not parTypes:
            parTypes = G.iimRunArgsGet().iifArgs
        if not parTypes:
            parTypes = validParTypes
            
        for each in parTypes:
            if each in validParTypes:
                fpBaseDir = os.path.join(
                    inMailAcctDirGet(controlProfile, inMailAcct),
                    each,
                )
                FP_readTreeAtBaseDir_CmndOutput(
                    interactive=interactive,
                    fpBaseDir=fpBaseDir,
                    iifOutcome=iifOutcome,
                )
            else:
                icm.EH_usageError("")
                continue

        return iifOutcome
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  inMailAcctAccessParsSet    [[elisp:(org-cycle)][| ]]
"""    
class inMailAcctAccessParsSet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct', 'userName', 'userPasswd', 'imapServer']       
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct userName userPasswd imapServer"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
        userName=None,         # or Cmnd-Input
        userPasswd=None,         # or Cmnd-Input
        imapServer=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, 'userName': userName, 'userPasswd': userPasswd, 'imapServer': imapServer, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
        userName = callParamsDict['userName']
        userPasswd = callParamsDict['userPasswd']
        imapServer = callParamsDict['imapServer']
####+END:

        G = icm.IicmGlobalContext()        

        inMailAcctDir = os.path.join(
            inMailAcctDirGet(inMailAcct),
            "access",
        )

        if userName:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "userName"),
                parValue=userName,
            )

        if userPasswd:            
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "userPasswd"),
                parValue=userPasswd,
            )
            
        if imapServer:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "imapServer"),
                parValue=imapServer,
            )
        
        if interactive:
            icm.ANN_here(inMailAcctDir)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=inMailAcctDir,
        )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  inMailAcctControllerInfoParsSet    [[elisp:(org-cycle)][| ]]
"""
class inMailAcctControllerInfoParsSet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct', 'firstName', 'lastName']
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct firstName lastName"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
        firstName=None,         # or Cmnd-Input
        lastName=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, 'firstName': firstName, 'lastName': lastName, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
        firstName = callParamsDict['firstName']
        lastName = callParamsDict['lastName']
####+END:

        G = icm.IicmGlobalContext()        

        inMailAcctDir = os.path.join(
            inMailAcctDirGet(inMailAcct),
            "controllerInfo",
        )

        if firstName:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "firstName"),
                parValue=firstName,
            )

        if lastName:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "lastName"),
                parValue=lastName,
            )
        
        if interactive:
            icm.ANN_here(inMailAcctDir)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=inMailAcctDir,
        )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  inMailAcctRetrievalParsSet    [[elisp:(org-cycle)][| ]]
"""
class inMailAcctRetrievalParsSet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'inMailAcct', 'inMailAcctMboxesPath', 'mboxesList', 'ssl']       
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile inMailAcct inMailAcctMboxesPath mboxesList ssl"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        inMailAcct=None,         # or Cmnd-Input
        inMailAcctMboxesPath=None,         # or Cmnd-Input
        mboxesList=None,         # or Cmnd-Input
        ssl=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'inMailAcct': inMailAcct, 'inMailAcctMboxesPath': inMailAcctMboxesPath, 'mboxesList': mboxesList, 'ssl': ssl, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        inMailAcct = callParamsDict['inMailAcct']
        inMailAcctMboxesPath = callParamsDict['inMailAcctMboxesPath']
        mboxesList = callParamsDict['mboxesList']
        ssl = callParamsDict['ssl']
####+END:

        G = icm.IicmGlobalContext()        

        inMailAcctDir = os.path.join(
            inMailAcctDirGet(controlProfile, inMailAcct),
        "retrieval",
        )

        if inMailAcctMboxesPath: (           
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "inMailAcctMboxesPath"),
                parValue=os.path.abspath(
                    inMailAcctMboxesPath,
                )))

        if mboxesList: (           
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "mboxesList"),
                parValue=mboxesList,
                ))

        if ssl: (
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(inMailAcctDir, "ssl"),
                parValue=ssl,
            ))
            
        if interactive:
            icm.ANN_here(inMailAcctDir)

        return (
            iifOutcome.set(
                opError=icm.OpError.Success,
                opResults=inMailAcctDir,
            ))
    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  outMailAcctParsGet    [[elisp:(org-cycle)][| ]]
"""
class outMailAcctParsGet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = ['controlProfile', 'outMailAcct']       
    iifArgsLen = {'Min': 0, 'Max': 0,}
    iifArgsSpec = {0: ['access', 'controllerInfo', 'submission']}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile outMailAcct" :args "parTypes"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        outMailAcct=None,         # or Cmnd-Input
        parTypes=None,         # or Args-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'outMailAcct': outMailAcct, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        outMailAcct = callParamsDict['outMailAcct']
####+END:

        G = icm.IicmGlobalContext()

        validParTypes = self.__class__.iifArgsSpec[0]

        if not parTypes:
            parTypes = G.iimRunArgsGet().iifArgs
        if not parTypes:
            parTypes = validParTypes
            
        for each in parTypes:
            if each in validParTypes:
                fpBaseDir = os.path.join(
                    outMailAcctDirGet(controlProfile, outMailAcct),
                    each,
                )
                FP_readTreeAtBaseDir_CmndOutput(
                    interactive=interactive,
                    fpBaseDir=fpBaseDir,
                    iifOutcome=iifOutcome,
                )
            else:
                icm.EH_usageError("")
                continue

        return iifOutcome
    
    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  outMailAcctAccessParsSet    [[elisp:(org-cycle)][| ]]
"""    
class outMailAcctParsSet(icm.Iif):
    """."""

    iifParamsMandatory = []
    iifParamsOptional = [
        'controlProfile', 'outMailAcct',
        'userName', 'userPasswd', 'mtaRemHost', 'mtaRemProtocol',
        'firstName', 'lastName',
        'sendingMethod', 'envelopeAddr',
    ]       
    iifArgsLen = {'Min': 1, 'Max': 1,}
    iifArgsSpec = {0: ['access', 'controllerInfo', 'submission']}


####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "controlProfile outMailAcct userName userPasswd mtaRemHost mtaRemProtocol firstName lastName sendingMethod envelopeAddr" :args "parGroup"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        controlProfile=None,         # or Cmnd-Input
        outMailAcct=None,         # or Cmnd-Input
        userName=None,         # or Cmnd-Input
        userPasswd=None,         # or Cmnd-Input
        mtaRemHost=None,         # or Cmnd-Input
        mtaRemProtocol=None,         # or Cmnd-Input
        firstName=None,         # or Cmnd-Input
        lastName=None,         # or Cmnd-Input
        sendingMethod=None,         # or Cmnd-Input
        envelopeAddr=None,         # or Cmnd-Input
        parGroup=None,         # or Args-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'controlProfile': controlProfile, 'outMailAcct': outMailAcct, 'userName': userName, 'userPasswd': userPasswd, 'mtaRemHost': mtaRemHost, 'mtaRemProtocol': mtaRemProtocol, 'firstName': firstName, 'lastName': lastName, 'sendingMethod': sendingMethod, 'envelopeAddr': envelopeAddr, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        controlProfile = callParamsDict['controlProfile']
        outMailAcct = callParamsDict['outMailAcct']
        userName = callParamsDict['userName']
        userPasswd = callParamsDict['userPasswd']
        mtaRemHost = callParamsDict['mtaRemHost']
        mtaRemProtocol = callParamsDict['mtaRemProtocol']
        firstName = callParamsDict['firstName']
        lastName = callParamsDict['lastName']
        sendingMethod = callParamsDict['sendingMethod']
        envelopeAddr = callParamsDict['envelopeAddr']
####+END:

        G = icm.IicmGlobalContext()

        validParGroups = self.__class__.iifArgsSpec[0]

        if not parGroup:
            parGroup = G.iimRunArgsGet().iifArgs[0]

        if not parGroup in validParGroups:
            return icm.EH_badUsage("mis-match")

        outMailAcctDir = os.path.join(
            outMailAcctDirGet(controlProfile, outMailAcct),
        )

        if parGroup == "access":
            if userName:
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "userName"),
                    parValue=userName,
                )

            if userPasswd:                        
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "userPasswd"),
                    parValue=userPasswd,
                )

            if mtaRemHost:
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "mtaRemHost"),
                    parValue=mtaRemHost,
                )
                
            if mtaRemProtocol:
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "mtaRemProtocol"),
                    parValue=mtaRemProtocol,
                )
                
        elif parGroup == "controllerInfo":
            if firstName:                        
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "firstName"),
                    parValue=firstName,
                )

            if lastName:
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "lastName"),
                    parValue=lastName,
                )

        elif parGroup == "submission":
            if sendingMethod:                        
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "sendingMethod"),
                    parValue=sendingMethod,
                )

            if envelopeAddr:
                icm.FILE_ParamWriteToPath(
                    parNameFullPath=os.path.join(outMailAcctDir, parGroup, "envelopeAddr"),
                    parValue=envelopeAddr,
                )
            
        else:
            return icm.EH_badUsage("OOPS")
        
        if interactive:
            icm.ANN_here(outMailAcctDir)

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=outMailAcctDir,
        )
    

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *End Of Editable Text*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [COMMON]      :: /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
"""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall

####+END:

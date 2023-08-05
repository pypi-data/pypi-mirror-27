# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  A /library/ to support icmsPkg facilities
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


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Base Directory Locations*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  pkgBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def pkgBaseDir_obtain():
    return os.path.abspath(
        ".."
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  pkgInfoBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def pkgInfoBaseDir_obtain():
    return os.path.abspath(
        "../pkgInfo"
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF       ::  pkgInputsBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def pkgInputsBaseDir_obtain():
    return os.path.abspath(
        "../pkgInputs"
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  pkgInfoFpBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def pkgInfoFpBaseDir_obtain():
    return os.path.abspath(
        "../pkgInfo/fp"
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  controlBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def controlBaseDir_obtain():
    return(
        icm.FILE_ParamValueReadFrom(
            parRoot="../pkgInfo/fp",
            parName="icmsPkgControlBaseDir")
    )


def logBaseDir_obtain():
    return(
        icm.FILE_ParamValueReadFrom(
            parRoot="../pkgInfo/fp",
            parName="icmsPkgLogBaseDir")
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  varBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def varBaseDir_obtain():
    return(
        icm.FILE_ParamValueReadFrom(
            parRoot="../pkgInfo/fp",
            parName="icmsPkgVarBaseDir")
    )


def varConfigBaseDir_obtain():
    return(
        os.path.join(varBaseDir_obtain(), "config")
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  tmpBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def tmpBaseDir_obtain():
    return(
        icm.FILE_ParamValueReadFrom(
            parRoot="../pkgInfo/fp",
            parName="icmsPkgTmpBaseDir")
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF          ::  icmsBxoBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def icmsBxoBaseDir_obtain():
    return os.path.abspath(
        "../../.."
    )

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || IIF          ::  icmsRunEnvBaseDir_obtain    [[elisp:(org-cycle)][| ]]
"""
def icmsRunEnvBaseDir_obtain():
    return icmsBxoBaseDir_obtain()


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *File Parameters Obtain*
"""


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  icmsPkgName_fpObtain    [[elisp:(org-cycle)][| ]]
"""
def icmsPkgName_fpObtain():
    """NOTYET -- Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            pkgInfoFpBaseDir_obtain(),
        ),
        parName="icmsPkgName",
    )


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  icmsPkgControlBaseDir_fpObtain    [[elisp:(org-cycle)][| ]]
"""
def icmsPkgControlBaseDir_fpObtain():
    """NOTYET -- Called obtain to leave Get for the IIF"""
    return icm.FILE_ParamValueReadFrom(
        parRoot=os.path.join(
            pkgInfoFpBaseDir_obtain(),            
        ),
        parName="icmsPkgControlBaseDir",        
    )



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common Arguments Specification*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  commonParamsSpecify    [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
        iicmParams,
):
    
    iicmParams.parDictAdd(
        parName='icmsPkgName',
        parDescription="ICMs Package Name",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgName',
    )
    
    iicmParams.parDictAdd(
        parName='icmsPkgRunBaseDir',
        parDescription="ICMs Package Run Environment -- A BaseDir for var/log/tmp (bxo=current bxo)",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgRunBaseDir',
    )
    
    iicmParams.parDictAdd(
        parName='icmsPkgControlBaseDir',
        parDescription="ICMs Package Control Base Directory",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgControlBaseDir',
    )
    
    iicmParams.parDictAdd(
        parName='icmsPkgVarBaseDir',
        parDescription="ICMs Package Var Base Directory",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgVarBaseDir',
    )

    
    iicmParams.parDictAdd(
        parName='icmsPkgLogBaseDir',
        parDescription="ICMs Package Log Base Directory",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgLogBaseDir',
    )

        
    iicmParams.parDictAdd(
        parName='icmsPkgTmpBaseDir',
        parDescription="ICMs Package Tmp Base Directory",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--icmsPkgTmpBaseDir',
    )


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Common Examples Sections*
"""
    

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_pkgInfoPars    [[elisp:(org-show-subtree)][|=]]   [[elisp:(org-cycle)][| ]]
"""    
def examples_pkgInfoPars():
    """
** Auxiliary examples to be commonly used.
"""
    icm.iifExampleMenuChapter('* =FP Values=  pkgInfo Parameters')

    iifAction = " -i inMailAcctParsGet" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, verbosity='none')

    menuLine = """"""
    icm.iifExampleMenuItem(menuLine, icmName="pkgManage.py", verbosity='none')    

    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func         ::  examples_pkgInfoParsFull    [[elisp:(org-cycle)][| ]]
"""
def examples_pkgInfoParsFull(
    icmsPkgName,
    icmsPkgControlBaseDir=None,
    icmsPkgRunBaseDir=None,
):
    """
** Auxiliary examples to be commonly used.
"""
    icm.iifExampleMenuChapter(' =FP Values=  *pkgInfo Get Parameters*')    

    iifAction = " -i pkgInfoParsGet" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, verbosity='none')

    icm.iifExampleMenuChapter(' =FP Values=  *PkgInfo Defaults ParsSet  --*')

    cmndName = "pkgInfoParsDefaultsSet" ; cmndArgs = "bystarPolicy" ;
    cps = collections.OrderedDict() ; cps['icmsPkgName'] = icmsPkgName 
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
    cmndName = "pkgInfoParsDefaultsSet" ; cmndArgs = "bxoPolicy" ;
    cps = collections.OrderedDict() ; cps['icmsPkgName'] = icmsPkgName ; cps['icmsPkgControlBaseDir'] = icmsPkgControlBaseDir 
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
    cmndName = "pkgInfoParsDefaultsSet" ; cmndArgs = "runBaseDirPolicy" ;
    cps = collections.OrderedDict() ; cps['icmsPkgName'] = icmsPkgName
    cps['icmsPkgControlBaseDir'] = icmsPkgControlBaseDir ; cps['icmsPkgRunBaseDir'] = icmsPkgRunBaseDir
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
    cmndName = "pkgInfoParsDefaultsSet" ; cmndArgs = "debianPolicy" ;
    cps = collections.OrderedDict() ; cps['icmsPkgName'] = icmsPkgName 
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
    cmndName = "pkgInfoParsDefaultsSet" ; cmndArgs = "centosPolicy" ;
    cps = collections.OrderedDict() ; cps['icmsPkgName'] = icmsPkgName 
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    

    icm.iifExampleMenuChapter(' =FP Values=  *PkgInfo ParsSet -- Set Parameters Explicitly*')

    iifAction = " -i pkgInfoParsSet" ; iifArgs = ""
    menuLine = """--icmsPkgName="pkgName" {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    iifAction = " -i pkgInfoParsSet" ; iifArgs = ""
    menuLine = """--icmsPkgControlBaseDir="path"  {iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    iifAction = " -i pkgInfoParsSet" ; iifArgs = ""
    varPath = os.path.join(icmsRunEnvBaseDir_obtain(), "var", icmsPkgName_fpObtain())
    menuLine = """--icmsPkgVarBaseDir={varPath}  {iifAction} {iifArgs}""".format(
        varPath=varPath, iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')

    iifAction = " -i pkgInfoParsSet" ; iifArgs = ""
    tmpPath = os.path.join(icmsRunEnvBaseDir_obtain(), "tmp", icmsPkgName_fpObtain())
    menuLine = """--icmsPkgTmpBaseDir={tmpPath}  {iifAction} {iifArgs}""".format(
        tmpPath=tmpPath, iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="echo", verbosity='none')
    
    icm.iifExampleMenuChapter(' =RunEnv=  *Run Environment (BaseDirs) Setups/Clean*')    

    iifAction = " -i icmsRunEnvsPreps" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    iifAction = " -i icmsRunEnvsClean" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    icm.iifExampleMenuChapter(' =RunEnv=  *SymLinks To var/log/tmp/ Setups/Clean*')    

    iifAction = " -i icmsRunEnvsLinks" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    iifAction = " -i icmsRunEnvsLinksClean" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    icm.iifExampleMenuChapter(' =RunEnv=  *SymLinks To Libraries Setups/Clean*')    
    
    iifAction = " -i icmsLibsLinks" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')

    iifAction = " -i icmsLibsLinksClean" ; iifArgs = ""
    menuLine = """{iifAction} {iifArgs}""".format(iifAction=iifAction, iifArgs=iifArgs)
    icm.iifExampleMenuItem(menuLine, icmWrapper="", verbosity='none')
     
    

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
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  pkgInfoParsGet    [[elisp:(org-cycle)][| ]]
"""
class pkgInfoParsGet(icm.Iif):
    """
** Read File Parameters at pkgInfo/fp
"""

    iifParamsMandatory = []
    iifParamsOptional = []       
    iifArgsLen = {'Min': 0, 'Max': 0,}
    iifArgsSpec = {}    

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "" :args ""
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

        FP_readTreeAtBaseDir_CmndOutput(
            interactive=interactive,
            fpBaseDir=pkgInfoFpBaseDir_obtain(),
            iifOutcome=iifOutcome,
        )

        return iifOutcome


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  pkgInfoParsSet    [[elisp:(org-cycle)][| ]]
"""    
class pkgInfoParsSet(icm.Iif):
    """
** Set File Parameters at ../pkgInfo/fp
"""

    iifParamsMandatory = []
    iifParamsOptional = ['icmsPkgName', 'icmsPkgControlBaseDir', 'icmsPkgVarBaseDir',
                         'icmsPkgTmpBaseDir', 'icmsPkgBasesPolicy', 'icmsPkgLogBaseDir']       
    iifArgsLen = {'Min': 0, 'Max': 0,}

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "icmsPkgName icmsPkgBasesPolicy icmsPkgControlBaseDir icmsPkgVarBaseDir icmsPkgLogBaseDir icmsPkgTmpBaseDir"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        icmsPkgName=None,         # or Cmnd-Input
        icmsPkgBasesPolicy=None,         # or Cmnd-Input
        icmsPkgControlBaseDir=None,         # or Cmnd-Input
        icmsPkgVarBaseDir=None,         # or Cmnd-Input
        icmsPkgLogBaseDir=None,         # or Cmnd-Input
        icmsPkgTmpBaseDir=None,         # or Cmnd-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'icmsPkgName': icmsPkgName, 'icmsPkgBasesPolicy': icmsPkgBasesPolicy, 'icmsPkgControlBaseDir': icmsPkgControlBaseDir, 'icmsPkgVarBaseDir': icmsPkgVarBaseDir, 'icmsPkgLogBaseDir': icmsPkgLogBaseDir, 'icmsPkgTmpBaseDir': icmsPkgTmpBaseDir, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        icmsPkgName = callParamsDict['icmsPkgName']
        icmsPkgBasesPolicy = callParamsDict['icmsPkgBasesPolicy']
        icmsPkgControlBaseDir = callParamsDict['icmsPkgControlBaseDir']
        icmsPkgVarBaseDir = callParamsDict['icmsPkgVarBaseDir']
        icmsPkgLogBaseDir = callParamsDict['icmsPkgLogBaseDir']
        icmsPkgTmpBaseDir = callParamsDict['icmsPkgTmpBaseDir']
####+END:

        #G = icm.IicmGlobalContext()        

        def createPathAndFpWrite(
                fpPath,
                valuePath,
        ):
            valuePath = os.path.abspath(valuePath)
            try:
                os.makedirs(valuePath)
            except OSError:
                if not os.path.isdir(valuePath):
                    raise
            
            icm.FILE_ParamWriteToPath(
                parNameFullPath=fpPath,
                parValue=valuePath,
            )

            
        if icmsPkgName:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgName"),
                parValue=icmsPkgName,
            )

        if icmsPkgBasesPolicy:
            icm.FILE_ParamWriteToPath(
                parNameFullPath=os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgBasesPolicy"),
                parValue=icmsPkgBasesPolicy,
            )

        if icmsPkgControlBaseDir:
            createPathAndFpWrite(
                os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgControlBaseDir"),
                icmsPkgControlBaseDir,
            )

        if icmsPkgVarBaseDir:
            createPathAndFpWrite(
                os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgVarBaseDir"),
                icmsPkgVarBaseDir,
            )

        if icmsPkgLogBaseDir:
            createPathAndFpWrite(
                os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgLogBaseDir"),
                icmsPkgLogBaseDir,
            )
            
        if icmsPkgTmpBaseDir:
            createPathAndFpWrite(
                os.path.join(pkgInfoFpBaseDir_obtain(), "icmsPkgTmpBaseDir"),
                icmsPkgTmpBaseDir,
            )
            
        if interactive:
            icm.ANN_here("pkgInfoParsSet")

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )



    
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  pkgInfoParsDefaultsSet    [[elisp:(org-cycle)][| ]]
"""
class pkgInfoParsDefaultsSet(icm.Iif):
    """
** Set File Parameters at ../pkgInfo/fp -- By default
** TODO NOTYET auto detect marme.dev -- marme.control and decide where they should be, perhaps in /var/
"""

    iifParamsMandatory = ['icmsPkgName']
    iifParamsOptional = ['icmsPkgControlBaseDir', 'icmsPkgRunBaseDir']           
    iifArgsLen = {'Min': 0, 'Max': 1,}
    iifArgsSpec = {0: ['any']}    
    

####+BEGIN: bx:dblock:python:iim:iif:parsValidate :par "icmsPkgName icmsPkgControlBaseDir icmsPkgRunBaseDir" :args "basesPolicy"
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        icmsPkgName=None,         # or Cmnd-Input
        icmsPkgControlBaseDir=None,         # or Cmnd-Input
        icmsPkgRunBaseDir=None,         # or Cmnd-Input
        basesPolicy=None,         # or Args-Input
    ):
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'icmsPkgName': icmsPkgName, 'icmsPkgControlBaseDir': icmsPkgControlBaseDir, 'icmsPkgRunBaseDir': icmsPkgRunBaseDir, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        icmsPkgName = callParamsDict['icmsPkgName']
        icmsPkgControlBaseDir = callParamsDict['icmsPkgControlBaseDir']
        icmsPkgRunBaseDir = callParamsDict['icmsPkgRunBaseDir']
####+END:
        G = icm.IicmGlobalContext()

        #basesPolicyChoices = self.__class__.iifArgsSpec[0]

        if not basesPolicy:
            basesPolicy = G.iimRunArgsGet().iifArgs[0]

        pkgInfoParsSet().iif(
            interactive=False,
            icmsPkgName=icmsPkgName,  
        )

        if basesPolicy == "byStarPolicy":
            return icm.EH_badUsage("")

        elif basesPolicy == "bxoPolicy":
            if not icmsPkgControlBaseDir:
                return icm.EH_badUsage("")

            controlPath = icmsPkgControlBaseDir
            varPath = os.path.join(icmsRunEnvBaseDir_obtain(), "var", icmsPkgName_fpObtain())
            logPath = os.path.join(icmsRunEnvBaseDir_obtain(), "log", icmsPkgName_fpObtain())            
            tmpPath = os.path.join(icmsRunEnvBaseDir_obtain(), "tmp", icmsPkgName_fpObtain())

        elif basesPolicy == "runBaseDirPolicy":
            if not icmsPkgRunBaseDir:
                return icm.EH_badUsage("")
            
            if icmsPkgControlBaseDir:
                controlPath = icmsPkgControlBaseDir
            else:
                controlPath = os.path.join(icmsPkgRunBaseDir, "control", icmsPkgName_fpObtain())

            varPath = os.path.join(icmsPkgRunBaseDir, "var", icmsPkgName_fpObtain())
            logPath = os.path.join(icmsPkgRunBaseDir, "log", icmsPkgName_fpObtain())            
            tmpPath = os.path.join(icmsPkgRunBaseDir, "tmp", icmsPkgName_fpObtain())
            
        elif basesPolicy == "debianPolicy":
            controlPath = os.path.join("/etc/bystar", icmsPkgName)
            varPath = os.path.join("/var/lib/bystar/", icmsPkgName)
            logPath = os.path.join("/var/log/bystar/", icmsPkgName)            
            tmpPath = os.path.join("/tmp/bystar", icmsPkgName)
            
        elif basesPolicy == "centosPolicy":
            controlPath = os.path.join("/etc/bystar", icmsPkgName)
            varPath = os.path.join("/var/lib/bystar/", icmsPkgName)
            logPath = os.path.join("/var/log/bystar/", icmsPkgName)            
            tmpPath = os.path.join("/tmp/bystar", icmsPkgName)
            
        else:
            icm.EH_critical_oops("")

        pkgInfoParsSet().iif(
            interactive=False,
            icmsPkgBasesPolicy=basesPolicy,
            icmsPkgControlBaseDir=controlPath,
            icmsPkgVarBaseDir=varPath,
            icmsPkgLogBaseDir=logPath,            
            icmsPkgTmpBaseDir=tmpPath,
        )

        
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Run Envs Setup/Clean*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsRunEnvsPreps    [[elisp:(org-cycle)][| ]]
"""
class icmsRunEnvsPreps(icm.Iif):
    """
** Create run time environment directories (tmp var)
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

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsRunEnvsClean    [[elisp:(org-cycle)][| ]]
"""        
class icmsRunEnvsClean(icm.Iif):
    """
** Remove run time environment directories (tmp var)
    opDo rm -r "${icmsRunEnvBaseDir}/tmp/${icmsPkgName}"
    opDo rm -r "${icmsRunEnvBaseDir}/var/${icmsPkgName}"
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

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsRunEnvLinks    [[elisp:(org-cycle)][| ]]
"""        
class icmsRunEnvLinks(icm.Iif):
    """
** Create links for ../tmp ../var and ../control
    opDo rm -r "${icmsRunEnvBaseDir}/tmp/${icmsPkgName}"
    opDo rm -r "${icmsRunEnvBaseDir}/var/${icmsPkgName}"
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

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsRunEnvLinksClean    [[elisp:(org-cycle)][| ]]
"""        
class icmsRunEnvLinksClean(icm.Iif):
    """
** Remove links of ../tmp ../var and ../control
    opDo FN_fileSymlinkRemoveIfThere "${icmsPkgBaseDir}/tmp"
    opDo FN_fileSymlinkRemoveIfThere "${icmsPkgBaseDir}/var"

    opDo FN_fileSymlinkRemoveIfThere "${controlsBaseDir}"
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
        
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsLibsLinks    [[elisp:(org-cycle)][| ]]
"""        
class icmsLibsLinks(icm.Iif):
    """
** Creates links in ../lib/python/
    opDo FN_fileSymlinkUpdate /de/bx/nne/dev-py/libs/iicmPkg/iicm ${icmsPkgBaseDir}/lib/python/iicm
    opDo FN_fileSymlinkUpdate /de/bx/nne/dev-py/libs/bxMsgPkg/bxMsg ${icmsPkgBaseDir}/lib/python/bxMsg
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

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-IIF    ::  icmsLibsLinksClean    [[elisp:(org-cycle)][| ]]
"""        
class icmsLibsLinksClean(icm.Iif):
    """
** Remove links in ../lib/python/
    opDo FN_fileSymlinkRemoveIfThere ${icmsPkgBaseDir}/lib/python/iicm
    opDo FN_fileSymlinkRemoveIfThere ${icmsPkgBaseDir}/lib/python/bxMsg    
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
        


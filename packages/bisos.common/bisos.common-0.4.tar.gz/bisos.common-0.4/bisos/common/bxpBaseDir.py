# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  A /library/ to support icmsPkg facilities
"""
"""
####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
* 
*  An Interactively Command Module (ICM) :: Best Used With Blee-IICM-Players in Emacs -- Part Of ByStar
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

####+BEGIN: bx:dblock:python:section :title "Imports"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Imports*
"""
####+END:


####+BEGINNOT: bx:dblock:global:file-insert :file "" Add Path As ParameterNOTYET
####+BEGIN: bx:dblock:python:func :funcName "insertPathForImports" :funcType "FrameWrk" :retType "none" :deco "" :argsList "path"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-FrameWrk  :: /insertPathForImports/ retType=none argsList=(path)  [[elisp:(org-cycle)][| ]]
"""
def insertPathForImports(
    path,
):
####+END:
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


####+BEGIN: bx:dblock:python:icmItem :itemType "=Imports=" :itemTitle "IMPORTS"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=      :: IMPORTS  [[elisp:(org-cycle)][| ]]
"""
####+END:

import os
import collections
import enum

from unisos import ucf
from unisos import icm


####+BEGIN: bx:dblock:python:section :title "Library Description (Overview)"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Library Description (Overview)*
"""
####+END:

####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "overview_bxpBaseDir" :parsMand "" :parsOpt "" :argsMin "0" :argsMax "3" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /overview_bxpBaseDir/ parsMand= parsOpt= argsMin=0 argsMax=3 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class overview_bxpBaseDir(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ ]
    iifArgsLen = {'Min': 0, 'Max': 3,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        argsList=None,         # or Args-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome
            effectiveArgsList = G.iimRunArgsGet().iifArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {}
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
####+END:

        moduleDescription="""
*       [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**  [[elisp:(org-cycle)][| ]]	Model and Terminology 					   :Overview:
*** bxpRootXxFile   -- /etc/bystarRoot, ~/.bystarRoot, /bystar
*** bxpRoot         -- Base For This Module
*** bpb             -- ByStar Platform Base, Location Of Relevant Parts (Bisos, blee, bsip
*** bpd             -- ByStar Platform Directory (Object), An instance of Class BxpBaseDir
**      [End-Of-Description]
"""
        
        moduleUsage="""
*       [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos:
**      [End-Of-Usage]
"""
        
        moduleStatus="""
*       [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  Current         :: Just getting started [[elisp:(org-cycle)][| ]]
**      [End-Of-Status]
"""
        cmndArgsSpec = {"0&-1": ['moduleDescription', 'moduleUsage', 'moduleStatus']}
        cmndArgsValid = cmndArgsSpec["0&-1"]
        for each in effectiveArgsList:
            if each in cmndArgsValid:
                print each
                if interactive:
                    #print( str( __doc__ ) )  # This is the Summary: from the top doc-string
                    #version(interactive=True)
                    exec("""print({})""".format(each))
                
        return(format(str(__doc__)+moduleDescription))

####+BEGIN: bx:dblock:python:section :title "Directory Base Locations"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Directory Base Locations*
"""
####+END:


####+BEGIN: bx:dblock:python:subSection :title "ByStar Root"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *ByStar Root*
"""
####+END:



####+BEGIN: bx:dblock:python:func :funcName "bxpRootBaseDirPtrSysFile_obtain" :comment "/etc/bystarRoot" :funcType "obtain" :retType "str" :argsList "" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bxpRootBaseDirPtrSysFile_obtain/ =/etc/bystarRoot= retType=str argsList=nil deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bxpRootBaseDirPtrSysFile_obtain(
):
####+END:
    return os.path.abspath(
        "/etc/bystarRoot"
    )


####+BEGIN: bx:dblock:python:func :funcName "bxpRootBaseDirPtrUserFile_obtain" :comment "~/.bystarRoot" :funcType "obtain" :retType "str" :argsList "" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bxpRootBaseDirPtrUserFile_obtain/ =~/.bystarRoot= retType=str argsList=nil deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bxpRootBaseDirPtrUserFile_obtain(
):
####+END:
    return os.path.abspath(
        os.path.expanduser(
            "~/.bystarRoot"
        )
    )

####+BEGIN: bx:dblock:python:func :funcName "bxpRootBaseDirDefault_obtain" :comment "/bystar" :funcType "obtain" :retType "str" :argsList "" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bxpRootBaseDirDefault_obtain/ =~/.bystarRoot= retType=str argsList=nil deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bxpRootBaseDirDefault_obtain(
):
####+END:
    return os.path.abspath(
        "/bystar"
    )


####+BEGIN: bx:dblock:python:subSection :title "BISOS Bases"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *BISOS Bases*
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "bpbDist_baseObtain_bin" :comment "BISOS" :funcType "obtain" :retType "str" :argsList "baseDir" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbDist_baseObtain_bin/ =BISOS= retType=str argsList=(baseDir) deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bpbDist_baseObtain_bin(
    baseDir,
):
####+END:
    """
** /bystar/dist/pip/bisos/bin
"""
    bxpRoot = bxpRoot_baseObtain(baseDir)            

    return( os.path.join(
        bxpRoot, "dist/pip/bisos", "bin"
    ))

####+BEGIN: bx:dblock:python:func :funcName "bpbDist_baseObtain_input" :comment "DATA" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbDist_baseObtain_input/ =DATA= retType=bool argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbDist_baseObtain_input(
    baseDir,
):
####+END:
    """
** /bystar/dist/pip/bisos/input
"""
    bxpRoot = bxpRoot_baseObtain(baseDir)                

    return( os.path.join(
        bxpRoot, "dist/pip/bisos", "input"
    ))


####+BEGIN: bx:dblock:python:func :funcName "bpbBisos_baseObtain_bin" :comment "BISOS" :funcType "obtain" :retType "str" :argsList "baseDir" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisos_baseObtain_bin/ =BISOS= retType=str argsList=(baseDir) deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bpbBisos_baseObtain_bin(
    baseDir,
):
####+END:
    bxpRoot = bxpRoot_baseObtain()            

    return( os.path.join(
        bxpRoot, "bisos", "bin"
    ))

####+BEGIN: bx:dblock:python:func :funcName "bpbBisos_baseObtain_input" :comment "DATA" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisos_baseObtain_input/ =DATA= retType=bool argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisos_baseObtain_input(
    baseDir,
):
####+END:
    bxpRoot = bxpRoot_baseObtain()                

    return( os.path.join(
        bxpRoot, "bisos", "input"
    ))


####+BEGIN: bx:dblock:python:subSection :title "BISOS Pkg Bases"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *BISOS Pkg Bases*
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "bpbBisosPkg_baseObtain_var" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisosPkg_baseObtain_var/ retType=bool argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisosPkg_baseObtain_var(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return( os.path.join(
        outcome.results, "unisos", "data"
    ))

####+BEGIN: bx:dblock:python:func :funcName "bpbBisosPkg_baseObtain_tmp" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisosPkg_baseObtain_tmp/ funcType=obtain retType=bool deco= argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisosPkg_baseObtain_tmp(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return( os.path.join(
        outcome.results, "unisos", "data"
    ))

####+BEGIN: bx:dblock:python:func :funcName "bpbBisosPkg_baseObtain_log" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisosPkg_baseObtain_log/ funcType=obtain retType=bool deco= argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisosPkg_baseObtain_log(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return( os.path.join(
        outcome.results, "unisos", "data"
    ))


####+BEGIN: bx:dblock:python:func :funcName "bpbBisosPkg_baseObtain_control" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisosPkg_baseObtain_control/ funcType=obtain retType=bool deco= argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisosPkg_baseObtain_control(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return( os.path.join(
        outcome.results, "unisos", "data"
    ))



####+BEGIN: bx:dblock:python:func :funcName "bpbBisosPkg_baseObtain_input" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bpbBisosPkg_baseObtain_input/ funcType=obtain retType=bool deco= argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisosPkg_baseObtain_input(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return( os.path.join(
        outcome.results, "unisos", "data"
    ))


####+BEGIN: bx:dblock:python:section :title "Common Arguments Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Arguments Specification*
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "icmParams"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-ParSpec   :: /commonParamsSpecify/ retType= argsList=(icmParams)  [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
    icmParams,
):
####+END:
    icmParams.parDictAdd(
        parName='baseDir',
        parDescription="Bx Platform Base Dir",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--baseDir',
    )

    icmParams.parDictAdd(
        parName='pbdName',
        parDescription="Platform BaseDirs Dict Name",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.IIM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--pbdName',
    )

        
####+BEGIN: bx:dblock:python:section :title "Common Examples Sections"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Examples Sections*
"""
####+END:

####+BEGIN: bx:dblock:python:func :funcName "examples_bxPlatformBaseDirsCommon" :funcType "examples" :retType "none" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-examples  :: /examples_bxPlatformBaseDirsCommon/ retType=none argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def examples_bxPlatformBaseDirsCommon(
):
####+END:
    icm.iifExampleMenuChapter('* =BxP BaseDir=  ByStar Platform Base Dirs')

    cmndName = "bxRootGet" ; cmndArgs = "" ;
    cps = collections.OrderedDict()
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    cmndName = "bxRootGet" ; cmndArgs = "" ;
    cps = collections.OrderedDict() ;  cps['baseDir'] = '/tmp/bxBase'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    icm.ex_gExecMenuItem(execLine="""cat {}""".format(bxpRootBaseDirPtrUserFile_obtain()),)
    icm.ex_gExecMenuItem(execLine="""cat {}""".format(bxpRootBaseDirPtrSysFile_obtain()),)
    icm.ex_gExecMenuItem(execLine="""ls -l {}""".format(bxpRootBaseDirDefault_obtain(),))
    icm.ex_gExecMenuItem(execLine="""sudo mkdir /bystar; sudo chown lsipusr:employee /bystar""")
  

####+BEGIN: bx:dblock:python:func :funcName "examples_bxPlatformBaseDirs" :funcType "examples" :retType "none" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-examples  :: /examples_bxPlatformBaseDirs/ funcType=examples retType=none deco= argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def examples_bxPlatformBaseDirs(
):
####+END:
    """
** Auxiliary examples to be commonly used.
"""
    #examples_bxPlatformBaseDirsCommon()

    icm.iifExampleMenuChapter('* =BxP BaseDir=  ByStar Platform Base Dirs Command')
    
    menuLine = """"""
    icm.iifExampleMenuItem(menuLine, icmName="bx-bases", verbosity='none')    


####+BEGIN: bx:dblock:python:func :funcName "examples_bxPlatformBaseDirsFull" :funcType "examples" :retType "none" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-examples  :: /examples_bxPlatformBaseDirsFull/ funcType=examples retType=none deco= argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def examples_bxPlatformBaseDirsFull(
):
####+END:
    """
** Common examples.
"""
    bxRootBase = bxpRoot_baseObtain(None)

    examples_bxPlatformBaseDirsCommon()
    
    icm.iifExampleMenuChapter('* =Module=  Overview (desc, usage, status)')    
   
    cmndName = "overview_bxpBaseDir" ; cmndArgs = "moduleDescription moduleUsage moduleStatus" ;
    cps = collections.OrderedDict()
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    

    icm.iifExampleMenuChapter(' =BxP DirBases=  *pbdShow/pbdVerify/pbdUpdate*')    
    
    cmndName = "pbdShow" ; cmndArgs = "/ dist" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
    cmndName = "pbdShow" ; cmndArgs = "/ dist" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR' ; cps['pbdName'] = 'bxpRoot'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    
    cmndName = "pbdUpdate" ; cmndArgs = "all" ;
    cps = collections.OrderedDict()
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    cmndName = "pbdVerify" ; cmndArgs = "all" ;
    cps = collections.OrderedDict()
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    

    cmndName = "pbdShow" ; cmndArgs = "bxRoot bxRoot/var bxRoot/bisos" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
   
    cmndName = "pbdVerify" ; cmndArgs = "bxRoot bxRoot/var bxRoot/bisos" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
     
    cmndName = "pbdUpdate" ; cmndArgs = "bxRoot bxRoot/var bxRoot/bisos" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    icm.iifExampleMenuChapter(' =BxP DirBases=  *pbdShow/pbdVerify/pbdUpdate*')    

    cmndName = "pbdListUpdate" ; cmndArgs = "pbdList_bystar" ;
    cps = collections.OrderedDict() ; cps['baseDir'] = '/tmp/BySTAR'
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')

    cmndName = "pbdListUpdate" ; cmndArgs = "pbdList_bystar" ;
    cps = collections.OrderedDict() ; cps['baseDir'] =  bxRootBase
    icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='little')
    
####+BEGIN: bx:dblock:python:section :title "Misc To Be Sorted Out"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Misc To Be Sorted Out*
"""
####+END:


    
####+BEGIN: bx:dblock:python:func :funcName "bxUserId_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-Obtain    :: /bxUserId_obtain/ retType=str argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def bxUserId_obtain(
):
####+END:
    """
** ByStar platform base directory specification. 
"""
    return "lsipusr"


####+BEGIN: bx:dblock:python:func :funcName "bxGroupId_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-Obtain    :: /bxGroupId_obtain/ retType=str argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def bxGroupId_obtain(
):
####+END:
    """
** ByStar platform base directory specification. 
"""
    return "employee"


####+BEGIN: bx:dblock:python:section :title "Base Dirs Specifications"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Base Dirs Specifications*
"""
####+END:


####+BEGIN: bx:dblock:python:icmItem :itemType "List" :itemTitle "pbdList_bystar"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || List           :: pbdList_bystar  [[elisp:(org-cycle)][| ]]
"""
####+END:

pbdList_bystar = [
    "/"
    "var",
    "control",
    "data",
    "tmp",
    "log",    
    "dist",
    "vcAuth",
    "vcAnon",
    "bisos",
    "bsip",
    "blee",    
]

####+BEGIN: bx:dblock:python:func :funcName "pbdDict_bxpRoot" :comment "pbd Dictionary" :funcType "Init" :retType "bxpRootBaseDirsDict" :argsList "baseDir" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-Init      :: /pbdDict_bxpRoot/ =pbd Dictionary= retType=bxpRootBaseDirsDict argsList=(baseDir) deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def pbdDict_bxpRoot(
    baseDir,
):
####+END:

    pbdDict = collections.OrderedDict()

    root = bxpRoot_baseObtain(baseDir)
    pbdDict['/'] = bxpObjGet_baseDir(root, '')

    def directory(pathRel):
        pbdDict[pathRel] = bxpObjGet_baseDir(root, pathRel)

    def symLink(dstPathRel, srcPath, srcPathType='internal'):
        pbdDict[dstPathRel] = bxpObjGet_symLink(root, dstPathRel, srcPath, srcPathType=srcPathType)

    directory('dist')
    directory('dist/pip')
    directory('dist/pip/bisos')
    directory('dist/pip/bisos/bin')
    directory('dist/pip/bisos/input')                
    directory('dist/pip/blee')
    directory('dist/pip/bsip')    
    
    directory('vcAuth')
    directory('vcAuth/bisos')
    
    directory('vcAnon')
    directory('vcAnon/bisos')    

    directory('control')
    directory('control/bisos')    
    directory('control/bisos/site')    

    directory('var')
    directory('var/bisos')
    directory('var/bisos/icmsPkg')        
    
    
    directory('tmp')
    
    directory('log')
    directory('log/bisos')

    directory('bisos')
    symLink(  'bisos/bin', 'dist/pip/bisos/bin')
    symLink(  'bisos/input', 'dist/pip/bisos/input')
    symLink(  'bisos/var', 'var/bisos')
    symLink(  'bisos/tmp', 'tmp')
    symLink(  'bisos/log', 'log/bisos')                
              
    directory('bsip')
    
    directory('blee')

    return pbdDict


####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "bxpRoot_baseObtain" :funcType "obtain" :retType "str" :argsList "baseDir" :deco "ucf.runOnceOnlyReturnFirstInvokation"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-obtain    :: /bxpRoot_baseObtain/ retType=str argsList=(baseDir) deco=ucf.runOnceOnlyReturnFirstInvokation  [[elisp:(org-cycle)][| ]]
"""
@ucf.runOnceOnlyReturnFirstInvokation
def bxpRoot_baseObtain(
    baseDir,
):
####+END:
    outcome = bxpRootGet().iif(
        interactive=False,
        baseDir=baseDir,
    )
    if outcome.isProblematic(): return icm.EH_badOutcome(outcome)    

    return outcome.results

    
####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "bxpRootGet" :parsMand "" :parsOpt "baseDir" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /bxpRootGet/ parsMand= parsOpt=baseDir argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bxpRootGet(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ 'baseDir', ]
    iifArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        baseDir=None,         # or Cmnd-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome

        callParamsDict = {'baseDir': baseDir, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        baseDir = callParamsDict['baseDir']
####+END:
	def cmndDesc(): """
** if --baseDir Was specified, it is returned
** If ~/.bystarRoot exists, its content is returned
** If /etc/bystarRoot exists, its content is returned
** If /bystar exists, "/bystar" is returned
"""
        retVal = None
        while True:
            if baseDir:
                retVal = baseDir
                break

            userFileName = bxpRootBaseDirPtrUserFile_obtain()
            if os.path.isfile(
                    userFileName
            ):
                with open(userFileName, 'r') as myfile:
                    data=myfile.read().replace('\n', '')
                    retVal = data
                    break

            sysFileName = bxpRootBaseDirPtrSysFile_obtain()
            if os.path.isfile(
                    sysFileName
            ):
                with open(sysFileName, 'r') as myfile:
                    data=myfile.read().replace('\n', '')
                    retVal = data
                    break

            # Default ByStar Root Directory
            defaultBxRootDir = bxpRootBaseDirDefault_obtain()
            if os.path.isdir(defaultBxRootDir):
                retVal = defaultBxRootDir
                break

            icm.EH_problem_usageError("Missing /bystar and no /etc/bystarRoot")            
            retVal = None
            break

        if interactive:
            icm.ANN_write("{}".format(retVal))

        return iifOutcome.set(
            opError=icm.notAsFailure(retVal),
            opResults=retVal,
        )


####+BEGIN: bx:dblock:python:subSection :title "ICM Each Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *ICM Each Commands*
"""
####+END:
            
            
####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "pbdShow" :parsMand "" :parsOpt "baseDir pbdName" :argsMin "1" :argsMax "1000" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /pbdShow/ parsMand= parsOpt=baseDir pbdName argsMin=1 argsMax=1000 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class pbdShow(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ 'baseDir', 'pbdName', ]
    iifArgsLen = {'Min': 1, 'Max': 1000,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        baseDir=None,         # or Cmnd-Input
        pbdName=None,         # or Cmnd-Input
        argsList=None,         # or Args-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome
            effectiveArgsList = G.iimRunArgsGet().iifArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'baseDir': baseDir, 'pbdName': pbdName, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        baseDir = callParamsDict['baseDir']
        pbdName = callParamsDict['pbdName']
####+END:
	def cmndDesc(): """
** for each arg, output bxp parameters.
"""
        icm.ANN_write("{}".format(baseDir))

        if not pbdName:
            pbdName = 'bxpRoot'

        if baseDir:
            pbdDict = eval("""pbdDict_{}("{}")""".format(pbdName, baseDir))
        else:
            pbdDict = eval("""pbdDict_{}({})""".format(pbdName, baseDir))

        def procEach(pbdItem):
            pbdObj = pbdDict[pbdItem]
            pbdObj.show()

        if effectiveArgsList[0] == "all":
            for each in pbdDict:
                procEach(each)

            return iifOutcome.set(
                opError=icm.OpError.Success,
                opResults=None,
            )
 
        for each in  effectiveArgsList:
            procEach(each)
            
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )
    
####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "pbdVerify" :parsMand "" :parsOpt "baseDir pbdName" :argsMin "1" :argsMax "1000" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /pbdVerify/ parsMand= parsOpt=baseDir pbdName argsMin=1 argsMax=1000 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class pbdVerify(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ 'baseDir', 'pbdName', ]
    iifArgsLen = {'Min': 1, 'Max': 1000,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        baseDir=None,         # or Cmnd-Input
        pbdName=None,         # or Cmnd-Input
        argsList=None,         # or Args-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome
            effectiveArgsList = G.iimRunArgsGet().iifArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'baseDir': baseDir, 'pbdName': pbdName, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        baseDir = callParamsDict['baseDir']
        pbdName = callParamsDict['pbdName']
####+END:
	def cmndDesc(): """
** for each arg, verify that each exists as expected.
"""
        icm.ANN_write("{}".format(baseDir))
                
        if not pbdName:
            pbdName = 'bxpRoot'

        if baseDir:
            pbdDict = eval("""pbdDict_{}("{}")""".format(pbdName, baseDir))
        else:
            pbdDict = eval("""pbdDict_{}({})""".format(pbdName, baseDir))

        def procEach(pbdItem):
            pbdObj = pbdDict[pbdItem]
            pbdObj.verify()

        if effectiveArgsList[0] == "all":
            for each in pbdDict:
                procEach(each)

            return iifOutcome.set(
                opError=icm.OpError.Success,
                opResults=None,
            )
 
        for each in  effectiveArgsList:
            procEach(each)
            
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )
 
####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "pbdUpdate" :parsMand "" :parsOpt "baseDir pbdName" :argsMin "1" :argsMax "1000" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /pbdUpdate/ parsMand= parsOpt=baseDir pbdName argsMin=1 argsMax=1000 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class pbdUpdate(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ 'baseDir', 'pbdName', ]
    iifArgsLen = {'Min': 1, 'Max': 1000,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        baseDir=None,         # or Cmnd-Input
        pbdName=None,         # or Cmnd-Input
        argsList=None,         # or Args-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome
            effectiveArgsList = G.iimRunArgsGet().iifArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'baseDir': baseDir, 'pbdName': pbdName, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        baseDir = callParamsDict['baseDir']
        pbdName = callParamsDict['pbdName']
####+END:
	def cmndDesc(): """
** For each arg, update each to what has been specified.
"""
        icm.ANN_write("{}".format(baseDir))
                
        if not pbdName:
            pbdName = 'bxpRoot'

        if baseDir:
            pbdDict = eval("""pbdDict_{}("{}")""".format(pbdName, baseDir))
        else:
            pbdDict = eval("""pbdDict_{}({})""".format(pbdName, baseDir))

        def procEach(pbdItem):
            pbdObj = pbdDict[pbdItem]
            pbdObj.update()

        if effectiveArgsList[0] == "all":
            for each in pbdDict:
                procEach(each)

            return iifOutcome.set(
                opError=icm.OpError.Success,
                opResults=None,
            )
 
        for each in  effectiveArgsList:
            procEach(each)
            
        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )
 

        
####+BEGIN: bx:dblock:python:subSection :title "ICM List Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *ICM List Commands*
"""
####+END:
    

####+BEGIN: bx:dblock:python:iim:cmnd:classHead :cmndName "pbdListUpdate" :parsMand "" :parsOpt "baseDir pbdName" :argsMin "1" :argsMax "1000" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || ICM-Cmnd       :: /pbdListUpdate/ parsMand= parsOpt=baseDir pbdName argsMin=1 argsMax=1000 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class pbdListUpdate(icm.Iif):
    iifParamsMandatory = [ ]
    iifParamsOptional = [ 'baseDir', 'pbdName', ]
    iifArgsLen = {'Min': 1, 'Max': 1000,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def iif(self,
        interactive=False,        # Can also be called non-interactively
        baseDir=None,         # or Cmnd-Input
        pbdName=None,         # or Cmnd-Input
        argsList=None,         # or Args-Input
    ):
        G = icm.IicmGlobalContext()
        iifOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=iifOutcome):
                return iifOutcome
            effectiveArgsList = G.iimRunArgsGet().iifArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'baseDir': baseDir, 'pbdName': pbdName, }
        if not icm.iifCallParamsValidate(callParamsDict, interactive, outcome=iifOutcome):
            return iifOutcome
        baseDir = callParamsDict['baseDir']
        pbdName = callParamsDict['pbdName']
####+END:
	def cmndDesc(): """
** Doc String Outside Of Dblock.
"""
        icm.ANN_write("{}".format(baseDir))

        for eachArg in  effectiveArgsList:
            pbdList = eval('{}'.format(eachArg))
            for each in pbdList:
                pbdUpdate().iif(
                    interactive=False,
                    baseDir=baseDir,
                    argsList=each.split(),
                )

        return iifOutcome.set(
            opError=icm.OpError.Success,
            opResults=None,
        )


####+BEGIN: bx:dblock:python:section :title "BxpBaseDir Classes"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *BxpBaseDir Classes*
"""
####+END:
    

####+BEGIN: bx:dblock:python:enum :enumName "bpd_BaseDirType" :comment ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Enum           :: /bpd_BaseDirType/  [[elisp:(org-cycle)][| ]]
"""
@enum.unique
class bpd_BaseDirType(enum.Enum):
####+END:
    directory = 'directory'
    symLink = 'symLink'
    gitClone = 'gitClone'


####+BEGIN: bx:dblock:python:func :funcName "bxpObjGet_baseDir" :funcType "BxPD" :retType "BxpBaseDir_Dir" :argsList "pathRoot pathRel" :deco "default"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-BxPD      :: /bxpObjGet_baseDir/ retType=BxpBaseDir_Dir argsList=(pathRoot pathRel) deco=default  [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def bxpObjGet_baseDir(
    pathRoot,
    pathRel,
):
####+END:
    return (
        BxpBaseDir_Dir(
            destPathRoot=pathRoot,
            destPathRel=pathRel,
        )
    )

####+BEGIN: bx:dblock:python:func :funcName "bxpObjGet_symLink" :comment "Incomplete" :funcType "BxPD" :retType "BxpBaseDir_SymLink" :argsList "pathRoot dstPathRel srcPath srcPathType='internal'" :deco "default"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-BxPD      :: /bxpObjGet_symLink/ =Incomplete= retType=BxpBaseDir_SymLink argsList=(pathRoot dstPathRel srcPath srcPathType='internal') deco=default  [[elisp:(org-cycle)][| ]]
"""
@icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
def bxpObjGet_symLink(
    pathRoot,
    destPathRel,
    srcPath,
    srcPathType='internal',
):
####+END:
    return (
        BxpBaseDir_SymLink(
            destPathRoot=pathRoot,
            destPathRel=destPathRel,
            srcPath=srcPath,
            srcPathType=srcPathType,
        )
    )

####+BEGIN: bx:dblock:python:subSection :title "Class Definitions"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *Class Definitions*
"""
####+END:



####+BEGIN: bx:dblock:python:class :className "BxpBaseDir" :superClass "object" :comment "Expected to be subclassed" :classType "basic"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-basic    :: /BxpBaseDir/ object =Expected to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class BxpBaseDir(object):
####+END:
    """	
** ByStar platform base directory specification. 	
"""
    owner = bxUserId_obtain()
    group = bxGroupId_obtain()
    permissions = "775"
    
    def __init__(
        self,
        baseDirType=None,
        destPathRoot=None,
        destPathRel=None,            
    ):
        self.baseDirType=baseDirType
        self.destPathRoot=destPathRoot
        self.destPathRel=destPathRel

    def destPathFullGet(self,):
        return (
            os.path.abspath(
                os.path.join(self.destPathRoot, self.destPathRel)
            )
        )
        


####+BEGIN: bx:dblock:python:class :className "BxpBaseDir_Dir" :superClass "BxpBaseDir" :comment "Actual" :classType "basic"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-basic    :: /BxpBaseDir_Dir/ BxpBaseDir =Actual=  [[elisp:(org-cycle)][| ]]
"""
class BxpBaseDir_Dir(BxpBaseDir):
####+END:
    """	
** ByStar platform base directory specification. 	
"""
    
    def __init__(
        self,
        baseDirType=bpd_BaseDirType.directory,
        destPathRoot=None,
        destPathRel=None,            
        basePrepFunc=None,
        baseCleanFunc=None,
        comment=None,                        
    ):
        self.baseDirType=baseDirType
        self.destPathRoot=destPathRoot
        self.destPathRel=destPathRel
        self.basePrepFunc=basePrepFunc
        self.baseCleanFunc=baseCleanFunc
        self.comment=comment

    def __str__(self):
        return (
            """
baseDirType={baseDirType}
destPathRoot={destPathRoot}
destPathRel={destPathRel}
owner={owner}
group={group}
permissions={permissions}
basePrepFunc={basePrepFunc}
baseCleanFunc={baseCleanFunc}
comment={comment}
""".format(
    baseDirType=self.baseDirType,
    destPathRoot=self.destPathRoot,
    destPathRel=self.destPathRel,
    owner=self.__class__.owner,
    group=self.__class__.group,
    permissions=self.__class__.permissions,
    basePrepFunc=self.basePrepFunc,
    baseCleanFunc=self.baseCleanFunc,
    comment=self.comment,
        ))

    def update(self):
        destFullPath = self.destPathFullGet()
        if os.path.isdir(destFullPath):
            icm.ANN_here("{} Exists -- mkdir Skipped".format(destFullPath))
        else:
            try:
                os.makedirs(destFullPath)
            except OSError:
                if not os.path.isdir(destFullPath):
                    raise
            icm.ANN_write("Created {}".format(destFullPath))


    def verify(self):
        destFullPath = self.destPathFullGet()        
        if os.path.isdir(destFullPath):
            icm.ANN_here("{} Exists -- As Expected".format(destFullPath))
        else:
            icm.ANN_here("{} Missing -- Un-Expected".format(destFullPath))
        
    def show(self):
        icm.ANN_write("{}".format(self.__str__()))
        

    


####+BEGIN: bx:dblock:python:class :className "BxpBaseDir_SymLink" :superClass "BxpBaseDir" :comment "Actual" :classType "basic"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-basic    :: /BxpBaseDir_SymLink/ BxpBaseDir =Actual=  [[elisp:(org-cycle)][| ]]
"""
class BxpBaseDir_SymLink(BxpBaseDir):
####+END:
    """	
** ByStar platform base directory specification. 	
"""
    
    def __init__(
        self,
        destPathRoot,
        destPathRel,
        srcPath,
        srcPathType='internal',            
        basePrepFunc=None,
        baseCleanFunc=None,
        comment=None,                        
    ):
        self.baseDirType=bpd_BaseDirType.symLink
        self.destPathRoot=destPathRoot
        self.destPathRel=destPathRel
        self.srcPath=srcPath
        self.srcPathType=srcPathType        
        self.basePrepFunc=basePrepFunc
        self.baseCleanFunc=baseCleanFunc
        self.comment=comment

    def __str__(self):
        return (
            """
baseDirType={baseDirType}
destPathRoot={destPathRoot}
srcPath={srcPath}
srcPathType={srcPathType}
owner={owner}
group={group}
permissions={permissions}
basePrepFunc={basePrepFunc}
baseCleanFunc={baseCleanFunc}
comment={comment}
""".format(
    baseDirType=self.baseDirType,
    destPathRoot=self.destPathRoot,
    srcPath=self.srcPath,
    srcPathType=self.srcPathType,
    destPathRel=self.destPathRel,    
    owner=self.__class__.owner,
    group=self.__class__.group,
    permissions=self.__class__.permissions,
    basePrepFunc=self.basePrepFunc,
    baseCleanFunc=self.baseCleanFunc,
    comment=self.comment,
        ))

    def srcFullPathObtain(self):
        # NOTYET, check srcPathType
        return (
            os.path.abspath(
                os.path.join(self.destPathRoot, self.srcPath)
            )
        )
    

    def update(self):
        destFullPath = self.destPathFullGet()
        srcFullPath = self.srcFullPathObtain()

        def createSymLink():
            try:            
                os.remove(destFullPath)
            except OSError:
                pass
            
            try:
                os.symlink(srcFullPath, destFullPath)
            except OSError:
                if not os.path.islink(destFullPath):
                    raise
            icm.ANN_write("Created {} SymLink pointing to: {}".format(
                destFullPath, srcFullPath))
        
        if os.path.islink(destFullPath):
            linkPointsToPath = os.readlink(destFullPath)
            if srcFullPath == linkPointsToPath:
                icm.ANN_here("{} SymLink exists and correctly points to: {}".format(
                    destFullPath, srcFullPath))
            else:
                createSymLink() 
        else:
            createSymLink()

    def verify(self):
        destFullPath = self.destPathFullGet()
        srcFullPath = self.srcFullPathObtain()

        if os.path.islink(destFullPath):
            linkPointsToPath = os.readlink(destFullPath)
            if srcFullPath == linkPointsToPath:
                icm.ANN_here("{} SymLink exists and correctly points to: {}".format(
                    destFullPath, srcFullPath))
            else:
                icm.ANN_here("{} SymLink exists but is wrong -- points to: {} instead of".format(
                    destFullPath, linkPointsToPath, srcFullPath))
        else:
            icm.ANN_here("{} SymLink is missing".format(
                destFullPath,))

        

        
    def show(self):
        icm.ANN_write("{}".format(self.__str__()))
        
 


####+BEGIN: bx:dblock:python:class :className "BxpBaseDir_GitClone" :superClass "BxpBaseDir" :comment "" :classType ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-         :: /BxpBaseDir_GitClone/ BxpBaseDir  [[elisp:(org-cycle)][| ]]
"""
class BxpBaseDir_GitClone(BxpBaseDir):
####+END:
    """	
** ByStar platform base directory specification. 	
"""
   
    def __init__(
        self,
        destPathRel=None,
    ):
        #self.baseDirType = 
        #self.__class__.destPathRel = destPathRel
        pass

    def __str__(self):
        return format(
            'baseDirType: ' + str(self.baseDirType)
        )
    


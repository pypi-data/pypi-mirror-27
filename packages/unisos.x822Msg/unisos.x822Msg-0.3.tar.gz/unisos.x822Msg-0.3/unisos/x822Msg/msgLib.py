#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
"""\
*      *[Summary]* ::  msgLib.py library assists with COMMON to msgIn and msgOut.
* Authors: Mohsen Banan --  http://mohsen.1.banan.byname.net/contact\
* Module Name and Version :: [[elisp:(org-cycle)][| ]]
"""

####+BEGIN: bx:dblock:global:iim:name-py :style "fileName"
__iimName__ = "msgLib"
####+END:

####+BEGIN: bx:dblock:global:timestamp:version-py :style "date"
__version__ = "201706134745"
####+END:

"""
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/topControls.org"
*      ================
*  /Controls/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]] 

####+END:
"""

"""
*      ================
*  #################### CONTENTS-LIST ################
*  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Current      :: Just getting started [[elisp:(org-cycle)][| ]]
*  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]  Current      :: [[file:/libre/ByStar/InitialTemplates/activeDocs/bxServices/versionControl/fullUsagePanel-en.org::Xref-VersionControl][Panel Roadmap Documentation]] [[elisp:(org-cycle)][| ]]
"""

"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *Imports And Description -- describe()*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=   ::  Imports [[elisp:(org-cycle)][| ]]
"""


import email

"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func        ::  describe    [[elisp:(org-cycle)][| ]]
"""

def describe():
    moduleDescription="""
*       [[elisp:(org-cycle)][| *Description:* | ]]
** :Overview: (Functional Specification)
** :Contacts:
	[[elisp:(bystar:bbdb:search-here "Mohsen Banan")][Mohsen BANAN]]
**       *[End-Of-Description]*
"""
    print( str( __doc__ ) )  # This is the Summary: from the top doc-string
    print(moduleDescription)
    return


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func        ::  msgAllRecipients    [[elisp:(org-cycle)][| ]]
"""
def msgAllRecipients(
        msg,
):
    """Given msg, get list of all recipients.

    """
    tos = msg.get_all('to', [])
    ccs = msg.get_all('cc', [])
    bccs = msg.get_all('bcc', [])    
    resent_tos = msg.get_all('resent-to', [])
    resent_ccs = msg.get_all('resent-cc', [])
    allRecipients = email.utils.getaddresses(tos + ccs + bccs + resent_tos + resent_ccs)
    return allRecipients



"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *End Of Editable Text*
"""

"""
*  [[elisp:(org-cycle)][| ]]  [COMMON]      :: /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
"""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall

####+END:


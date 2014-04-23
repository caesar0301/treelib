#!/usr/bin/env python
#===============================================================================
# Copyright (C) 2011    Brett Alistair Kromkamp - brettkromkamp@gmail.com
# Copyright (C) 2012,2013   Xiaming Chen - chenxm35@gmail.com
# Copyright (C) 2013    Holger Bast - holgerbast@gmx.de
# All rights reserved.
#
# This file is part of project treelib.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Neither the name of the copyright holder nor the names of the contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
# treelib - Simple to use for you.
# Python 2/3 Tree Implementation
#===============================================================================
"""
        node.py

        o       NodeIDTypeException class
        o       Node class
"""

import uuid

#///////////////////////////////////////////////////////////////////////////////
# error class :
class NodeIDTypeException(Exception):
    """
        NodeIDTypeException class
    """
    pass

#///////////////////////////////////////////////////////////////////////////////
class Node(object):
    """
        Node class

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        CLASS ATTRIBUTES :

        o ADD
        o DELETE
        o INSERT

        ATTRIBUTES :

        o _identifier
        o _tag
        o expanded
        o _bpointer
        o _fpointer
        o data

        METHODS :

        o __init__(self, tag=None, identifier=None, expanded=True, data=None)
        o __lt__(self, other)
        o _set_identifier(self, nid)
        o @property bpointer(self)
        o @bpointer.setter bpointer(self, nid)
        o @property fpointer(self)
        o @fpointer.setter fpointer(self, value)
        o @property identifier(self)
        o @identifier.setter identifier(self, value)
        o is_leaf(self)
        o @property tag(self)
        o @tag.setter tag(self, value)
        o update_bpointer(self, nid)
        o update_fpointer(self, nid, mode=ADD)
    """

    # ADD, DELETE, INSERT constants :
    (ADD, DELETE, INSERT) = list(range(3))

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 tag=None,
                 identifier=None,
                 expanded=True,
                 data=None):
        """
                Node.__init__()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                PARAMETERS

                o node
                o tag           : None or something else
                                  if None, self._identifier will be set to the
                                  identifier's value.
                o identifier
                o expanded      : bool
                o data
        """
        self._identifier = None
        self._set_identifier(identifier)

        if tag is None:
            self._tag = self._identifier
        else:
            self._tag = tag

        self.expanded = expanded
        self._bpointer = None
        self._fpointer = list()
        self.data = data

    #///////////////////////////////////////////////////////////////////////////
    def __lt__(self, other):
        """
                Node.lt()

               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               RETURN VALUE : a boolean
        """
        return self.tag < other.tag

    #///////////////////////////////////////////////////////////////////////////
    def _set_identifier(self, nid):
        """
                Node._set_identifier()

                Initialize self._set_identifier
        """
        if nid is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = nid

    #///////////////////////////////////////////////////////////////////////////
    @property
    def bpointer(self):
        """
                Node.bpointer()
        """
        return self._bpointer

    #///////////////////////////////////////////////////////////////////////////
    @bpointer.setter
    def bpointer(self, nid):
        """
                Node.bpointer()
        """
        if nid is not None:
            self._bpointer = nid
        else:
            #print("WARNNING: the bpointer of node %s " \
            #      "is set to None" % self._identifier)
            self._bpointer = None

    #///////////////////////////////////////////////////////////////////////////
    @property
    def fpointer(self):
        """
                Node.fpointer()
        """
        return self._fpointer

    #///////////////////////////////////////////////////////////////////////////
    @fpointer.setter
    def fpointer(self, value):
        """
                Node.fpointer()
        """
        if value is None:
            self._fpointer = list()
        elif isinstance(value, list):
            self._fpointer = value
        elif isinstance(value, dict):
            self._fpointer = list(value.keys())
        elif isinstance(value, set):
            self._fpointer = list(value)
        else: #TODO: add deprecated routine
            pass

    #///////////////////////////////////////////////////////////////////////////
    @property
    def identifier(self):
        """
                Node.identifier()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE : self._identifier
        """
        return self._identifier

    #///////////////////////////////////////////////////////////////////////////
    @identifier.setter
    def identifier(self, value):
        """
                Node.identifier()

                Initialize self._set_identifier
        """
        if value is None:
            print("WARNNING: node ID can not be None")
        else:
            self._set_identifier(value)

    #///////////////////////////////////////////////////////////////////////////
    def is_leaf(self):
        """
                Node.is_leaf()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE : a boolean
        """
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    #///////////////////////////////////////////////////////////////////////////
    @property
    def tag(self):
        """
                Node.tag()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE: self._tag
        """
        return self._tag

    #///////////////////////////////////////////////////////////////////////////
    @tag.setter
    def tag(self, value):
        """
                Node.tag()

                Initialize self._tag
        """
        self._tag = value if value is not None else None

    #///////////////////////////////////////////////////////////////////////////
    def update_bpointer(self, nid):
        """
                Node.update_bpointer()
        """
        self.bpointer = nid

    #///////////////////////////////////////////////////////////////////////////
    def update_fpointer(self, nid, mode=ADD):
        """
                Node.update_fpointer()
        """
        if nid is None:
            return
        
        if mode is self.ADD:
            self._fpointer.append(nid)
        elif mode is self.DELETE:
            if nid in self._fpointer:
                self._fpointer.remove(nid)
        elif mode is self.INSERT: # deprecate to ADD mode
            print("WARNNING: INSERT is deprecated to ADD mode")
            self.update_fpointer(nid)

if __name__ == '__main__':
    pass

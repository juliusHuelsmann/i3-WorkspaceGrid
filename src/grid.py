from subprocess import Popen, PIPE
import numpy as np
import json



class Grid:
    """
    Class containing the grid logic bein ginterfaced via the i3 grid interface 
    script. 
    """

    def __init__(self):
        #XXX:
        #self.rows, self.cos = np.genfromtxt("config")
        #self.titles = reload the titles

        #XXX: this sucks.
        self.titles = np.array(["0", "1git", "2vim", "3ide", "4pdf", 
            5, 6, "7qt", "8fire", "9chat"])

        self.cols = 3
        self.rows = 3
        self.reloadWorkspaces()
       
    def reloadWorkspaces(self):
        workspaces = str(Popen(
            ["i3-msg", "-t", "get_workspaces"], 
            stdout = PIPE).communicate()[0])
        self.workspaces = json.loads(workspaces[2:-3])
    
    def _switchWs(self, r1, c1, r2, c2):
        """
        switch windows of (r1, c1) and (r2, c2).
        """
        #XXX: 
        pass

    def _switchWs(self, i1, i2):
        """
        Switch two workspaces by unidimensional identifier.
        :i1:, :i2:      do not have to be in range, is checked and corrected by 
                        this method.
        """
        #XXX: 
        pass
   

    def _getExistingWorkspace(self, i):
        """
        Returns workspace at identifier.
        :i:         identifier of the workspace.
        If that workspace does not exist yet, create new workspace.
        """
        val = self._getWorkspaceByPredicate(lambda xs : xs["num"] == i)
        if val.shape[0]:
            return val[0]

    def _getWorkspace(self, i):
        """
        Returns workspace at identifier.
        :i:         identifier of the workspace.
        If that workspace does not exist yet, create new workspace.
        """
        val = self._getWorkspaceByPredicate(lambda xs : xs["num"] == i)
        if val.shape[0]:
            return val[0]
        if i < len(self.titles):
            return i, self.titles[i]
        return i, i


    def _switchWsParam(self, dr, dc):

        cw = self._getCurrentWorkspace()
        if (cw.shape[0]):
            ident, _ = cw[0]
            cr, cc = coords = self._idToPos(int(ident)-1)



            newc = cc + dc
            newr = cr + dr 

            newcPos = newc % self.cols
            newrPos = newr % self.rows

            while newcPos < 0:
                newcPos += self.cols
            
            if newrPos < 0:
                newrPos += self.rows; 


            print("  + ", dr, dc)
            print("------------")

            nid = self._posToId(newrPos, newcPos) + 1
            name = self._getWorkspace(nid)[1]
            print("to  ", newrPos, newcPos, nid, name)
            
            return newcPos, newrPos, nid, name 


    def moveWindowBy(self, dr, dc):
        """
        moves currently focused window to new workspace. 
        :dr:        r_new = r_old + dr
        :dc:        c_new = c_old + dc
        """

        ret = self._switchWsParam(dr, dc)
        if ret:
            c, r, ident, name = ret
            print(c, r, ident, "name=" , name)
            self._moveWindowTo(name)

    def moveWorkspaceBy(self, dr, dc):
        """
        moves currently active workspace to new workspace. 
        :dr:        r_new = r_old + dr
        :dc:        c_new = c_old + dc
        """
        ret = self._switchWsParam(dr, dc)
        if ret:
            c, r, ident, name = ret
            print(c, r, ident, "name=" , name)
            self._moveWorkspaceTo(name)

    def _moveWindowTo(self, i):
        """
        Moves widow to identifier
        """
        Popen(["i3-msg", "move", "container", "to", "workspace", str(i)], 
                stdout = PIPE).communicate()
        self._moveWorkspaceTo(i)

    def _moveWorkspaceTo(self, i):
        """
        Moves widow to identifier
        """
        Popen(["i3-msg", "workspace", str(i)], stdout = PIPE).communicate()

    def _getCurrentWorkspace(self ):
        """
        Determines the currently active workspace
        """
        return self._getWorkspaceByPredicate(lambda ws : ws["focused"])



    def _getWorkspaceByPredicate(self, func):

        # find list of selected workspaces and return number and identifier 
        spaces = np.empty([len(self.workspaces), 2]).astype("str"); j = 0
        for i, ws in enumerate(self.workspaces):
            if func(ws):
                num = ws["num"]; name = ws["name"]
                spaces[j] = num, name; j+=1
                
        return spaces[:j]     

    def _idToPos(self, ident):
        ident = int(ident)
        re = int(np.floor(ident/self.cols)), ident%self.cols, # rather ugly
        return re

    def _posToId(self, row, col):
        res = int(col) + int(row) * self.cols 
        return res 

    ## API //XXX to be excluded

    
    ##
    # Extend cols
    ## 
    #XXX: Command for extending the schema. 
    # will be done when the amount of cols and rows are written into the configuration file
    # see swap workspace for this.
    """

    # swap ws
    i3-msg "rename workspace 2 to temporary; rename workspace 5 to 2; rename workspace temporary to 5"



    """



class GridInterface:

    """
    This class offers the following operations: 

    - moveWindow{Up, Down, Left, Right}
    - moveWorkspace{Up, Down, Left, Right}

    """

    def __init__(self):
        #XXX: implement the link to the view
        self.gridController = Grid()
    ##
    # Move window
    ## 

    def moveWindowUp(self):
        self.gridController.moveWindowBy(-1, 0)
    def moveWindowDown(self):
        self.gridController.moveWindowBy(1, 0)
    def moveWindowLeft(self):
        self.gridController.moveWindowBy(0, -1)
    def moveWindowRight(self):
        self.gridController.moveWindowBy(0, 1)


    ##
    # Move workspace 
    ## 
    def moveWorkspaceUp(self):
        self.gridController.moveWorkspaceBy(-1, 0)
    def moveWorkspaceDown(self):
        self.gridController.moveWorkspaceBy(1, 0)
    def moveWorkspaceLeft(self):
        self.gridController.moveWorkspaceBy(0, -1)
    def moveWorkspaceRight(self):
        self.gridController.moveWorkspaceBy(0, 1)

    def reloadWorkspaces(self):
        self.gridController.reloadWorkspaces()


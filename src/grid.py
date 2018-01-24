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

        self.wsmat = np.zeros([self.rows, self.cols, 2]).astype("int").astype("str")
        for ws in self.workspaces:
            i = ws["num"]
            r, c = self._idToPos(i-1)

            # in case the dimensions do not match with the default dimensions,
            # update
            if r >= self.wsmat.shape[0] or c >= self.wsmat.shape[1]:
                a = self.wsmat;
                self.wsmat = np.zeros([max(r+1, self.wsmat.shape[0]), max(c+1, self.wsmat.shape[1]), 2]).astype("int").astype("str")
                self.wsmat[:a.shape[0], :a.shape[1]] = a
                self.rows , self.cols, _ = self.wsmat.shape

            self.wsmat[r, c] = int(ws["num"]), ws["name"]
        #self.vw.load(self.wsmat)
        
        
    
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
        return np.empty([0,0])

    def _getWorkspace(self, i):
        """
        Returns workspace at identifier.
        :i:         identifier of the workspace.
        If that workspace does not exist yet, create new workspace.
        """
        val = self._getExistingWorkspace(i)
        if val.shape[0]:
            return val
        if i < len(self.titles):
            return i, self.titles[i]
        return i, i

    def _getNextExistingWorkspace(self, cr, cc, dr, dc):

        rows, cols, _ = self.wsmat.shape
        for i in range(1, max(self.wsmat.shape[0] * (dr != 0), (dc != 0) * self.wsmat.shape[1])):
            r = int((cr + dr * i) % rows)
            c = int((cc + dc * i) %  cols)
            if r < 0: r+= rows
            if c < 0: c+= cols
            cv = self.wsmat[r,c]
            if int(cv[0]):

                return r, c, cv[0], cv[1]


    def _changeExistingWsParam(self, dr, dc):
        cw = self._getCurrentWorkspace()
        if (cw.shape[0]):
            ident, _ = cw[0]
            cr, cc = coords = self._idToPos(int(ident)-1)
            
            result = self._getNextExistingWorkspace(cr, cc, dr, dc)
            print("next ex", result)
            if result: 
                return result


    def _changeWsParam(self, dr, dc):

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
            
            return newrPos, newcPos, nid, name 


    def moveWindowBy(self, dr, dc):
        """
        moves currently focused window to new workspace. 
        :dr:        r_new = r_old + dr
        :dc:        c_new = c_old + dc
        """

        ret = self._changeWsParam(dr, dc)
        if ret:
            r, c, ident, name = ret
            print(c, r, ident, "name=" , name)
            self._moveWindowTo(name)

    def moveWorkspaceBy(self, dr, dc):
        """
        moves currently active workspace to new workspace. 
        :dr:        r_new = r_old + dr
        :dc:        c_new = c_old + dc
        """
        ret = self._changeWsParam(dr, dc)
        if ret:
            r, c, ident, name = ret
            print(c, r, ident, "name=" , name)
            self._moveWorkspaceTo(name)
    
    def moveWindowIntoDir(self, dr, dc):
        """
        moves currently active window to new (already existing) workspace 
        in the direction of dr, dc. 
        :dr:        r_new = r_old + \lambda dr
        :dc:        c_new = c_old + \lambda dc
        """

        ret = self._changeExistingWsParam(dr, dc)
        if ret:
            r, c, ident, name = ret
            print(c, r, ident, "name=" , name)
            self._moveWindowTo(name)
    def moveWorkspaceIntoDir(self, dr, dc):
        """
        moves currently active workspace to new (already existing) workspace 
        in the direction of dr, dc. 
        :dr:        r_new = r_old + \lambda dr
        :dc:        c_new = c_old + \lambda dc
        """
        ret = self._changeExistingWsParam(dr, dc)
        if ret:
            r, c, ident, name = ret
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
    # Movements along the grid, possibly spawning a new workpace in case it
    # does not exist already. Movements are always performed one step at a
    # time. 
    ## 

    # window
    def moveWindowUp(self):
        self.gridController.moveWindowBy(-1, 0)
    def moveWindowDown(self):
        self.gridController.moveWindowBy(1, 0)
    def moveWindowLeft(self):
        self.gridController.moveWindowBy(0, -1)
    def moveWindowRight(self):
        self.gridController.moveWindowBy(0, 1)


    # workspace 
    def moveWorkspaceUp(self):
        self.gridController.moveWorkspaceBy(-1, 0)
    def moveWorkspaceDown(self):
        self.gridController.moveWorkspaceBy(1, 0)
    def moveWorkspaceLeft(self):
        self.gridController.moveWorkspaceBy(0, -1)
    def moveWorkspaceRight(self):
        self.gridController.moveWorkspaceBy(0, 1)
    
    ##
    # Movements only taking into consideration those workspaces that do already
    # exist.
    ## 

    # window
    def moveWindowExistingUp(self):
        self.gridController.moveWindowIntoDir(-1, 0)
    def moveWindowExistingDown(self):
        self.gridController.moveWindowIntoDir(1, 0)
    def moveWindowExistingLeft(self):
        self.gridController.moveWindowIntoDir(0, -1)
    def moveWindowExistingRight(self):
        self.gridController.moveWindowIntoDir(0, 1)

    # workspace 
    def moveWorkspaceExistingUp(self):
        self.gridController.moveWorkspaceIntoDir(-1, 0)
    def moveWorkspaceExistingDown(self):
        self.gridController.moveWorkspaceIntoDir(1, 0)
    def moveWorkspaceExistingLeft(self):
        self.gridController.moveWorkspaceIntoDir(0, -1)
    def moveWorkspaceExistingRight(self):
        self.gridController.moveWorkspaceIntoDir(0, 1)


    ##
    # Movements expanding the grid if necessary
    ## 

    #XXX: tbd

    ##
    # Makes no sense to access this function via api, just for the controller.
    ##
    def reloadWorkspaces(self):
        self.gridController.reloadWorkspaces()


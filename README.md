# About 
I3-grid is a python script that organizes i3 Window Manager workspaces into
a customizable (logical) grid. 


It can be run from the command line or bound to hotkeys through the i3 
configuration file. 
Forked from [https://github.com/lukeshimanuki/i3-grid](Luke Shimanuki).


# interfaces 
- python3 ~/.config/i3/i3-grid/src/i3GridInterface.py [COMMAND]
     bindsym <key> exec ~/.config/i3/i3-grid/src/i3GridInterface <command>

### available
- moveWindow{Left, Right, Up, Down} 
    - let the current monitor display the workspace {Left, Right, Up, Down} 
      (in relation to the current position).
- moveWorkspace{Left, Right, Up, Down}
    - move currently active window {Left, Right, Up, Down} a workspace.

### TODOs and Drawbacks 
#### Drawbacks 
- observable time consumption for switching workspaces.
- works as supposed, but might be a little bit confusing due to missing visual
  feedback. 
- In case the workspaces are named, the naming is to be inserted into the
  configuration of this script, too.
  
#### TBD
- write and read configuration  
- possibility to alter the grid configuration otf. E.g. start with rows = cols = 1, 
  Add new row / column in case the move\*{[Left, ..., Down]}  is evoked and
  the 'next' screen is not existing + outside the range of the current grid.
  - do that on special key combination 
  reorganize existing windows in position. 
- visual feedback
```
+---+
| e |
|e  |
|xe |
+---+ (3, 1), 
```
  - display the current location and the currently active workspaces 


# Setup
For setting up, simply clone to configuration folder (as a submodule in case 
you have got your i3config  version controlled).

```bash
> mkdir -p ~/.config/i3/
> cd ~/.config/i3/
# in case your configuration directory is version controlled using git
> git submodule add git@github.com:juliusHuelsmann/i3-grid.git
> git submodule init
> git submodule update #< for getting the latest changes
# otherwise
> git clone git@github.com:juliusHuelsmann/i3-grid.git
```

Example `.config/i3/config`:
```bash
bindsym $mod+Ctrl+h exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceLeft
bindsym $mod+Ctrl+l exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceRight
bindsym $mod+Ctrl+j exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceDown
bindsym $mod+Ctrl+k exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceUp
```

For `disabeling` the jump from first to last column in a row (and thus just
adding rows as logical unit, simply use the following configuration.
```bash
bindsym $mod+Ctrl+j exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceDown
bindsym $mod+Ctrl+k exec /mnt/data/repos/i3-grid/src/i3GridInterface.py moveWorkspaceUp
#bindsym $mod+Ctrl+h workspace prev
#bindsym $mod+Ctrl+l workspace next
```

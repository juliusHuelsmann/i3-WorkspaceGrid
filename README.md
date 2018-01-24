# About 
I3-grid is a python script that organizes i3 Window Manager workspaces into
a customizable (logical) grid. 


It can be run from the command line or bound to hotkeys through the i3 
configuration file. 
Forked from (https://github.com/lukeshimanuki/i3-grid)[Luke Shimanuki].


# interfaces 
There recommended two possible ways to use this extension is via communication 
with the current `controller.py` script. This can be done
by simply appending  
```
exec_always --no-startup-id starti3Grid.sh 
```
to the i3 configuration script (after running setup.sh as root or manually
changing the PATH). Communication with this controller is achieved via the
`i3Grid` script which receives the operation as its paramter. For example:

```
bindsym $mod+Ctrl+Mod1+h exec --no-startup-id i3Grid moveWorkspaceLeft
```

```
bindsym $mod+Ctrl+Mod1+l exec --no-startup-id i3Grid moveWorkspaceRight
bindsym $mod+Ctrl+Mod1+j exec --no-startup-id i3Grid moveWorkspaceDown
bindsym $mod+Ctrl+Mod1+k exec --no-startup-id i3Grid moveWorkspaceUp

bindsym $mod+Ctrl+h exec --no-startup-id i3Grid moveWorkspaceExistingLeft
bindsym $mod+Ctrl+l exec --no-startup-id i3Grid moveWorkspaceExistingRight
bindsym $mod+Ctrl+j exec --no-startup-id i3Grid moveWorkspaceExistingDown
bindsym $mod+Ctrl+k exec --no-startup-id i3Grid moveWorkspaceExistingUp
```



### available
- moveWindow{Left, Right, Up, Down} 
    - move currently active window {Left, Right, Up, Down} a workspace.
- moveWorkspace{Left, Right, Up, Down}
    - let the current monitor display the workspace {Left, Right, Up, Down} 
      (in relation to the current position). This also spawns new workspaces if
      the requested element does not exist yet. 
- moveWorkspaceExisting{Left, Right, Up, Down}
    - as moveWorkspace{...}, but only taking into consideration existing
      workspaces (just like in the original implementation of left and right
      commands in i3, but two-dimensional.

### TODOs and Drawbacks 
#### Drawbacks 
- works as supposed, but might be a little bit confusing due to missing visual
  feedback. 
- In case the workspaces are named, the naming is to be inserted into the
  scritp `grid.py` for now.
  
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

For setting up simply have a look at the `setup.sh` script, which does only
create symbolic links for finding the scripts in the `bash` folder if executed
as root.

Initialization as submodule (in case your i3 config is version controlled) or
simply cloning this script into your `.config/i3` folder and adapting the paths
to the scripts might be preferrable.

### Possibility A) Execute setup script
```bash
sudo ./setup.sh
```

### Possibility B)
Clone 
```bash
> mkdir -p ~/.config/i3/
> cd ~/.config/i3/
# in case your configuration directory is version controlled using git
> git submodule add git@github.com:juliusHuelsmann/i3-grid.git
> git submodule init
> git submodule update #< for getting the latest changes
# otherwise
> git clone git@github.com:juliusHuelsmann/i3-grid.git
# then keep in mind that the location to the scripts mentioned below is
# ~/.config/i3/scripts/[NAME]
```

# Configuration
Configuration for workspace switch
```
bindsym $mod+Ctrl+Mod1+h exec --no-startup-id i3Grid moveWorkspaceLeft
bindsym $mod+Ctrl+Mod1+l exec --no-startup-id i3Grid moveWorkspaceRight
bindsym $mod+Ctrl+Mod1+j exec --no-startup-id i3Grid moveWorkspaceDown
bindsym $mod+Ctrl+Mod1+k exec --no-startup-id i3Grid moveWorkspaceUp

bindsym $mod+Ctrl+h exec --no-startup-id i3Grid moveWorkspaceExistingLeft
bindsym $mod+Ctrl+l exec --no-startup-id i3Grid moveWorkspaceExistingRight
bindsym $mod+Ctrl+j exec --no-startup-id i3Grid moveWorkspaceExistingDown
bindsym $mod+Ctrl+k exec --no-startup-id i3Grid moveWorkspaceExistingUp
```

Afa the configuration for window switching is concerned, just use the commands:
provided above, switching `Workspace` with `Window`.

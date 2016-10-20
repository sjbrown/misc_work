

# For up-arrow completion the way I like, make these changes to .inputrc:
# "\e[A": history-search-backward
# "\e[B": history-search-forward
# set completion-ignore-case on


export PATH=$PATH:~/bin:/usr/local/sbin:/usr/sbin:/sbin

export EDITOR=vim

alias term="gnome-terminal --profile=SJB"

alias gr='grep -Irs --exclude "*.css" --exclude "*.json" --exclude "*.map" --exclude "ace.js"'


# ----------------------------------------------------------------------
# I like to keep a history of all shell commands across all the xterms
# Append to the history file on shell exit, don't overwrite (so multiple
# exiting shells don't race to scribble over your saved history)
shopt -s histappend

# Keep lots of history around
export HISTSIZE=1000000 HISTFILESIZE=1000000

# Store history in a different file, so it won't get overwritten if you
# don't have these settings
export HISTFILE=~/.bash_history_safe

# Write unsaved history immediately before emitting each prompt
PROMPT_COMMAND='history -a'
export PROMPT_COMMAND='history -a'
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# PS1 Stuff - make prompt look like this:
#
# ____[sjbrown@comp-sjb-t560] [~/work/misc_work]____
#  $
#
# For some unknown reason bash refuses to inherit
# PS1 in some circumstances that I can't figure out.
# Putting PS1 here ensures that it gets loaded every time.
# The following sets up the console prompt
# the foreground colors
BLK="\[\033[0;30m\]"  ;  BLK1="\[\033[1;30m\]"  #dark grey
RED="\[\033[0;31m\]"  ;  RED1="\[\033[1;31m\]"
GRN="\[\033[0;32m\]"  ;  GRN1="\[\033[1;32m\]"
YEL="\[\033[0;33m\]"  ;  YEL1="\[\033[1;33m\]"
BLU="\[\033[0;34m\]"  ;  BLU1="\[\033[1;34m\]"
PUR="\[\033[0;35m\]"  ;  PUR1="\[\033[1;35m\]"
AQA="\[\033[0;36m\]"  ;  AQA1="\[\033[1;36m\]"
GRY="\[\033[0;37m\]"  ;  GRY1="\[\033[1;37m\]"  #white
WHT="\[\033[0;38m\]"  ;  WHT1="\[\033[1;38m\]"  #white
# the background colors
BBLK="\[\033[0;40m\]"  ;  BBLK1="\[\033[1;40m\]"  #dark grey
BRED="\[\033[0;41m\]"  ;  BRED1="\[\033[1;41m\]"
BGRN="\[\033[0;42m\]"  ;  BGRN1="\[\033[1;42m\]"
BYEL="\[\033[0;43m\]"  ;  BYEL1="\[\033[1;43m\]"
BBLU="\[\033[0;44m\]"  ;  BBLU1="\[\033[1;44m\]"
BPUR="\[\033[0;45m\]"  ;  BPUR1="\[\033[1;45m\]"
BAQA="\[\033[0;45m\]"  ;  BAQA1="\[\033[1;46m\]"
BGRY="\[\033[0;45m\]"  ;  BGRY1="\[\033[1;47m\]"  #white
BWHT="\[\033[0;45m\]"  ;  BWHT1="\[\033[1;48m\]"  #white
# color termination token
NOCOLOR="\[\033[0m\]"

HOSTCOL=`python -c "
import commands, hashlib
colorTuples = zip( [0]*8 + [1]*8, range(30,39)*2 )
hostname = commands.getoutput( 'hostname' )
index = int(   hashlib.md5(hostname).hexdigest(), 16   ) % len(colorTuples)
hostColor = r'%d;%dm' % colorTuples[index]
print hostColor
"`
HOSTCOL="\[\033[$HOSTCOL\]"

BAR=$GRY"____"
COL=$AQA
PS1="\n$BAR$COL[$GRY\u$COL@$HOSTCOL\h$COL] [$GRY\w$COL]$BAR$NOCOLOR\n \$ "
export PS1
# ----------------------------------------------------------------------


#------------ Caps -> Esc -------------
xmodmap -e "remove Lock = Caps_Lock"
xmodmap -e "keycode 66 = Escape NoSymbol Escape"
#--------------------------------------


# ----Git stuff----------------------------------------------------------------
git config --global user.name "Shandy Brown"
git config --global user.email github@ezide.com
git config --global color.ui "auto"
git config --global core.excludesfile ~/.gitignore_global
git config diff.tool gvimdiff
alias glog='git log -10 --format=format:"%Cgreen%h%Creset %aN %Cblue%cD%Creset %n %s%+b%n"'
# -----------------------------------------------------------------------------


# ----Docker stuff-------------------------------------------------------------
alias d.images='docker images --format "{{printf \"%10.10s\" .CreatedSince}} {{printf \"%10s\" .Size}} {{printf \"%8s\" .Tag}} {{.ID}} {{printf .Repository}}"'
alias d.ps='docker ps --format "{{printf \"%-15.15s\" .Image}} {{printf \"%30.30s\" .Names}}: {{printf \"%20.20s\" .Command}} || {{.Status}}"'
# -----------------------------------------------------------------------------

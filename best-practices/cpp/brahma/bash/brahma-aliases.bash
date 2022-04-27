# auto-complete helper
function make-completion-wrapper () {
  local function_name="$2"
  local arg_count=$(($#-3))
  local comp_function_name="$1"
  shift 2
  local function="
    function $function_name {
      ((COMP_CWORD+=$arg_count))
      COMP_WORDS=( "$@" \${COMP_WORDS[@]:1} )
      "$comp_function_name"
      return 0
    }"
  eval "$function"
}

# aliases
alias brahma_source='source $(brahma info source_file)'

function brahma_catkin() {
    if [ $# -eq 0 ]
    then
      echo "No arguments provided for catkin"
      return 1
    fi
    verb=$1
    shift
    eval 'catkin $verb --workspace $(brahma info catkin_dir) $@'
    return 0
}

make-completion-wrapper _catkin _brahma_catkin catkin
complete -F _brahma_catkin brahma_catkin

function brahma_git() {
    if [ $# -eq 0 ]
    then
      echo "No repository provided for git command"
      return 1
    fi
    verb=$1
    shift
    eval 'git -C $(brahma info source_dir)/$verb $@'
    return 0
}

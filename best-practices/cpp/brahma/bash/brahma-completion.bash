# ZSH support
if [[ -n ${ZSH_VERSION-} ]]; then
  autoload -U +X bashcompinit && bashcompinit
fi

_brahma_last_option()
{
  # search backwards for the last given option
  for (( i=${cword} ; i > 0 ; i-- )) ; do
    if [[ ${words[i]} == -* ]]; then
      echo ${words[i]}
      return
    fi
  done
}

_brahma_verb()
{
  # search forwards to find brahma verb=
  for (( i=1 ; i < ${cword} ; i++ )) ; do
    if [[ ${words[i]} == -* ]] ; then continue; fi
    if [[ ${brahma_verbs} == *${words[i]}* ]] ; then
      echo ${words[i]}
      return
    fi
  done
}


_brahma()
{
  local cur prev words cword brahma_verbs brahma_opts
  _init_completion || return # this handles default completion (variables, redirection)

  # complete to the following verbs
  local brahma_verbs="create init config update setup info"

  # filter for long options (from bash_completion)
  local OPTS_FILTER='s/.*\(--[-A-Za-z0-9]\{1,\}=\{0,1\}\).*/\1/p'

  # complete to verbs ifany of these are the previous word
  local brahma_opts=$(brahma --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)

  local verb=$(_brahma_verb)
  case ${verb} in
    "")
      if [[ ${cur} == -* ]]; then
        COMPREPLY=($(compgen -W "${brahma_opts}" -- ${cur}))
      else
        COMPREPLY=($(compgen -W "${brahma_verbs}" -- ${cur}))
      fi
      ;;
    create)
      if [[ ${cur} == -* ]]; then
        local brahma_create_opts=$(brahma create --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)
        COMPREPLY=($(compgen -W "${brahma_create_opts}" -- ${cur}))
      fi
      ;;
    init)
      if [[ ${cur} == -* ]]; then
        local brahma_init_opts=$(brahma init --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)
        COMPREPLY=($(compgen -W "${brahma_init_opts}" -- ${cur}))
      fi
      ;;
    config)
      if [[ ${cur} == -* ]]; then
        local brahma_config_opts=$(brahma config --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)
        COMPREPLY=($(compgen -W "${brahma_config_opts}" -- ${cur}))
      fi
      ;;
    update)
      if [[ ${cur} == -* ]]; then
        local brahma_update_opts=$(brahma update --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)
        COMPREPLY=($(compgen -W "${brahma_update_opts}" -- ${cur}))
      fi
      ;;
    info)
      if [[ ${cur} == -* ]]; then
        local brahma_info_opts=$(brahma info --help 2>&1 | sed -ne $OPTS_FILTER | sort -u)
        COMPREPLY=($(compgen -W "${brahma_info_opts}" -- ${cur}))
      fi
      ;;
  esac

  return 0
}

complete -F _brahma brahma
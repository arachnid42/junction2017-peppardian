# Took from here:
# https://unix.stackexchange.com/questions/175648/use-config-file-for-my-shell-script#331965
#
# After all, it's hackathon and we don't have time

config_read_file() {
    (grep -E "^${2}=" -m 1 "${1}" 2>/dev/null || echo "VAR=__UNDEFINED__") | \
        head -n 1 | cut -d '=' -f 2-;
}

config_get() {
    val="$(config_read_file config.cfg "${1}")";
    if [ "${val}" = "__UNDEFINED__" ]; then
        val="$(config_read_file config.cfg.defaults "${1}")";
    fi
    printf -- "%s" "${val}";
}

class PluginHook:
    PRE_BUILD = "pre-build"
    POST_BUILD = "post-build"
    PRE_START = "pre-start"
    POST_START = "post-start"
    PRE_GROUP_BUILD = "pre-group-build"
    POST_GROUP_BUILD = "post-group-build"
    PRE_GROUP_START = "pre-group-start"
    POST_GROUP_START = "post-group-start"
    DOCKER_FAILURE = "docker-fail"
    CONTAINER_FAILURE = "container-fail"

    valid_hooks = frozenset([
        PRE_BUILD,
        POST_BUILD,
        PRE_START,
        POST_START,
        PRE_GROUP_BUILD,
        POST_GROUP_BUILD,
        PRE_GROUP_START,
        POST_GROUP_START,
        DOCKER_FAILURE,
        CONTAINER_FAILURE,
    ])

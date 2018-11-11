from django.conf import settings

from flags import conditions


def _get_deploy_environment():
    print("DEPLOY_ENVIRONMENT => %s" % getattr(settings, "DEPLOY_ENVIRONMENT", "beta"))
    return getattr(settings, "DEPLOY_ENVIRONMENT", "beta")


@conditions.register("environment_is")
def environment_is_condition(environment, request=None, **kwargs):
    if request is None:
        raise conditions.RequiredForCondition(
            "request is required for condition 'environment_is'"
        )
    return environment == _get_deploy_environment()


@conditions.register("environment_is_not")
def environment_is_not_condition(environment, request=None, **kwargs):
    if request is None:
        raise conditions.RequiredForCondition(
            "request is required for condition 'environment_is_not'"
        )
    return environment != _get_deploy_environment()

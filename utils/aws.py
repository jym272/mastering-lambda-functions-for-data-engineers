import os

AWS_PROFILE = 'AWS_PROFILE'
profile = 'jorge-admin'


def aws_init_profile():
    aws_profile = os.environ.get(AWS_PROFILE)
    if aws_profile is None:
        os.environ[AWS_PROFILE] = profile
        aws_profile = os.environ.get(AWS_PROFILE)
    return aws_profile

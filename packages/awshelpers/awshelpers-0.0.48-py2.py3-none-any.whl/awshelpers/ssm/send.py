from awshelpers.ssm import _connect
from typing import List, Optional


def command(instance_ids: List[str], document_name: str, timeout: int, comment: str, commands: List[str],
            s3_region: Optional[str] = None,
            s3_bucket: Optional[str] = None, s3_prefix: Optional[str] = None) -> dict:
    """
    Sends a command to SSM.

    Args:
        instance_ids: A list of instance ids.
        document_name: The name of an existing AWS Command document or a custom document.
        timeout: Timeout in seconds for command to run.
        comment: A comment, useful when parsing large lists of commands.
        commands: A list of commands to run.
        s3_region: Deprecated, SSM automatically determines this.
        s3_bucket: The name of the S3 bucket to store command output in.
        s3_prefix (): The prefix to use within the S3 bucket.

    Returns:

    """
    kwargs = {'InstanceIds': instance_ids, 'DocumentName': document_name, 'TimeoutSeconds': timeout, 'Comment': comment,
              'Parameters': {'commands': commands}}
    if s3_region is not None:
        kwargs['OutputS3Region'] = s3_region
    if s3_bucket is not None:
        kwargs['OutputS3BucketName'] = s3_bucket
    if s3_prefix is not None:
        kwargs['OutputS3KeyPrefix'] = s3_prefix

    return _connect.client().send_command(**kwargs)

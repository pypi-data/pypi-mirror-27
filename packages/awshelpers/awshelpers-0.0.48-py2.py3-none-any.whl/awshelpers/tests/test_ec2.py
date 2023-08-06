from awshelpers.ec2 import describe as ec2_describe

AWSHELPERS_NETWORK_INTERFACE = 'eni-3b630110'
AWSHELPERS_INSTANCE_ID = 'i-073a59252f493d63a'


def test_describe_eip_addresses():
    """
    Lookup a known elastic IP for an ENI

    """
    assert len(ec2_describe.eip_addresses(
        [AWSHELPERS_NETWORK_INTERFACE], 'PublicIp')) >= 1


def test_describe_tags():
    """
    List tags of a known instance

    """
    assert len(ec2_describe.tags([AWSHELPERS_INSTANCE_ID])) > 0

def test_lan_addresses():
    """
    Retrieve the lan address of a know instance

    """
    assert len(ec2_describe.lan_addresses('all', 'test', 'endpoint')) > 0

def test_instance_ids():
    """
    Retrieve the instance id of a know instance

    Returns:

    """
    assert len(ec2_describe.instance_ids(ec2_describe.lan_addresses('beta', 'email-service', 'halon'))) > 0
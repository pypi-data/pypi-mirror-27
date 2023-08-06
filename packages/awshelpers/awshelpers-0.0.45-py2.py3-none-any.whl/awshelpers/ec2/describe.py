from awshelpers.ec2 import _connect


def eip_addresses(ids: list, attribute: str) -> list:
    """
    Describes Elastic IP details associated with an instance or instances
    and filters off of attribute.

    Args:
        ids: Network interface id(s).
        attribute: Value to return/search for.

    Returns:
        A list attributes.

    """

    filters = [
        {'Name': 'network-interface-id', 'Values': ids}
        ]

    interfaces = _connect.client().describe_addresses(Filters=filters)[
        'Addresses']

    return [interface[attribute] for interface in interfaces]


def lan_addresses(cloud: str, service: str, string: str) -> list:
    """
    Search EC2 instances via tags.

    Filter EC2 instances with tags of cloud, service, and a string identifier.

    Args:
        cloud: Alpha, beta, staging, production, etc.
        service: Name of the service eg: email-service.
        string: Value to include in the Name filter.

    Returns:
        LAN addresses of filters EC2 instances.

    """

    filters = [
        {'Name': 'tag:cloud', 'Values': [cloud]},
        {'Name': 'tag:service', 'Values': [service]},
        # make sure instance is running
        {'Name': 'instance-state-code', 'Values': ['16']},
        {'Name': 'tag:Name',
         'Values': ["{0}-{1}-{2}".format(cloud, service, string)]}
        ]

    return [
        instance.private_ip_address for instance in
        _connect.resource().instances.filter(Filters=filters)]


def instance_ids(private_ips: list) -> list:
    """
    Gets EC2 instance ID for each private ip address.

    Args:
        ips: List of LAN addresses.

    Returns:
        List of EC2 instance ids.

    """
    filters = [
        {'Name': 'private-ip-address', 'Values': private_ips}
        ]

    return [
        instance.instance_id for instance in
        _connect.resource().instances.filter(Filters=filters)]


def tags(instance_ids: list):
    """
    Describes tags for an instance(s).

    Args:
        instance_ids: EC2 instance IDs.

    Returns:
        A list of dicts of tag key/values.

    """
    filters = [
        {'Name': 'resource-id', 'Values': instance_ids}
        ]
    return _connect.client().describe_tags(Filters=filters)['Tags']

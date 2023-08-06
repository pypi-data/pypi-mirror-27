# Copyright (C) 2009 Robert Collins <robertc@robertcollins.net>
# Copyright (C) 2009 Canonical Ltd
# Copyright (C) 2009 Duncan McGreggor <oubiwann@adytum.us>
# Licenced under the txaws licence available at /LICENSE in the txaws source.

from datetime import datetime
import os

from dateutil.zoneinfo import gettz

from twisted.internet import reactor
from twisted.internet.defer import succeed, fail
from twisted.internet.error import ConnectionRefusedError
from twisted.protocols.policies import WrappingFactory
from twisted.python.failure import Failure
from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase
from twisted.web import server, static, util
from twisted.web.error import Error as TwistedWebError

from txaws.util import iso8601time
from txaws.credentials import ENV_ACCESS_KEY, ENV_SECRET_KEY, AWSCredentials
from txaws.ec2 import client
from txaws.ec2 import model
from txaws.ec2.exception import EC2Error
from txaws.exception import CredentialsNotFoundError
from txaws.service import AWSServiceEndpoint, EC2_ENDPOINT_US
from txaws.testing import payload
from txaws.testing.ec2 import FakePageGetter


class ReservationTestCase(TestCase):

    def test_reservation_creation(self):
        reservation = model.Reservation(
            "id1", "owner", groups=["one", "two"])
        self.assertEquals(reservation.reservation_id, "id1")
        self.assertEquals(reservation.owner_id, "owner")
        self.assertEquals(reservation.groups, ["one", "two"])


class InstanceTestCase(TestCase):

    def test_instance_creation(self):
        instance = model.Instance(
            "id1", "running", "type", "id2", "dns1", "dns2", "ip1",
            "ip2", "key", "ami", "time", "placement",
            ["prod1", "prod2"], "id3", "id4")
        self.assertEquals(instance.instance_id, "id1")
        self.assertEquals(instance.instance_state, "running")
        self.assertEquals(instance.instance_type, "type")
        self.assertEquals(instance.image_id, "id2")
        self.assertEquals(instance.private_dns_name, "dns1")
        self.assertEquals(instance.dns_name, "dns2")
        self.assertEquals(instance.private_ip_address, "ip1")
        self.assertEquals(instance.ip_address, "ip2")
        self.assertEquals(instance.key_name, "key")
        self.assertEquals(instance.ami_launch_index, "ami")
        self.assertEquals(instance.launch_time, "time")
        self.assertEquals(instance.placement, "placement")
        self.assertEquals(instance.product_codes, ["prod1", "prod2"])
        self.assertEquals(instance.kernel_id, "id3")
        self.assertEquals(instance.ramdisk_id, "id4")


class EC2ClientTestCase(TestCase):

    def test_init_no_creds(self):
        self.addCleanup(os.environ.update, os.environ.copy())
        self.addCleanup(os.environ.clear)
        os.environ.clear()
        os.environ.update([(ENV_ACCESS_KEY, "foo"), (ENV_SECRET_KEY, "bar")])

        ec2 = client.EC2Client()
        self.assertEqual(
            ec2.creds, AWSCredentials(access_key="foo", secret_key="bar"),
        )

    def test_post_method(self):
        """
        If the method of the endpoint is POST, the parameters are passed in the
        body.
        """
        self.addCleanup(setattr, client.Query, "get_page",
                        client.Query.get_page)

        def get_page(query, url, *args, **kwargs):
            self.assertEquals(args, ())
            self.assertEquals(
                kwargs["headers"],
                {"Content-Type": "application/x-www-form-urlencoded"})
            self.assertIn("postdata", kwargs)
            self.assertEquals(kwargs["method"], "POST")
            self.assertEquals(kwargs["timeout"], 30)
            return succeed(payload.sample_describe_instances_result)

        client.Query.get_page = get_page

        creds = AWSCredentials("foo", "bar")
        endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US, method="POST")
        ec2 = client.EC2Client(creds=creds, endpoint=endpoint)
        return ec2.describe_instances()

    def test_init_no_creds_non_available_errors(self):
        self.assertRaises(CredentialsNotFoundError, client.EC2Client)

    def test_init_explicit_creds(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds=creds)
        self.assertEqual(creds, ec2.creds)

    def test_describe_availability_zones_single(self):

        factory = make_query_factory(
            payload.sample_describe_availability_zones_single_result,
            "DescribeAvailabilityZones",
            "foo",
            "bar",
            {"ZoneName.1": "us-east-1a"},
        )

        def check_parsed_availability_zone(results):
            self.assertEquals(len(results), 1)
            [zone] = results
            self.assertEquals(zone.name, "us-east-1a")
            self.assertEquals(zone.state, "available")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.describe_availability_zones(["us-east-1a"])
        d.addCallback(check_parsed_availability_zone)
        return d

    def test_describe_availability_zones_multiple(self):

        factory = make_query_factory(
            payload.sample_describe_availability_zones_multiple_results,
            "DescribeAvailabilityZones",
            "foo",
            "bar",
            None,
        )

        def check_parsed_availability_zones(results):
            self.assertEquals(len(results), 3)
            self.assertEquals(results[0].name, "us-east-1a")
            self.assertEquals(results[0].state, "available")
            self.assertEquals(results[1].name, "us-east-1b")
            self.assertEquals(results[1].state, "available")
            self.assertEquals(results[2].name, "us-east-1c")
            self.assertEquals(results[2].state, "available")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.describe_availability_zones()
        d.addCallback(check_parsed_availability_zones)
        return d


class EC2ClientInstancesTestCase(TestCase):

    def check_parsed_instances(self, results):
        instance = results[0]
        # check reservations
        reservation = instance.reservation
        self.assertEquals(reservation.reservation_id, "r-cf24b1a6")
        self.assertEquals(reservation.owner_id, "123456789012")
        # check groups
        group = reservation.groups[0]
        self.assertEquals(group[0], "sg-64f9eb08")
        self.assertEquals(group[1], "default")
        # check instance
        self.assertEquals(instance.instance_id, "i-abcdef01")
        self.assertEquals(instance.instance_state, "running")
        self.assertEquals(instance.instance_type, "c1.xlarge")
        self.assertEquals(instance.image_id, "ami-12345678")
        self.assertEquals(
            instance.private_dns_name,
            "domU-12-31-39-03-15-11.compute-1.internal")
        self.assertEquals(
            instance.dns_name,
            "ec2-75-101-245-65.compute-1.amazonaws.com")
        self.assertEquals(instance.private_ip_address, "10.0.0.1")
        self.assertEquals(instance.ip_address, "75.101.245.65")
        self.assertEquals(instance.key_name, "keyname")
        self.assertEquals(instance.ami_launch_index, "0")
        self.assertEquals(instance.launch_time, "2009-04-27T02:23:18.000Z")
        self.assertEquals(instance.placement, "us-east-1c")
        self.assertEquals(instance.product_codes, ["774F4FF8"])
        self.assertEquals(instance.kernel_id, "aki-b51cf9dc")
        self.assertEquals(instance.ramdisk_id, "ari-b31cf9da")

    def check_parsed_instances_required(self, results):
        instance = results[0]
        # check reservations
        reservation = instance.reservation
        self.assertEquals(reservation.reservation_id, "r-cf24b1a6")
        self.assertEquals(reservation.owner_id, "123456789012")
        # check groups
        group = reservation.groups[0]
        self.assertEquals(group[0], "sg-64f9eb08")
        self.assertEquals(group[1], "default")
        # check instance
        self.assertEquals(instance.instance_id, "i-abcdef01")
        self.assertEquals(instance.instance_state, "running")
        self.assertEquals(instance.instance_type, "c1.xlarge")
        self.assertEquals(instance.image_id, "ami-12345678")
        self.assertEquals(
            instance.private_dns_name,
            "domU-12-31-39-03-15-11.compute-1.internal")
        self.assertEquals(
            instance.dns_name,
            "ec2-75-101-245-65.compute-1.amazonaws.com")
        self.assertEquals(instance.private_ip_address, "10.0.0.1")
        self.assertEquals(instance.ip_address, "75.101.245.65")
        self.assertEquals(instance.key_name, None)
        self.assertEquals(instance.ami_launch_index, None)
        self.assertEquals(instance.launch_time, "2009-04-27T02:23:18.000Z")
        self.assertEquals(instance.placement, "us-east-1c")
        self.assertEquals(instance.product_codes, [])
        self.assertEquals(instance.kernel_id, None)
        self.assertEquals(instance.ramdisk_id, None)

    def test_parse_reservation(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds=creds)
        results = ec2.parser.describe_instances(
            payload.sample_describe_instances_result)
        self.check_parsed_instances(results)

    def test_describe_instances(self):

        factory = make_query_factory(
            payload.sample_describe_instances_result,
            "DescribeInstances",
            "foo",
            "bar",
            {},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.describe_instances()
        d.addCallback(self.check_parsed_instances)
        return d

    def test_describe_instances_required(self):

        factory = make_query_factory(
            payload.sample_required_describe_instances_result,
            "DescribeInstances",
            "foo",
            "bar",
            {},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.describe_instances()
        d.addCallback(self.check_parsed_instances_required)
        return d

    def test_describe_instances_specific_instances(self):

        factory = make_query_factory(
            payload.sample_required_describe_instances_result,
            "DescribeInstances",
            "foo",
            "bar",
            {"InstanceId.1": "i-16546401",
             "InstanceId.2": "i-49873415"},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.describe_instances("i-16546401", "i-49873415")
        d.addCallback(self.check_parsed_instances_required)
        return d

    def test_terminate_instances(self):

        factory = make_query_factory(
            payload.sample_terminate_instances_result,
            "TerminateInstances",
            "foo",
            "bar",
            {"InstanceId.1": "i-1234", "InstanceId.2": "i-5678"},
        )

        def check_transition(changes):
            self.assertEqual([("i-1234", "running", "shutting-down"),
                ("i-5678", "shutting-down", "shutting-down")], sorted(changes))

        creds = AWSCredentials("foo", "bar")
        endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)
        ec2 = client.EC2Client(creds=creds, endpoint=endpoint,
                               query_factory=factory)
        d = ec2.terminate_instances("i-1234", "i-5678")
        d.addCallback(check_transition)
        return d

    def check_parsed_run_instances(self, results):
        instance = results[0]
        # check reservations
        reservation = instance.reservation
        self.assertEquals(reservation.reservation_id, "r-47a5402e")
        self.assertEquals(reservation.owner_id, "495219933132")
        # check groups
        group = reservation.groups[0]
        self.assertEquals(group[0], "sg-64f9eb08")
        self.assertEquals(group[1], "default")
        # check instance
        self.assertEquals(instance.instance_id, "i-2ba64342")
        self.assertEquals(instance.instance_state, "pending")
        self.assertEquals(instance.instance_type, "m1.small")
        self.assertEquals(instance.placement, "us-east-1b")
        instance = results[1]
        self.assertEquals(instance.instance_id, "i-2bc64242")
        self.assertEquals(instance.instance_state, "pending")
        self.assertEquals(instance.instance_type, "m1.small")
        self.assertEquals(instance.placement, "us-east-1b")
        instance = results[2]
        self.assertEquals(instance.instance_id, "i-2be64332")
        self.assertEquals(instance.instance_state, "pending")
        self.assertEquals(instance.instance_type, "m1.small")
        self.assertEquals(instance.placement, "us-east-1b")

    def test_run_instances(self):

        factory = make_query_factory(
            payload.sample_run_instances_result,
            "RunInstances",
            "foo",
            "bar",
            {"ImageId": "ami-1234", "MaxCount": "2", "MinCount": "1",
             "SecurityGroup.1": u"group1", "KeyName": u"default",
             "UserData": "Zm9v", "InstanceType": u"m1.small",
             "Placement.AvailabilityZone": u"us-east-1b",
             "KernelId": u"k-1234", "RamdiskId": u"r-1234"},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.run_instances("ami-1234", 1, 2, security_groups=[u"group1"],
            key_name=u"default", user_data=u"foo", instance_type=u"m1.small",
            availability_zone=u"us-east-1b", kernel_id=u"k-1234",
            ramdisk_id=u"r-1234")
        d.addCallback(self.check_parsed_run_instances)

    def test_run_instances_with_subnet(self):
        factory = make_query_factory(
            payload.sample_run_instances_result,
            "RunInstances",
            "foo",
            "bar",
            {"ImageId": "ami-1234", "MaxCount": "2", "MinCount": "1",
             "SecurityGroupId.1": u"sg-a72d9f92e", "KeyName": u"default",
             "UserData": "Zm9v", "InstanceType": u"m1.small",
             "Placement.AvailabilityZone": u"us-east-1b",
             "KernelId": u"k-1234", "RamdiskId": u"r-1234",
             "SubnetId": "subnet-a72d829f"},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.run_instances("ami-1234", 1, 2, security_group_ids=[u"sg-a72d9f92e"],
            key_name=u"default", user_data=u"foo", instance_type=u"m1.small",
            availability_zone=u"us-east-1b", kernel_id=u"k-1234",
            ramdisk_id=u"r-1234", subnet_id="subnet-a72d829f")
        d.addCallback(self.check_parsed_run_instances)

    def test_run_instances_with_subnet_but_without_secgroup_id(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.run_instances, "ami-1234", 1, 2,
            key_name=u"default", user_data=u"foo", instance_type=u"m1.small",
            availability_zone=u"us-east-1b", kernel_id=u"k-1234",
            ramdisk_id=u"r-1234", subnet_id="subnet-a72d829f")
        self.assertEqual(
            str(error),
            "You must specify the security_group_ids with the subnet_id"
        )

    def test_run_instances_without_subnet_and_secgroups(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.run_instances, "ami-1234", 1, 2,
            key_name=u"default", user_data=u"foo", instance_type=u"m1.small",
            availability_zone=u"us-east-1b", kernel_id=u"k-1234",
            ramdisk_id=u"r-1234")
        self.assertEqual(
            str(error),
            ("You must specify either the subnet_id and "
             "security_group_ids or security_groups")
        )


def make_query_factory(result, action, key_id, secret_key, params):
    class FakeQuery(object):
        def __init__(
                self, action, creds=None, endpoint=None,
                other_params={},
        ):
            self.action = action
            self.creds = creds
            self.endpoint = endpoint
            self.other_params = other_params

        def submit(self):
            mismatch = self._mismatches()
            if mismatch is None:
                return succeed(result)
            return fail(Exception(mismatch))

        def _mismatches(self):
            mismatches = []
            to_check = [
                ("action", self.action, action),
                ("key_id", self.creds.access_key, key_id),
                ("secret_key", self.creds.secret_key, secret_key),
                ("params", self.other_params, params),
            ]
            for label, actual, expected in to_check:
                if actual != expected:
                    mismatches.append(
                        "{}: got {}, expected {}".format(
                            label,
                            actual,
                            expected,
                        ),
                    )
            if mismatches:
                return "\n".join(mismatches)
            return None

    return FakeQuery


class FakeQueryTests(TestCase):
    """
    Tests for L{make_query_factory}.
    """
    def test_mismatch_action(self):
        """
        If there is a mismatch between the expected and presented action,
        submiting the query results in an error.
        """
        factory = make_query_factory(object(), b"GET", b"id", b"key", {})
        query = factory(b"POST", AWSCredentials(b"id", b"key"), other_params={})
        self.assertFailure(query.submit(), Exception)


class EC2ClientConsoleOutputTestCase(TestCase):
    def test_get_console_output(self):
        """
        L{EC2Client.get_console_output} returns a L{Deferred} that eventually
        fires with a L{ConsoleOutput} instance created using XML data received
        from the cloud.
        """
        creds = AWSCredentials("foo", "bar")
        instance_id = u"i-abcdef0123456789"
        query_factory = make_query_factory(
            payload.sample_get_console_output_result,
            "GetConsoleOutput",
            creds.access_key,
            creds.secret_key,
            {"InstanceId": instance_id},
        )

        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.get_console_output(instance_id)
        console_output = self.successResultOf(d)

        utc = gettz("UTC")
        self.assertEqual(
            console_output,
            model.ConsoleOutput(
                instance_id,
                # Take from hard-coded payload
                datetime(2010, 10, 14, 1, 12, 41, tzinfo=utc),
                u"""\
Linux version 2.6.16-xenU (builder@patchbat.amazonsa) (gcc version 4.0.1 20050727 (Red Hat 4.0.1-5)) #1 SMP Thu Oct 26 08:41:26 SAST 2006
BIOS-provided physical RAM map:
Xen: 0000000000000000 - 000000006a400000 (usable)
980MB HIGHMEM available.
727MB LOWMEM available.
NX (Execute Disable) protection: active
IRQ lockup detection disabled
Built 1 zonelists
Kernel command line: root=/dev/sda1 ro 4
Enabling fast FPU save and restore... done.
""",
            ),
        )



class EC2ClientSecurityGroupsTestCase(TestCase):

    def test_describe_security_groups(self):
        """
        L{EC2Client.describe_security_groups} returns a C{Deferred} that
        eventually fires with a list of L{SecurityGroup} instances created
        using XML data received from the cloud.
        """
        query_factory = make_query_factory(
            payload.sample_describe_security_groups_result,
            "DescribeSecurityGroups",
            "foo",
            "bar",
            {},
        )

        def check_results(security_groups):
            [security_group] = security_groups
            self.assertEquals(security_group.id, "sg-a1a1a1")
            self.assertEquals(security_group.owner_id,
                              "UYY3TLBUXIEON5NQVUUX6OMPWBZIQNFM")
            self.assertEquals(security_group.name, "WebServers")
            self.assertEquals(security_group.description, "Web Servers")
            self.assertEquals(security_group.allowed_groups, [])
            self.assertEquals(
                [(ip.ip_protocol, ip.from_port, ip.to_port, ip.cidr_ip)
                 for ip in security_group.allowed_ips],
                [("tcp", 80, 80, "0.0.0.0/0")])

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.describe_security_groups()
        return d.addCallback(check_results)

    def test_describe_security_groups_with_multiple_results(self):
        """
        The C{DescribeSecurityGroupsResponse} XML payload retrieved when
        L{EC2Client.describe_security_groups} is called can contain
        information about more than one L{SecurityGroup}.
        """
        query_factory = make_query_factory(
            payload.sample_describe_security_groups_multiple_result,
            "DescribeSecurityGroups",
            "foo",
            "bar",
            {},
        )

        def check_results(security_groups):
            self.assertEquals(len(security_groups), 2)

            security_group = security_groups[0]
            self.assertEquals(security_group.owner_id,
                              "UYY3TLBUXIEON5NQVUUX6OMPWBZIQNFM")
            self.assertEquals(security_group.id, "sg-a1a1a1")
            self.assertEquals(security_group.name, "MessageServers")
            self.assertEquals(security_group.description, "Message Servers")
            self.assertEquals(security_group.allowed_groups, [])
            self.assertEquals(
                [(ip.ip_protocol, ip.from_port, ip.to_port, ip.cidr_ip)
                 for ip in security_group.allowed_ips],
                [("tcp", 80, 80, "0.0.0.0/0")])

            security_group = security_groups[1]
            self.assertEquals(security_group.owner_id,
                              "UYY3TLBUXIEON5NQVUUX6OMPWBZIQNFM")
            self.assertEquals(security_group.id, "sg-c3c3c3")
            self.assertEquals(security_group.name, "WebServers")
            self.assertEquals(security_group.description, "Web Servers")
            self.assertEquals([(pair.user_id, pair.group_name)
                               for pair in security_group.allowed_groups],
                              [("group-user-id", "group-name1"),
                               ("group-user-id", "group-name2")])
            self.assertEquals(
                [(ip.ip_protocol, ip.from_port, ip.to_port, ip.cidr_ip)
                 for ip in security_group.allowed_ips],
                [("tcp", 80, 80, "0.0.0.0/0")])

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.describe_security_groups()
        return d.addCallback(check_results)

    def test_describe_security_groups_with_multiple_groups(self):
        """
        Several groups can be contained in a single ip permissions content, and
        there are recognized by the group parser.
        """
        query_factory = make_query_factory(
            payload.sample_describe_security_groups_multiple_groups,
            "DescribeSecurityGroups",
            "foo",
            "bar",
            {},
        )

        def check_results(security_groups):
            self.assertEquals(len(security_groups), 1)

            security_group = security_groups[0]
            self.assertEquals(security_group.name, "web/ssh")
            self.assertEquals([(pair.user_id, pair.group_name)
                               for pair in security_group.allowed_groups],
                              [("170723411662", "default"),
                               ("175723011368", "test1")])
            self.assertEquals(
                [(ip.ip_protocol, ip.from_port, ip.to_port, ip.cidr_ip)
                 for ip in security_group.allowed_ips],
                [('tcp', 22, 22, '0.0.0.0/0'), ("tcp", 80, 80, "0.0.0.0/0")])

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.describe_security_groups()
        return d.addCallback(check_results)

    def test_describe_security_groups_with_name(self):
        """
        L{EC2Client.describe_security_groups} optionally takes a list of
        security group names to limit results to.
        """
        query_factory = make_query_factory(
            payload.sample_describe_security_groups_result,
            "DescribeSecurityGroups",
            "foo",
            "bar",
            {"GroupName.1": "WebServers"},
        )

        def check_result(security_groups):
            [security_group] = security_groups
            self.assertEquals(security_group.name, "WebServers")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.describe_security_groups("WebServers")
        return d.addCallback(check_result)

    def test_describe_security_groups_with_openstack(self):
        """
        L{EC2Client.describe_security_groups} can work with openstack
        responses, which may lack proper port information for
        self-referencing group. Verifying that the response doesn't
        cause an internal error, workaround for nova launchpad bug
        #829609.
        """
        query_factory = make_query_factory(
            payload.sample_describe_security_groups_with_openstack,
            "DescribeSecurityGroups",
            "foo",
            "bar",
            {"GroupName.1": "WebServers"},
        )

        def check_result(security_groups):
            [security_group] = security_groups
            self.assertEquals(security_group.name, "WebServers")
            self.assertEqual(
                security_group.allowed_groups[0].group_name, "WebServers")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.describe_security_groups("WebServers")
        return d.addCallback(check_result)

    def test_create_security_group(self):
        """
        L{EC2Client.create_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        query_factory = make_query_factory(
            payload.sample_create_security_group,
            "CreateSecurityGroup",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "GroupDescription": "The group for the web server farm.",
            },
        )

        def check_result(id):
            self.assertEquals(id, "sg-1a2b3c4d")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.create_security_group(
            "WebServers",
            "The group for the web server farm.")
        return d.addCallback(check_result)

    def test_create_security_group_with_VPC(self):
        query_factory = make_query_factory(
            payload.sample_create_security_group,
            "CreateSecurityGroup",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "GroupDescription": "The group for the web server farm.",
                "VpcId": "vpc-a4f2",
            },
        )

        def check_result(id):
            self.assertEquals(id, "sg-1a2b3c4d")

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.create_security_group(
            "WebServers",
            "The group for the web server farm.",
            "vpc-a4f2")
        return d.addCallback(check_result)

    def test_delete_security_group_using_name(self):
        """
        L{EC2Client.delete_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        query_factory = make_query_factory(
            payload.sample_delete_security_group,
            "DeleteSecurityGroup",
            "foo",
            "bar",
            {"GroupName": "WebServers"},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.delete_security_group("WebServers")
        return self.assertTrue(d)

    def test_delete_security_group_using_id(self):
        """
        L{EC2Client.delete_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        query_factory = make_query_factory(
            payload.sample_delete_security_group,
            "DeleteSecurityGroup",
            "foo",
            "bar",
            {"GroupId": "sg-a1a1a1"},
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        d = ec2.delete_security_group(id="sg-a1a1a1")
        return self.assertTrue(d)

    def test_delete_security_group_without_id_and_name(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.delete_security_group)
        self.assertEquals(
            str(error),
            "You must provide either the security group name or id",
        )

    def test_delete_security_group_failure(self):
        """
        L{EC2Client.delete_security_group} returns a C{Deferred} that
        eventually fires with a failure when EC2 is asked to delete a group
        that another group uses in that other group's policy.
        """
        query_factory = make_query_factory(
            Failure(EC2Error(
                payload.sample_delete_security_group_failure, 400,
            )),
            "DeleteSecurityGroup",
            "foo",
            "bar",
            {"GroupName": "GroupReferredTo"},
        )

        def check_error(error):
            self.assertEquals(
                str(error),
                ("Error Message: Group groupID1:GroupReferredTo is used by "
                 "groups: groupID2:UsingGroup"))

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=query_factory)
        failure = ec2.delete_security_group("GroupReferredTo")
        d = self.assertFailure(failure, EC2Error)
        return d.addCallback(check_error)

    def test_authorize_security_group_with_user_group_pair(self):
        """
        L{EC2Client.authorize_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions; this test checks the first
        way.
        """
        factory = make_query_factory(
            payload.sample_authorize_security_group,
            "AuthorizeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.authorize_security_group(
            group_name="WebServers", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_authorize_security_group_using_group_id(self):
        factory = make_query_factory(
            payload.sample_authorize_security_group,
            "AuthorizeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupId": "sg-a1b2c3d4e5f6",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.authorize_security_group(
            group_id="sg-a1b2c3d4e5f6", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_authorize_security_group_without_group_id_and_group_name(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.authorize_security_group,
                source_group_name="AppServers", source_group_owner_id="123456789123")
        self.assertEquals(
            str(error),
            "You must specify either the group name of the group id.")

    def test_authorize_security_group_with_ip_permissions(self):
        """
        L{EC2Client.authorize_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions; this test checks the second
        way.
        """
        factory = make_query_factory(
            payload.sample_authorize_security_group,
            "AuthorizeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "FromPort": "22", "ToPort": "80",
                "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.authorize_security_group(
            group_name="WebServers", ip_protocol="tcp", from_port="22", to_port="80",
            cidr_ip="0.0.0.0/0")
        return self.assertTrue(d)

    def test_authorize_security_group_with_missing_parameters(self):
        """
        L{EC2Client.authorize_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions. If not all group-setting
        parameters are set and not all IP permission parameters are set, an
        error is raised.
        """
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.authorize_security_group,
                group_name="WebServers", ip_protocol="tcp", from_port="22")
        self.assertEquals(
            str(error),
            ("You must specify either both group parameters or all the "
             "ip parameters."))

    def test_authorize_group_permission(self):
        """
        L{EC2Client.authorize_group_permission} returns a C{Deferred}
        that eventually fires with a true value, indicating the success of the
        operation.
        """
        factory = make_query_factory(
            payload.sample_authorize_security_group,
            "AuthorizeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.authorize_group_permission(
            "WebServers", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_authorize_ip_permission(self):
        """
        L{EC2Client.authorize_ip_permission} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        factory = make_query_factory(
            payload.sample_authorize_security_group,
            "AuthorizeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "FromPort": "22", "ToPort": "80",
                "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.authorize_ip_permission(
            "WebServers", ip_protocol="tcp", from_port="22", to_port="80",
            cidr_ip="0.0.0.0/0")
        return self.assertTrue(d)

    def test_revoke_security_group_with_user_group_pair(self):
        """
        L{EC2Client.revoke_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions; this test checks the first
        way.
        """
        factory = make_query_factory(
            payload.sample_revoke_security_group,
            "RevokeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.revoke_security_group(
            "WebServers", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_revoke_security_group_using_group_id(self):
        factory = make_query_factory(
            payload.sample_revoke_security_group,
            "RevokeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupId": "sg-a1a1a1",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.revoke_security_group(
            group_id="sg-a1a1a1", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_revoke_security_group_with_ip_permissions(self):
        """
        L{EC2Client.revoke_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions; this test checks the second
        way.
        """
        factory = make_query_factory(
            payload.sample_revoke_security_group,
            "RevokeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "FromPort": "22", "ToPort": "80",
                "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.revoke_security_group(
            "WebServers", ip_protocol="tcp", from_port="22", to_port="80",
            cidr_ip="0.0.0.0/0")
        return self.assertTrue(d)

    def test_revoke_security_group_without_group_id_and_group_name(self):
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.revoke_security_group,
                source_group_name="AppServers", source_group_owner_id="123456789123")
        self.assertEquals(
            str(error),
            "You must specify either the group name of the group id.")

    def test_revoke_security_group_with_missing_parameters(self):
        """
        L{EC2Client.revoke_security_group} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation. There are two ways to use the method: set another group's
        IP permissions or set new IP permissions. If not all group-setting
        parameters are set and not all IP permission parameters are set, an
        error is raised.
        """
        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds)
        error = self.assertRaises(ValueError, ec2.revoke_security_group,
                group_name="WebServers", ip_protocol="tcp", from_port="22")
        self.assertEquals(
            str(error),
            ("You must specify either both group parameters or all the "
             "ip parameters."))

    def test_revoke_group_permission(self):
        """
        L{EC2Client.revoke_group_permission} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        factory = make_query_factory(
            payload.sample_revoke_security_group,
            "RevokeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "SourceSecurityGroupName": "AppServers",
                "SourceSecurityGroupOwnerId": "123456789123",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.revoke_group_permission(
            "WebServers", source_group_name="AppServers",
            source_group_owner_id="123456789123")
        return self.assertTrue(d)

    def test_revoke_ip_permission(self):
        """
        L{EC2Client.revoke_ip_permission} returns a C{Deferred} that
        eventually fires with a true value, indicating the success of the
        operation.
        """
        factory = make_query_factory(
            payload.sample_revoke_security_group,
            "RevokeSecurityGroupIngress",
            "foo",
            "bar",
            {
                "GroupName": "WebServers",
                "FromPort": "22", "ToPort": "80",
                "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0",
            },
        )

        creds = AWSCredentials("foo", "bar")
        ec2 = client.EC2Client(creds, query_factory=factory)
        d = ec2.revoke_ip_permission(
            "WebServers", ip_protocol="tcp", from_port="22", to_port="80",
            cidr_ip="0.0.0.0/0")
        return self.assertTrue(d)


class EC2ClientEBSTestCase(TestCase):

    def setUp(self):
        self.creds = AWSCredentials("foo", "bar")
        self.endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)

    def check_parsed_volumes(self, volumes):
        self.assertEquals(len(volumes), 1)
        volume = volumes[0]
        self.assertEquals(volume.id, "vol-4282672b")
        self.assertEquals(volume.size, 800)
        self.assertEquals(volume.status, "in-use")
        self.assertEquals(volume.availability_zone, "us-east-1a")
        self.assertEquals(volume.snapshot_id, "snap-12345678")
        create_time = datetime(2008, 05, 07, 11, 51, 50)
        self.assertEquals(volume.create_time, create_time)
        self.assertEquals(len(volume.attachments), 1)
        attachment = volume.attachments[0]
        self.assertEquals(attachment.instance_id, "i-6058a509")
        self.assertEquals(attachment.status, "attached")
        self.assertEquals(attachment.device, u"/dev/sdh")
        attach_time = datetime(2008, 05, 07, 12, 51, 50)
        self.assertEquals(attachment.attach_time, attach_time)

    def test_describe_volumes(self):

        factory = make_query_factory(
            payload.sample_describe_volumes_result,
            "DescribeVolumes",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_volumes()
        d.addCallback(self.check_parsed_volumes)
        return d

    def test_describe_specified_volumes(self):

        factory = make_query_factory(
            payload.sample_describe_volumes_result,
            "DescribeVolumes",
            "foo",
            "bar",
            {"VolumeId.1": "vol-4282672b"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_volumes("vol-4282672b")
        d.addCallback(self.check_parsed_volumes)
        return d

    def check_parsed_snapshots(self, snapshots):
        self.assertEquals(len(snapshots), 1)
        snapshot = snapshots[0]
        self.assertEquals(snapshot.id, "snap-78a54011")
        self.assertEquals(snapshot.volume_id, "vol-4d826724")
        self.assertEquals(snapshot.status, "pending")
        start_time = datetime(2008, 05, 07, 12, 51, 50)
        self.assertEquals(snapshot.start_time, start_time)
        self.assertEquals(snapshot.progress, 0.8)

    def test_describe_snapshots(self):

        factory = make_query_factory(
            payload.sample_describe_snapshots_result,
            "DescribeSnapshots",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_snapshots()
        d.addCallback(self.check_parsed_snapshots)
        return d

    def test_describe_specified_snapshots(self):

        factory = make_query_factory(
            payload.sample_describe_snapshots_result,
            "DescribeSnapshots",
            "foo",
            "bar",
            {"SnapshotId.1": "snap-78a54011"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_snapshots("snap-78a54011")
        d.addCallback(self.check_parsed_snapshots)
        return d

    def test_create_volume(self):

        factory = make_query_factory(
            payload.sample_create_volume_result,
            "CreateVolume",
            "foo",
            "bar",
            {"AvailabilityZone": "us-east-1", "Size": "800"},
        )

        def check_parsed_volume(volume):
            self.assertEquals(volume.id, "vol-4d826724")
            self.assertEquals(volume.size, 800)
            self.assertEquals(volume.snapshot_id, "")
            create_time = datetime(2008, 05, 07, 11, 51, 50)
            self.assertEquals(volume.create_time, create_time)

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.create_volume("us-east-1", size=800)
        d.addCallback(check_parsed_volume)
        return d

    def test_create_volume_with_snapshot(self):

        factory = make_query_factory(
            payload.sample_create_volume_result,
            "CreateVolume",
            "foo",
            "bar",
            {"AvailabilityZone": "us-east-1",
             "SnapshotId": "snap-12345678"},
        )

        def check_parsed_volume(volume):
            self.assertEquals(volume.id, "vol-4d826724")
            self.assertEquals(volume.size, 800)
            create_time = datetime(2008, 05, 07, 11, 51, 50)
            self.assertEquals(volume.create_time, create_time)

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.create_volume("us-east-1", snapshot_id="snap-12345678")
        d.addCallback(check_parsed_volume)
        return d

    def test_create_volume_no_params(self):
        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint)
        error = self.assertRaises(ValueError, ec2.create_volume, "us-east-1")
        self.assertEquals(
            str(error),
            "Please provide either size or snapshot_id")

    def test_create_volume_both_params(self):
        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint)
        error = self.assertRaises(ValueError, ec2.create_volume, "us-east-1",
                                  size=800, snapshot_id="snap-12345678")
        self.assertEquals(
            str(error),
            "Please provide either size or snapshot_id")

    def test_delete_volume(self):

        factory = make_query_factory(
            payload.sample_delete_volume_result,
            "DeleteVolume",
            "foo",
            "bar",
            {"VolumeId": "vol-4282672b"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.delete_volume("vol-4282672b")
        d.addCallback(self.assertEquals, True)
        return d

    def test_create_snapshot(self):

        factory = make_query_factory(
            payload.sample_create_snapshot_result,
            "CreateSnapshot",
            "foo",
            "bar",
            {"VolumeId": "vol-4d826724"},
        )

        def check_parsed_snapshot(snapshot):
            self.assertEquals(snapshot.id, "snap-78a54011")
            self.assertEquals(snapshot.volume_id, "vol-4d826724")
            self.assertEquals(snapshot.status, "pending")
            start_time = datetime(2008, 05, 07, 12, 51, 50)
            self.assertEquals(snapshot.start_time, start_time)
            self.assertEquals(snapshot.progress, 0)

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.create_snapshot("vol-4d826724")
        d.addCallback(check_parsed_snapshot)
        return d

    def test_delete_snapshot(self):

        factory = make_query_factory(
            payload.sample_delete_snapshot_result,
            "DeleteSnapshot",
            "foo",
            "bar",
            {"SnapshotId": "snap-78a54011"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.delete_snapshot("snap-78a54011")
        d.addCallback(self.assertEquals, True)
        return d

    def test_attach_volume(self):

        factory = make_query_factory(
            payload.sample_attach_volume_result,
            "AttachVolume",
            "foo",
            "bar",
            {"VolumeId": "vol-4d826724", "InstanceId": "i-6058a509",
             "Device": "/dev/sdh"},
        )

        def check_parsed_response(response):
            self.assertEquals(
                response,
                {"status": "attaching",
                 "attach_time": datetime(2008, 05, 07, 11, 51, 50)})

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.attach_volume("vol-4d826724", "i-6058a509", "/dev/sdh")
        d.addCallback(check_parsed_response)
        return d

    def check_parsed_keypairs(self, results):
        self.assertEquals(len(results), 1)
        keypair = results[0]
        self.assertEquals(keypair.name, "gsg-keypair")
        self.assertEquals(
            keypair.fingerprint,
            "1f:51:ae:28:bf:89:e9:d8:1f:25:5d:37:2d:7d:b8:ca:9f:f5:f1:6f")

    def test_single_describe_keypairs(self):

        factory = make_query_factory(
            payload.sample_single_describe_keypairs_result,
            "DescribeKeyPairs",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.describe_keypairs()
        d.addCallback(self.check_parsed_keypairs)
        return d

    def test_multiple_describe_keypairs(self):

        def check_parsed_keypairs(results):
            self.assertEquals(len(results), 2)
            keypair1, keypair2 = results
            self.assertEquals(keypair1.name, "gsg-keypair-1")
            self.assertEquals(
                keypair1.fingerprint,
                "1f:51:ae:28:bf:89:e9:d8:1f:25:5d:37:2d:7d:b8:ca:9f:f5:f1:6f")
            self.assertEquals(keypair2.name, "gsg-keypair-2")
            self.assertEquals(
                keypair2.fingerprint,
                "1f:51:ae:28:bf:89:e9:d8:1f:25:5d:37:2d:7d:b8:ca:9f:f5:f1:70")

        factory = make_query_factory(
            payload.sample_multiple_describe_keypairs_result,
            "DescribeKeyPairs",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.describe_keypairs()
        d.addCallback(check_parsed_keypairs)
        return d

    def test_describe_specified_keypairs(self):

        factory = make_query_factory(
            payload.sample_single_describe_keypairs_result,
            "DescribeKeyPairs",
            "foo",
            "bar",
            {"KeyName.1": "gsg-keypair"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.describe_keypairs("gsg-keypair")
        d.addCallback(self.check_parsed_keypairs)
        return d

    def test_create_keypair(self):

        def check_parsed_create_keypair(keypair):
            self.assertEquals(keypair.name, "example-key-name")
            self.assertEquals(
                keypair.fingerprint,
                "1f:51:ae:28:bf:89:e9:d8:1f:25:5d:37:2d:7d:b8:ca:9f:f5:f1:6f")
            self.assertTrue(keypair.material.startswith(
                "-----BEGIN RSA PRIVATE KEY-----"))
            self.assertTrue(keypair.material.endswith(
                "-----END RSA PRIVATE KEY-----"))
            self.assertEquals(len(keypair.material), 1670)

        factory = make_query_factory(
            payload.sample_create_keypair_result,
            "CreateKeyPair",
            "foo",
            "bar",
            {"KeyName": "example-key-name"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.create_keypair("example-key-name")
        d.addCallback(check_parsed_create_keypair)
        return d

    def test_delete_keypair_true_result(self):

        factory = make_query_factory(
            payload.sample_delete_keypair_true_result,
            "DeleteKeyPair",
            "foo",
            "bar",
            {"KeyName": "example-key-name"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.delete_keypair("example-key-name")
        d.addCallback(self.assertTrue)
        return d

    def test_delete_keypair_false_result(self):

        factory = make_query_factory(
            payload.sample_delete_keypair_false_result,
            "DeleteKeyPair",
            "foo",
            "bar",
            {"KeyName": "example-key-name"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.delete_keypair("example-key-name")
        d.addCallback(self.assertFalse)
        return d

    def test_delete_keypair_no_result(self):

        factory = make_query_factory(
            payload.sample_delete_keypair_no_result,
            "DeleteKeyPair",
            "foo",
            "bar",
            {"KeyName": "example-key-name"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        d = ec2.delete_keypair("example-key-name")
        d.addCallback(self.assertFalse)
        return d

    def test_import_keypair(self):
        """
        L{client.EC2Client.import_keypair} calls the C{ImportKeyPair} method
        with the given arguments, encoding the key material in base64, and
        returns a C{Keypair} instance.
        """

        def check_parsed_import_keypair(keypair):
            self.assertEquals(keypair.name, "example-key-name")
            self.assertEquals(
                keypair.fingerprint,
                "1f:51:ae:28:bf:89:e9:d8:1f:25:5d:37:2d:7d:b8:ca:9f:f5:f1:6f")
            self.assertEquals(keypair.material, material)

        factory = make_query_factory(
            payload.sample_import_keypair_result,
            "ImportKeyPair",
            "foo",
            "bar",
            {"KeyName": "example-key-name",
             "PublicKeyMaterial":
             "c3NoLWRzcyBBQUFBQjNOemFDMWtjM01BQUFDQkFQNmFjakFQeitUR"
             "jJkREtmZGlhcnp2cXBBcjhlbUl6UElBWUp6QXNoTFgvUTJCZ2tWc0"
             "42eGI2QUlIUGE1MUFtWXVieU5PYjMxeVhWS2FRQTF6L213SHZtRld"
             "LQ1ZFQ0wwPSkgdXNlckBob3N0"},
        )

        ec2 = client.EC2Client(creds=self.creds, query_factory=factory)
        material = (
            "ssh-dss AAAAB3NzaC1kc3MAAACBAP6acjAPz+TF2dDKfdiarzvqpAr8emIzPIAY"
            "JzAshLX/Q2BgkVsN6xb6AIHPa51AmYubyNOb31yXVKaQA1z/mwHvmFWKCVECL0=)"
            " user@host")
        d = ec2.import_keypair("example-key-name", material)
        d.addCallback(check_parsed_import_keypair)
        return d


class EC2ErrorWrapperTestCase(TestCase):

    def make_failure(self, status=None, type=None, message="", response=""):
        if not response:
            response = payload.sample_ec2_error_message
        if type is TwistedWebError:
            error = type(status, message, response)
        elif message:
            error = type(message)
        else:
            error = type()
        return Failure(error)

    def test_302_error(self):
        failure = self.make_failure(302, Exception, "found")
        error = self.assertRaises(Exception, client.ec2_error_wrapper, failure)
        self.assertEquals(failure.type, type(error))
        self.assertFalse(isinstance(error, EC2Error))
        self.assertTrue(isinstance(error, Exception))
        self.assertEquals(str(error), "found")

    def test_400_error(self):
        failure = self.make_failure(400, TwistedWebError)
        error = self.assertRaises(EC2Error, client.ec2_error_wrapper, failure)
        self.assertNotEquals(failure.type, type(error))
        self.assertTrue(isinstance(error, EC2Error))
        self.assertEquals(error.get_error_codes(), "Error.Code")
        self.assertEquals(error.get_error_messages(), "Message for Error.Code")

    def test_404_error(self):
        failure = self.make_failure(404, TwistedWebError)
        error = self.assertRaises(EC2Error, client.ec2_error_wrapper, failure)
        self.assertNotEquals(failure.type, type(error))
        self.assertTrue(isinstance(error, EC2Error))
        self.assertEquals(error.get_error_codes(), "Error.Code")
        self.assertEquals(error.get_error_messages(), "Message for Error.Code")

    def test_non_EC2_404_error(self):
        """
        The error wrapper should handle cases where an endpoint returns a
        non-EC2 404.
        """
        status = "404"
        some_html = "<html><body>{}</body></html>".format(status)
        failure = self.make_failure(status, TwistedWebError, "not found",
                                    some_html)
        error = self.assertRaises(
            TwistedWebError, client.ec2_error_wrapper, failure)
        self.assertTrue(isinstance(error, TwistedWebError))
        self.assertEquals(error.status, status)
        self.assertEquals(str(error), "{} Not Found".format(status))

    def test_500_error(self):
        failure = self.make_failure(
            500, type=TwistedWebError,
            response=payload.sample_server_internal_error_result)
        error = self.assertRaises(EC2Error, client.ec2_error_wrapper, failure)
        self.assertTrue(isinstance(error, EC2Error))
        self.assertEquals(error.get_error_codes(), "InternalError")
        self.assertEquals(
            error.get_error_messages(),
            "We encountered an internal error. Please try again.")
        self.assertEquals(error.request_id, "A2A7E5395E27DFBB")
        self.assertEquals(
            error.host_id,
            "f691zulHNsUqonsZkjhILnvWwD3ZnmOM4ObM1wXTc6xuS3GzPmjArp8QC/sGsn6K")

    def test_non_EC2_500_error(self):
        failure = self.make_failure(500, Exception, "A server error occurred")
        error = self.assertRaises(Exception, client.ec2_error_wrapper, failure)
        self.assertFalse(isinstance(error, EC2Error))
        self.assertTrue(isinstance(error, Exception))
        self.assertEquals(str(error), "A server error occurred")

    def test_timeout_error(self):
        failure = self.make_failure(type=Exception, message="timeout")
        error = self.assertRaises(Exception, client.ec2_error_wrapper, failure)
        self.assertFalse(isinstance(error, EC2Error))
        self.assertTrue(isinstance(error, Exception))
        self.assertEquals(str(error), "timeout")

    def test_connection_error(self):
        failure = self.make_failure(type=ConnectionRefusedError)
        error = self.assertRaises(ConnectionRefusedError,
                                  client.ec2_error_wrapper, failure)
        self.assertFalse(isinstance(error, EC2Error))
        self.assertTrue(isinstance(error, ConnectionRefusedError))

    def test_response_parse_error(self):
        bad_payload = "<bad></xml>"
        failure = self.make_failure(400, type=TwistedWebError,
                                    response=bad_payload)
        error = self.assertRaises(Exception, client.ec2_error_wrapper, failure)
        self.assertEquals(str(error), "400 Bad Request")


class QueryTestCase(TestCase):

    def setUp(self):
        self.creds = AWSCredentials("foo", "bar")
        self.endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)

    def test_init_minimum(self):
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint)
        self.assertTrue("Timestamp" in query.params)
        del query.params["Timestamp"]
        self.assertEqual(
            query.params,
            {"AWSAccessKeyId": "foo",
             "Action": "DescribeInstances",
             "SignatureVersion": "2",
             "Version": "2012-08-15"})

    def test_init_other_args_are_params(self):
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint, other_params={"InstanceId.0": "12345"},
            time_tuple=(2007, 11, 12, 13, 14, 15, 0, 0, 0))
        self.assertEqual(
            query.params,
            {"AWSAccessKeyId": "foo",
             "Action": "DescribeInstances",
             "InstanceId.0": "12345",
             "SignatureVersion": "2",
             "Timestamp": "2007-11-12T13:14:15Z",
             "Version": "2012-08-15"})

    def test_no_timestamp_if_expires_in_other_params(self):
        """
        If Expires is present in other_params, Timestamp won't be added,
        since a request should contain either Expires or Timestamp, but
        not both.
        """
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint,
            other_params={"Expires": "2007-11-12T13:14:15Z"})
        self.assertEqual(
            query.params,
            {"AWSAccessKeyId": "foo",
             "Action": "DescribeInstances",
             "SignatureVersion": "2",
             "Expires": "2007-11-12T13:14:15Z",
             "Version": "2012-08-15"})

    def test_sign(self):
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint,
            time_tuple=(2007, 11, 12, 13, 14, 15, 0, 0, 0))
        query.sign()
        self.assertEqual("c0gbkemrGEJdqxWOl2UZYaygYiBLVjrpWBs7bTN7Ndo=",
            query.params["Signature"])

    def test_old_sign(self):
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint,
            time_tuple=(2007, 11, 12, 13, 14, 15, 0, 0, 0),
            other_params={"SignatureVersion": "1"})
        query.sign()
        self.assertEqual(
            "7tWrIC5VYvXOjVE+roVoyDUt2Yw=", query.params["Signature"])

    def test_unsupported_sign(self):
        query = client.Query(
            action="DescribeInstances", creds=self.creds,
            endpoint=self.endpoint,
            time_tuple=(2007, 11, 12, 13, 14, 15, 0, 0, 0),
            other_params={"SignatureVersion": "0"})
        self.assertRaises(RuntimeError, query.sign)

    def test_submit_with_port(self):
        """
        If the endpoint port differs from the default one, the Host header
        of the request will include it.
        """
        self.addCleanup(setattr, client.Query, "get_page",
                        client.Query.get_page)

        def get_page(query, url, **kwargs):
            self.assertEqual("example.com:99", kwargs["headers"]["Host"])
            return succeed(None)

        client.Query.get_page = get_page
        endpoint = AWSServiceEndpoint(uri="http://example.com:99/foo")
        query = client.Query(action="SomeQuery", creds=self.creds,
                             endpoint=endpoint)

        d = query.submit()
        return d

    def test_submit_400(self):
        """A 4xx response status from EC2 should raise a txAWS EC2Error."""
        status = "400"
        self.addCleanup(setattr, client.Query, "get_page",
                        client.Query.get_page)
        fake_page_getter = FakePageGetter(
            status, payload.sample_ec2_error_message)
        client.Query.get_page = fake_page_getter.get_page_with_exception

        def check_error(error):
            self.assertTrue(isinstance(error, EC2Error))
            self.assertEquals(error.get_error_codes(), "Error.Code")
            self.assertEquals(
                error.get_error_messages(),
                "Message for Error.Code")
            self.assertEquals(error.status, status)
            self.assertEquals(error.response, payload.sample_ec2_error_message)

        query = client.Query(
            action='BadQuery', creds=self.creds, endpoint=self.endpoint,
            time_tuple=(2009, 8, 15, 13, 14, 15, 0, 0, 0))

        failure = query.submit()
        d = self.assertFailure(failure, TwistedWebError)
        d.addCallback(check_error)
        return d

    def test_submit_non_EC2_400(self):
        """
        A 4xx response status from a non-EC2 compatible service should raise a
        Twisted web error.
        """
        status = "400"
        self.addCleanup(setattr, client.Query, "get_page",
                        client.Query.get_page)
        fake_page_getter = FakePageGetter(
            status, payload.sample_ec2_error_message)
        client.Query.get_page = fake_page_getter.get_page_with_exception

        def check_error(error):
            self.assertTrue(isinstance(error, TwistedWebError))
            self.assertEquals(error.status, status)

        query = client.Query(
            action='BadQuery', creds=self.creds, endpoint=self.endpoint,
            time_tuple=(2009, 8, 15, 13, 14, 15, 0, 0, 0))

        failure = query.submit()
        d = self.assertFailure(failure, TwistedWebError)
        d.addCallback(check_error)
        return d

    def test_submit_500(self):
        """
        A 5xx response status from EC2 should raise the original Twisted
        exception.
        """
        status = "500"
        self.addCleanup(setattr, client.Query, "get_page",
                        client.Query.get_page)
        fake_page_getter = FakePageGetter(
            status, payload.sample_server_internal_error_result)
        client.Query.get_page = fake_page_getter.get_page_with_exception

        def check_error(error):
            self.assertTrue(isinstance(error, EC2Error))
            self.assertEquals(error.status, status)
            self.assertEquals(error.get_error_codes(), "InternalError")
            self.assertEquals(
                error.get_error_messages(),
                "We encountered an internal error. Please try again.")

        query = client.Query(
            action='BadQuery', creds=self.creds, endpoint=self.endpoint,
            time_tuple=(2009, 8, 15, 13, 14, 15, 0, 0, 0))

        failure = query.submit()
        d = self.assertFailure(failure, TwistedWebError)
        d.addCallback(check_error)
        return d


class SignatureTestCase(TestCase):

    def setUp(self):
        self.creds = AWSCredentials("foo", "bar")
        self.endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)
        self.params = {}

    def test_encode_unreserved(self):
        all_unreserved = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz0123456789-_.~")
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.assertEqual(all_unreserved, signature.encode(all_unreserved))

    def test_encode_space(self):
        """This may be just 'url encode', but the AWS manual isn't clear."""
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.assertEqual("a%20space", signature.encode("a space"))

    def test_encode_unicode(self):
        """
        L{Signature.encode} accepts unicode strings and encode them un UTF-8.
        """
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.assertEqual(
            "f%C3%A9e",
            signature.encode(u"f\N{LATIN SMALL LETTER E WITH ACUTE}e"))

    def test_canonical_query(self):
        signature = client.Signature(self.creds, self.endpoint, self.params)
        time_tuple = (2007, 11, 12, 13, 14, 15, 0, 0, 0)
        self.params.update({"AWSAccessKeyId": "foo",
                            "fu n": "g/ames",
                            "argwithnovalue": "",
                            "SignatureVersion": "2",
                            "Timestamp": iso8601time(time_tuple),
                            "Version": "2009-11-30",
                            "Action": "DescribeInstances",
                            "InstanceId.1": "i-1234"})
        expected_params = ("AWSAccessKeyId=foo&Action=DescribeInstances"
            "&InstanceId.1=i-1234"
            "&SignatureVersion=2&"
            "Timestamp=2007-11-12T13%3A14%3A15Z&Version=2009-11-30&"
            "argwithnovalue=&fu%20n=g%2Fames")
        self.assertEqual(
            expected_params, signature.get_canonical_query_params())

    def test_signing_text(self):
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.params.update({"AWSAccessKeyId": "foo",
                            "SignatureVersion": "2",
                            "Action": "DescribeInstances"})
        signing_text = ("GET\n%s\n/\n" % self.endpoint.host +
                        "AWSAccessKeyId=foo&Action=DescribeInstances&" +
                        "SignatureVersion=2")
        self.assertEqual(signing_text, signature.signing_text())

    def test_signing_text_with_non_default_port(self):
        """
        The signing text uses the canonical host name, which includes
        the port number, if it differs from the default one.
        """
        endpoint = AWSServiceEndpoint(uri="http://example.com:99/path")
        signature = client.Signature(self.creds, endpoint, self.params)
        self.params.update({"AWSAccessKeyId": "foo",
                            "SignatureVersion": "2",
                            "Action": "DescribeInstances"})
        signing_text = ("GET\n"
                        "example.com:99\n"
                        "/path\n"
                        "AWSAccessKeyId=foo&"
                        "Action=DescribeInstances&"
                        "SignatureVersion=2")
        self.assertEqual(signing_text, signature.signing_text())

    def test_old_signing_text(self):
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.params.update({"AWSAccessKeyId": "foo",
                            "SignatureVersion": "1",
                            "Action": "DescribeInstances"})
        signing_text = (
            "ActionDescribeInstancesAWSAccessKeyIdfooSignatureVersion1")
        self.assertEqual(signing_text, signature.old_signing_text())

    def test_sorted_params(self):
        signature = client.Signature(self.creds, self.endpoint, self.params)
        self.params.update({"AWSAccessKeyId": "foo",
                            "fun": "games",
                            "SignatureVersion": "2",
                            "Version": "2009-11-30",
                            "Action": "DescribeInstances"})

        self.assertEqual([
            ("AWSAccessKeyId", "foo"),
            ("Action", "DescribeInstances"),
            ("SignatureVersion", "2"),
            ("Version", "2009-11-30"),
            ("fun", "games"),
            ], signature.sorted_params())


class QueryPageGetterTestCase(TestCase):

    def setUp(self):
        self.creds = AWSCredentials("foo", "bar")
        self.endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)
        self.twisted_client_test_setup()
        self.cleanupServerConnections = 0

    def tearDown(self):
        """Copied from twisted.web.test.test_webclient."""
        # If the test indicated it might leave some server-side connections
        # around, clean them up.
        connections = self.wrapper.protocols.keys()
        # If there are fewer server-side connections than requested,
        # that's okay.  Some might have noticed that the client closed
        # the connection and cleaned up after themselves.
        for n in range(min(len(connections), self.cleanupServerConnections)):
            proto = connections.pop()
            #msg("Closing %r" % (proto,))
            proto.transport.loseConnection()
        if connections:
            #msg("Some left-over connections; this test is probably buggy.")
            pass
        return self.port.stopListening()

    def _listen(self, site):
        return reactor.listenTCP(0, site, interface="127.0.0.1")

    def twisted_client_test_setup(self):
        name = self.mktemp()
        os.mkdir(name)
        FilePath(name).child("file").setContent("0123456789")
        resource = static.File(name)
        resource.putChild("redirect", util.Redirect("/file"))
        self.site = server.Site(resource, timeout=None)
        self.wrapper = WrappingFactory(self.site)
        self.port = self._listen(self.wrapper)
        self.portno = self.port.getHost().port

    def get_url(self, path):
        return "http://127.0.0.1:%d/%s" % (self.portno, path)

    def test_get_page(self):
        """Copied from twisted.web.test.test_webclient."""
        query = client.Query(
            action="DummyQuery", creds=self.creds, endpoint=self.endpoint,
            time_tuple=(2009, 8, 15, 13, 14, 15, 0, 0, 0))
        deferred = query.get_page(self.get_url("file"))
        deferred.addCallback(self.assertEquals, "0123456789")
        return deferred


class EC2ClientAddressTestCase(TestCase):

    def setUp(self):
        self.creds = AWSCredentials("foo", "bar")
        self.endpoint = AWSServiceEndpoint(uri=EC2_ENDPOINT_US)

    def test_describe_addresses(self):

        factory = make_query_factory(
            payload.sample_describe_addresses_result,
            "DescribeAddresses",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_addresses()
        d.addCallback(
            self.assertEquals, [("67.202.55.255", "i-28a64341"),
                                ("67.202.55.233", None)])
        return d

    def test_describe_specified_addresses(self):

        factory = make_query_factory(
            payload.sample_describe_addresses_result,
            "DescribeAddresses",
            "foo",
            "bar",
            {"PublicIp.1": "67.202.55.255"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.describe_addresses("67.202.55.255")
        d.addCallback(
            self.assertEquals, [("67.202.55.255", "i-28a64341"),
                                ("67.202.55.233", None)])
        return d

    def test_associate_address(self):


        factory = make_query_factory(
            payload.sample_associate_address_result,
            "AssociateAddress",
            "foo",
            "bar",
            {"InstanceId": "i-28a64341", "PublicIp": "67.202.55.255"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.associate_address("i-28a64341", "67.202.55.255")
        d.addCallback(self.assertTrue)
        return d

    def test_allocate_address(self):

        factory = make_query_factory(
            payload.sample_allocate_address_result,
            "AllocateAddress",
            "foo",
            "bar",
            {},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.allocate_address()
        d.addCallback(self.assertEquals, "67.202.55.255")
        return d

    def test_release_address(self):

        factory = make_query_factory(
            payload.sample_release_address_result,
            "ReleaseAddress",
            "foo",
            "bar",
            {"PublicIp": "67.202.55.255"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.release_address("67.202.55.255")
        d.addCallback(self.assertTrue)
        return d

    def test_disassociate_address(self):

        factory = make_query_factory(
            payload.sample_disassociate_address_result,
            "DisassociateAddress",
            "foo",
            "bar",
            {"PublicIp": "67.202.55.255"},
        )

        ec2 = client.EC2Client(creds=self.creds, endpoint=self.endpoint,
                               query_factory=factory)
        d = ec2.disassociate_address("67.202.55.255")
        d.addCallback(self.assertTrue)
        return d


class EC2ParserTestCase(TestCase):

    def setUp(self):
        self.parser = client.Parser()

    def test_ec2_terminate_instances(self):
        """
        Given a well formed response from EC2, parse the correct thing.
        """
        ec2_xml = """<?xml version="1.0" encoding="UTF-8"?>
<TerminateInstancesResponse xmlns="http://ec2.amazonaws.com/doc/2008-12-01/">
    <requestId>d0adc305-7f97-4652-b7c2-6993b2bb8260</requestId>
    <instancesSet>
        <item>
            <instanceId>i-cab0c1aa</instanceId>
            <currentState>
                <code>32</code>
                <name>shutting-down</name>
            </currentState>
            <previousState>
                <code>16</code>
                <name>running</name>
            </previousState>
        </item>
    </instancesSet>
</TerminateInstancesResponse>"""
        ec2_response = self.parser.terminate_instances(ec2_xml)
        self.assertEquals(
            [('i-cab0c1aa', 'running', 'shutting-down')], ec2_response)

    def test_nova_terminate_instances(self):
        """
        Ensure parser can handle the somewhat non-standard response from nova
        Note that the bug has been reported in nova here:
          https://launchpad.net/bugs/862680
        """

        nova_xml = (
            '<?xml version="1.0" ?><TerminateInstancesResponse '
            'xmlns="http://ec2.amazonaws.com/doc/2008-12-01/"><requestId>'
            '4fe6643d-2346-4add-adb7-a1f61f37c043</requestId>'
            '<return>true</return></TerminateInstancesResponse>')
        nova_response = self.parser.terminate_instances(nova_xml)
        self.assertEquals([], nova_response)

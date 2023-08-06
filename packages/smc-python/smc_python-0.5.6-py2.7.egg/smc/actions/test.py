# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2016

@author: davidlepage
'''
import logging
from smc import session
from smc.base.model import Element, prepared_request, SubElement, SMCCommand,\
    SimpleElement, ElementCreator
from smc.core.engine import Engine
from smc.elements.helpers import zone_helper, logical_intf_helper
from smc.core.sub_interfaces import InlineL2FWInterface, _add_vlan_to_inline,\
    InlineInterface
from smc.elements.servers import LogServer, ManagementServer
from smc.vpn.route import RouteVPN, TunnelEndpoint
from smc.base.collection import Search, CollectionManager, ElementCollection
from smc.policy.interface import InterfacePolicy,\
    InterfaceTemplatePolicy
from smc.policy.layer2 import Layer2TemplatePolicy, Layer2Policy
from smc.policy.layer3 import FirewallPolicy
from smc.base.decorators import classproperty, cached_property, deprecated
from smc.elements.network import Network, Host, IPList, Alias, DomainName
from smc.elements.group import Group, ICMPServiceGroup, URLCategoryGroup
from smc.api.exceptions import NodeCommandFailed, FetchElementFailed,\
    EngineCommandFailed, ElementNotFound, ActionCommandFailed,\
    UnsupportedEntryPoint, InvalidSearchFilter, DeleteElementFailed,\
    SMCConnectionError, CreatePolicyFailed, CreateElementFailed
from smc.elements.user import ApiClient, AdminUser
from smc.vpn.elements import ExternalGateway, VPNSite
from smc.core.engines import Layer3Firewall
from smc.api.common import SMCRequest
from smc.administration.tasks import Task, TaskHistory
from smc.routing.ospf import OSPFProfile, OSPFArea
from smc.elements.other import AdminDomain, prepare_blacklist, FilterExpression,\
    CategoryTag
from smc.base.util import element_resolver, merge_dicts
from smc.api.session import available_api_versions, get_entry_points,\
    get_api_version
from smc.base.mixins import UnicodeMixin
from smc.core.engine_vss import VSSContainer, VSSContext
from smc.core.waiters import ConfigurationStatusWaiter, NodeStateWaiter,\
    NodeStatusWaiter
from codecs import ignore_errors
from smc.actions.search import element_references
from smc.policy.rule import IPv4Rule
from pip._vendor.requests.api import request
from smc_monitoring.wsocket import SMCSocketProtocol
from smc.tests.constants import is_min_required_smc_version
from smc.compat import min_smc_version
from smc.core.interfaces import PhysicalVlanInterface, InterfaceModifier
from smc.vpn.policy import PolicyVPN, GatewayNode
from smc.administration.scheduled_tasks import RefreshPolicyTask, \
    DisableUnusedAdminTask, DeleteOldSnapshotsTask,\
    RenewInternalCertificatesTask, RenewInternalCATask,\
    FetchCertificateRevocationTask, SGInfoTask, RefreshMasterEnginePolicyTask,\
    UploadPolicyTask, ValidatePolicyTask, DeleteLogTask
from smc.elements.service import Protocol, ApplicationSituation, TCPService,\
    UDPService, RPCService, EthernetService, ICMPService, URLCategory, IPService
from smc.elements.certificates import ClientProtectionCA, TLSServerCredential
from smc.core.node import ApplianceInfo
from smc.policy.policy import InspectionPolicy
from smc.policy.rule_elements import MatchExpression
from smc.routing.bgp import AutonomousSystem, BGPProfile


logger = logging.getLogger(__name__)


def get_options_for_link(link):
    r = session.session.options(link)  # @UndefinedVariable
    headers = r.headers['allow']
    allowed = []
    if headers:
        for header in headers.split(','):
            if header.replace(' ', '') != 'OPTIONS':
                allowed.append(header)
    return allowed

def head_request(link):
    r = session.session.head(link)  # @UndefinedVariable
    print(vars(r))


if __name__ == '__main__':
    import sys
    import time
    from pprint import pprint
    start_time = time.time()
    #try:
    #    import http.client as http_client
    #except ImportError:
    # Python 2
    #    import httplib as http_client
    #    http_client.HTTPConnection.debuglevel = 1
    
    logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s')
    
    #from requests_toolbelt import SSLAdapter
    #import requests
    #import ssl

    #s = requests.Session()
    #s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
    
    
    session.login(url='http://172.18.1.151:8082',
                  api_key='AUhABgoiQ6tkDNvbPVA6o3A9', timeout=30,
                  verify=False, beta=True)
    
    #oR2FMUrdKHBAkQcpXZLuP8xY
    #session.login(url='http://172.18.1.26:8082', api_key='kKphtsbQKjjfHR7amodA0001', timeout=45,
    #             beta=True)
    

    #session.login(url='http://172.18.1.150:8082', api_key='EiGpKD4QxlLJ25dbBEp20001', timeout=30,
    #              verify=False)
    
    class Field(object):
        def __init__(self, primary):
            self.primary = primary

        def __get__(self, obj, owner):
            return getattr(obj, self.primary)
    
    class Doodoo(object):
        primary = Field('ipv4_network')
        
        @property
        def ipv4_network(self):
            return '1.1.1.1'
        
    d = Doodoo()
    print(d.primary)
    print(vars(d))
    

        

    engine = Engine('myfirewall')
    pprint(engine.data.get('dynamic_routing'))
    if getattr(engine, 'bgp'):
        print("True")
    
    #pprint(engine.data.get('dynamic_routing'))
    #print(engine.ospf.is_enabled)
    #print(engine.ospf.profile)
    #o = OSPFProfile.create(name='fooprofile')
    #engine.ospf.reset_profile(o)
    #engine.update()
    #print(engine.ospf.profile)
    
    
    #Host.get_or_create(filter_key={'secondary': '1.1.1.1'},
    #                   name='foohost',
    #                   address='1.1.1.1')
    
    #pprint(engine.data.get('dynamic_routing'))
    #engine.bgp.enable(AutonomousSystem('myas'), [Network('network-10.10.0.0/24')], router_id='1.1.1.1')
    #engine.update()
    #print(engine.is_bgp_enabled)
    #engine.enable_bgp(AutonomousSystem('myas'), [Network('network-10.10.0.0/24')], router_id='1.1.1.1')
    #engine.update()
    
   
    '''
    policy = PolicyVPN('mynewvpn')
    policy.open()
    
    external = 'anothergw'
    
    print(list(policy.tunnels))
    for tunnel in policy.tunnels:
        tunnel.update(enabled=True)
        policy.save()

    policy.close()
    
    policy = PolicyVPN('test')
    policy.open()
    for x in policy.central_gateway_node.all():
        print(x)
    for x in policy.satellite_gateway_node.all():
        print(x)

    print(list(policy.tunnels))
    
    tunnels = {'gateway_tunnel': []}
    for tunnel in policy.tunnels:
        tunnel_map = {}
        tunnela = tunnel.tunnel_side_a
        tunnelb = tunnel.tunnel_side_b
        
        # Gateways
        gw_tunnela = tunnela.gateway
        gw_tunnelb = tunnelb.gateway
        
        tunnel_map.update(
            tunnel_side_a=gw_tunnela.name,
            tunnel_side_a_type=gw_tunnela.typeof,
            tunnel_side_b=gw_tunnelb.name,
            tunnel_side_b_type=gw_tunnelb.typeof,
            enabled=tunnel.enabled
        )
        tunnels['gateway_tunnel'].append(tunnel_map)
    
    policy.close()
    pprint(tunnels)
    '''
        
    session.logout()
    #print(list(a.tunnels.all()))
    #for tunnel in a.tunnels:
    #    my_tunnels = GatewayTunnel(href='http://172.18.1.26:8082/6.3/elements/vpn/10/tunnels/ACgAKQ==')
    #    print(my_tunnels)
    #    pprint(my_tunnels.data)
    #    print(my_tunnels.enabled)
    #    my_tunnels.enable_disable()
    #    print(my_tunnels.enabled)
    #    my_tunnels.preshared_key(None)
    
    
    #x = PolicyVPN('testvpn')
    #x.open()
    #pprint(x.data)
    #print(x.tunnels)
    #pprint(x.data)
    #tunnels = prepared_request(href='http://172.18.1.150:8082/6.3/elements/vpn/17/tunnels').read()
    #pprint(tunnels.json)
    #specific_tunnel = prepared_request(href='http://172.18.1.150:8082/6.3/elements/vpn/161/tunnels/AAIAFA==').read()
    #pprint(specific_tunnel.json)
    #print(get_options_for_link('http://172.18.1.150:8082/6.3/elements/vpn/161/tunnels/gzuDaA=='))
    #x.close()
    #session.logout()
    
    sys.exit(1)
    #tls = TLSServerCredential.create(name='tlstest', common_name="CN=myserver.lepages.local")
    #tls = TLSServerCredential('LePagesCA')
    #pprint(tls.data)
    
    
    print(vars(session))
    #c = copy.copy(session)
    #print("Copy of...")
    #print(vars(c))
    print("Switch domain to nsx.....")
    session.switch_domain('nsx')
    print(vars(session))
    print(session.domain)
    
    #print("copied instance after switching domains: %s" % vars(c))
    result = SMCRequest(params={'filter_context': 'single_fw',
                                'exact_match': False,
                                'domain': 'nsx'}).read()
    print(result)
    for x in session.entry_points.all():
        if 'tls' in x:
            print(x)

    engine = Engine('bar')
    pprint(engine.data)
    
    #ClientProtectionCA.create('foo')
    print(engine.server_credential)
        
    #    print(x.certificate_export())

        
        
        
    #engine = Engine('sg_vm')
    #from datetime import datetime
    #dt = datetime(1970, 9, 7, 23, 00, 00)
    #a = int(time.mktime(dt.timetuple()))
    #print(a)
    
    #DT: 1970-09-07 19:00:00 -> 21600000 21614400
    sys.exit(1)
    """@type engine: Engine"""
    # Create the engine with a tunnel interface
    
    for x in Search.objects.entry_point('archive_log_task'):
        pprint(x.data)
    

    for x in RefreshPolicyTask.objects.all():
        pprint(x.data)
        for schedule in x.task_schedule:
            pprint(schedule.data)
    
    task = RefreshPolicyTask('testtasj')
    #for schedule in task.task_schedule:
    #    schedule.suspend()
        
    result = task.add_schedule(
        name='monthly2', 
        activation_date='2017-10-04T00:00:00Z',
        day_period='monthly')
    
    print(result)
    
    from smc.administration.system import System
    system = System()
    system.empty_trash_bin()
    import sys
    sys.exit(1)
    
    # Daily
    {'day_period': 'daily',
     'minute_period': 'hourly', # every hour
     'minute_period': 'each_half', # each half hour
     'minute_period': 'each_quarter'} # every 15 minutes
    
    # Weekly - I cant figure out the day mask
    {'day_period': 'weekly',
     'minute_period': 'one_time',
     'day_mask': 124 # Mon - Friday
     }
    
    # Monthly
    {'day_period': 'monthly',
     'minute_period': 'one_time'}
    
    # Yearly
    {'day_period': 'yearly',
     'minute_period': 'one_time'}
    
    a = {u'activated': True,
         u'activation_date': '2017-10-04T09:33:09.890000-05:00',
         u'comment': u'test',
         u'day_mask': 0,
         u'day_period': u'one_time',
         u'final_action': u'ALERT_FAILURE',
         u'minute_period': u'one_time',
         u'name': u'test7'}
    
    #b = prepared_request(href='https://172.18.1.151:8082/6.3/elements/refresh_policy_task/42/task_schedule',
    #                     json=a).create()
    #print(b)
    
    '''
    export_log_task
    archive_log_task
    remote_upgrade_task
    '''
    #client_gateway
    #validate_policy_task
    #refresh_policy_task
    
    #print(get_options_for_link('https://172.18.1.151:8082/6.3/elements/fw_alert'))
    
         
    import pexpect  # @UnresolvedImport
    import tempfile
   
    def ssh(host, cmd, user, password, timeout=15, bg_run=False):                                                                                                 
        """SSH'es to a host using the supplied credentials and executes a command.                                                                                                 
        Throws an exception if the command doesn't return 0.                                                                                                                       
        bgrun: run command in the background"""                                                                                                                                    
    
        fname = tempfile.mktemp()                                                                                                                                                  
        fout = open(fname, 'w')                                                                                                                                                    
    
        options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'                                                                         
        if bg_run:                                                                                                                                                         
            options += ' -f'                                                                                                                                                       
        ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
        print("SSH CMD: %s" % ssh_cmd)                                                                                                               
        child = pexpect.spawn(ssh_cmd, timeout=timeout)
        
        #child.expect(['[sudo] password for nsxadmin: '])
        #child.sendline(password)
        child.expect(['Password: '])                                                                                                                                                                                                                                                                                               
        child.sendline(password)
        if 'sudo' in ssh_cmd:
            child.expect(['sudo'])
            child.sendline(password)                                                                                                                                          
        #child.logfile = fout
        child.logfile = sys.stdout.buffer                                                                                                                                                      
        child.expect(pexpect.EOF)                                                                                                                                                  
        child.close()                                                                                                                                                              
        fout.close()                                                                                                                                                               
    
        fin = open(fname, 'r')                                                                                                                                                     
        stdout = fin.read()
        fin.close()                                                                                                                                                                
    
        if 0 != child.exitstatus:                                                                                                                                                  
            raise Exception(stdout)                                                                                                                                                
    
        return stdout
    
    
    cmd = 'sudo -u root -S msvc -r dpa'
    #print(ssh('172.18.1.111', cmd=cmd, user='nsxadmin', password='password'))
    

    
    from smc.administration.system import System
    for x in Search.objects.entry_point('tls_server_credentials').all():
        if x.name == 'lepages':
            pprint(x.data)

   
            
    
    
    class ProbingProfile(Element):
        typeof = 'probing_profile'
        def __init__(self, name, **meta):
            super(ProbingProfile, self).__init__(name, **meta)
    
    class ThirdPartyMonitoring(object):
        def __init__(self, log_server=None, probing_profile=None,
                     netflow=False, snmp_trap=False):

            if not log_server:
                log_server = LogServer.objects.first()

            self.monitoring_log_server_ref = element_resolver(log_server)

            if not probing_profile:
                probing_profile = ProbingProfile.objects.filter('Ping').first()

            self.probing_profile_ref = element_resolver(probing_profile)

            self.netflow = netflow
            self.snmp_trap = snmp_trap

        def __call__(self):
            return vars(self)



    #host.third_party_monitoring = ThirdPartyMonitoring()
    #print(vars(host))
    #host.update()

    #t = ThirdPartyMonitoring()
    #host.third_party_monitoring = t

    #print("Finished polling, result is: %s" % poller.result())
    vss_def = {"isc_ovf_appliance_model": 'virtual',
               "isc_ovf_appliance_version": '',
               "isc_ip_address": '1.1.1.1',
               "isc_vss_id": 'foo',
               "isc_virtual_connector_name": 'smc-python'}

    vss_node_def = {
            'management_ip': '4.4.4.6',
            'management_netmask': '24',
            'isc_hypervisor': 'default',
            'management_gateway': '2.2.2.1',
            'contact_ip': None}
    '''
    rbvpn_tunnel_side
    rbvpn_tunnel_monitoring_group
    rbvpn_tunnel
    '''
  
    
    
            
    '''
    by_action = {
        "format": {
            "type": "texts",
            "field_ids": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": LogField.ACTION},
                "right":[
                    {"type": "constant", "value":Actions.DISCARD}]}
        },
        "fetch":{"quantity":100}
    }
    
    by_protocol = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": "Protocol"
                },
                "right":[{
                    "type": "number",
                    "value":6}]
            }
        },
        "fetch":{"quantity":100}
    }
    
    by_service = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "field",
                    "name": "Service"},
                "right":[
                    {"type": "service",
                     "value": "TCP/80"}]
            }
        },
        "fetch":{"quantity":100}
    }
    
    by_sender = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "in",
                "left": {
                    "type": "id",
                    "name": LogField.SRC},
                "right":[
                    {"type": "ip",
                     "value": "1.1.1.1"}]
            }
        },
        "fetch":{"quantity":100}
    }

    ip_and_service = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "start_ms": 0,
            "end_ms": 0,
            "filter": {
                "type": "and",
                "values": [
                    {"type": "in",
                     "left": {
                         "type": "field",
                         "name": "Service"},
                     "right":[
                         {"type": "service",
                          "value": "TCP/443"}]
                    },
                    {"type": "in",
                     "left": {
                         "type": "field",
                         "id": LogField.SRC},
                     "right":[
                         {"type": "ip",
                          "value": "192.168.4.84"}]
                    },       
                    ]
            }
        },
        "fetch":{"quantity":100}
    }
    
    
    cs_like_filter = {
        "format": {
            "type": "texts",
            "field_format": "name"
        },
        "query": {
            "type":"stored",
            "filter": {
                "type": "ci_like",
                "left": {
                    "type": "field",
                    "id": LogField.INFOMSG},
                "right": {
                    "type": "string", 
                    "value":"Connection was reset by client" }
                }
        },
        "fetch":{"quantity":100}
    }
    
    bl2 = {
        'fetch': {},
        'format': {
            "type": "texts",
            "field_format": "name",
            "resolving": {
                "senders": True}
        },
        'query': {
            'definition': 'BLACKLIST', 
            'target': 'sg_vm'}
    }
    
    blacklist = {
        'fetch': {},
        'format': {
            'type': 'combined',
            'formats': {
                "fields": {
                    "type": "detailed",
                    "field_format": "name"
                },
                "bldata": {
                    "type": "texts",
                    "field_format": "name",
                    "resolving": {"time_show_zone": True,
                                  "timezone": "CST"
                    }
                },
                "blentry": {
                    "type": "texts",
                    "field_format": "pretty",
                    "field_ids": [LogField.BLACKLISTENTRYID]
                }
            }
        },
        'query': {
            'definition': 'BLACKLIST', 
            'target': 'sg_vm'}
    }
    '''
    '''
    ids = resolve_field_ids(list(range(1000)))
    for x in ids:
        pprint(x)
    for x in reversed(ids):
        print('{}={} #: {}'.format(
            x.get('name').upper(),
            x.get('id'),
            x.get('comment')))

    sys.exit(1)
    '''
    
    
    
    #import timeit
    #print(timeit.repeat("{link['rel']:link['href'] for link in links}",
    #                    setup="from __main__ import links", number=1000000,
    #                    repeat=3))
    
    #import timeit
    # print(timeit.timeit("ElementFactory('http://172.18.1.150:8082/6.1/elements/host/978')",
    # setup="from __main__ import ElementFactory", number=1000000))

    #print(timeit.timeit("find_link_by_name('self', [])", setup="from smc.base.util import find_link_by_name"))


    print(time.time() - start_time)
    session.logout()

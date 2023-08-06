# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2016

@author: davidlepage
'''
import logging
from smc import session
from smc.base.model import Element, prepared_request, SubElement, SMCCommand, SimpleElement, ElementCreator,\
    lookup_class, LoadElement, SubDict
from smc.core.engine import Engine, InternalEndpoint, InternalGateway
from smc.elements.helpers import zone_helper, logical_intf_helper,\
    location_helper
from smc.core.sub_interfaces import InlineL2FWInterface, _add_vlan_to_inline,\
    InlineInterface
from smc.elements.servers import LogServer, ManagementServer, HttpProxy,\
    DNSServer
from smc.vpn.route import RouteVPN, TunnelEndpoint
from smc.base.collection import Search, CollectionManager, ElementCollection,\
    create_collection, sub_collection
from smc.policy.interface import InterfacePolicy,\
    InterfaceTemplatePolicy
from smc.policy.layer2 import Layer2TemplatePolicy, Layer2Policy
from smc.policy.layer3 import FirewallPolicy, FirewallSubPolicy
from smc.base.decorators import classproperty, cached_property, deprecated,\
    cacheable_resource
from smc.elements.network import Network, Host, IPList, Alias, DomainName,\
    AddressRange, Country
from smc.elements.group import Group, ICMPServiceGroup, URLCategoryGroup,\
    TCPServiceGroup
from smc.api.exceptions import NodeCommandFailed, FetchElementFailed,\
    EngineCommandFailed, ElementNotFound, ActionCommandFailed,\
    UnsupportedEntryPoint, InvalidSearchFilter, DeleteElementFailed,\
    SMCConnectionError, CreatePolicyFailed, CreateElementFailed,\
    ResourceNotFound, UnsupportedEngineFeature
from smc.elements.user import ApiClient, AdminUser
from smc.vpn.elements import ExternalGateway, VPNSite
from smc.core.engines import Layer3Firewall
from smc.api.common import SMCRequest, fetch_no_filter
from smc.administration.tasks import Task, TaskHistory
from smc.routing.ospf import OSPFProfile, OSPFArea
from smc.elements.other import prepare_blacklist, FilterExpression,\
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
from smc.policy.rule_elements import MatchExpression, RuleElement, LogOptions
from smc.routing.bgp import AutonomousSystem, BGPProfile, ExternalBGPPeer,\
    BGPPeering, BGPConnectionProfile
from smc.administration.access_rights import AccessControlList
from smc.elements.profiles import DNSRelayProfile
from smc.core.route import PolicyRouteEntry


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
    
    #logging.getLogger()
    #logging.basicConfig(
    #    level=logging.DEBUG, format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
    
    #from requests_toolbelt import SSLAdapter
    #import requests
    #import ssl

    print(session.session_id)
    #s = requests.Session()
    #s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
    #session.set_file_logger(log_level=10, path='/Users/davidlepage/Downloads/smc-test.log')
    
    session.set_stream_logger(log_level=logging.DEBUG)
    session.set_stream_logger(log_level=logging.DEBUG, logger_name='urllib3')
    
    session.login(url='http://172.18.1.151:8082',
                  api_key='zJ35gRLnmYlvctl2Y7xevV5u', timeout=30,
                  verify=False, beta=True)
    
    #session.login(url='http://172.18.1.26:8082', api_key='kKphtsbQKjjfHR7amodA0001', timeout=45,
    #             beta=True)

    #session.login(url='http://172.18.1.150:8082', api_key='EiGpKD4QxlLJ25dbBEp20001', timeout=30,
    #              verify=False)
   
    
    def format_dict(element):
        for key in ('link', 'key'):
            element.data.pop(key, None)
        return element.data
        
    def to_dict(vpn, expand=None):
        """
        Flatten the policy VPN
        
        :param policy_vpn PolicyVPN
        :return dict
        """
        expand = expand if expand else []
        
        gateway_cache = {} # Cache gateways to reduce repetitive queries
        vpn.open()
        if 'vpn_profile' in expand:
            vpn.data['vpn_profile'] = format_dict(vpn.vpn_profile)

        central = []
        for cgw in vpn.central_gateway_node:
            gateway_cache[cgw.href] = cgw
            gateway_cache[cgw.gateway.href] = cgw.gateway
            
            vpn_site = []
            for site in cgw.enabled_sites:
                if cgw.gateway.name in expand:
                    site.data['site_element'] = [format_dict(s) for s in site.vpn_site.site_element]
                    vpn_site.append(format_dict(site))
                else:
                    vpn_site.append(format_dict(site.vpn_site))
    
            central.append({'name': cgw.gateway.name, 'type': cgw.gateway.typeof, 'vpn_site': vpn_site})
        
        satellite = []
        for sgw in vpn.satellite_gateway_node:
            gateway_cache[sgw.href] = sgw
            gateway_cache[sgw.gateway.href] = sgw.gateway
            
            vpn_site = []
            for site in sgw.enabled_sites:
                if sgw.gateway.name in expand:
                    site.data['site_element'] = [format_dict(s) for s in site.vpn_site.site_element]
                    vpn_site.append(format_dict(site))
                else:
                    vpn_site.append(format_dict(site.vpn_site))
    
            satellite.append({'name': sgw.gateway.name, 'type': sgw.gateway.typeof, 'vpn_site': vpn_site})
        
        gateway_tunnel = []
        
        for tunnel in vpn.tunnels:
            tunnel_map = {}
            
            tunnela = gateway_cache.get(tunnel.data.get('gateway_node_1')).gateway
            tunnelb = gateway_cache.get(tunnel.data.get('gateway_node_2')).gateway
           
            tunnel_map.update(
                tunnel_side_a=tunnela.name,
                tunnel_side_a_type=tunnela.typeof,
                tunnel_side_b=tunnelb.name,
                tunnel_side_b_type=tunnelb.typeof,
                enabled=tunnel.enabled)
        
            gateway_tunnel.append(tunnel_map)
    
        vpn.data.update(central_gateway=central, satellite_gateway=satellite,
                        gateway_tunnel=gateway_tunnel)       
        vpn.close()
        return format_dict(vpn)
    
    
    gateway_tunnel = [] 
    #vpn = PolicyVPN('mypolicyvpn')
    #vpn.open()
    import functools

    def ReloadElement(href, only_etag=False): 
        """ 
        Return an instance of a element as a SimpleElement dict 
        used as a cache. 
         
        :rtype SimpleElement 
        """ 
        request = SMCRequest(href=href) 
        request.exception = FetchElementFailed 
        result = request.read() 
        if only_etag: 
            return result.etag 
        return ElementContainer( 
            etag=result.etag, **result.json) 
    
    
    class FooElement(object):
        def __init__(self, engine):
            self.engine = engine
            
        @cached_property
        def data(self):
            return ReloadElement(self.engine.href)
        
        @property 
        def etag(self): 
            return self.data.etag(self.engine.href)
    
    from collections import MutableMapping
    class ExSubDict(MutableMapping):
        """
        Generic dict structure that can be used to objectify
        complex json. This dict will return None if an attribute
        is not found.
        """
        def __init__(self, data=None, **kwargs):
            self.data = data if data else {}
            self.update(self.data, **kwargs)
    
        def __setitem__(self, key, value):
            self.data[key] = value
    
        def __getitem__(self, key):
            return self.data[key]
    
        def __delitem__(self, key):
            del self.data[key]
    
        def __iter__(self):
            #return ((key, value) for key, value in self.data.items())
            return iter(self.data)
    
        def __len__(self):
            return len(self.data)
        
        def __repr__(self):
            return str(dict(self.items()))


    class ElementContainer(ExSubDict):
        def __init__(self, **kwargs):
            self._etag = kwargs.pop('etag', None)
            super(ElementContainer, self).__init__(data=kwargs)
        
        def etag(self, href):
            """
            ETag can be None if a subset of element json is using
            this container, such as the case with Routing.
            """
            if self and self._etag is None:
                self._etag = LoadElement(href, only_etag=True)
            return self._etag
        
        @property
        def links(self):
            return {link['rel']:link['href'] for link in self['link']}
        
        def get_link(self, rel):
            """
            Return link for specified resource
            """
            for link in self['link']:
                if link.get('rel') == rel:
                    return link['href']
            raise ResourceNotFound('Resource requested: %r is not available '
                                   'on this element.' % rel)
    
        
    from smc.elements.other import Location
    engine = Engine(name='dingo2')
    
    rule = {u'action': {u'action': u'jump',
                        u'connection_tracking_options': {u'mss_enforced': False,
                                                          u'mss_enforced_max': 0,
                                                          u'mss_enforced_min': 0,
                                                          u'timeout': -1},
                        u'scan_detection': u'undefined',
                        u'sub_policy': u'http://172.18.1.151:8082/6.4/elements/sub_ipv4_fw_policy/18'},
             u'authentication_options': {u'methods': [],
                                         u'require_auth': False,
                                         u'timeout': 3600,
                                         u'users': []},
             u'destinations': {u'any': True},
             u'is_disabled': False,
             u'key': 36,
             u'link': [{u'href': u'http://172.18.1.151:8082/6.4/elements/fw_policy/16/fw_ipv4_access_rule/112',
                        u'rel': u'self',
                        u'type': u'fw_ipv4_access_rule'},
                       {u'href': u'http://172.18.1.151:8082/6.4/elements/fw_policy/16/fw_ipv4_access_rule/112/history',
                        u'rel': u'history'},
                       {u'href': u'http://172.18.1.151:8082/6.4/elements/fw_policy/16/fw_ipv4_access_rule?after=112.1',
                        u'rel': u'add_after'},
                       {u'href': u'http://172.18.1.151:8082/6.4/elements/fw_policy/16/fw_ipv4_access_rule?before=112.1',
                        u'rel': u'add_before'}],
             u'name': u'last rule',
             u'options': {u'log_accounting_info_mode': False,
                          u'log_closing_mode': True,
                          u'log_level': u'undefined',
                          u'log_payload_additionnal': False,
                          u'log_payload_excerpt': False,
                          u'log_payload_record': False,
                          u'log_severity': -1},
             u'parent_policy': u'http://172.18.1.151:8082/6.4/elements/fw_policy/16',
             u'rank': 3.0,
             u'read_only': False,
             u'services': {u'any': True},
             u'sources': {u'src': [u'http://172.18.1.151:8082/6.4/elements/network/680']},
             u'system': False,
             u'tag': u'112.1'}
    
    
    class SetterProperty(object):
        def __init__(self, func, doc=None):
            self.func = func
            self.__doc__ = doc if doc is not None else func.__doc__
        def __set__(self, obj, value):
            return self.func(obj, value)

                     
    class ConnectTracking(SubDict):
        def __init__(self, data=None):
            if data is None:
                mss = dict(
                    mss_enforced=False,
                    mss_enforced_max=0,
                    mss_enforced_min=0,
                    timeout=-1)
                data = dict(connection_tracking_options=mss)
            ct = data.get('connection_tracking_options', {})
            super(ConnectTracking, self).__init__(data=ct)
        
        def mss_enforced_max(self, value):
            self.update(mss_enforced_max=value)
        
    
    class RuleAction(SubDict):
        def __init__(self, data=None):
            if data is None:
                action = dict(action='allow')
                action.update(connection_tracking_options=ConnectTracking())
                action.update(scan_detection='undefined') 
            else: 
                action = data.get('action', {})
            super(RuleAction, self).__init__(data=action)
    
        @property
        def action(self):
            return self.get('action')
        
        @action.setter
        def action(self, value):
            self.update(action=value)
        
        @property
        def connection_tracking(self):
            return ConnectTracking(self)

    
    class Source(RuleElement, SubDict):
        
        def __init__(self, data=None):
            if data is None:
                sources = dict(none=True)
            else:
                sources = data.get('sources')
            self.data = {'none': True} if data is None else data
    
        def __call__(self):
            return {'sources': self.data}
        
                
    ruletest = RuleAction()
    
    
    log_options = LogOptions()
    pprint(log_options.data)
    policy = FirewallPolicy('fwpolicy')
    
    for rule in policy.fw_ipv4_access_rules.all():
        print(rule.options)
        rule.options.log_accounting_info_mode = False
        rule.options.log_level = 'stored'
        rule.options.application_logging = 'enforced'
        rule.options.user_logging = 'default'
        pprint(rule.data)
        pprint(vars(rule))
        rule.save()
    
    
    #pprint(vars(ruletest))
    #print(vars(ConnectTracking()))
    
    
    #ruletest.action = 'FOOBAR'
    #ruletest.connection_tracking.mss_enforced_max(100)
    #pprint(rule)
    #engine.rename('dingo2')
    #pprint(engine._meta)
    #print(vars(engine.vpn.internal_gateway))
    
    sys.exit(1)
    session.logout()
    foo = FooElement(engine)
    #pprint(foo.data)
    print('policy: %s' % foo.data.get('policy_route'))
    pprint(vars(foo))
    
    #print(foo.data['policy_route'])
    import json
    pprint(json.loads(foo.data))
    foo.data.update(dingo='foo')
    print(foo.etag)
    #pprint(foo.data.data)
    
    '''
    print('vpn clinet: %s' % engine.vpn.vpn_client)
    print(vars(engine.vpn))
    print(vars(engine))
    engine.vpn.internal_gateway.update(antivirus=False)
    print('engine vpn after update: %s' % vars(engine.vpn))
    print('get data and validate refresh')
    pprint(vars(engine.vpn.internal_gateway))
    engine.vpn.internal_gateway.data
    pprint(vars(engine.vpn.internal_gateway))
    print("RENAMING!!!")
    engine.rename('dingo')
    '''
    
    #pprint(vars(engine))
    #pprint(engine.data)
    #engine.update()
    
    
    #from smc.elements.other import Location
    #a = location_helper('test')
    #print(a)
    
    
  
    #engine = Engine('dingo')
    #print(engine.internal_gateway.data)
    #print(list(engine.internal_gateway.internal_endpoint))
    #print(list(engine.internal_gateway.internal_endpoint))
    
    #x = prepared_request(href='http://172.18.1.151:8082/6.4/elements/single_fw/948/internal_gateway/114/loopback_endpoint').read()
    #pprint(x.json)
    
    #y = prepared_request(href='http://172.18.1.151:8082/6.4/elements/single_fw/948/internal_gateway/114/loopback_endpoint/214').read()
    #pprint(y.json)
            
    
    
    
    #print(engine.default_nat)
    #print(list(engine.dns))
    
    #engine.vpn.endpoints
    #engine.vpn.sites
    #engine.vpn.gateway
    #engine.vpn.profile
    
    #alias_list = list(Alias.objects.all()) 
    #for alias in self.read_cmd(resource='alias_resolving'): 
    #    yield Alias.from_engine(alias, alias_list) 
            
    #print(engine.permissions)
    #engine.update()
    #engine.update()
    #pprint(engine.data)
    
    
    
    
    
    
    
    
    #pprint(engine.data)
    #engine.antivirus.enable()
    #pprint(engine.data.get('antivirus'))
    #engine.update()
    #testengine = TestEngine(engine.data)
    #testengine.antivirus.proxy_port(80)
    #testengine.antivirus.proxy_user('foo')
    #pprint(testengine.data)
    
    #pprint(vars(testengine))
    #av = AntiVirus(engine)
    #av.http_proxy('1.1.1.1')
    #av.proxy_port(80)
    
    
    session.logout()
    sys.exit(1)
    #session.logout()
    
    #print(session.url)
    #print(Host('kali').href)
    #engine = Engine('tester')
    #engine.bgp.enable( 
    #    autonomous_system=AutonomousSystem('lepages-bgp'), 
    #    announced_networks=[Network('192net')], 
    #    router_id='10.10.10.10') 
    #pprint(vars(session.session))
    
    import inspect
    import smc.elements.network as network
    import smc.elements.group as group
    
    
    def network_elements():   
        types = dict(
            host=dict(type=network.Host),
            network=dict(type=network.Network),
            address_range=dict(type=network.AddressRange),
            router=dict(type=network.Router),
            ip_list=dict(type=network.IPList),
            group=dict(type=group.Group),
            interface_zone=dict(type=network.Zone),
            domain_name=dict(type=network.DomainName))
        
        for t in types.keys():
            clazz = types.get(t)['type']
            types[t]['attr'] = inspect.getargspec(clazz.create).args[1:]
        
        return types
    
    
    def ro_network_elements():
        types = dict(
            alias=dict(type=network.Alias),
            country=dict(type=network.Country),
            expression=dict(type=network.Expression),
            engine=dict(type=Engine))
    
        for t in types.keys():
            clazz = types.get(t)['type']
            types[t]['attr'] = inspect.getargspec(clazz.__init__).args[1:]
        
        return types
    
    ELEMENT_TYPES = network_elements()
    ELEMENT_TYPES.update(ro_network_elements())

    
    #g = Group('group_referencing_existing_elements')
    #print([x.href for x in g.obtain_members()])
    #pprint(element_dict_from_obj(g, ELEMENT_TYPES, expand=['group']))
    
    # All other elements use name/comments to search
    SEARCH_HINTS = dict(
        network='ipv4_network',
        address_range='ip_range',
        host='address',
        router='address'
    )
    
    def is_element_valid(element, type_dict, check_required=True):
        """
        Are all provided arguments valid for this element type.
        Name and comment are valid for all.
        
        :param dict element: dict of element
        :param bool check_required: check required validates that at least
            one of the required arguments from the elements `create` constructor
            is provided. This is set to True when called from the network_element
            or service_element modules. This can be False when called from the
            firewall_rule module which allows an element to be fetched only.
        :return: None
        """
        for key, values in element.items():
            if not key in type_dict:
                return 'Unsupported element type: {} provided'.format(key)
    
            valid_values = type_dict.get(key).get('attr', [])

            # Verify that all attributes are supported for this element type
            provided_values = values.keys() if isinstance(values, dict) else []
            if provided_values:
                # Name is always required
                if 'name' not in provided_values:
                    return 'Entry: {}, missing required name field'.format(key)
            
                for value in provided_values:
                    if value not in valid_values:
                        return 'Entry type: {} with name {} has an invalid field: {}. '\
                            'Valid values: {} '.format(key, values['name'], value, valid_values)
                
                if check_required:
                    required_arg = [arg for arg in valid_values if arg not in ('name', 'comment')]
                    if required_arg: #Something other than name and comment fields
                        if not any(arg for arg in required_arg if arg in provided_values):
                            return 'Missing a required argument for {} entry: {}, Valid values: {}'\
                                .format(key, values['name'], valid_values)
                
                if 'group' in element and values.get('members', []):
                    for element in values['members']:
                        if not isinstance(element, dict):
                            return 'Group {} has a member: {} with an invalid format. Members must be '\
                                'of type dict.'.format(values['name'], element)
                        invalid = is_element_valid(element, type_dict, check_required=False)
                        if invalid:
                            return invalid
            else:
                return 'Entry type: {} has no values. Valid values: {} '\
                    .format(key, valid_values)
        
    
    elements = [
                {
                    "address": "1.1.1.1", 
                    "host": "foobar4562"
                }, 
                {
                    "comment": "foo",
                    "ipv4_network": "1.1.0.0/24",
                    "network": "foonetwork1.2.3"
                },
                {
                    "network": "any"
                },
                {
                    "address_range": "myrange3", 
                    "ip_range": "3.3.3.1-3.3.3.5"
                }, 
                {
                        "address": "172.18.1.254", 
                        "ipv6_address": "2003:dead:beef:4dad:23:46:bb:101", 
                        "router": "myrouter2", 
                        "secondary": [
                            "172.18.1.253"
                        ]
                },
                {
                    "alias": "$ EXTERNAL_NET",
                }, 
                {
                    "domain_name": "dogpile.com",
                    "comment": "bar"
                }, 
                {
                    "interface_zone": "external_zone123"
                },
                {
                    "interface_zone": "new123zone",
                    "comment": "dingo"
                },
                {
                    "ip_list": "mylist",
                    "iplist": ['45.45.45.45']
                }, 
                {
                    "group": "doodoo",
                    "members": [
                        {'host': {'name':'blah'}
                        }]
                }, 
                {
                    "country": [
                        "Armenia", 
                        "United States", 
                        "China"
                    ]
                }, 
                {
                    "engine": [
                        "fw2", 
                        "myfirewall"
                    ]
                }
            ]            
    
    
    NETWORK_ELEMENTS = ELEMENT_TYPES.keys()
    
    
    def extract_element(element, type_dict):
        """
        Extract a dict like yml entry. Split this into a dict in
        the correct format if the element type exists.
        """
        key = [key for key in set(element) if key in type_dict]
        if key and len(key) == 1:
            typeof = key.pop()
            element['name'] = element.pop(typeof)
            return typeof, {typeof: element}

    def is_field_any(field):
        """
        Is the source/destination or service field using an ANY
        value.
        
        :rtype: bool
        """
        if 'network' in field and field['network']['name'].upper() == 'ANY':
            return True
        return False
    
    def update_or_create(element, type_dict, hint=None, check_mode=False):
        """
        Create or get the element specified. The strategy is to look at the
        element type and check the default arguments. Some elements require
        only name and comment to create. Others require specific arguments.
        If only name and comment is provided and the constructor requires
        additional args, try to fetch the element, otherwise call
        get_or_create. If the constructor only requires name and comment,
        these will also call get_or_create.
        
        :param dict element: element dict, key is typeof element and values
        :param dict type_dict: type dict mappings to get class mapping
        :param str hint: element attribute to use when finding the element
        :raises CreateElementFailed: may fail due to duplicate name or other
        :raises ElementNotFound: if fetch and element doesn't exist
        :return: The result as type Element
        """
        for typeof, values in element.items():
            type_dict = type_dict.get(typeof)
            
            filter_key = {hint: values.get(hint)} if hint in values else None
            raise_exc = False if check_mode else True
            
            if check_mode:
                result = type_dict['type'].get(values.get('name'), raise_exc)
                if result is None:
                    return dict(
                        name=values.get('name'),
                        type=typeof,
                        msg='Specified element does not exist')
            else:
                attr_names = type_dict.get('attr', []) # Constructor args
                provided_args = set(values)
                
                # Guard against calling update_or_create for elements that
                # may not be found and do not have valid `create` constructor
                # arguments
                if set(attr_names) == set(['name', 'comment']) or \
                    any(arg for arg in provided_args if arg not in ('name',)):
                    
                    result = type_dict['type'].update_or_create(filter_key=filter_key, **values)
                else:
                    print("Only perform GET!")
                    result = type_dict['type'].get(values.get('name'))

                return result
            
            
    def get_or_create_element(element, type_dict, hint=None, check_mode=False):
        """
        Create or get the element specified. The strategy is to look at the
        element type and check the default arguments. Some elements require
        only name and comment to create. Others require specific arguments.
        If only name and comment is provided and the constructor requires
        additional args, try to fetch the element, otherwise call
        get_or_create. If the constructor only requires name and comment,
        these will also call get_or_create.
        
        :param dict element: element dict, key is typeof element and values
        :param dict type_dict: type dict mappings to get class mapping
        :param str hint: element attribute to use when finding the element
        :raises CreateElementFailed: may fail due to duplicate name or other
        :raises ElementNotFound: if fetch and element doesn't exist
        :return: The result as type Element
        """
        for typeof, values in element.items():
            type_dict = type_dict.get(typeof)
        
        # An optional filter key specifies a valid attribute of
        # the element that is used to refine the search so the
        # match is done on that exact attribute. This is generally
        # useful for networks and address ranges due to how the SMC
        # interprets / or - when searching attributes. This changes
        # the query to use the attribute for the top level search to
        # get matches, then gets the elements attributes for the exact
        # match. Without filter_key, only the name value is searched.
        filter_key = {hint: values.get(hint)} if hint in values else None
        
        if check_mode:
            result = type_dict['type'].get(values.get('name'), raise_exc=False)
            if result is None:
                return dict(
                    name=values.get('name'),
                    type=typeof,
                    msg='Specified element does not exist')
        else:
            result = type_dict['type'].get_or_create(filter_key=filter_key, **values)
            return result
        
    def field_resolver(elements, type_dict, check_mode=False):
        """
        Field resolver, specific to retrieving network or service level
        elements in different formats.
        YAML format #1:
            - tcp_service: service_name
                
        Format #2, as list (elements are expected to exist):
            - tco_service:
                - service1
                - service2
        
        Format #1 can also be used to get_or_create if the element types
        attributes are provided:
        
            - host: myhost
              address: 1.1.1.1
        
        :param list elements: list of elements as parsed from YAML file
        :param dict type_dict: type dictionary for elements that should be
            supported for this run.
        """
        for element in elements:
            if isinstance(element, dict):
                filter_key = element.pop('filter_key', None)
                
                key = [key for key in set(element) if key in type_dict]
                if key and len(key) == 1:
                    typeof = key.pop()
                    element['name'] = element.pop(typeof)
                    
                    # Is format #2
                    if isinstance(element['name'], list):
                        print("Is a list: %s" % element)
                        clazz = type_dict.get(typeof)['type']
                        for e in element['name']:
                            match = clazz.objects.filter(e, exact_match=True).first()
                            if match:
                                print("Match: %s" % match)
                            else:
                                print("NO MATCH ON LIST ITEM!!")
                    elif element['name'].upper() == 'ANY':
                        print("Element is Any!")
                
                    else:
                        element_dict = {typeof: element}
                        invalid = is_element_valid(element_dict, type_dict, check_required=False)
                        if invalid:
                            print("INVALID ELEMENT: %s" % invalid)
                        
                        if not filter_key and SEARCH_HINTS:
                            filter_key = SEARCH_HINTS.get(typeof)
                        
                        if 'group' in typeof:
                            members = []
                            for member in element_dict['group']['members']:
                                members.append(update_or_create(member, type_dict, check_mode=check_mode))
                            
                            element_dict['group']['members'] = members
                        
                        value = update_or_create(element_dict, type_dict, check_mode=check_mode)
                        if check_mode:
                            if value is not None:
                                print("----> CHECK MODE FAILURE: %s " % value)
                        else:
                            print("**Found value: %s" % value)
                          
                else:
                    print("***ELEMENT TYPE NOT FOUND: %s" % element)
            else:
                print("Invalid format, expecting dict!")
            
    
    field_resolver(elements, ELEMENT_TYPES, check_mode=False)        
    
    
    #import timeit
    #print(timeit.repeat("test()",
    #                    setup="from __main__ import test", number=1000000,
    #                    repeat=3))
    session.logout()
    sys.exit(1)
    
    import requests  # @UnresolvedImport
   
    
    '''
    a = requests.post(url='http://172.18.1.151:8082/6.4/lms_login',
                     params={'login': 'testadmin',
                             'pwd': '1970keegan'},
                     headers={'content-type': 'application/json'})
    
    pprint(vars(a))
    '''
    
    
    session.login('http://172.18.1.151:8082', login='testadmin', pwd='1970keegan',
                  beta=True)
    pprint(vars(session))
    print(vars(session.session))
    
    a = prepared_request(href='http://172.18.1.151:8082/6.4/system/mgt_integration_configuration').read()
    print(vars(a))


    sys.exit(0)
    


    
    #engine = Engine('myfirewall')
    
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
    
    #a = Network.get_or_create(name='network-10.10.0.0/24',
    #                          ipv4_network='10.10.0.0/24')
    
    def test(filter_key=None, **kwargs):
        print("Start query!")
        if filter_key:
            value = {filter_key: kwargs.get(filter_key)}
            print("Filter key: %s, value: %s" % (filter_key,value))
            elements = Network.objects.filter(**value)
            print(vars(elements))
            if elements.exists(): 
                return elements.first()
        else:
            element = Network.get(kwargs.get('name'))
            print(element)
            #element = cls.create(**kwargs)
    
    #a = [{"href":"http://172.18.1.151:8082/6.3/elements/network/738","name":"10.10.0.0/16","type":"network"},{"href":"http://172.18.1.151:8082/6.3/elements/network/723","name":"network-10.10.0.0/24","type":"network"},{"href":"http://172.18.1.151:8082/6.3/elements/network/736","name":"crap","type":"network"}]        
    #filter_key = {'ipv4_network': '10.10.0.0/24'}
    #for item in a:
    #    element = Element.from_meta(**item)
    #    if all(element.data.get(k) == v for k, v in filter_key.items()):
    #        print("ALL!")
    
    #print(test(filter_key={'ipv4_network': '10.10.0.0/24'},
    print(test(filter_key='ipv4_network',
        name='kali', ipv4_network='10.10.0.0/24'))
    
    #c = Network.objects.filter(ipv4_network='10.10.0.0/24')
    #print(c.first())
    #Network.get_or_create(name='foo', ipv4_network='2.2.2.0/24',
    #                      values='ipv4_network')
    
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

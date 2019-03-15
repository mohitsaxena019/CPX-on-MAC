#!/usr/bin/env python
import os
from threading import Thread
import copy
from functools import wraps
import logging
import time
import base64
import hashlib
import requests
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver_binding\
    import csvserver_binding

from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsfeature import nsfeature
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nstimeout import nstimeout
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip import nsip
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nstcpprofile import nstcpprofile
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey import sslcertkey
from nssrc.com.citrix.netscaler.nitro.resource.config.system.systemfile import systemfile
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver import sslvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding import sslvserver_sslcertkey_binding
from nssrc.com.citrix.netscaler.nitro.resource.stat.system.system_stats import system_stats
from nssrc.com.citrix.netscaler.nitro.resource.config.responder.responderaction import responderaction
from nssrc.com.citrix.netscaler.nitro.resource.config.responder.responderpolicy import responderpolicy
from nssrc.com.citrix.netscaler.nitro.resource.config.rewrite.rewritepolicy import rewritepolicy  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.rewrite.rewriteaction import rewriteaction  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policydataset import policydataset  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policydataset_value_binding import policydataset_value_binding  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset import policypatset  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policypatset_pattern_binding import policypatset_pattern_binding  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policystringmap import policystringmap  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.policy.policystringmap_pattern_binding import policystringmap_pattern_binding  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_rewritepolicy_binding import lbvserver_rewritepolicy_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_responderpolicy_binding import lbvserver_responderpolicy_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.rewrite.rewritepolicy_lbvserver_binding import rewritepolicy_lbvserver_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.responder.responderpolicy_lbvserver_binding import responderpolicy_lbvserver_binding
from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception \
    import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver \
    import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbmonitor_servicegroup_binding \
    import lbmonitor_servicegroup_binding

from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbmonitor \
    import lbmonitor
from nssrc.com.citrix.netscaler.nitro.service.nitro_service\
    import nitro_service
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.servicegroup\
    import servicegroup
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_servicegroup_binding\
    import lbvserver_servicegroup_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.servicegroup_servicegroupmember_binding\
    import servicegroup_servicegroupmember_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.server_servicegroup_binding import server_servicegroup_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver \
    import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver_lbvserver_binding \
    import csvserver_lbvserver_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csaction \
    import csaction
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.cspolicy \
    import cspolicy
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver_cspolicy_binding \
    import csvserver_cspolicy_binding

from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver_responderpolicy_binding \
    import csvserver_responderpolicy_binding

from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsconfig \
    import nsconfig
from nssrc.com.citrix.netscaler.nitro.util.filtervalue import filtervalue
from nssrc.com.citrix.netscaler.nitro.resource.config.ha.hanode \
    import hanode
from nssrc.com.citrix.netscaler.nitro.resource.config.network.route \
    import route
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslaction \
    import sslaction
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslpolicy \
    import sslpolicy
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslpolicy_binding \
    import sslvserver_sslpolicy_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslservicegroup_sslcertkey_binding \
    import sslservicegroup_sslcertkey_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.audit.auditmessageaction import auditmessageaction  # noqa
from nssrc.com.citrix.netscaler.nitro.resource.config.audit.auditsyslogparams \
    import auditsyslogparams

LOG_FILENAME = 'citrix_nitro.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)



def ns_session_login_handler():
    """ This method creates Nitro session and returns its handle """
    try:
        ip_port = '127.0.0.1' + ':' + '9080'
        logging.info("Processing request to establish Nitro session for NS IP {}".format(ip_port))
        ns_session = nitro_service(ip_port, 'http')
        ns_session.certvalidation = False
        ns_session.hostnameverification = False
        ns_session.set_credential('nsroot', 'nsroot')
        ns_session.timeout = 600
        ns_session.login()
        call_nitro_commands(ns_session)
        logging.info('Configuration completed')
        logging.info("Finished processing request to establish Nitro session for NS IP {}".format(ip_port))
        return ns_session
    except nitro_exception as nitroe:
        logging.error("Nitro Exception::login_logout::errorcode=" +
                     str(nitroe.errorcode) + ",message=" + nitroe.message)
        return None
    except requests.exceptions.ConnectionError as e:
        logging.error("Received requests.exceptions.ConnectionError Exception: {}".format(e))
        logging.error("Exception: %s" % e.message)
        return None
    except Exception as e:
        logging.error("Exception: %s" % e.message)
        return None

def call_nitro_commands(ns_session):
    try:
        ns_session.clear_config(force=True, level='full')
        logging.debug('Clear config executed') 
        needed_features = [
            nsfeature.Feature.CS,
            nsfeature.Feature.LB,
            nsfeature.Feature.SSL,
            nsfeature.Feature.RESPONDER,
            nsfeature.Feature.REWRITE]
        ns_session.enable_features(needed_features)
        
        logging.debug('Adding CS vserver')
        csvserver_instance= csvserver()
        csvserver_instance.name = 'drinks_sample'
        csvserver_instance.ipv46= '127.0.0.1'
        csvserver_instance.servicetype = 'http'
        csvserver_instance.port = '443'
        csvserver_instance.add(ns_session, csvserver_instance)

        logging.debug('Adding LB vserver')
        lbvserver_instance = lbvserver()
        lbvserver_instance.name = 'lbvs_hotdrink_http_example'
        lbvserver_instance.ipv46 = '0.0.0.0'
        lbvserver_instance.port = 0
        lbvserver_instance.servicetype = 'http'
        lbvserver_instance.add(ns_session, lbvserver_instance)


        logging.debug('Adding servicegroup')
        servicegroup_instance = servicegroup()
        servicegroup_instance.servicegroupname = 'sg_hotdrink_http_example'
        servicegroup_instance.servicetype = 'http'
        servicegroup_instance.add(ns_session, servicegroup_instance)

        logging.debug('Adding servieegroup binding')
        servicegroup_servicegroupmember_binding_instance = servicegroup_servicegroupmember_binding()
        servicegroup_servicegroupmember_binding_instance.servicegroupname = 'sg_hotdrink_http_example'
        servicegroup_servicegroupmember_binding_instance.ip = '172.100.100.3' 
        servicegroup_servicegroupmember_binding_instance.port = 80
        servicegroup_servicegroupmember_binding_instance.add(ns_session, servicegroup_servicegroupmember_binding_instance)


        logging.debug('Adding servicegroup lb vserver binding')
        lbvserver_servicegroup_binding_instance = lbvserver_servicegroup_binding()
        lbvserver_servicegroup_binding_instance.name = 'lbvs_hotdrink_http_example'
        lbvserver_servicegroup_binding_instance.servicegroupname = 'sg_hotdrink_http_example'
        lbvserver_servicegroup_binding_instance.add(ns_session, lbvserver_servicegroup_binding_instance)

        logging.debug('SUCCESS: Configuration completed')
    except Exception as e:
        logging.error('FAILURE: Error during configuration: {}'.format(e.message));

ns_session_login_handler()

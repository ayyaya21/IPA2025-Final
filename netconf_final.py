from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.61",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)

def net_create():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070221</name>
                <description>Configured by NETCONF</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>172.2.21.1</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070221 is created successfully using Netconf"
    except:
        return "Cannot create: Interface loopback 66070221"


def net_delete():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback66070221</name>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070221 is deleted successfully using Netconf"
    except:
        return "Cannot delete: Interface loopback 66070221"


def net_enable():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070221</name>
            </interface>
        </interfaces-state>
    </filter>
    """
    try:
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        interface_info = netconf_reply_dict.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {}).get("interface")

        if interface_info:
            admin_status = interface_info.get("admin-status")
            if admin_status == "up":
                return "Cannot enable: Interface loopback 66070221 is already enabled (checked by Netconf)"

        netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070221</name>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
        """

        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070221 is enabled successfully using Netconf"

    except Exception as e:
        return f"Cannot enable: Interface loopback 66070221 (checked by Netconf)"



def net_disable():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070221</name>
            </interface>
        </interfaces-state>
    </filter>
    """
    try:
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        interface_info = netconf_reply_dict.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {}).get("interface")

        if interface_info:
            admin_status = interface_info.get("admin-status")
            if admin_status == "down":
                return "Cannot shutdown: Interface loopback 66070221 is already shutdown (checked by Netconf)"

        netconf_config = """
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback66070221</name>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
        """

        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070221 is shutdowned successfully using Netconf"

    except Exception as e:
        return f"Cannot shutdown: Interface loopback 66070221 (checked by Netconf)"



def net_status():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070221</name>
            </interface>
        </interfaces-state>
    </filter>
    """

    try:
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        interfaces_state = netconf_reply_dict.get("rpc-reply", {}).get("data", {}).get("interfaces-state", {})
        interface_info = interfaces_state.get("interface")

        if interface_info:
            admin_status = interface_info.get("admin-status")
            oper_status = interface_info.get("oper-status")
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070221 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070221 is disabled (checked by Netconf)"
    except:
        return "No Interface loopback 66070221 (checked by Netconf)"

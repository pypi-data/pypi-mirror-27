# PyWinWiFi - Python Windows WiFi library.
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
# Author		: Nishant Sharma <nishant@binarysecuritysolutions.com>
# Organizations	: Pentester Academy <www.pentesteracademy.com> and Hacker Arsenal <www.hackerarsenal.com>


from WindowsWifi import *
from time import sleep
import datetime
import sqlite3
import xml.etree.ElementTree as ET
# Install plotly     pip install plotly
from plotly import session, tools, utils
from plotly.graph_objs import Bar,Scatter
import uuid
import json


def listInterfaces():
    """
        Prints all wireless interfaces available on system.
       
        **Arguments:** None
    """
    # Add "wlan netsh show drivers" output
    ifaces = getWirelessInterfaces()
    counter = 1
    totalInterfaces = len(ifaces)
    print "Total interfaces available: %s"  %totalInterfaces
    print ""
    for iface in ifaces:
        print "Interface: %s" %counter
        print iface
        print ""
        counter += 1
        
def wlanNetshShowInterfaces():
    """
        Prints output similar to "netsh wlan show interfaces" command.
       
        **Arguments:** None
    """
    ifaces = getWirelessInterfaces()
    for iface in ifaces:
        print iface
        print ""
        
        value = queryInterface(iface,"interface_state")
        state=value[1]
        
        if state == "wlan_interface_state_connected":
            temp = queryInterfaceStateStr(iface,"current_connection")
            print temp
            print ""

def connect(wireless_interface, profileName, connectionMode, bssid, bssidType):
    """
        Prints SSIDs present in scan results after each 10 seconds.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
        - profileName: Name of the profile or SSID (String)
        - connectionMode: Mode of connection (String)
                - wlan_connection_mode_temporary_profile
                - wlan_connection_mode_discovery_secure
                - wlan_connection_mode_discovery_unsecure
                - wlan_connection_mode_auto
                - wlan_connection_mode_invalid
        - bssid: BSSID of the target network (String)
        - bssidType: Type of BSSID(String)
                - dot11_BSS_type_infrastructure (Infrastructure mode)
                - dot11_BSS_type_independent (Ad-hoc mode) 
    """
    specs = { "connectionMode": connectionMode, "profile": profileName, "ssid": profileName, "bssidList": [bssid], "bssType": bssidType, "flags": 0x00000001}
    result = connectToNetwork(wireless_interface, specs)
    return result
        
def snifferSsid(wireless_interface):
    """
        Prints SSIDs present in scan results after each 10 seconds.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type) 
    """
    while 1:
        print " \n Scanned Network SSIDs at %s" %datetime.datetime.now()
        print "-------------------------------------------"
        networks = getWirelessAvailableNetworkList(wireless_interface)
        for network in networks:
            #print network
            lineList = str(network).split('\n')
            Ssid = lineList[1].split(':')
            ssidName = Ssid[1]
            if ssidName == "":
                ssidName = "Hidden Network"
            print ssidName
        sleep(10)
        
def snifferBssid(wireless_interface):
    """
        Prints SSIDs present in scan results after each 10 seconds.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type) 
    """
    while 1:
        print "\nScanned Network SSIDs and BSSIDs at %s" %datetime.datetime.now()
        print "-------------------------------------------"
        networks = getWirelessNetworkBssList(wireless_interface)
        for network in networks:
            #print network
            lineList = str(network).split('\n')
            Bssid = lineList[0].split(' ')
            bssidName = Bssid[1]
            Ssid = lineList[1].split(':')
            ssidName = Ssid[1]
            if ssidName == "":
                ssidName = "Hidden Network"
            print "SSID:%s   BSSID: %s " %(ssidName,bssidName) 
        sleep(10)

def widoorPolling(iface, ssidToCheck, hostedNetwork, securityPassPhrase, maxPeer, pollPeriod):
    """
        Start WiDoor functionality. An infinite loop will checks scan results after every "pollPeriod".
        If "ssidToCheck" is present: Hosted network named "hostedNetwork" starts.
        If "ssidToCheck" is NOT present and hosted network is up: Stops hosted network.
    
        **Arguments:**
        
        - ssidToCheck: signal SSID to look for (String)
        - hostedNetwork: Name of hosted backdoor network (String)
        - securityPassPhrase: Shared Pass Phrase for the hosted network (String)
        - maxPeer: Maximum allowed devices for hosted network (int)
        - pollPeriod: Polling period in seconds (int)
        """
        
    # Default parameter values
    if ssidToCheck == "": 
        ssidToCheck = "Binary_Tech"
    if hostedNetwork == "":
        hostedNetwork = "Test_network_lol"
    if securityPassPhrase == "":
        securityPassPhrase = "abc_123321"
    if maxPeer == "":
        maxPeer = 5
    if pollPeriod == "": 
        pollPeriod = 10 #seconds
        
    while 1:
        #Adding wait
        sleep(pollPeriod)
        # Check if signal SSID is present
        if networkPresentCheck(iface, ssidToCheck) == True:
            print "Found Signal Network: %s" %(ssidToCheck)
            #Start Hosted network
            hostedNetworkStart(hostedNetwork, securityPassPhrase, maxPeer)
              
            # Waiting for signal network to go down
            while 1:
                #Adding wait
                sleep(pollPeriod)
                if networkPresentCheck(iface, ssidToCheck) == False:
                    print "Lost Signal Network: %s" %(ssidToCheck)
                    # Stop Hosted Network
                    hostedNetworkStop()
                    # Going to outer loop
                    break
                
def widoorCallback():
    """
        Starts widoor functionality based on callback from WiFi subsystem.
       
        **Arguments:** None
    """
    hostedNetworkStarted = "started"
    if os.path.isfile(hostedNetworkStarted):
        os.remove(hostedNetworkStarted)
        
    # Calling registering function
    registerWlanNotifications(notifyCallbackWidoor, "WLAN_NOTIFICATION_SOURCE_ACM")
    

def logNotifications(wlanNotificationSource = "WLAN_NOTIFICATION_SOURCE_ALL"):
    """
        Prints event notifications received from WiFi subsystem's source "wlanNotificationSource".
        If no argument is passed, notifications from all sources will be shown.
        **Arguments:**
        
        - wlanNotificationSource: WLAN event notification source  (String)
            - "WLAN_NOTIFICATION_SOURCE_ONEX": 802.1x notifications
            - "WLAN_NOTIFICATION_SOURCE_ACM": Auto COnfiguration Module notifications
            - "WLAN_NOTIFICATION_SOURCE_MSM": Media Specific Module notifications
            - "WLAN_NOTIFICATION_SOURCE_SECURITY": Security notifications
            - "WLAN_NOTIFICATION_SOURCE_IHV": Independent Hardware Vendors notifications
            - "WLAN_NOTIFICATION_SOURCE_HNWK": Host Network notifications
            - "WLAN_NOTIFICATION_SOURCE_ALL": All notifications
    """
    registerWlanNotifications(notifyCallbackLogNotifications, wlanNotificationSource)
    
def unregisterNotifications():
    """
        Unregisters from WiFi event notifications.
       
        **Arguments:** None
    """
    registerWlanNotifications(notifyCallbackLogNotifications, "WLAN_NOTIFICATION_SOURCE_NONE")

def printInterfaceCapability(wireless_interface):
    """
        Prints interface capability information.
       
        **Arguments:**
        
        - wireless_interface: Wireless interface (object of WirelessInterface type)
    """
    capabilityStruct = wlanGetInterfaceCapability(wireless_interface)
    print "Capability Information for Interface: %s" %(wireless_interface.guid)
    print "-------------------------------------------------------"
    print "Interface type: %s " %WLAN_INTERFACE_TYPE_DICT[capabilityStruct.contents.interfaceType]
    print "Supports 802.11d: %r " %bool(capabilityStruct.contents.bDot11DSupported)
    print "Maximum size of the SSID list supported: %d " %capabilityStruct.contents.dwMaxDesiredSsidListSize
    print "Maximum size of the BSSID list supported: %d " %capabilityStruct.contents.dwMaxDesiredBssidListSize
    print "Number of supported PHY types: %d " %capabilityStruct.contents.dwNumberOfSupportedPhys
    print "Supported interfaces:"
    for num in range(0,capabilityStruct.contents.dwNumberOfSupportedPhys):
        print " %d: %s " %(num + 1, DOT11_PHY_TYPE_DICT[capabilityStruct.contents.dot11PhyTypes[num]])

# TODO: Check problem with AD HOC profile creation
# WIndows 8 onwards support for AdHoc network is reduced and changed
# https://globalcache.zendesk.com/entries/82172789-FAQ-Windows-8-1-and-Windows-10-AdHoc-network-support-solution

def createPSKProfile(guid, ssidName, Type, sharedKey, overWrite, wpaVersion):
    """
        Create a new WPA/WPA2-PSK wireless profile.
       
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssidName: Profile/SSID name of the profile to be created (String) 
        - Type: Type of BSSID i.e.infrastructure or adhoc (String)
        - sharedKey: Secret passphrase (String)
        - overWrite: Overwrite if profile already exist i.e. True or False(bool)
        - wpaVersion: WPA version i.e. 1 or 2 (int)
    """
    if wpaVersion == 1:
        authentication = "WPAPSK"
        encryption = "TKIP"
    elif wpaVersion == 2:
        authentication = "WPA2PSK"
        encryption = "AES"
    else:
        print "wrong choice of WPA version"
        SystemExit
    
    if Type == "infrastructure":
        connectionType = "ESS"
    elif Type == "adhoc":
        connectionType = "IBSS"
    else:
        print "wrong choice of types"
        SystemExit
    #print connectionType
    
    data = """<?xml version=\"1.0\" encoding=\"US-ASCII\"?>
         <WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">
         <name>%s</name><SSIDConfig><SSID><name>%s</name></SSID></SSIDConfig>
         <connectionType>%s</connectionType><connectionMode>auto</connectionMode>
         <autoSwitch>false</autoSwitch><MSM><security><authEncryption>
         <authentication>%s</authentication><encryption>%s</encryption>
         <useOneX>false</useOneX></authEncryption><sharedKey>
         <keyType>passPhrase</keyType><protected>false</protected>
         <keyMaterial>%s</keyMaterial></sharedKey></security></MSM></WLANProfile>""" %(ssidName, ssidName, connectionType, authentication, encryption, sharedKey) 
    
    #print data 
    wlanSetProfile(guid, data, overWrite) 

def createEAPProfile(guid, ssidName, username, password, overWrite, wpaVersion):
    """
        Create a new WPA/WPA2-EAP wireless profile.
       
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssidName: Profile/SSID name of the profile to be created (String) 
        - username: EAP user name (String)
        - password: EAP user password (String)
        - overWrite: Overwrite if profile already exist i.e. True or False(bool)
        - wpaVersion: WPA version i.e. 1 or 2 (int)
    """
    if wpaVersion == 1:
        authentication = "WPA"
        encryption = "TKIP"
    elif wpaVersion == 2:
        authentication = "WPA2"
        encryption = "AES"
    else:
        print "wrong choice of WPA version"
        SystemExit
    
    data = """<?xml version="1.0" encoding="US-ASCII"?>
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>%s</name>
    <SSIDConfig><SSID><name>%s</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM><security><authEncryption>
                <authentication>%s</authentication>
                <encryption>%s</encryption>
                <useOneX>true</useOneX>
            </authEncryption>
            <OneX xmlns="http://www.microsoft.com/networking/OneX/v1">
                <EAPConfig><EapHostConfig xmlns="http://www.microsoft.com/provisioning/EapHostConfig" 
                                   xmlns:eapCommon="http://www.microsoft.com/provisioning/EapCommon" 
                                   xmlns:baseEap="http://www.microsoft.com/provisioning/BaseEapMethodConfig">
                        <EapMethod>
                            <eapCommon:Type>25</eapCommon:Type> 
                            <eapCommon:AuthorId>0</eapCommon:AuthorId> 
                       </EapMethod>
                       <Config xmlns:baseEap="http://www.microsoft.com/provisioning/BaseEapConnectionPropertiesV1" 
                               xmlns:msPeap="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV1" 
                               xmlns:msChapV2="http://www.microsoft.com/provisioning/MsChapV2ConnectionPropertiesV1">
                           <baseEap:Eap>
                               <baseEap:Type>25</baseEap:Type> 
                               <msPeap:EapType>
                                   <msPeap:ServerValidation>
                                       <msPeap:DisableUserPromptForServerValidation>false</msPeap:DisableUserPromptForServerValidation> 
                                       <msPeap:TrustedRootCA /> 
                                   </msPeap:ServerValidation>
                                   <msPeap:FastReconnect>true</msPeap:FastReconnect> 
                                   <msPeap:InnerEapOptional>0</msPeap:InnerEapOptional> 
                                   <baseEap:Eap>
                                       <baseEap:Type>26</baseEap:Type> 
                                       <msChapV2:EapType>
                                           <msChapV2:UseWinLogonCredentials>false</msChapV2:UseWinLogonCredentials> 
                                       </msChapV2:EapType>
                                   </baseEap:Eap>
                                   <msPeap:EnableQuarantineChecks>false</msPeap:EnableQuarantineChecks> 
                                   <msPeap:RequireCryptoBinding>false</msPeap:RequireCryptoBinding> 
                                   <msPeap:PeapExtensions /> 
                               </msPeap:EapType>
                           </baseEap:Eap>
                       </Config>
                   </EapHostConfig>
                </EAPConfig>
            </OneX>
        </security>
    </MSM> </WLANProfile>""" %(ssidName, ssidName, authentication, encryption) 
    wlanSetProfile(guid, data, overWrite)

def editEAPCredentials(guid, ssidName, username, password):
    """
        Edit user credentials of an WPA/WPA2-EAP wireless profile.
       
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssidName: Profile/SSID name of the profile to be edited (String) 
        - username: EAP user name (String)
        - password: EAP user password (String)
    """
        
    data = """<?xml version="1.0" ?> 
    <EapHostUserCredentials xmlns="http://www.microsoft.com/provisioning/EapHostUserCredentials"
    xmlns:eapCommon="http://www.microsoft.com/provisioning/EapCommon" 
    xmlns:baseEap="http://www.microsoft.com/provisioning/BaseEapMethodUserCredentials">
    <EapMethod>
      <eapCommon:Type>25</eapCommon:Type> 
      <eapCommon:AuthorId>0</eapCommon:AuthorId> 
    </EapMethod>
    <Credentials xmlns:eapUser="http://www.microsoft.com/provisioning/EapUserPropertiesV1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:baseEap="http://www.microsoft.com/provisioning/BaseEapUserPropertiesV1"
      xmlns:MsPeap="http://www.microsoft.com/provisioning/MsPeapUserPropertiesV1"
      xmlns:MsChapV2="http://www.microsoft.com/provisioning/MsChapV2UserPropertiesV1">
      <baseEap:Eap>
        <baseEap:Type>25</baseEap:Type> 
        <MsPeap:EapType>
          <MsPeap:RoutingIdentity>test</MsPeap:RoutingIdentity> 
          <baseEap:Eap>
            <baseEap:Type>26</baseEap:Type> 
            <MsChapV2:EapType>
              <MsChapV2:Username>%s</MsChapV2:Username> 
              <MsChapV2:Password>%s</MsChapV2:Password> 
              <MsChapV2:LogonDomain>ias-domain</MsChapV2:LogonDomain> 
            </MsChapV2:EapType>
          </baseEap:Eap>
        </MsPeap:EapType>
      </baseEap:Eap>
    </Credentials>
    </EapHostUserCredentials>""" %(username, password) 
    wlanSetProfileEapXmlUserData(guid, ssidName, data)

def createWEPProfile(guid, ssidName, Type, sharedKey, overWrite):
    """
        Create a new WEP wireless profile.
       
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssidName: Profile/SSID name of the profile to be created (String) 
        - Type: Type of BSSID i.e.infrastructure/adhoc (String)
        - sharedKey: Secret passphrase (String)
        - overWrite: Overwrite if profile already exist i.e. True or False(bool)
    """
    if Type == "infrastructure":
        connectionType = "ESS"
    elif Type == "adhoc":
        connectionType = "IBSS"
    else:
        print "wrong choice of types"
        SystemExit
    print connectionType

    data = """<?xml version=\"1.0\"?>
          <WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">
          <name>%s</name><SSIDConfig><SSID><name>%s</name></SSID></SSIDConfig>
          <connectionType>%s</connectionType><MSM><security><authEncryption>
          <authentication>open</authentication><encryption>WEP</encryption>
          <useOneX>false</useOneX></authEncryption><sharedKey>
          <keyType>networkKey</keyType><protected>false</protected>
          <keyMaterial>%s</keyMaterial></sharedKey><keyIndex>0</keyIndex>
          </security></MSM></WLANProfile>""" %(ssidName, ssidName, connectionType, sharedKey) 
    wlanSetProfile(guid, data, overWrite) 
    
    
def listProfiles():
    """
        List all WiFi profiles present on the system.
       
        **Arguments:** None
    """
    ifaces = getWirelessInterfaces()
    for iface in ifaces:
        profiles = getWirelessProfiles(iface)
        print ""
        for profile in profiles:
            print profile
            print "-" * 20
        print ""

namespace = 'http://schemas.microsoft.com/win/2004/08/events/event'

def query(tree, nodename):
    return tree.findall('{{{ex}}}{nodename}'.format(ex=namespace, nodename=nodename))

def createResultDB(eventType):
    """
        Creates sqlite DB "queryResults" and table "RESULTS". Then, populates the table with
        event logs of type "eventType".
        
        **Arguments:**
        
        - eventType: Type of events (String)
                - 8000    : started a connection to a wireless network
                - 8001    : successfully connected to a wireless network
                - 8003    : successfully disconnected from a wireless network
                - 8012    : NLO discovery (WLAN Wake)
                - 11000    : Wireless network association started
                - 11001    : Wireless network association succeeded
                - 11004    : Wireless security stopped
                - 11005    : Wireless security succeeded
                - 11010    : Wireless security started
                - all
            You can add other events as per your needs. To know the eventType code and its description
            Open eventvwr.msc and goto Applications > Microsoft > Windows > WLAN-Autoconfig > Operational.
                 
    """
    conn = sqlite3.connect('queryResult.db')
    print "Opened database successfully";
    
    if eventType == "8000" or eventType == "all":
        conn.executescript('drop table if exists Event8000;')
        conn.execute('''CREATE TABLE Event8000
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           InterfaceGuid    TEXT,
           InterfaceDescription    TEXT,
           ConnectionMode    TEXT,
           ProfileName        TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           ConnectionId        TEXT);''')
    
    if eventType == "8001" or eventType == "all":
        conn.executescript('drop table if exists Event8001;')
        conn.execute('''CREATE TABLE Event8001
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           InterfaceGuid    TEXT,
           InterfaceDescription    TEXT,
           ConnectionMode    TEXT,
           ProfileName        TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           PHYType            TEXT,
           AuthenticationAlgorithm    TEXT,
           CipherAlgorithm    TEXT,
           OnexEnabled    TEXT,
           ConnectionId        TEXT,
           NonBroadcast        TEXT);''')
    
    if eventType == "8003" or eventType == "all":
        conn.executescript('drop table if exists Event8003;')
        conn.execute('''CREATE TABLE Event8003
                    (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           InterfaceGuid    TEXT,
           InterfaceDescription    TEXT,
           ConnectionMode    TEXT,
           ProfileName        TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           Reason            TEXT,
           ConnectionId        TEXT);''')
    
    if eventType == "8012" or eventType == "all":
        conn.executescript('drop table if exists Event8012;')
        conn.execute('''CREATE TABLE Event8012
                    (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           InterfaceGuid    TEXT,
           InterfaceDescription    TEXT);''')
    
    if eventType == "11000" or eventType == "all":
        conn.executescript('drop table if exists Event11000;')
        conn.execute('''CREATE TABLE Event11000
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           Adapter        TEXT,
           DeviceGuid    TEXT,
           LocalMac    TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           Auth            TEXT,
           Cipher            TEXT,
           OnexEnabled            TEXT,
           IhvConnectivitySetting    TEXT,
           ConnectionId        TEXT);''')
    
    if eventType == "11001" or eventType == "all":
        conn.executescript('drop table if exists Event11001;')
        conn.execute('''CREATE TABLE Event11001
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           Adapter        TEXT,
           DeviceGuid    TEXT,
           LocalMac    TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           ConnectionId        TEXT,
           MgmtFrameProtection        TEXT);''')
    
    if eventType == "11004" or eventType == "all":
        conn.executescript('drop table if exists Event11004;')
        conn.execute('''CREATE TABLE Event11004
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           Adapter        TEXT,
           DeviceGuid    TEXT,
           LocalMac    TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           SecurityHint            TEXT,
           SecurityHintCode            TEXT,
           ConnectionId        TEXT);''')
    
    if eventType == "11005" or eventType == "all":
        conn.executescript('drop table if exists Event11005;')
        conn.execute('''CREATE TABLE Event11005
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           Adapter        TEXT,
           DeviceGuid    TEXT,
           LocalMac    TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           ConnectionId        TEXT);''')
        
    if eventType == "11010" or eventType == "all":
        conn.executescript('drop table if exists Event11010;')
        conn.execute('''CREATE TABLE Event11010
           (EventID        INT,
           Version        INT,
           Level        INT,
           Task        INT,
           OpCode        INT,
           Keywords        TEXT,
           TimeCreated    TEXT,
           EventRecordID    INT,
           ProcessID        INT,
           ThreadID            INT,
           Channel        TEXT,
           Computer        TEXT,
           UserID            TEXT,
           Adapter        TEXT,
           DeviceGuid    TEXT,
           LocalMac    TEXT,
           SSID                TEXT,
           BSSType            TEXT,
           Auth            TEXT,
           AuthVal            TEXT,
           Cipher            TEXT,
           CipherVal            TEXT,
           FIPSMode            TEXT,
           OnexEnabled            TEXT,
           ConnectionId        TEXT);''')
        
    print "Table created successfully";
    count = 0
    listEvents = getEventLogs(eventType)
    for eventsItem in listEvents:
        #print eventsItem
        attribDict = {}
        count = count + 1 
        root = ET.fromstring(eventsItem)
        for subelement in root:
            for subsub in subelement:
                tag = subsub.tag.replace("{"+namespace+"}","")
                text = subsub.text
                
                if tag == "Data":
                    tag = subsub.items()[0][1]
                if text == None:
                    if tag == "Provider" or tag == "Correlation":
                        continue
                    if tag == "TimeCreated":
                        text = subsub.items()[0][1]
                    if tag == "Execution":
                        tag = subsub.items()[0][0]
                        text = subsub.items()[0][1]
                        # Adding extra member here directly
                        attribDict[subsub.items()[1][0]] = subsub.items()[1][1]
                    if tag == "Security":
                        tag = subsub.items()[0][0]
                        text = subsub.items()[0][1]
                    if tag == "IhvConnectivitySetting":
                        text = "NA"
                # Cleaning data
                if tag == "Keywords" or tag == "ConnectionId":
                    text = text.replace("0x","")
                if tag == "TimeCreated":
                    text = text.replace("T"," ")
                
                if tag =="EventID" and text == "8000":
                    if tag == "InterfaceGuid":
                        text = text.replace("{","").replace("}","")
                        
                    
                #print "Tag: %s     Value: %s" %(tag, text)
                if tag =="EventID" and text == "11005":
                    if tag == "DeviceGuid":
                        text = text.replace("{","").replace("}","")
                    
                attribDict[tag] = text
                
        if attribDict.get("EventID") == "8000":
            sqlQuery = "INSERT INTO Event8000 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, InterfaceGuid, InterfaceDescription, ConnectionMode,\
                    ProfileName, SSID, BSSType, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("InterfaceGuid")+"','"+attribDict.get("InterfaceDescription")+"','"\
                    +attribDict.get("ConnectionMode")+"','"+attribDict.get("ProfileName")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("ConnectionId")+"')"
        
        elif attribDict.get("EventID") == "8001":
            sqlQuery = "INSERT INTO Event8001 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, InterfaceGuid, InterfaceDescription, ConnectionMode,\
                    ProfileName, SSID, BSSType, PHYType, AuthenticationAlgorithm, CipherAlgorithm, OnexEnabled, \
                    ConnectionId, NonBroadcast) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("InterfaceGuid")+"','"+attribDict.get("InterfaceDescription")+"','"\
                    +attribDict.get("ConnectionMode")+"','"+attribDict.get("ProfileName")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("PHYType")+"','"+attribDict.get("AuthenticationAlgorithm")+"','"+attribDict.get("CipherAlgorithm")+"','" \
                    +attribDict.get("OnexEnabled")+"','"+attribDict.get("ConnectionId")+"','"+attribDict.get("NonBroadcast")+"')"
        
        elif attribDict.get("EventID") == "8003":
            sqlQuery = "INSERT INTO Event8003 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, InterfaceGuid, InterfaceDescription, ConnectionMode,\
                    ProfileName, SSID, BSSType, Reason, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("InterfaceGuid")+"','"+attribDict.get("InterfaceDescription")+"','"\
                    +attribDict.get("ConnectionMode")+"','"+attribDict.get("ProfileName")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("Reason")+"','"+attribDict.get("ConnectionId")+"')"
                    
        elif attribDict.get("EventID") == "8012":
            sqlQuery = "INSERT INTO Event8012 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, InterfaceGuid, InterfaceDescription) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("InterfaceGuid")+"','"+attribDict.get("InterfaceDescription")+"')"
        
        elif attribDict.get("EventID") == "11000":
            sqlQuery = "INSERT INTO Event11000 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, Adapter, DeviceGuid, LocalMac,\
                    SSID, BSSType, Auth, Cipher, OnexEnabled, IhvConnectivitySetting, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("Adapter")+"','"+attribDict.get("DeviceGuid")+"','"\
                    +attribDict.get("LocalMac")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("Auth")+"','"+attribDict.get("Cipher")+"','"+attribDict.get("OnexEnabled")+"','"\
                    +attribDict.get("IhvConnectivitySetting")+"','"+attribDict.get("ConnectionId")+"')"
        
        elif attribDict.get("EventID") == "11001":
            sqlQuery = "INSERT INTO Event11001 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, Adapter, DeviceGuid, LocalMac,\
                    SSID, BSSType, ConnectionId, MgmtFrameProtection) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("Adapter")+"','"+attribDict.get("DeviceGuid")+"','"\
                    +attribDict.get("LocalMac")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("ConnectionId")+"','"+attribDict.get("MgmtFrameProtection")+"')"
                    
        elif attribDict.get("EventID") == "11004":
            sqlQuery = "INSERT INTO Event11004 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, Adapter, DeviceGuid, LocalMac,\
                    SSID, BSSType, SecurityHint, SecurityHintCode, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("Adapter")+"','"+attribDict.get("DeviceGuid")+"','"\
                    +attribDict.get("LocalMac")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("SecurityHint")+"','"+attribDict.get("SecurityHintCode")+"','"+attribDict.get("ConnectionId")+"')"
                    
        elif attribDict.get("EventID") == "11005":
            sqlQuery = "INSERT INTO Event11005 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, Adapter, DeviceGuid, LocalMac,\
                    SSID, BSSType, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("Adapter")+"','"+attribDict.get("DeviceGuid")+"','"\
                    +attribDict.get("LocalMac")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("ConnectionId")+"')"
            
        elif attribDict.get("EventID") == "11010":
            sqlQuery = "INSERT INTO Event11010 (EventID, Version, Level, Task, OpCode, Keywords, TimeCreated, EventRecordID, ProcessID, \
                    ThreadID, Channel, Computer, UserID, Adapter, DeviceGuid, LocalMac,\
                    SSID, BSSType, Auth, AuthVal, Cipher, CipherVal, FIPSMode, OnexEnabled, ConnectionId) \
                    VALUES ("+attribDict.get("EventID")+","+ attribDict.get("Version")+","+ attribDict.get("Level")+"," \
                    +attribDict.get("Task")+","+ attribDict.get("Opcode")+",'"+attribDict.get("Keywords")+"','"+attribDict.get("TimeCreated")+"'," \
                    +attribDict.get("EventRecordID")+","+attribDict.get("ProcessID")+","+attribDict.get("ThreadID")+",'"+attribDict.get("Channel")+"','"\
                    +attribDict.get("Computer")+"','"+attribDict.get("UserID")+"','"+attribDict.get("Adapter")+"','"+attribDict.get("DeviceGuid")+"','"\
                    +attribDict.get("LocalMac")+"','"+attribDict.get("SSID")+"','" \
                    +attribDict.get("BSSType")+"','"+attribDict.get("Auth")+"','"+attribDict.get("AuthVal")+"','"+attribDict.get("Cipher")+"','" \
                    +attribDict.get("CipherVal")+"','"+attribDict.get("FIPSMode")+"','"+attribDict.get("OnexEnabled")+"','"\
                    +attribDict.get("ConnectionId")+"')"    
        
        else:
            print " Non Handled EventID: %s " %attribDict.get("EventID") 
        #print sqlQuery
        conn.execute(sqlQuery)         
    conn.commit()
    print "Table populated with query results"
    conn.close()

def plotPie(labels, values, title):
    """
        Outputs an HTML file (named "generated_graph.html") containing the pie chart.
        
        **Arguments:**
        
        - labels: List of category labels (List)
        - values: List of values/count for corresponding category (List)
        - title: Title for this plot (String) 
    """
    figure = {
            'data': [{'labels': labels,
                    'values': values,
                    'type': 'pie'}],
            'layout': {'title': 'APs in channel'}
        }
    width = '100%'
    height = 525
    plotdivid="plot"
    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout={"title": title}
    jconfig = json.dumps({})
    script = '\n'.join([
        'Plotly.plot("{id}", {data}, {layout}, {config}).then(function() {{',
        '    $(".{id}.loading").remove();',
        '}})'
    ]).format(id=plotdivid,
              data=jdata,
              layout=jlayout,
              config=jconfig)
    html="""<div class="{id} loading" style="color: rgb(50,50,50);">
                 </div>
                 <div id="{id}" style="height: {height}; width: {width};" 
                 class="plotly-graph-div">
                 </div>
                 <script type="text/javascript">
                 {script}
                 </script>
                 """.format(id=plotdivid, script=script,
                           height=height, width=width)
    html='<html><body><script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>'+html+'</body></html>'
    testfile = open("generated_graph.html","w")
    testfile.write(html)
    testfile.close()

def plotBar(labels, values, title, xlabel="X axis", ylabel="Y axis"):
    """
        Outputs an HTML file (named "generated_graph.html") containing the bar chart.
        
        **Arguments:**
        
        - labels: List of category labels (List)
        - values: List of values/count for corresponding category (List)
        - title: Title for this plot (String)
        - xlabel: Label for X-axis (String)
        - ylabel: Label for Y-axis (String)
    """
    trace = Bar(x=labels,y=values)
    figure_or_data = [trace]
    figure = tools.return_figure_from_figure_or_data(figure_or_data, 1)
    width = '100%'
    height = 525
    plotdivid="plot"
    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout={"title": title, 'margin':{'l':200},"xaxis": {"title": xlabel},"yaxis": {"title": ylabel}}
    jconfig = json.dumps({})
    script = '\n'.join([
        'Plotly.plot("{id}", {data}, {layout}, {config}).then(function() {{',
        '    $(".{id}.loading").remove();',
        '}})'
    ]).format(id=plotdivid,
              data=jdata,
              layout=jlayout,
              config=jconfig)

    html="""<div class="{id} loading" style="color: rgb(50,50,50);">
                 </div>
                 <div id="{id}" style="height: {height}; width: {width};" 
                 class="plotly-graph-div">
                 </div>
                 <script type="text/javascript">
                 {script}
                 </script>
                 """.format(id=plotdivid, script=script,
                           height=height, width=width)
    html='<html><body><script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>'+html+'</body></html>'
    testfile = open("generated_graph.html","w")
    testfile.write(html)
    testfile.close()
    
def plotLine(labels, values, title, xlabel="X axis", ylabel="Y axis"):
    """
        Outputs an HTML file (named "generated_graph.html") containing the line graph.
        
        **Arguments:**
        
        - labels: List of category labels (List)
        - values: List of values/count for corresponding category (List)
        - title: Title for this plot (String)
        - xlabel: Label for X-axis (String)
        - ylabel: Label for Y-axis (String)
    """
    trace = Scatter(x=labels,y=values)
    figure_or_data = [trace]
    figure = tools.return_figure_from_figure_or_data(figure_or_data, 1)
    width = '90%'
    height = 525
    plotdivid="plot"
    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout={"title": title,'margin':{'l':200}, "xaxis": {"title": xlabel},"yaxis": {"title": ylabel}}
    jconfig = json.dumps({})
    script = '\n'.join([
        'Plotly.plot("{id}", {data}, {layout}, {config}).then(function() {{',
        '    $(".{id}.loading").remove();',
        '}})'
    ]).format(id=plotdivid,
              data=jdata,
              layout=jlayout,
              config=jconfig)

    html="""<div class="{id} loading" style="color: rgb(50,50,50);">
                 </div>
                 <div id="{id}" style="height: {height}; width: {width};" 
                 class="plotly-graph-div">
                 </div>
                 <script type="text/javascript">
                 {script}
                 </script>
                 """.format(id=plotdivid, script=script,
                           height=height, width=width)
    html='<html><body><script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>'+html+'</body></html>'
    testfile = open("output.html","w")
    testfile.write(html)
    testfile.close()

maxCap = 15
def sendToCovertChannel(guid, ssid="CovertChannel", ElementId = 12, data=""):
    """
        Sends data over covert channel created over probe requests.
        This function handles re-sending, data fragmentation
        
        **Arguments:**
        
        - guid: GUID of the Interface (String) 
        - ssid: Profile/SSID name to be filled in for probe requests (String)
        - ElementId: Information Element ID to be used for packing (Integer)
        - data: Data to be passed over channel (String)
    """
    dataLen = len(data)
    counter = 1
    # Breaking big string into multiple packets
    while (dataLen+2 > maxCap):
        #print "dataLen: %s" %dataLen
        counter_len= len(str(counter)+"_")
        tempData = str(counter) + "_" + data[0:maxCap-1-counter_len]
        result = wlanScan(guid, ssid, 12, tempData)
        # Retrying in case of resource busy
        if result == ERROR_RESOURCE_BUSY:
            sleep(5)
            print "Resource busy received. Resending."
            continue
        print " Sent fragment : %d" %counter
        counter = counter +1 
        remData = data[maxCap-1-counter_len:dataLen]
        data = remData
        dataLen = len(data)
        #print "==> tempData=%s     \nremData=%s  \ndata=%s" %(tempData, remData, data)
        # Sleep is to give the interface time otherwise RESOURCE_BUSY is thrown
        sleep(5)
    data = str(0)+"_"+data
    dataLen = len(data)
    # Padding last packet to maxLen-1 
    if (dataLen != maxCap-1):
        padding = "-" * ((maxCap-1) - dataLen)
        data = data + padding
        dataLen = len(data)
    while True:
        result = wlanScan(guid, ssid, 12, data)
        if result != ERROR_RESOURCE_BUSY:
            break
        print "Resource busy received. Resending."
        sleep(5)
    print " Sent fragment : %d" %counter
    
def listenForCommand(wireless_interface, ssid = "CovertChannel", ElementId = 12):
    """
        Listens and returns the commands which are supposed to come in Information Element
        "ElementId" of Beacons of wireless network "ssid". 
        
        **Arguments:**
            
        - wireless_interface: Wireless interface (String) 
        - ssid: Profile/SSID name to be filled in for probe requests (String)
        - ElementId: Information Element ID to be used for packing (Integer)
    """
    print "Listening"
    while(1):
        bsss = getWirelessNetworkBssList(wireless_interface)
        for bss in bsss:
                lineList = str(bss).split('\n')
                Ssid = lineList[1].split(':')
                ssidName = Ssid[1].replace(" ","")
                if ssidName == ssid:
                    neededIE = " + Element ID: "+str(ElementId)
                    if neededIE in lineList: 
                        loc = lineList.index(neededIE)
                        length = lineList[loc + 1].split(':')
                        length = length[1].replace(" ","")
                        body = lineList[loc + 2].split(':')
                        body = body[1].replace(" ","").replace("'","").replace("$","")
                        contentList = body.split('\\x')
                        output = ""
                        for item in contentList:
                            output = output + item
                        return output
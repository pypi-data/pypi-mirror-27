##################################################################################
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
# Author: Andres Blanco (6e726d)     <6e726d@gmail.com>
#
################################################################################## 
#
# This file is distributed as a part of PyWinWiFi library
#
# We have added the following functions to it:
# -	WlanSetProfile()					:	Sets the contents to a network profile 
# -	WlanHostedNetworkForceStart()		:	Starts and manages a hosted network
# - EvtQuery(), EvtNext(), EvtClose()	: 	Facilitates interception of live WiFI events
#											and retrieval WiFi logs
#
# Original file LoC: 890 
# Modified file LoC: 1726
#
# Author		: Nishant Sharma <nishant@binarysecuritysolutions.com>
# Organizations	: Pentester Academy <www.pentesteracademy.com> and Hacker Arsenal <www.hackerarsenal.com>
#
##################################################################################

from ctypes import *
from comtypes import GUID

from ctypes.wintypes import BOOL
from ctypes.wintypes import USHORT
from ctypes.wintypes import UINT
from ctypes.wintypes import DWORD
from ctypes.wintypes import HANDLE
from ctypes.wintypes import LPWSTR
from ctypes.wintypes import LPCWSTR
from comtypes.typeinfo import PVOID
from time import sleep

ERROR_SUCCESS = 0
ERROR_RESOURCE_BUSY = 170

CLIENT_VERSION_WINDOWS_XP_SP3 = 1
CLIENT_VERSION_WINDOWS_VISTA_OR_LATER = 2

# Windot11.h defines
DOT11_SSID_MAX_LENGTH = 32
DOT11_BSSID_LIST_REVISION_1 = 1

# Ntddndis.h defines
NDIS_OBJECT_TYPE_DEFAULT = 0x80

wlanapi = windll.LoadLibrary('wlanapi.dll')
logapi = windll.LoadLibrary('Wevtapi.dll')

# The WLAN_INTERFACE_STATE enumerated type indicates the state of an interface.
WLAN_INTERFACE_STATE = c_uint
WLAN_INTERFACE_STATE_DICT = {0: "wlan_interface_state_not_ready",
                             1: "wlan_interface_state_connected",
                             2: "wlan_interface_state_ad_hoc_network_formed",
                             3: "wlan_interface_state_disconnecting",
                             4: "wlan_interface_state_disconnected",
                             5: "wlan_interface_state_associating",
                             6: "wlan_interface_state_discovering",
                             7: "wlan_interface_state_authenticating"}

# The DOT11_MAC_ADDRESS types are used to define an IEEE media access control
# (MAC) address.
DOT11_MAC_ADDRESS = c_ubyte * 6

# The DOT11_BSS_TYPE enumerated type defines a basic service set (BSS) network
# type.
DOT11_BSS_TYPE = c_uint
DOT11_BSS_TYPE_DICT_KV = {1: "dot11_BSS_type_infrastructure",
                       2: "dot11_BSS_type_independent",
                       3: "dot11_BSS_type_any"}
DOT11_BSS_TYPE_DICT_VK = { v: k for k, v in
        DOT11_BSS_TYPE_DICT_KV.iteritems() }

# The DOT11_PHY_TYPE enumeration defines an 802.11 PHY and media type.
DOT11_PHY_TYPE = c_uint
DOT11_PHY_TYPE_DICT = {0: "dot11_phy_type_unknown",
                       1: "dot11_phy_type_fhss",
                       2: "dot11_phy_type_dsss",
                       3: "dot11_phy_type_irbaseband",
                       4: "dot11_phy_type_ofdm",
                       5: "dot11_phy_type_hrdsss",
                       6: "dot11_phy_type_erp",
                       7: "dot11_phy_type_ht",
                       8: "dot11_phy_type_IHV_start",
                       0x80000000: "dot11_phy_type_IHV_start",
                       0xffffffff: "dot11_phy_type_IHV_end"}

# The WLAN_INTERFACE_TYPE enumeration defines an 802.11 PHY and media type.
WLAN_INTERFACE_TYPE = c_uint
WLAN_INTERFACE_TYPE_DICT = {0: "wlan_interface_type_emulated_802_11",
                       1: "wlan_interface_type_native_802_11",
                       2: "wlan_interface_type_invalid"}


# The DOT11_AUTH_ALGORITHM enumerated type defines a wireless LAN
# authentication algorithm.
DOT11_AUTH_ALGORITHM_TYPE = c_uint
DOT11_AUTH_ALGORITHM_DICT = {1: "DOT11_AUTH_ALGO_80211_OPEN",
                             2: "DOT11_AUTH_ALGO_80211_SHARED_KEY",
                             3: "DOT11_AUTH_ALGO_WPA",
                             4: "DOT11_AUTH_ALGO_WPA_PSK",
                             5: "DOT11_AUTH_ALGO_WPA_NONE",
                             6: "DOT11_AUTH_ALGO_RSNA",
                             7: "DOT11_AUTH_ALGO_RSNA_PSK",
                             0x80000000: "DOT11_AUTH_ALGO_IHV_START",
                             0xffffffff: "DOT11_AUTH_ALGO_IHV_END"}

# The DOT11_CIPHER_ALGORITHM enumerated type defines a cipher algorithm for
# data encryption and decryption.
DOT11_CIPHER_ALGORITHM_TYPE = c_uint
DOT11_CIPHER_ALGORITHM_DICT = {0x00: "DOT11_CIPHER_ALGO_NONE",
                               0x01: "DOT11_CIPHER_ALGO_WEP40",
                               0x02: "DOT11_CIPHER_ALGO_TKIP",
                               0x04: "DOT11_CIPHER_ALGO_CCMP",
                               0x05: "DOT11_CIPHER_ALGO_WEP104",
                               0x100: "DOT11_CIPHER_ALGO_WPA_USE_GROUP",
                               0x100: "DOT11_CIPHER_ALGO_RSN_USE_GROUP",
                               0x101: "DOT11_CIPHER_ALGO_WEP",
                               0x80000000: "DOT11_CIPHER_ALGO_IHV_START",
                               0xffffffff: "DOT11_CIPHER_ALGO_IHV_END"}

DOT11_RADIO_STATE = c_uint
#TODO: values not verified
DOT11_RADIO_STATE_DICT = {0: "dot11_radio_state_unknown",
                          1: "dot11_radio_state_on",
                          2: "dot11_radio_state_off"}

WLAN_REASON_CODE = DWORD
WLAN_SIGNAL_QUALITY = c_ulong

WLAN_MAX_PHY_TYPE_NUMBER = 8

DOT11_RATE_SET_MAX_LENGTH = 126

# WLAN_AVAILABLE_NETWORK Flags
WLAN_AVAILABLE_NETWORK_CONNECTED = 0x00000001
WLAN_AVAILABLE_NETWORK_HAS_PROFILE = 0x00000002
WLAN_AVAILABLE_NETWORK_CONSOLE_USER_PROFILE = 0x00000004

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002

WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_ADHOC_PROFILES = 0x00000001
WLAN_AVAILABLE_NETWORK_INCLUDE_ALL_MANUAL_HIDDEN_PROFILES = 0x00000002

# WLAN Profile Flags
WLAN_PROFILE_GROUP_POLICY = 0x00000001
WLAN_PROFILE_USER = 0x00000002
WLAN_PROFILE_GET_PLAINTEXT_KEY = 0x00000004


class WLAN_INTERFACE_INFO(Structure):
    """
        The WLAN_INTERFACE_INFO structure contains information about a wireless
        LAN interface.

        typedef struct _WLAN_INTERFACE_INFO {
            GUID                 InterfaceGuid;
            WCHAR                strInterfaceDescription[256];
            WLAN_INTERFACE_STATE isState;
        } WLAN_INTERFACE_INFO, *PWLAN_INTERFACE_INFO;
    """
    _fields_ = [("InterfaceGuid", GUID),
                ("strInterfaceDescription", c_wchar * 256),
                ("isState", WLAN_INTERFACE_STATE)]


class WLAN_INTERFACE_INFO_LIST(Structure):
    """
        The WLAN_INTERFACE_INFO_LIST structure contains an array of NIC
        interface information.

        typedef struct _WLAN_INTERFACE_INFO_LIST {
            DWORD               dwNumberOfItems;
            DWORD               dwIndex;
            WLAN_INTERFACE_INFO InterfaceInfo[];
        } WLAN_INTERFACE_INFO_LIST, *PWLAN_INTERFACE_INFO_LIST;
    """
    _fields_ = [("NumberOfItems", DWORD),
                ("Index", DWORD),
                ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)]


class WLAN_PHY_RADIO_STATE(Structure):
    """
        The WLAN_PHY_RADIO_STATE structure specifies the radio state on a specific physical layer (PHY) type.
        
        typedef struct _WLAN_PHY_RADIO_STATE {
            DWORD             dwPhyIndex;
            DOT11_RADIO_STATE dot11SoftwareRadioState;
            DOT11_RADIO_STATE dot11HardwareRadioState;
        } WLAN_PHY_RADIO_STATE, *PWLAN_PHY_RADIO_STATE;
    """
    _fields_ = [("dwPhyIndex", DWORD),
                ("dot11SoftwareRadioState", DOT11_RADIO_STATE),
                ("dot11HardwareRadioState", DOT11_RADIO_STATE)]


class WLAN_RADIO_STATE(Structure):
    """
        The WLAN_RADIO_STATE structure specifies the radio state on a list
        of physical layer (PHY) types.

        typedef struct _WLAN_RADIO_STATE {
            DWORD                dwNumberOfPhys;
            WLAN_PHY_RADIO_STATE PhyRadioState[64];
        } WLAN_RADIO_STATE, *PWLAN_RADIO_STATE
    """
    _fields_ = [("dwNumberOfPhys", DWORD),
                ("PhyRadioState", WLAN_PHY_RADIO_STATE * 64)]

class DOT11_SSID(Structure):
    """
        A DOT11_SSID structure contains the SSID of an interface.

        typedef struct _DOT11_SSID {
            ULONG uSSIDLength;
            UCHAR ucSSID[DOT11_SSID_MAX_LENGTH];
        } DOT11_SSID, *PDOT11_SSID;
    """
    _fields_ = [("SSIDLength", c_ulong),
                ("SSID", c_char * DOT11_SSID_MAX_LENGTH)]


class WLAN_RAW_DATA(Structure):
    """
        The WLAN_RAW_DATA structure contains raw data in the form of a blob
        that is used by some Native Wifi functions.

        typedef struct _WLAN_RAW_DATA {
            DWORD dwDataSize;
            BYTE  DataBlob[1];
        } WLAN_RAW_DATA, *PWLAN_RAW_DATA;
    """
    _fields_ = [("DataSize", DWORD),
                ("DataBlob", c_byte * 20)]


class WLAN_RATE_SET(Structure):
    """
        typedef struct _WLAN_RATE_SET {
            ULONG  uRateSetLength;
            USHORT usRateSet[DOT11_RATE_SET_MAX_LENGTH];
        } WLAN_RATE_SET, *PWLAN_RATE_SET;
    """
    _fields_ = [("RateSetLength", c_ulong),
                ("RateSet", c_ushort * DOT11_RATE_SET_MAX_LENGTH)]


class WLAN_BSS_ENTRY(Structure):
    """
        The WLAN_BSS_ENTRY structure contains information about a basic service
        set (BSS).

        typedef struct _WLAN_BSS_ENTRY {
            DOT11_SSID        dot11Ssid;
            ULONG             uPhyId;
            DOT11_MAC_ADDRESS dot11Bssid;
            DOT11_BSS_TYPE    dot11BssType;
            DOT11_PHY_TYPE    dot11BssPhyType;
            LONG              lRssi;
            ULONG             uLinkQuality;
            BOOLEAN           bInRegDomain;
            USHORT            usBeaconPeriod;
            ULONGLONG         ullTimestamp;
            ULONGLONG         ullHostTimestamp;
            USHORT            usCapabilityInformation;
            ULONG             ulChCenterFrequency;
            WLAN_RATE_SET     wlanRateSet;
            ULONG             ulIeOffset;
            ULONG             ulIeSize;
        } WLAN_BSS_ENTRY, *PWLAN_BSS_ENTRY;
    """
    _fields_ = [("dot11Ssid", DOT11_SSID),
                ("PhyId", c_ulong),
                ("dot11Bssid", DOT11_MAC_ADDRESS),
                ("dot11BssType", DOT11_BSS_TYPE),
                ("dot11BssPhyType", DOT11_PHY_TYPE),
                ("Rssi", c_long),
                ("LinkQuality", c_ulong),
                ("InRegDomain", BOOL),
                ("BeaconPeriod", c_ushort),
                ("Timestamp", c_ulonglong),
                ("HostTimestamp", c_ulonglong),
                ("CapabilityInformation", c_ushort),
                ("ChCenterFrequency", c_ulong),
                ("wlanRateSet", WLAN_RATE_SET),
                ("IeOffset", c_ulong),
                ("IeSize", c_ulong)]


class WLAN_BSS_LIST(Structure):
    """
        The WLAN_BSS_LIST structure contains a list of basic service set (BSS)
        entries.

        typedef struct _WLAN_BSS_LIST {
            DWORD          dwTotalSize;
            DWORD          dwNumberOfItems;
            WLAN_BSS_ENTRY wlanBssEntries[1];
        } WLAN_BSS_LIST, *PWLAN_BSS_LIST;
    """
    _fields_ = [("TotalSize", DWORD),
                ("NumberOfItems", DWORD),
                ("wlanBssEntries", WLAN_BSS_ENTRY * 1)]


class WLAN_AVAILABLE_NETWORK(Structure):
    """
        The WLAN_AVAILABLE_NETWORK structure contains information about an
        available wireless network.

        typedef struct _WLAN_AVAILABLE_NETWORK {
            WCHAR                  strProfileName[256];
            DOT11_SSID             dot11Ssid;
            DOT11_BSS_TYPE         dot11BssType;
            ULONG                  uNumberOfBssids;
            BOOL                   bNetworkConnectable;
            WLAN_REASON_CODE       wlanNotConnectableReason;
            ULONG                  uNumberOfPhyTypes;
            DOT11_PHY_TYPE         dot11PhyTypes[WLAN_MAX_PHY_TYPE_NUMBER];
            BOOL                   bMorePhyTypes;
            WLAN_SIGNAL_QUALITY    wlanSignalQuality;
            BOOL                   bSecurityEnabled;
            DOT11_AUTH_ALGORITHM   dot11DefaultAuthAlgorithm;
            DOT11_CIPHER_ALGORITHM dot11DefaultCipherAlgorithm;
            DWORD                  dwFlags;
            DWORD                  dwReserved;
        } WLAN_AVAILABLE_NETWORK, *PWLAN_AVAILABLE_NETWORK;
    """
    _fields_ = [("ProfileName", c_wchar * 256),
                ("dot11Ssid", DOT11_SSID),
                ("dot11BssType", DOT11_BSS_TYPE),
                ("NumberOfBssids", c_ulong),
                ("NetworkConnectable", BOOL),
                ("wlanNotConnectableReason", WLAN_REASON_CODE),
                ("NumberOfPhyTypes", c_ulong),
                ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_TYPE_NUMBER),
                ("MorePhyTypes", BOOL),
                ("wlanSignalQuality", WLAN_SIGNAL_QUALITY),
                ("SecurityEnabled", BOOL),
                ("dot11DefaultAuthAlgorithm", DOT11_AUTH_ALGORITHM_TYPE),
                ("dot11DefaultCipherAlgorithm", DOT11_CIPHER_ALGORITHM_TYPE),
                ("Flags", DWORD),
                ("Reserved", DWORD)]


class WLAN_AVAILABLE_NETWORK_LIST(Structure):
    """
        The WLAN_AVAILABLE_NETWORK_LIST structure contains an array of
        information about available networks.

        typedef struct _WLAN_AVAILABLE_NETWORK_LIST {
            DWORD                  dwNumberOfItems;
            DWORD                  dwIndex;
            WLAN_AVAILABLE_NETWORK Network[1];
        } WLAN_AVAILABLE_NETWORK_LIST, *PWLAN_AVAILABLE_NETWORK_LIST;
    """
    _fields_ = [("NumberOfItems", DWORD),
                ("Index", DWORD),
                ("Network", WLAN_AVAILABLE_NETWORK * 1)]


class WLAN_PROFILE_INFO(Structure):
    """
        The WLAN_PROFILE_INFO structure contains basic information about a
        profile.

        typedef struct _WLAN_PROFILE_INFO {
            WCHAR strProfileName[256];
            DWORD dwFlags;
        } WLAN_PROFILE_INFO, *PWLAN_PROFILE_INFO;
    """
    _fields_ = [("ProfileName", c_wchar * 256),
                ("Flags", DWORD)]


class WLAN_PROFILE_INFO_LIST(Structure):
    """
        The WLAN_PROFILE_INFO_LIST structure contains a list of wireless
        profile information.

        typedef struct _WLAN_PROFILE_INFO_LIST {
            DWORD             dwNumberOfItems;
            DWORD             dwIndex;
            WLAN_PROFILE_INFO ProfileInfo[1];
        } WLAN_PROFILE_INFO_LIST, *PWLAN_PROFILE_INFO_LIST;
    """
    _fields_ = [("NumberOfItems", DWORD),
                ("Index", DWORD),
                ("ProfileInfo", WLAN_PROFILE_INFO * 1)]


def WlanOpenHandle():
    """
        The WlanOpenHandle function opens a connection to the server.

        DWORD WINAPI WlanOpenHandle(
            _In_        DWORD dwClientVersion,
            _Reserved_  PVOID pReserved,
            _Out_       PDWORD pdwNegotiatedVersion,
            _Out_       PHANDLE phClientHandle
        );
    """
    func_ref = wlanapi.WlanOpenHandle
    func_ref.argtypes = [DWORD, c_void_p, POINTER(DWORD), POINTER(HANDLE)]
    func_ref.restype = DWORD
    negotiated_version = DWORD()
    client_handle = HANDLE()
    result = func_ref(2, None, byref(negotiated_version), byref(client_handle))
    if result != ERROR_SUCCESS:
        raise Exception("WlanOpenHandle failed.")
    return client_handle


def WlanCloseHandle(hClientHandle):
    """
        The WlanCloseHandle function closes a connection to the server.

        DWORD WINAPI WlanCloseHandle(
            _In_        HANDLE hClientHandle,
            _Reserved_  PVOID pReserved
        );
    """
    func_ref = wlanapi.WlanCloseHandle
    func_ref.argtypes = [HANDLE, c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle, None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanCloseHandle failed.")
    return result


def WlanFreeMemory(pMemory):
    """
        The WlanFreeMemory function frees memory. Any memory returned from
        Native Wifi functions must be freed.

        VOID WINAPI WlanFreeMemory(
            _In_  PVOID pMemory
        );
    """
    func_ref = wlanapi.WlanFreeMemory
    func_ref.argtypes = [c_void_p]
    func_ref(pMemory)


def WlanEnumInterfaces(hClientHandle):
    """
        The WlanEnumInterfaces function enumerates all of the wireless LAN
        interfaces currently enabled on the local computer.

        DWORD WINAPI WlanEnumInterfaces(
            _In_        HANDLE hClientHandle,
            _Reserved_  PVOID pReserved,
            _Out_       PWLAN_INTERFACE_INFO_LIST *ppInterfaceList
        );
    """
    func_ref = wlanapi.WlanEnumInterfaces
    func_ref.argtypes = [HANDLE,
                         c_void_p,
                         POINTER(POINTER(WLAN_INTERFACE_INFO_LIST))]
    func_ref.restype = DWORD
    wlan_ifaces = pointer(WLAN_INTERFACE_INFO_LIST())
    result = func_ref(hClientHandle, None, byref(wlan_ifaces))
    if result != ERROR_SUCCESS:
        raise Exception("WlanEnumInterfaces failed.")
    return wlan_ifaces


def WlanScan(hClientHandle, pInterfaceGuid, ssid="", pIeData=None):
    """
        The WlanScan function requests a scan for available networks on the
        indicated interface.

        DWORD WINAPI WlanScan(
            _In_        HANDLE hClientHandle,
            _In_        const GUID *pInterfaceGuid,
            _In_opt_    const PDOT11_SSID pDot11Ssid,
            _In_opt_    const PWLAN_RAW_DATA pIeData,
            _Reserved_  PVOID pReserved
        );
    """
    func_ref = wlanapi.WlanScan
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         POINTER(DOT11_SSID),
                         POINTER(WLAN_RAW_DATA),
                         c_void_p]
    func_ref.restype = DWORD
    if ssid:
        length = len(ssid)
        if length > DOT11_SSID_MAX_LENGTH:
            raise Exception("SSIDs have a maximum length of 32 characters.")
        # data = tuple(ord(char) for char in ssid)
        data = ssid
        dot11_ssid = byref(DOT11_SSID(length, data))
    else:
        dot11_ssid = None
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      dot11_ssid,
                      byref(pIeData),
                      None)
    if result != ERROR_SUCCESS and result != ERROR_RESOURCE_BUSY:
        raise Exception("WlanScan failed.")
    return result


def WlanGetNetworkBssList(hClientHandle, pInterfaceGuid):
    """
        The WlanGetNetworkBssList function retrieves a list of the basic
        service set (BSS) entries of the wireless network or networks on a
        given wireless LAN interface.

        DWORD WINAPI WlanGetNetworkBssList(
            _In_        HANDLE hClientHandle,
            _In_        const GUID *pInterfaceGuid,
            _In_        const  PDOT11_SSID pDot11Ssid,
            _In_        DOT11_BSS_TYPE dot11BssType,
            _In_        BOOL bSecurityEnabled,
            _Reserved_  PVOID pReserved,
            _Out_       PWLAN_BSS_LIST *ppWlanBssList
        );
    """
    func_ref = wlanapi.WlanGetNetworkBssList
    # TODO: handle the arguments descibed below.
    # pDot11Ssid - When set to NULL, the returned list contains all of
    # available BSS entries on a wireless LAN interface.
    # dot11BssType - The BSS type of the network. This parameter is ignored if
    # the SSID of the network for the BSS list is unspecified (the pDot11Ssid
    # parameter is NULL).
    # bSecurityEnabled - A value that indicates whether security is enabled on
    # the network. This parameter is only valid when the SSID of the network
    # for the BSS list is specified (the pDot11Ssid parameter is not NULL).
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         c_void_p,
                         c_void_p,
                         c_void_p,
                         c_void_p,
                         POINTER(POINTER(WLAN_BSS_LIST))]
    func_ref.restype = DWORD
    wlan_bss_list = pointer(WLAN_BSS_LIST())
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      None,
                      None,
                      None,
                      None,
                      byref(wlan_bss_list))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetNetworkBssList failed.")
    return wlan_bss_list


def WlanGetAvailableNetworkList(hClientHandle, pInterfaceGuid):
    """
        The WlanGetAvailableNetworkList function retrieves the list of
        available networks on a wireless LAN interface.

        DWORD WINAPI WlanGetAvailableNetworkList(
            _In_        HANDLE hClientHandle,
            _In_        const GUID *pInterfaceGuid,
            _In_        DWORD dwFlags,
            _Reserved_  PVOID pReserved,
            _Out_       PWLAN_AVAILABLE_NETWORK_LIST *ppAvailableNetworkList
        );
    """
    func_ref = wlanapi.WlanGetAvailableNetworkList
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         DWORD,
                         c_void_p,
                         POINTER(POINTER(WLAN_AVAILABLE_NETWORK_LIST))]
    func_ref.restype = DWORD
    wlan_available_network_list = pointer(WLAN_AVAILABLE_NETWORK_LIST())
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      0,
                      None,
                      byref(wlan_available_network_list))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetAvailableNetworkList failed.")
    return wlan_available_network_list

def WlanHostedNetworkForceStart(hClientHandle):
    """
        The WlanHostedNetworkForceStart function transitions the wireless
        Hosted Network to the wlan_hosted_network_active state without 
        associating the request with the application's calling handle.
    
        DWORD WINAPI WlanHostedNetworkForceStart(
            _In_       HANDLE                      hClientHandle,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    func_ref = wlanapi.WlanHostedNetworkForceStart
    func_ref.argtypes = [HANDLE,
                         UINT,
                         c_void_p]
    func_ref.restype = DWORD
    code = 0
    result = func_ref(hClientHandle,
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkForceStart failed.")
    return result

def WlanHostedNetworkForceStop(hClientHandle):
    """
        The WlanHostedNetworkForceStop function transitions the wireless
        Hosted Network to the wlan_hosted_network_idle without associating
        the request with the application's calling handle.
        
        DWORD WINAPI WlanHostedNetworkForceStop(
            _In_       HANDLE                      hClientHandle,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    func_ref = wlanapi.WlanHostedNetworkForceStop
    func_ref.argtypes = [HANDLE,
                         UINT,
                         c_void_p]
    func_ref.restype = DWORD
    code = 0
    result = func_ref(hClientHandle,
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkForceStop failed.")
    return result

def WlanHostedNetworkSetProperty(hClientHandle, OpCode, dwDataSize, pvData, pFailReason):
    """
        The WlanHostedNetworkSetProperty function sets static properties of the wireless Hosted Network.
        
        DWORD WINAPI WlanHostedNetworkSetProperty(
            _In_       HANDLE                      hClientHandle,
            _In_       WLAN_HOSTED_NETWORK_OPCODE  OpCode,
            _In_       DWORD                       dwDataSize,
            _In_       PVOID                       pvData,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    
    func_ref = wlanapi.WlanHostedNetworkSetProperty
    func_ref.argtypes = [HANDLE,
                         WLAN_OPCODE_VALUE_TYPE,
                         UINT,
                         POINTER(WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS),
                         UINT,
                         c_void_p]
    func_ref.restype = DWORD
    opcode_name = WLAN_HOSTED_NETWORK_OPCODE_DICT[OpCode]
    print "    Using Option : %s" %opcode_name
    
    code =0 
    result = func_ref(hClientHandle,
                      OpCode,
                      dwDataSize,
                      byref(pvData),
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkSetProperty failed.")
    return result

def WlanHostedNetworkSetSecondaryKey(hClientHandle, dwKeyLength, pucKeyData, bIsPassPhrase, bPersistent, pFailReason):
    """
        The WlanHostedNetworkSetSecondaryKey function configures the secondary
        security key that will be used by the wireless Hosted Network.
        
        DWORD WINAPI WlanHostedNetworkSetSecondaryKey(
            _In_       HANDLE                      hClientHandle,
            _In_       DWORD                       dwKeyLength,
            _In_       PUCHAR                      pucKeyData,
            _In_       BOOL                        bIsPassPhrase,
            _In_       BOOL                        bPersistent,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    func_ref = wlanapi.WlanHostedNetworkSetSecondaryKey
    func_ref.argtypes = [HANDLE,
                         DWORD,
                         POINTER(c_char),
                         BOOL,
                         BOOL,
                         UINT,
                         c_void_p]
    code = 0
    pucKeyData.encode('utf-8')
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      dwKeyLength,
                      c_char_p(pucKeyData),
                      bIsPassPhrase,
                      bPersistent,
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkSetSecondaryKey failed.")
    return result

def WlanHostedNetworkStartUsing(hClientHandle, pFailReason):
    """
        The WlanHostedNetworkStartUsing function starts the wireless Hosted Network.
    
        DWORD WINAPI WlanHostedNetworkStartUsing(
            _In_       HANDLE                      hClientHandle,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    func_ref = wlanapi.WlanHostedNetworkStartUsing
    func_ref.argtypes = [HANDLE,
                         UINT,
                         c_void_p]
    func_ref.restype = DWORD
    code =0 
    result = func_ref(hClientHandle,
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkStartUsing failed.")
    return result


def WlanHostedNetworkStopUsing(hClientHandle, pFailReason):
    """
        The WlanHostedNetworkStopUsing function stops the wireless Hosted Network.

        DWORD WINAPI WlanHostedNetworkStopUsing(
            _In_       HANDLE                      hClientHandle,
            _Out_opt_  PWLAN_HOSTED_NETWORK_REASON pFailReason,
            _Reserved_ PVOID                       pvReserved
        );
    """
    func_ref = wlanapi.WlanHostedNetworkStopUsing
    func_ref.argtypes = [HANDLE,
                         UINT,
                         c_void_p]
    func_ref.restype = DWORD
    code = 0
    result = func_ref(hClientHandle,
                      code,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanHostedNetworkStopUsing failed.")
    return result

WLAN_MAX_PHY_INDEX = 64

class WLAN_INTERFACE_CAPABILITY(Structure):
    """
        The WLAN_INTERFACE_CAPABILITY structure contains information about the capabilities of an interface.
    
        typedef struct _WLAN_INTERFACE_CAPABILITY {
        WLAN_INTERFACE_TYPE interfaceType;
        BOOL                bDot11DSupported;
        DWORD               dwMaxDesiredSsidListSize;
        DWORD               dwMaxDesiredBssidListSize;
        DWORD               dwNumberOfSupportedPhys;
        DOT11_PHY_TYPE      dot11PhyTypes[WLAN_MAX_PHY_INDEX];
        } WLAN_INTERFACE_CAPABILITY, *PWLAN_INTERFACE_CAPABILITY;
    """
    _fields_ = [("interfaceType", WLAN_INTERFACE_TYPE),
                ("bDot11DSupported", BOOL),
                ("dwMaxDesiredSsidListSize", DWORD),
                ("dwMaxDesiredBssidListSize", DWORD),
                ("dwNumberOfSupportedPhys", DWORD),
                ("dot11PhyTypes", DOT11_PHY_TYPE * WLAN_MAX_PHY_INDEX)]


def WlanGetInterfaceCapability(hClientHandle, guid):
    """
        The WlanGetInterfaceCapability function retrieves the capabilities of an interface.

        DWORD WINAPI WlanGetInterfaceCapability(
        _In_             HANDLE                     hClientHandle,
        _In_       const GUID                       *pInterfaceGuid,
        _Reserved_       PVOID                      pReserved,
        _Out_            PWLAN_INTERFACE_CAPABILITY *ppCapability
    );

    """
    func_ref = wlanapi.WlanGetInterfaceCapability
    func_ref.argtypes = [HANDLE,
                         GUID,
                         c_void_p,
                         POINTER(POINTER(WLAN_INTERFACE_CAPABILITY))]
    func_ref.restype = DWORD
    wlanInterfaceCapabilityList = pointer(WLAN_INTERFACE_CAPABILITY())
    result = func_ref(hClientHandle,
                      guid,
                      None,
                      byref(wlanInterfaceCapabilityList))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetInterfaceCapability failed.")
    return wlanInterfaceCapabilityList


class WLAN_NOTIFICATION_DATA(Structure):
    """
        The WLAN_NOTIFICATION_DATA structure contains information provided when receiving notifications.

        typedef struct _WLAN_NOTIFICATION_DATA {
            DWORD NotificationSource;
            DWORD NotificationCode;
            GUID  InterfaceGuid;
            DWORD dwDataSize;
            PVOID pData;
        } WLAN_NOTIFICATION_DATA, *PWLAN_NOTIFICATION_DATA;
    """
    _fields_ = [("NotificationSource", DWORD),
                ("NotificationCode", DWORD),
                ("InterfaceGuid", GUID),
                ("dwDataSize", DWORD),
                ("context", c_void_p)]

def WlanRegisterNotification(hClientHandle, notify, wlanNotificationSource):
    
    """
        The WlanRegisterNotification function is used to register and unregister notifications on all wireless interfaces.

        DWORD WINAPI WlanRegisterNotification(
            _In_       HANDLE                      hClientHandle,
            _In_       DWORD                       dwNotifSource,
            _In_       BOOL                        bIgnoreDuplicate,
            _In_opt_   WLAN_NOTIFICATION_CALLBACK  funcCallback,
            _In_opt_   PVOID                       pCallbackContext,
            _Reserved_ PVOID                       pReserved,
            _Out_opt_  PDWORD                      pdwPrevNotifSource
        );
    
        we are only choosing Auto Configuration Module (ACM) as source for notifications i.e. only get notifications
        from this module
        
        For other sources: https://msdn.microsoft.com/en-us/library/windows/desktop/ms706771(v=vs.85).aspx
    """
    
    wlanNotificationSourceCode = WLAN_NOTIFICATION_SOURCE_DICT[wlanNotificationSource]

    # Callback 
    callback = CFUNCTYPE(None, POINTER(WLAN_NOTIFICATION_DATA), POINTER(c_void_p) )
    tempCallback = callback(notify)
    
    func_ref = wlanapi.WlanRegisterNotification
    func_ref.argtypes = [HANDLE,
                         DWORD,
                         BOOL,
                         callback,
                         c_void_p,
                         c_void_p,
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                wlanNotificationSourceCode,
                False,
                tempCallback,
                byref(c_void_p()),
                None,
                None)
       
    if result != ERROR_SUCCESS:
        raise Exception("WlanRegisterNotification failed.")
    else:
        print "Registered with API for notifications and waiting"
    
    # Waiting for notifications to come
    while 1:
        sleep(0.1)

WLAN_NOTIFICATION_SOURCE =c_uint
# WLAN event notification source dict
WLAN_NOTIFICATION_SOURCE_DICT = {
    "WLAN_NOTIFICATION_SOURCE_NONE": 0,
    "WLAN_NOTIFICATION_SOURCE_ONEX": 0X00000004,
    "WLAN_NOTIFICATION_SOURCE_ACM": 0X00000008,
    "WLAN_NOTIFICATION_SOURCE_MSM": 0X00000010,
    "WLAN_NOTIFICATION_SOURCE_SECURITY": 0X00000020,
    "WLAN_NOTIFICATION_SOURCE_IHV": 0X00000040,
    "WLAN_NOTIFICATION_SOURCE_HNWK": 0X00000080,
    "WLAN_NOTIFICATION_SOURCE_ALL": 0X0000FFFF
    }

    
WLAN_NOTIFICATION_ACM = c_uint
# WLAN ACM notification type dict
WLAN_NOTIFICATION_ACM_DICT = {
    0x000000000: "wlan_notification_acm_start",
    1: "wlan_notification_acm_autoconf_enabled",
    2: "wlan_notification_acm_autoconf_disabled",
    3: "wlan_notification_acm_background_scan_enabled",
    4: "wlan_notification_acm_background_scan_disabled",
    5: "wlan_notification_acm_bss_type_change",
    6: "wlan_notification_acm_power_setting_change",
    7: "wlan_notification_acm_scan_complete",
    8: "wlan_notification_acm_scan_fail",
    9: "wlan_notification_acm_connection_start",
    10: "wlan_notification_acm_connection_complete",
    11: "wlan_notification_acm_connection_attempt_fail",
    12: "wlan_notification_acm_filter_list_change",
    13: "wlan_notification_acm_interface_arrival",
    14: "wlan_notification_acm_interface_removal",
    15: "wlan_notification_acm_profile_change",
    16: "wlan_notification_acm_profile_name_change",
    17: "wlan_notification_acm_profiles_exhausted",
    18: "wlan_notification_acm_network_not_available",
    19: "wlan_notification_acm_network_available",
    20: "wlan_notification_acm_disconnecting",
    21: "wlan_notification_acm_disconnected",
    22: "wlan_notification_acm_adhoc_network_state_change",
    23: "wlan_notification_acm_profile_unblocked",
    24: "wlan_notification_acm_screen_power_change",
    25: "wlan_notification_acm_profile_blocked",
    26: "wlan_notification_acm_scan_list_refresh",
    27: "wlan_notification_acm_end"
    }


def WlanGetProfileList(hClientHandle, pInterfaceGuid):
    """
        The WlanGetProfileList function retrieves the list of profiles in
        preference order.

        DWORD WINAPI WlanGetProfileList(
            _In_        HANDLE hClientHandle,
            _In_        const GUID *pInterfaceGuid,
            _Reserved_  PVOID pReserved,
            _Out_       PWLAN_PROFILE_INFO_LIST *ppProfileList
        );
    """
    func_ref = wlanapi.WlanGetProfileList
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         c_void_p,
                         POINTER(POINTER(WLAN_PROFILE_INFO_LIST))]
    func_ref.restype = DWORD
    wlan_profile_info_list = pointer(WLAN_PROFILE_INFO_LIST())
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      None,
                      byref(wlan_profile_info_list))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetProfileList failed.")
    return wlan_profile_info_list

def WlanGetProfile(hClientHandle, pInterfaceGuid, profileName):
    """
        The WlanGetProfile function retrieves all information about a specified
        wireless profile.

        DWORD WINAPI WlanGetProfile(
            _In_         HANDLE hClientHandle,
            _In_         const GUID *pInterfaceGuid,
            _In_         LPCWSTR strProfileName,
            _Reserved_   PVOID pReserved,
            _Out_        LPWSTR *pstrProfileXml,
            _Inout_opt_  DWORD *pdwFlags,
            _Out_opt_    PDWORD pdwGrantedAccess
        );
    """
    func_ref = wlanapi.WlanGetProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         LPCWSTR,
                         c_void_p,
                         POINTER(LPWSTR),
                         POINTER(DWORD),
                         POINTER(DWORD)]
    func_ref.restype = DWORD
    pdw_granted_access = DWORD()
    xml = LPWSTR()
    flags = DWORD(WLAN_PROFILE_GET_PLAINTEXT_KEY)
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      profileName,
                      None,
                      byref(xml),
                      byref(flags),
                      byref(pdw_granted_access))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetProfile failed.")
    return xml


def WlanSetProfile(hClientHandle, InterfaceGuid, strProfileXml, bOverwrite):
    """
        The WlanSetProfile function sets the content of a specific profile.

        DWORD WINAPI WlanSetProfile(
            _In_             HANDLE  hClientHandle,
            _In_       const GUID    *pInterfaceGuid,
            _In_             DWORD   dwFlags,
            _In_             LPCWSTR strProfileXml,
            _In_opt_         LPCWSTR strAllUserProfileSecurity,
            _In_             BOOL    bOverwrite,
            _Reserved_       PVOID   pReserved,
            _Out_            DWORD   *pdwReasonCode
        );
    """
    # Setting all-user profile
    # 1 means group policy
    # 2 means per user profile
    dwFlag = 0
    # security descriptor string on the all-user profile
    strAllUserProfileSecurity = None
    dwReasonCode = DWORD()
    func_ref = wlanapi.WlanSetProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         DWORD,
                         LPCWSTR,
                         LPCWSTR,
                         BOOL,
                         c_void_p,
                         POINTER(DWORD)]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(InterfaceGuid),
                      dwFlag,
                      strProfileXml,
                      strAllUserProfileSecurity,
                      bOverwrite,
                      None,
                      byref(dwReasonCode))
    if result != ERROR_SUCCESS:
        print result 
        print dwReasonCode
        raise Exception("WlanSetProfile failed.")
    return result

def WlanSetProfileEapXmlUserData(hClientHandle, InterfaceGuid, strProfileName, strEapXmlUserData):
    """
        The WlanSetProfileEapXmlUserData function sets the Extensible Authentication Protocol (EAP) 
        user credentials as specified by an XML string. The user credentials apply to a profile on an adapter.
        These credentials can only be used by the caller.

        DWORD WlanSetProfileEapXmlUserData(
            _In_             HANDLE  hClientHandle,
            _In_       const GUID    *pInterfaceGuid,
            _In_             LPCWSTR strProfileName,
            _In_             DWORD   dwFlags,
            _In_             LPCWSTR strEapXmlUserData,
            _Reserved_       PVOID   pReserved
        );
    """
    # Setting all-user profile
    # 1 means group policy
    # 2 means per user profile
    dwFlag = 0
    func_ref = wlanapi.WlanSetProfileEapXmlUserData
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         LPCWSTR,
                         DWORD,
                         LPCWSTR,
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(InterfaceGuid),
                      strProfileName,
                      dwFlag,
                      strEapXmlUserData,
                      None)
    if result != ERROR_SUCCESS:
        print result 
        raise Exception("WlanSetProfileEapXmlUserData failed.")
    return result

def WlanDeleteProfile(hClientHandle, pInterfaceGuid, profileName):
    """
        The WlanDeleteProfile function deletes a wireless profile for a wireless interface on the local computer.

        DWORD WINAPI WlanDeleteProfile(
            _In_             HANDLE  hClientHandle,
            _In_       const GUID    *pInterfaceGuid,
            _In_             LPCWSTR strProfileName,
            _Reserved_       PVOID   pReserved
            );
    """
    func_ref = wlanapi.WlanDeleteProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         LPCWSTR,
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      profileName,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanDeleteProfile failed.")
    return result

def WlanRenameProfile(hClientHandle, pInterfaceGuid, oldProfileName, newProfileName):
    """
        The WlanRenameProfile function renames the specified profile.

        DWORD WINAPI WlanRenameProfile(
            _In_       HANDLE  hClientHandle,
            _In_ const GUID    *pInterfaceGuid,
            _In_       LPCWSTR strOldProfileName,
            _In_       LPCWSTR strNewProfileName,
            PVOID   pReserved
        );
    """
    func_ref = wlanapi.WlanRenameProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         LPCWSTR,
                         LPCWSTR,
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      oldProfileName,
                      newProfileName,
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanRenameProfile failed.")
    return result

def WlanSaveTemporaryProfile(hClientHandle, InterfaceGuid, strProfileName, bOverwrite):
    """
        The WlanSaveTemporaryProfile function saves a temporary profile to the profile store.

        DWORD WINAPI WlanSaveTemporaryProfile(
            _In_             HANDLE  hClientHandle,
            _In_       const GUID    *pInterfaceGuid,
            _In_             LPCWSTR strProfileName,
            _In_opt_         LPCWSTR strAllUserProfileSecurity,
            _In_             DWORD   dwFlags,
            _In_             BOOL    bOverWrite,
            _Reserved_       PVOID   pReserved
        );
    """
    # Setting all-user profile
    # 1 means group policy
    # 2 means per user profile
    dwFlag = 0
    # security descriptor string on the all-user profile
    #strAllUserProfileSecurity = None
    func_ref = wlanapi.WlanSaveTemporaryProfile
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         LPCWSTR,
                         LPCWSTR,
                         DWORD,
                         BOOL,
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(InterfaceGuid),
                      strProfileName,
                      #strAllUserProfileSecurity,
                      None,
                      DWORD(dwFlag),
                      bOverwrite,
                      None)
    if result != ERROR_SUCCESS:
        print result
        raise Exception("WlanSaveTemporaryProfile failed.")
    return result

WLAN_FILTER_LIST_TYPE = c_uint
# WLAN filter list type dict
WLAN_WLAN_FILTER_LIST_TYPE_DICT = {
    0: "wlan_filter_list_type_gp_permit",
    1: "wlan_filter_list_type_gp_deny",
    2: "wlan_filter_list_type_user_permit",
    3: "wlan_filter_list_type_user_deny"
    }

class DOT11_NETWORK(Structure):
    """
        The DOT11_NETWORK structure contains information about an available wireless network.
    
        typedef struct _DOT11_NETWORK {
            DOT11_SSID     dot11Ssid;
            DOT11_BSS_TYPE dot11BssType;
        } DOT11_NETWORK, *PDOT11_NETWORK;
    """
    _fields_ = [("dot11Ssid", DOT11_SSID),
                ("dot11BssType", DOT11_BSS_TYPE)]


# TODO: Check how do generate a dynamic array of DOT11_NETWORK 
DOT11_NETWORK_MAX = 25
class DOT11_NETWORK_LIST(Structure):
    """
        The DOT11_NETWORK_LIST structure contains a list of 802.11 wireless networks.

        typedef struct _DOT11_NETWORK_LIST {
            DWORD         dwNumberOfItems;
            DWORD         dwIndex;
            DOT11_NETWORK Network[1];
        } DOT11_NETWORK_LIST, *PDOT11_NETWORK_LIST;
    """
    _fields_ = [("dwNumberOfItems", DWORD),
                ("dwIndex", DWORD),
                ("Network", DOT11_NETWORK * DOT11_NETWORK_MAX)]

def WlanGetFilterList(hClientHandle, wlanFilterListTypeStr):
    """
        The WlanGetFilterList function retrieves a group policy or user permission list.

        DWORD WINAPI WlanGetFilterList(
            _In_       HANDLE                hClientHandle,
            _In_       WLAN_FILTER_LIST_TYPE wlanFilterListType,
            _Reserved_ PVOID                 pReserved,
            _Out_      PDOT11_NETWORK_LIST   *ppNetworkList
        );
    """
    func_ref = wlanapi.WlanGetFilterList
    func_ref.argtypes = [HANDLE,
                         WLAN_FILTER_LIST_TYPE,
                         c_void_p,
                         POINTER(POINTER(DOT11_NETWORK_LIST))]
    wlanFilterListType = WLAN_WLAN_FILTER_LIST_TYPE_DICT.keys()[WLAN_WLAN_FILTER_LIST_TYPE_DICT.values().index(wlanFilterListTypeStr)]
    networkList = pointer(DOT11_NETWORK_LIST())
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      wlanFilterListType,
                      None,
                      byref(networkList))
    if result != ERROR_SUCCESS:
        raise Exception("WlanGetFilterList failed.")
    return networkList

def WlanSetFilterList(hClientHandle, wlanFilterListTypeStr, networkList):
    """
        The WlanSetFilterList function sets the permit/deny list.

        DWORD WINAPI WlanSetFilterList(
            _In_             HANDLE                hClientHandle,
            _In_             WLAN_FILTER_LIST_TYPE wlanFilterListType,
            _In_opt_   const PDOT11_NETWORK_LIST   pNetworkList,
            _Reserved_       PVOID                 pReserved
        );
    """
    
    func_ref = wlanapi.WlanSetFilterList
    func_ref.argtypes = [HANDLE,
                         WLAN_FILTER_LIST_TYPE,
                         POINTER(DOT11_NETWORK_LIST),
                         c_void_p]
    wlanFilterListType = WLAN_WLAN_FILTER_LIST_TYPE_DICT.keys()[WLAN_WLAN_FILTER_LIST_TYPE_DICT.values().index(wlanFilterListTypeStr)]
    # Handing for flushing filter list 
    if networkList != None:
        networkList = pointer(networkList)
    result = func_ref(hClientHandle,
                      wlanFilterListType,
                      networkList,
                      None)
    if result != ERROR_SUCCESS:
        print result 
        raise Exception("WlanSetFilterList failed.")
    return result

def WlanSetInterface(hClientHandle, InterfaceGuid, opCode, dwDataSize, pData):
    """
        The WlanSetInterface function sets user-configurable parameters for a specified interface.

        DWORD WINAPI WlanSetInterface(
            _In_             HANDLE           hClientHandle,
            _In_       const GUID             *pInterfaceGuid,
            _In_             WLAN_INTF_OPCODE OpCode,
            _In_             DWORD            dwDataSize,
            _In_       const PVOID            pData,
            _Reserved_       PVOID            pReserved
        );
    """
    func_ref = wlanapi.WlanSetInterface
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         WLAN_INTF_OPCODE,
                         DWORD,
                         c_void_p,
                         c_void_p]
    OpCode = WLAN_INTF_OPCODE_DICT.keys()[WLAN_INTF_OPCODE_DICT.values().index(opCode)]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(InterfaceGuid),
                      OpCode,
                      dwDataSize,
                      byref(pData),
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanSetInterface failed.")
    return result



WLAN_CONNECTION_MODE = c_uint
WLAN_CONNECTION_MODE_KV = {0: "wlan_connection_mode_profile",
                           1: "wlan_connection_mode_temporary_profile",
                           2: "wlan_connection_mode_discovery_secure",
                           3: "wlan_connection_mode_discovery_unsecure",
                           4: "wlan_connection_mode_auto",
                           5: "wlan_connection_mode_invalid"}
WLAN_CONNECTION_MODE_VK = { v: k for k, v in
        WLAN_CONNECTION_MODE_KV.iteritems() }

class NDIS_OBJECT_HEADER(Structure):
    """
        The NDIS_OBJECT_HEADER structure packages the object type, version, and
        size information that is required in many NDIS 6.0 structures.

        typedef struct _NDIS_OBJECT_HEADER {
          UCHAR  Type;
          UCHAR  Revision;
          USHORT Size;
        } NDIS_OBJECT_HEADER, *PNDIS_OBJECT_HEADER;
    """
    _fields_ = [("Type", c_char),
                ("Revision", c_char),
                ("Size", c_ushort)]

class DOT11_BSSID_LIST(Structure):
    """
        The DOT11_BSSID_LIST structure contains a list of basic service set
        (BSS) identifiers.

        typedef struct _DOT11_BSSID_LIST {
          NDIS_OBJECT_HEADER Header;
          ULONG              uNumOfEntries;
          ULONG              uTotalNumOfEntries;
          DOT11_MAC_ADDRESS  BSSIDs[1];
        } DOT11_BSSID_LIST, *PDOT11_BSSID_LIST;
    """
    #NOTE: Would benefit from dynamic instantiation to mod # of BSSIDs
    _fields_ = [("Header", NDIS_OBJECT_HEADER),
                ("uNumOfEntries", c_ulong),
                ("uTotalNumOfEntries", c_ulong),
                ("BSSIDs", DOT11_MAC_ADDRESS * 1)]

class WLAN_CONNECTION_PARAMETERS(Structure):
    """
        The WLAN_CONNECTION_PARAMETERS structure specifies the parameters used
        when using the WlanConnect function.

        typedef struct _WLAN_CONNECTION_PARAMETERS {
          WLAN_CONNECTION_MODE wlanConnectionMode;
          LPCWSTR              strProfile;
          PDOT11_SSID          pDot11Ssid;
          PDOT11_BSSID_LIST    pDesiredBssidList;
          DOT11_BSS_TYPE       dot11BssType;
          DWORD                dwFlags;
        } WLAN_CONNECTION_PARAMETERS, *PWLAN_CONNECTION_PARAMETERS;
    """
    """
        Re strProfile:
        If wlanConnectionMode is set to wlan_connection_mode_profile, then
        strProfile specifies the name of the profile used for the connection.
        If wlanConnectionMode is set to wlan_connection_mode_temporary_profile,
        then strProfile specifies the XML representation of the profile used for
        the connection. If wlanConnectionMode is set to
        wlan_connection_mode_discovery_secure or wlan_connection_mode_discovery_unsecure,
        then strProfile should be set to NULL.

        NOTE: For now, only profile names will be accepted, per strProfileName
        elsewhere.
    """
    _fields_ = [("wlanConnectionMode", WLAN_CONNECTION_MODE),
                ("strProfile", LPCWSTR),
                ("pDot11_ssid", POINTER(DOT11_SSID)),
                ("pDesiredBssidList", POINTER(DOT11_BSSID_LIST)),
                ("dot11BssType", DOT11_BSS_TYPE),
                ("dwFlags", DWORD)]

def WlanConnect(hClientHandle, pInterfaceGuid, pConnectionParameters):
    """
    The WlanConnect function attempts to connect to a specific network.

    DWORD WINAPI WlanConnect(
            _In_        HANDLE hClientHandle,
            _In_        const GUID *pInterfaceGuid,
            _In_        const PWLAN_CONNECTION_PARAMETERS pConnectionParameters,
            _Reserved_  PVOID pReserved
    );
    """
    func_ref = wlanapi.WlanConnect
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         POINTER(WLAN_CONNECTION_PARAMETERS),
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      pointer(pInterfaceGuid),
                      pointer(pConnectionParameters),
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("".join(["WlanConnect failed with error ", str(result)]))
    return result

def WlanDisconnect(hClientHandle, pInterfaceGuid):
    """
        The WlanDisconnect function disconnects an interface from its current network.

        DWORD WINAPI WlanDisconnect(
            _In_             HANDLE hClientHandle,
            _In_       const GUID   *pInterfaceGuid,
            _Reserved_       PVOID  pReserved
        );
    """
    func_ref = wlanapi.WlanDisconnect
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         c_void_p]
    func_ref.restype = DWORD
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      None)
    if result != ERROR_SUCCESS:
        raise Exception("WlanDisconnect failed.")
    return result

class WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS(Structure):
    """
        The WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS structure contains information about
        the connection settings on the wireless Hosted Network.
        
        typedef struct _WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS {
            DOT11_SSID hostedNetworkSSID;
            DWORD      dwMaxNumberOfPeers;
        } WLAN_HOSTED_NETWORK_CONNECTION_SETTINGS, *PWLAN_HOSTED_NETWORK_CONNECTION_SETTINGS;    
    """

    _fields_ = [("hostedNetworkSSID", DOT11_SSID),
                ("dwMaxNumberOfPeers", DWORD)]

WLAN_INTF_OPCODE = c_uint
WLAN_INTF_OPCODE_DICT = {
    0x000000000: "wlan_intf_opcode_autoconf_start",
    1: "wlan_intf_opcode_autoconf_enabled",
    2: "wlan_intf_opcode_background_scan_enabled",
    3: "wlan_intf_opcode_media_streaming_mode",
    4: "wlan_intf_opcode_radio_state",
    5: "wlan_intf_opcode_bss_type",
    6: "wlan_intf_opcode_interface_state",
    7: "wlan_intf_opcode_current_connection",
    8: "wlan_intf_opcode_channel_number",
    9: "wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs",
    10: "wlan_intf_opcode_supported_adhoc_auth_cipher_pairs",
    11: "wlan_intf_opcode_supported_country_or_region_string_list",
    12: "wlan_intf_opcode_current_operation_mode",
    13: "wlan_intf_opcode_supported_safe_mode",
    14: "wlan_intf_opcode_certified_safe_mode",
    15: "wlan_intf_opcode_hosted_network_capable",
    16: "wlan_intf_opcode_management_frame_protection_capable",
    0x0fffffff: "wlan_intf_opcode_autoconf_end",
    0x10000100: "wlan_intf_opcode_msm_start",
    17: "wlan_intf_opcode_statistics",
    18: "wlan_intf_opcode_rssi",
    0x1fffffff: "wlan_intf_opcode_msm_end",
    0x20010000: "wlan_intf_opcode_security_start",
    0x2fffffff: "wlan_intf_opcode_security_end",
    0x30000000: "wlan_intf_opcode_ihv_start",
    0x3fffffff: "wlan_intf_opcode_ihv_end"
}

WLAN_HOSTED_NETWORK_OPCODE = c_uint
WLAN_HOSTED_NETWORK_OPCODE_DICT = {
    0: "wlan_hosted_network_opcode_connection_settings",
    1: "wlan_hosted_network_opcode_security_settings",
    2: "wlan_hosted_network_opcode_station_profile",
    3: "wlan_hosted_network_opcode_enable"
    }

WLAN_OPCODE_VALUE_TYPE = c_uint
WLAN_OPCODE_VALUE_TYPE_DICT = {
    0: "wlan_opcode_value_type_query_only",
    1: "wlan_opcode_value_type_set_by_group_policy",
    2: "wlan_opcode_value_type_set_by_user",
    3: "wlan_opcode_value_type_invalid"
}

class WLAN_ASSOCIATION_ATTRIBUTES(Structure):
    """
        The WLAN_ASSOCIATION_ATTRIBUTES structure contains association attributes for a connection.

        typedef struct _WLAN_ASSOCIATION_ATTRIBUTES {
            DOT11_SSID          dot11Ssid;
            DOT11_BSS_TYPE      dot11BssType;
            DOT11_MAC_ADDRESS   dot11Bssid;
            DOT11_PHY_TYPE      dot11PhyType;
            ULONG               uDot11PhyIndex;
            WLAN_SIGNAL_QUALITY wlanSignalQuality;
            ULONG               ulRxRate;
            ULONG               ulTxRate;
        } WLAN_ASSOCIATION_ATTRIBUTES, *PWLAN_ASSOCIATION_ATTRIBUTES;
    """
    _fields_ = [("dot11Ssid", DOT11_SSID),
                ("dot11BssType", DOT11_BSS_TYPE),
                ("dot11Bssid", DOT11_MAC_ADDRESS),
                ("dot11PhyType", DOT11_PHY_TYPE),
                ("uDot11PhyIndex", c_ulong),
                ("wlanSignalQuality", WLAN_SIGNAL_QUALITY),
                ("ulRxRate", c_ulong),
                ("ulTxRate", c_ulong)]

class WLAN_SECURITY_ATTRIBUTES(Structure):
    """
        The WLAN_SECURITY_ATTRIBUTES structure defines the security attributes for a wireless connection.

        typedef struct _WLAN_SECURITY_ATTRIBUTES {
            BOOL                   bSecurityEnabled;
            BOOL                   bOneXEnabled;
            DOT11_AUTH_ALGORITHM   dot11AuthAlgorithm;
            DOT11_CIPHER_ALGORITHM dot11CipherAlgorithm;
        } WLAN_SECURITY_ATTRIBUTES, *PWLAN_SECURITY_ATTRIBUTES;
    """
    _fields_ = [("bSecurityEnabled", BOOL),
                ("bOneXEnabled", BOOL),
                ("dot11AuthAlgorithm", DOT11_AUTH_ALGORITHM_TYPE),
                ("dot11CipherAlgorithm", DOT11_CIPHER_ALGORITHM_TYPE)]

class WLAN_CONNECTION_ATTRIBUTES(Structure):
    """
        The WlanQueryInterface function queries various parameters of a
        specified interface.

        typedef struct _WLAN_CONNECTION_ATTRIBUTES {
          WLAN_INTERFACE_STATE        isState;
          WLAN_CONNECTION_MODE        wlanConnectionMode;
          WCHAR                       strProfileName[256];
          WLAN_ASSOCIATION_ATTRIBUTES wlanAssociationAttributes;
          WLAN_SECURITY_ATTRIBUTES    wlanSecurityAttributes;
        } WLAN_CONNECTION_ATTRIBUTES, *PWLAN_CONNECTION_ATTRIBUTES;
    """
    _fields_ = [("isState", WLAN_INTERFACE_STATE),
                ("wlanConnectionMode", WLAN_CONNECTION_MODE),
                ("strProfileName", c_wchar * 256),
                ("wlanAssociationAttributes", WLAN_ASSOCIATION_ATTRIBUTES),
                ("wlanSecurityAttributes", WLAN_SECURITY_ATTRIBUTES)]

WLAN_INTF_OPCODE_TYPE_DICT = {
    "wlan_intf_opcode_autoconf_enabled": c_bool,
    "wlan_intf_opcode_background_scan_enabled": c_bool,
    "wlan_intf_opcode_radio_state": WLAN_RADIO_STATE,
    "wlan_intf_opcode_bss_type": DOT11_BSS_TYPE,
    "wlan_intf_opcode_interface_state": WLAN_INTERFACE_STATE,
    "wlan_intf_opcode_current_connection": WLAN_CONNECTION_ATTRIBUTES,
    "wlan_intf_opcode_channel_number": c_ulong,
    #"wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs": \
            #WLAN_AUTH_CIPHER_PAIR_LIST,
    #"wlan_intf_opcode_supported_adhoc_auth_cipher_pairs": \
            #WLAN_AUTH_CIPHER_PAIR_LIST,
    #"wlan_intf_opcode_supported_country_or_region_string_list": \
            #WLAN_COUNTRY_OR_REGION_STRING_LIST,
    "wlan_intf_opcode_media_streaming_mode": c_bool,
    #"wlan_intf_opcode_statistics": WLAN_STATISTICS,
    "wlan_intf_opcode_rssi": c_long,
    "wlan_intf_opcode_current_operation_mode": c_ulong,
    "wlan_intf_opcode_supported_safe_mode": c_bool,
    "wlan_intf_opcode_certified_safe_mode": c_bool
}

def WlanQueryInterface(hClientHandle, pInterfaceGuid, OpCode):
    """
        The WlanQueryInterface function queries various parameters of a specified interface.

        DWORD WINAPI WlanQueryInterface(
          _In_        HANDLE hClientHandle,
          _In_        const GUID *pInterfaceGuid,
          _In_        WLAN_INTF_OPCODE OpCode,
          _Reserved_  PVOID pReserved,
          _Out_       PDWORD pdwDataSize,
          _Out_       PVOID *ppData,
          _Out_opt_   PWLAN_OPCODE_VALUE_TYPE pWlanOpcodeValueType
        );
    """
    func_ref = wlanapi.WlanQueryInterface
    #TODO: Next two lines sketchy due to incomplete implementation.
    opcode_name = WLAN_INTF_OPCODE_DICT[OpCode.value]
    return_type = WLAN_INTF_OPCODE_TYPE_DICT[opcode_name]
    func_ref.argtypes = [HANDLE,
                         POINTER(GUID),
                         WLAN_INTF_OPCODE,
                         c_void_p,
                         POINTER(DWORD),
                         POINTER(POINTER(return_type)),
                         POINTER(WLAN_OPCODE_VALUE_TYPE)]
    func_ref.restype = DWORD
    pdwDataSize = DWORD()
    ppData = pointer(return_type())
    pWlanOpcodeValueType = WLAN_OPCODE_VALUE_TYPE()
    result = func_ref(hClientHandle,
                      byref(pInterfaceGuid),
                      OpCode,
                      None,
                      pdwDataSize,
                      ppData,
                      pWlanOpcodeValueType)
    if result != ERROR_SUCCESS:
        raise Exception("WlanQueryInterface failed.")
    return ppData


EVT_HANDLE = HANDLE

def EvtQuery(query):
    """
        Runs a query to retrieve events from a channel or log file that match the specified query criteria.

        EVT_HANDLE WINAPI EvtQuery(
            _In_ EVT_HANDLE Session,
            _In_ LPCWSTR    Path,
            _In_ LPCWSTR    Query,
            _In_ DWORD      Flags
        );
    """
    session = None
    path = "Microsoft-Windows-WLAN-AutoConfig/Operational"
    flags = 512
    #flags = "EvtQueryChannelPath | EvtQueryReverseDirection"
    func_ref = logapi.EvtQuery
    func_ref.argtypes = [EVT_HANDLE,
                         LPCWSTR,
                         LPCWSTR,
                         DWORD]
    func_ref.restype = EVT_HANDLE
    result = func_ref(session,
                      path,
                      query,
                      flags)
    if result == None:
        raise Exception("EvtQuery failed.")
    return result

def EvtRender(fragment, bufferSize, renderedContent, bufferUsed, propertyCount):
    """
        Renders an XML fragment based on the rendering context that you specify.

        BOOL WINAPI EvtRender(
            _In_  EVT_HANDLE Context,
            _In_  EVT_HANDLE Fragment,
            _In_  DWORD      Flags,
            _In_  DWORD      BufferSize,
            _In_  PVOID      Buffer,
            _Out_ PDWORD     BufferUsed,
            _Out_ PDWORD     PropertyCount
        );
    """
    context = None
    EvtRenderEventXml = 1
    flags = EvtRenderEventXml
    func_ref = logapi.EvtRender
    func_ref.argtypes = [EVT_HANDLE,
                         EVT_HANDLE,
                         DWORD,
                         DWORD,
                         c_void_p,
                         POINTER(DWORD),
                         POINTER(DWORD)]
    func_ref.restype = BOOL
    result = func_ref(context,
                      fragment,
                      flags,
                      bufferSize,
                      renderedContent,
                      byref(bufferUsed),
                      byref(propertyCount))
    if result == "False":
        raise Exception("EvtRender failed.")
    return result

ARRAY_SIZE = 10

def EvtNext(resultSet, eventArraySize, eventArray, timeout, returned):
    """
        Gets the next event from the query or subscription results.

        BOOL WINAPI EvtNext(
            _In_  EVT_HANDLE  ResultSet,
            _In_  DWORD       EventArraySize,
            _In_  EVT_HANDLE* EventArray,
            _In_  DWORD       Timeout,
            _In_  DWORD       Flags,
            _Out_ PDWORD      Returned
        );
    """
    flags = 0
    func_ref = logapi.EvtNext
    func_ref.argtypes = [EVT_HANDLE,
                         DWORD,
                         POINTER(EVT_HANDLE * ARRAY_SIZE),
                         DWORD,
                         DWORD,
                         POINTER(DWORD)]
    cast(eventArray, POINTER(c_ulong))
    func_ref.restype = BOOL
    result = func_ref(resultSet,
                      eventArraySize,
                      eventArray,
                      timeout,
                      flags,
                      byref(returned))
    #if result == False:
    #    raise Exception("EvtNext failed.")
    return result

def EvtClose(evtObject):
    """
        Closes an open handle.

        BOOL WINAPI EvtClose(
            _In_ EVT_HANDLE Object
        );
    """
    func_ref = logapi.EvtClose
    func_ref.argtypes = [EVT_HANDLE]
    func_ref.restype = BOOL
    result = func_ref(evtObject)
    if result == "NULL":
        raise Exception("EvtClose failed.")
    return result

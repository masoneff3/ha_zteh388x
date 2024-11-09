# ZTE H388X (TIM HUB+) Custom Component for Home Assistant

A [Home Assistant](https://www.home-assistant.io/) (HA) custom component for the ZTE H388X (TIM HUB+) router.

![Alt text](img/example_dashboard.png?raw=true "Example dashboard")

## Features

- **Supports both xDSL (ADSL/VDSL) and FTTH (SFP/Ethernet) connections**.
- Retrieves details including:
  - Connection status (connected/disconnected)
  - Line statistics (downstream/upstream rates, SNR margin, attenuation, profile, CRC/FEC errors, TX/RX power, etc.)
  - Connection uptime
  - Bytes and packets received/sent
  - WAN IP address and DNS servers
  - MAC addresses
  - And more...

<details>
  <summary>See the full list of entities</summary>

  ```
	- zteh388x_dsl_atuc_fec_errors
	- zteh388x_dsl_currentprofile
	- zteh388x_dsl_data_path
	- zteh388x_dsl_downcrc_errors
	- zteh388x_dsl_downinterleavedelay
	- zteh388x_dsl_downinterleavedepth
	- zteh388x_dsl_downstream_attenuation
	- zteh388x_dsl_downstream_current_rate
	- zteh388x_dsl_downstream_max_rate
	- zteh388x_dsl_downstream_noise_margin
	- zteh388x_dsl_downstream_power
	- zteh388x_dsl_downstreaminp
	- zteh388x_dsl_enable
	- zteh388x_dsl_fec_errors
	- zteh388x_dsl_link_retrain
	- zteh388x_dsl_module_type
	- zteh388x_dsl_showtime_start
	- zteh388x_dsl_status
	- zteh388x_dsl_tlinkencapsulationused
	- zteh388x_dsl_upcrc_errors
	- zteh388x_dsl_upinterleavedelay
	- zteh388x_dsl_upinterleavedepth
	- zteh388x_dsl_upstream_attenuation
	- zteh388x_dsl_upstream_current_rate
	- zteh388x_dsl_upstream_max_rate
	- zteh388x_dsl_upstream_noise_margin
	- zteh388x_dsl_upstream_power
	- zteh388x_dsl_upstreaminp
	- zteh388x_ethernet_bytesreceived
	- zteh388x_ethernet_bytessent
	- zteh388x_ethernet_if_errorid
	- zteh388x_ethernet_lastchange
	- zteh388x_ethernet_linkduplex
	- zteh388x_ethernet_linkspeed
	- zteh388x_ethernet_macaddress
	- zteh388x_ethernet_packetsreceived
	- zteh388x_ethernet_packetssent
	- zteh388x_ethernet_singlerxstrength
	- zteh388x_ethernet_singlestatus
	- zteh388x_ethernet_singletxstrength
	- zteh388x_ethernet_status
	- zteh388x_internet_ad_atmencapsulation
	- zteh388x_internet_ad_atmqos
	- zteh388x_internet_ad_authtype
	- zteh388x_internet_ad_connerror
	- zteh388x_internet_ad_connstatus
	- zteh388x_internet_ad_connstatus6
	- zteh388x_internet_ad_conntrigger
	- zteh388x_internet_ad_destaddress
	- zteh388x_internet_ad_dns1
	- zteh388x_internet_ad_dns2
	- zteh388x_internet_ad_dns3
	- zteh388x_internet_ad_enablepassthrough
	- zteh388x_internet_ad_gateway
	- zteh388x_internet_ad_ipaddress
	- zteh388x_internet_ad_ipmode
	- zteh388x_internet_ad_isnat
	- zteh388x_internet_ad_linkmode
	- zteh388x_internet_ad_mode
	- zteh388x_internet_ad_mtu
	- zteh388x_internet_ad_pagetype
	- zteh388x_internet_ad_strservlist
	- zteh388x_internet_ad_sub_destaddress0
	- zteh388x_internet_ad_sub_destaddress1
	- zteh388x_internet_ad_subnetmask
	- zteh388x_internet_ad_transtype
	- zteh388x_internet_ad_uplink
	- zteh388x_internet_ad_uptime
	- zteh388x_internet_ad_username
	- zteh388x_internet_ad_vlanenable
	- zteh388x_internet_ad_wancname
	- zteh388x_internet_ad_wantype
	- zteh388x_internet_ad_workifmac
	- zteh388x_internet_ad_xdslmode
	- zteh388x_internet_eth_authtype
	- zteh388x_internet_eth_connerror
	- zteh388x_internet_eth_connstatus
	- zteh388x_internet_eth_connstatus6
	- zteh388x_internet_eth_conntrigger
	- zteh388x_internet_eth_dns1
	- zteh388x_internet_eth_dns2
	- zteh388x_internet_eth_dns3
	- zteh388x_internet_eth_enablepassthrough
	- zteh388x_internet_eth_gateway
	- zteh388x_internet_eth_ipaddress
	- zteh388x_internet_eth_ipmode
	- zteh388x_internet_eth_isnat
	- zteh388x_internet_eth_linkmode
	- zteh388x_internet_eth_mode
	- zteh388x_internet_eth_mtu
	- zteh388x_internet_eth_pagetype
	- zteh388x_internet_eth_priority
	- zteh388x_internet_eth_strservlist
	- zteh388x_internet_eth_subnetmask
	- zteh388x_internet_eth_transtype
	- zteh388x_internet_eth_uplink
	- zteh388x_internet_eth_uptime
	- zteh388x_internet_eth_username
	- zteh388x_internet_eth_vlanenable
	- zteh388x_internet_eth_vlanid
	- zteh388x_internet_eth_wancname
	- zteh388x_internet_eth_wantype
	- zteh388x_internet_eth_workifmac
	- zteh388x_internet_eth_xdslmode
	- zteh388x_internet_fwa_addressingtype
	- zteh388x_internet_fwa_connerror
	- zteh388x_internet_fwa_connstatus
	- zteh388x_internet_fwa_dns1
	- zteh388x_internet_fwa_dns2
	- zteh388x_internet_fwa_dns3
	- zteh388x_internet_fwa_gateway
	- zteh388x_internet_fwa_ipaddress
	- zteh388x_internet_fwa_ipmode
	- zteh388x_internet_fwa_isnat
	- zteh388x_internet_fwa_linkmode
	- zteh388x_internet_fwa_mode
	- zteh388x_internet_fwa_mtu
	- zteh388x_internet_fwa_pagetype
	- zteh388x_internet_fwa_priority
	- zteh388x_internet_fwa_remainleasetime
	- zteh388x_internet_fwa_strservlist
	- zteh388x_internet_fwa_subnetmask
	- zteh388x_internet_fwa_uplink
	- zteh388x_internet_fwa_uptime
	- zteh388x_internet_fwa_vlanenable
	- zteh388x_internet_fwa_vlanid
	- zteh388x_internet_fwa_wancname
	- zteh388x_internet_fwa_wantype
	- zteh388x_internet_fwa_workifmac
	- zteh388x_internet_fwa_xdslmode
	- zteh388x_internet_vd_authtype
	- zteh388x_internet_vd_connerror
	- zteh388x_internet_vd_connstatus
	- zteh388x_internet_vd_connstatus6
	- zteh388x_internet_vd_conntrigger
	- zteh388x_internet_vd_dns1
	- zteh388x_internet_vd_dns2
	- zteh388x_internet_vd_dns3
	- zteh388x_internet_vd_enablepassthrough
	- zteh388x_internet_vd_gateway
	- zteh388x_internet_vd_ipaddress
	- zteh388x_internet_vd_ipmode
	- zteh388x_internet_vd_isnat
	- zteh388x_internet_vd_linkmode
	- zteh388x_internet_vd_mode
	- zteh388x_internet_vd_mtu
	- zteh388x_internet_vd_pagetype
	- zteh388x_internet_vd_priority
	- zteh388x_internet_vd_strservlist
	- zteh388x_internet_vd_subnetmask
	- zteh388x_internet_vd_transtype
	- zteh388x_internet_vd_uplink
	- zteh388x_internet_vd_uptime
	- zteh388x_internet_vd_username
	- zteh388x_internet_vd_vlanenable
	- zteh388x_internet_vd_vlanid
	- zteh388x_internet_vd_wancname
	- zteh388x_internet_vd_wantype
	- zteh388x_internet_vd_workifmac
	- zteh388x_internet_vd_xdslmode
	- zteh388x_iptv_ad_addressingtype
	- zteh388x_iptv_ad_atmencapsulation
	- zteh388x_iptv_ad_atmqos
	- zteh388x_iptv_ad_connerror
	- zteh388x_iptv_ad_connstatus
	- zteh388x_iptv_ad_destaddress
	- zteh388x_iptv_ad_dns1
	- zteh388x_iptv_ad_dns2
	- zteh388x_iptv_ad_dns3
	- zteh388x_iptv_ad_gateway
	- zteh388x_iptv_ad_ipaddress
	- zteh388x_iptv_ad_ipmode
	- zteh388x_iptv_ad_isnat
	- zteh388x_iptv_ad_linkmode
	- zteh388x_iptv_ad_mode
	- zteh388x_iptv_ad_mtu
	- zteh388x_iptv_ad_pagetype
	- zteh388x_iptv_ad_remainleasetime
	- zteh388x_iptv_ad_strservlist
	- zteh388x_iptv_ad_sub_destaddress0
	- zteh388x_iptv_ad_sub_destaddress1
	- zteh388x_iptv_ad_subnetmask
	- zteh388x_iptv_ad_uplink
	- zteh388x_iptv_ad_uptime
	- zteh388x_iptv_ad_vlanenable
	- zteh388x_iptv_ad_wancname
	- zteh388x_iptv_ad_wantype
	- zteh388x_iptv_ad_workifmac
	- zteh388x_iptv_ad_xdslmode
	- zteh388x_iptv_eth_addressingtype
	- zteh388x_iptv_eth_connerror
	- zteh388x_iptv_eth_connstatus
	- zteh388x_iptv_eth_dns1
	- zteh388x_iptv_eth_dns2
	- zteh388x_iptv_eth_dns3
	- zteh388x_iptv_eth_gateway
	- zteh388x_iptv_eth_ipaddress
	- zteh388x_iptv_eth_ipmode
	- zteh388x_iptv_eth_isnat
	- zteh388x_iptv_eth_linkmode
	- zteh388x_iptv_eth_mode
	- zteh388x_iptv_eth_mtu
	- zteh388x_iptv_eth_pagetype
	- zteh388x_iptv_eth_priority
	- zteh388x_iptv_eth_remainleasetime
	- zteh388x_iptv_eth_strservlist
	- zteh388x_iptv_eth_subnetmask
	- zteh388x_iptv_eth_uplink
	- zteh388x_iptv_eth_uptime
	- zteh388x_iptv_eth_vlanenable
	- zteh388x_iptv_eth_vlanid
	- zteh388x_iptv_eth_wancname
	- zteh388x_iptv_eth_wantype
	- zteh388x_iptv_eth_workifmac
	- zteh388x_iptv_eth_xdslmode
	- zteh388x_iptv_vd_addressingtype
	- zteh388x_iptv_vd_connerror
	- zteh388x_iptv_vd_connstatus
	- zteh388x_iptv_vd_dns1
	- zteh388x_iptv_vd_dns2
	- zteh388x_iptv_vd_dns3
	- zteh388x_iptv_vd_gateway
	- zteh388x_iptv_vd_ipaddress
	- zteh388x_iptv_vd_ipmode
	- zteh388x_iptv_vd_isnat
	- zteh388x_iptv_vd_linkmode
	- zteh388x_iptv_vd_mode
	- zteh388x_iptv_vd_mtu
	- zteh388x_iptv_vd_pagetype
	- zteh388x_iptv_vd_priority
	- zteh388x_iptv_vd_remainleasetime
	- zteh388x_iptv_vd_strservlist
	- zteh388x_iptv_vd_subnetmask
	- zteh388x_iptv_vd_uplink
	- zteh388x_iptv_vd_uptime
	- zteh388x_iptv_vd_vlanenable
	- zteh388x_iptv_vd_vlanid
	- zteh388x_iptv_vd_wancname
	- zteh388x_iptv_vd_wantype
	- zteh388x_iptv_vd_workifmac
	- zteh388x_iptv_vd_xdslmode
	- zteh388x_sfp_bytesreceived
	- zteh388x_sfp_bytessent
	- zteh388x_sfp_if_errorid
	- zteh388x_sfp_lastchange
	- zteh388x_sfp_linkduplex
	- zteh388x_sfp_linkspeed
	- zteh388x_sfp_macaddress
	- zteh388x_sfp_packetsreceived
	- zteh388x_sfp_packetssent
	- zteh388x_sfp_singlerxstrength
	- zteh388x_sfp_singlestatus
	- zteh388x_sfp_singletxstrength
	- zteh388x_sfp_status
	- zteh388x_voip_fwa_addressingtype
	- zteh388x_voip_fwa_connerror
	- zteh388x_voip_fwa_connstatus
	- zteh388x_voip_fwa_dns1
	- zteh388x_voip_fwa_dns2
	- zteh388x_voip_fwa_dns3
	- zteh388x_voip_fwa_gateway
	- zteh388x_voip_fwa_ipaddress
	- zteh388x_voip_fwa_ipmode
	- zteh388x_voip_fwa_isnat
	- zteh388x_voip_fwa_linkmode
	- zteh388x_voip_fwa_mode
	- zteh388x_voip_fwa_mtu
	- zteh388x_voip_fwa_pagetype
	- zteh388x_voip_fwa_priority
	- zteh388x_voip_fwa_remainleasetime
	- zteh388x_voip_fwa_strservlist
	- zteh388x_voip_fwa_subnetmask
	- zteh388x_voip_fwa_uplink
	- zteh388x_voip_fwa_uptime
	- zteh388x_voip_fwa_vlanenable
	- zteh388x_voip_fwa_vlanid
	- zteh388x_voip_fwa_wancname
	- zteh388x_voip_fwa_wantype
	- zteh388x_voip_fwa_workifmac
	- zteh388x_voip_fwa_xdslmode
  ```
</details>

## Installation and configuration

1. Download the `custom_components/zteh388x` folder in this repository.
2. Copy the `zteh388x` directory to your Home Assistant `/config/custom_components` directory (create this directory if it does not exist).
   Your configuration should look like this:
	```
	  config
	  └── custom_components
	      └── zteh388x
	          └── __init__.py
	          └── manifest.json
	          └── sensor.py
	          └── transform.py
	          └── interface_mapping.conf
	```
3. In your configuration file (e.g., `configuration.yaml`) add the following sensor and replace the default values (`host, username, password, linetype, interval`):
	```
	sensor:
	  - platform: zteh388x
	    host: 192.168.1.1       # Replace with your router's IP address
	    username: admin         # Replace with your router's username
	    password: password	    # Replace with your router's password
	    linetype: eth           # Use 'eth' for SFP or Ethernet (i.e., external ONT); use 'dsl' for xDSL (ADSL or VDSL)
	    interval: 300           # Sensors update interval in seconds; default is 120 seconds
	```
4. Restart Home Assistant.

> [!TIP]
> To store your password, consider using the `secrets.yaml` file instead. Replace the *password* line with:\
```password: !secret zteh388x```\
Then, in `secrets.yaml`, add the following:\
```zteh388x: password # Replace with your router's password```

> [!NOTE]
> If you're using an xDSL (ADSL or VDSL) connection, set `linetype: dsl`; for a fiber (FTTH) connection using an SFP module or external ONT, set `linetype: eth`.
> 
> To avoid overloading the router with requests, use an interval of 30 seconds or more.

> [!IMPORTANT]
> Because the router allows only one admin account (*admin*), this custom component will terminate any active sessions on the router's management page each time the sensors are refreshed. In case you need to access the management page (e.g., from your computer), either disable the custom component or set a longer update interval.

> [!NOTE]
> The router’s 32-bit integer limit causes counters to reset after reaching 2^32 bytes. This affects the *bytesreceived* and *bytessent* sensors (available for SFP or Ethernet connections only), which reset approximately every 4 GB.\
> To mitigate this behavior, the custom component detects the reset and calculates the cumulative value instead. If you restart your Home Assistant instance, the counter will reset by picking the current value available from the router.

### (Optional) Interface friendly names

By default, entities will have names like `zteh388x_igd.wd2.wcd1.wcppp1_uptime`, as these are the names provided by the router's APIs. Here, `wdX` represents the interface (e.g., DSL, SFP, Ethernet), while `wcd1.wcppp1` corresponds to the `INTERNET_ETH` section in the router's GUI. The following mapping has been defined, however please note that in your case it might be different.

| **ID** | **Friendly name** |
|:------:|:-----------------:|
|   WD3  |        SFP        |
|   WD2  |        ETH        |
|   WD1  |        DSL        |

The integration maps these names to the same friendly name appearing in the router's GUI, as shown in the following table:

| **Line type** |  **Category**  |         **ID**        | **Friendly name (GUI)** |
|:-------------:|:--------------:|:---------------------:|:-----------------------:|
| SFP/Ethernet  | Line stats     | _IGD.WD3.ETH5_        | _SFP_                   |
| SFP/Ethernet  | Line stats     | _IGD.WD2.ETH1_        | _ETHERNET_              |
| SFP/Ethernet  | Internet stats | _IGD.WD2.WCD1.WCIP1_  | _INTERNET_FWA_          |
| SFP/Ethernet  | Internet stats | _IGD.WD2.WCD1.WCIP2_  | _VOIP_FWA_              |
| SFP/Ethernet  | Internet stats | _IGD.WD2.WCD1.WCIP3_  | _IPTV_ETH_              |
| SFP/Ethernet  | Internet stats | _IGD.WD2.WCD1.WCPPP1_ | _INTERNET_ETH_          |
| DSL           | Line stats     | _IGD.WD1.LINE0_       | _DSL_                   |
| DSL           | Internet stats | _IGD.WD1.WCD1.WCIP1_  | _IPTV_VD_               |
| DSL           | Internet stats | _IGD.WD1.WCD3.WCIP1_  | _IPTV_AD_               |
| DSL           | Internet stats | _IGD.WD1.WCD1.WCPPP1_ | _INTERNET_VD_           |
| DSL           | Internet stats | _IGD.WD1.WCD2.WCPPP1_ | _INTERNET_AD_           |

To disable mappings and revert to default interface names, edit `interface_mapping.conf` inside the `custom_components/zteh388x` directory by commenting out (#) all the lines.\
You can also change the exiting mapping or add any new mappings by following the format described in the file.\
If needed, you can retrieve the default interface name by inspecting the router’s administrator page, as shown in this example:\
![Alt text](img/inspectpage.jpg?raw=true "Inspect page")

### (Optional) Debug

The custom component will only log certain errors. For troubleshooting purposes, you can enable debug-level logging.\
This will also include the raw XML output from API responses and may significantly increase log size, so enable it only when necessary.\
In order to enable debug-level logging, add the following section to your configuration file (e.g., `configuration.yaml`):

```
logger:
  default: warning
  logs:
    custom_components.zteh388x: debug
```

## Tested on

- Home Assistant (Container) 2024.9.x - 2024.11.x
- ZTE H388X - HW: V10.0.0 SW: AGZHP_1.4.0

## Possible improvements

- Convert the script to asynchronous, per Home Assistant best practices
- Test SFP and DSL connections
- ...

## Disclaimer

This software is provided "as-is", without any express or implied warranties. The author is not liable for any damages, legal or regulatory violations resulting from your use of the software.\
You use this software at your own risk.\
The author is under no obligation to provide maintenance, support, updates, or modifications to the software.\
"TIM" and "ZTE", along with their logos, are the property of their respective owners and are used for illustrative purposes only. Their use does not imply any affiliation with or endorsement by these companies.

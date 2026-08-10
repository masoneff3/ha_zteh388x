# ZTE H388X (TIM HUB+) Custom Component for Home Assistant

A [Home Assistant](https://www.home-assistant.io/) (HA) custom component for the ZTE H388X (TIM HUB+) router.

<p align="center">
  <img src="img/device.png?raw=true" alt="Device" height="290">
  <img src="img/example_dashboard.png?raw=true" alt="Example dashboard" height="290">
</p>

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
- **[V2.0]** **Device tracking** for Wi-Fi clients (see [Device tracker](#device-tracker-wi-fi-clients))
- **[V2.0]** **Supports multiple routers** (see [Multiple routers](#optional-multiple-routers))

<details>
  <summary>See the full list of entities</summary>

  The entity prefix is omitted for brevity.

  ```
	- dsl_atuc_fec_errors
	- dsl_currentprofile
	- dsl_data_path
	- dsl_downcrc_errors
	- dsl_downinterleavedelay
	- dsl_downinterleavedepth
	- dsl_downstream_attenuation
	- dsl_downstream_current_rate
	- dsl_downstream_max_rate
	- dsl_downstream_noise_margin
	- dsl_downstream_power
	- dsl_downstreaminp
	- dsl_enable
	- dsl_fec_errors
	- dsl_link_retrain
	- dsl_module_type
	- dsl_showtime_start
	- dsl_status
	- dsl_tlinkencapsulationused
	- dsl_upcrc_errors
	- dsl_upinterleavedelay
	- dsl_upinterleavedepth
	- dsl_upstream_attenuation
	- dsl_upstream_current_rate
	- dsl_upstream_max_rate
	- dsl_upstream_noise_margin
	- dsl_upstream_power
	- dsl_upstreaminp
	- ethernet_bytesreceived
	- ethernet_bytessent
	- ethernet_if_errorid
	- ethernet_lastchange
	- ethernet_linkduplex
	- ethernet_linkspeed
	- ethernet_macaddress
	- ethernet_packetsreceived
	- ethernet_packetssent
	- ethernet_singlerxstrength
	- ethernet_singlestatus
	- ethernet_singletxstrength
	- ethernet_status
	- internet_ad_atmencapsulation
	- internet_ad_atmqos
	- internet_ad_authtype
	- internet_ad_connerror
	- internet_ad_connstatus
	- internet_ad_connstatus6
	- internet_ad_conntrigger
	- internet_ad_destaddress
	- internet_ad_dns1
	- internet_ad_dns2
	- internet_ad_dns3
	- internet_ad_enablepassthrough
	- internet_ad_gateway
	- internet_ad_ipaddress
	- internet_ad_ipmode
	- internet_ad_isnat
	- internet_ad_linkmode
	- internet_ad_mode
	- internet_ad_mtu
	- internet_ad_pagetype
	- internet_ad_strservlist
	- internet_ad_sub_destaddress0
	- internet_ad_sub_destaddress1
	- internet_ad_subnetmask
	- internet_ad_transtype
	- internet_ad_uplink
	- internet_ad_uptime
	- internet_ad_uptime_days
	- internet_ad_username
	- internet_ad_vlanenable
	- internet_ad_wancname
	- internet_ad_wantype
	- internet_ad_workifmac
	- internet_ad_xdslmode
	- internet_eth_authtype
	- internet_eth_connerror
	- internet_eth_connstatus
	- internet_eth_connstatus6
	- internet_eth_conntrigger
	- internet_eth_dns1
	- internet_eth_dns2
	- internet_eth_dns3
	- internet_eth_enablepassthrough
	- internet_eth_gateway
	- internet_eth_ipaddress
	- internet_eth_ipmode
	- internet_eth_isnat
	- internet_eth_linkmode
	- internet_eth_mode
	- internet_eth_mtu
	- internet_eth_pagetype
	- internet_eth_priority
	- internet_eth_strservlist
	- internet_eth_subnetmask
	- internet_eth_transtype
	- internet_eth_uplink
	- internet_eth_uptime
	- internet_eth_uptime_days
	- internet_eth_username
	- internet_eth_vlanenable
	- internet_eth_vlanid
	- internet_eth_wancname
	- internet_eth_wantype
	- internet_eth_workifmac
	- internet_eth_xdslmode
	- internet_fwa_addressingtype
	- internet_fwa_connerror
	- internet_fwa_connstatus
	- internet_fwa_dns1
	- internet_fwa_dns2
	- internet_fwa_dns3
	- internet_fwa_gateway
	- internet_fwa_ipaddress
	- internet_fwa_ipmode
	- internet_fwa_isnat
	- internet_fwa_linkmode
	- internet_fwa_mode
	- internet_fwa_mtu
	- internet_fwa_pagetype
	- internet_fwa_priority
	- internet_fwa_remainleasetime
	- internet_fwa_strservlist
	- internet_fwa_subnetmask
	- internet_fwa_uplink
	- internet_fwa_uptime
	- internet_fwa_uptime_days
	- internet_fwa_vlanenable
	- internet_fwa_vlanid
	- internet_fwa_wancname
	- internet_fwa_wantype
	- internet_fwa_workifmac
	- internet_fwa_xdslmode
	- internet_vd_authtype
	- internet_vd_connerror
	- internet_vd_connstatus
	- internet_vd_connstatus6
	- internet_vd_conntrigger
	- internet_vd_dns1
	- internet_vd_dns2
	- internet_vd_dns3
	- internet_vd_enablepassthrough
	- internet_vd_gateway
	- internet_vd_ipaddress
	- internet_vd_ipmode
	- internet_vd_isnat
	- internet_vd_linkmode
	- internet_vd_mode
	- internet_vd_mtu
	- internet_vd_pagetype
	- internet_vd_priority
	- internet_vd_strservlist
	- internet_vd_subnetmask
	- internet_vd_transtype
	- internet_vd_uplink
	- internet_vd_uptime
	- internet_vd_uptime_days
	- internet_vd_username
	- internet_vd_vlanenable
	- internet_vd_vlanid
	- internet_vd_wancname
	- internet_vd_wantype
	- internet_vd_workifmac
	- internet_vd_xdslmode
	- iptv_ad_addressingtype
	- iptv_ad_atmencapsulation
	- iptv_ad_atmqos
	- iptv_ad_connerror
	- iptv_ad_connstatus
	- iptv_ad_destaddress
	- iptv_ad_dns1
	- iptv_ad_dns2
	- iptv_ad_dns3
	- iptv_ad_gateway
	- iptv_ad_ipaddress
	- iptv_ad_ipmode
	- iptv_ad_isnat
	- iptv_ad_linkmode
	- iptv_ad_mode
	- iptv_ad_mtu
	- iptv_ad_pagetype
	- iptv_ad_remainleasetime
	- iptv_ad_strservlist
	- iptv_ad_sub_destaddress0
	- iptv_ad_sub_destaddress1
	- iptv_ad_subnetmask
	- iptv_ad_uplink
	- iptv_ad_uptime
	- iptv_ad_uptime_days
	- iptv_ad_vlanenable
	- iptv_ad_wancname
	- iptv_ad_wantype
	- iptv_ad_workifmac
	- iptv_ad_xdslmode
	- iptv_eth_addressingtype
	- iptv_eth_connerror
	- iptv_eth_connstatus
	- iptv_eth_dns1
	- iptv_eth_dns2
	- iptv_eth_dns3
	- iptv_eth_gateway
	- iptv_eth_ipaddress
	- iptv_eth_ipmode
	- iptv_eth_isnat
	- iptv_eth_linkmode
	- iptv_eth_mode
	- iptv_eth_mtu
	- iptv_eth_pagetype
	- iptv_eth_priority
	- iptv_eth_remainleasetime
	- iptv_eth_strservlist
	- iptv_eth_subnetmask
	- iptv_eth_uplink
	- iptv_eth_uptime
	- iptv_eth_uptime_days
	- iptv_eth_vlanenable
	- iptv_eth_vlanid
	- iptv_eth_wancname
	- iptv_eth_wantype
	- iptv_eth_workifmac
	- iptv_eth_xdslmode
	- iptv_vd_addressingtype
	- iptv_vd_connerror
	- iptv_vd_connstatus
	- iptv_vd_dns1
	- iptv_vd_dns2
	- iptv_vd_dns3
	- iptv_vd_gateway
	- iptv_vd_ipaddress
	- iptv_vd_ipmode
	- iptv_vd_isnat
	- iptv_vd_linkmode
	- iptv_vd_mode
	- iptv_vd_mtu
	- iptv_vd_pagetype
	- iptv_vd_priority
	- iptv_vd_remainleasetime
	- iptv_vd_strservlist
	- iptv_vd_subnetmask
	- iptv_vd_uplink
	- iptv_vd_uptime
	- iptv_vd_uptime_days
	- iptv_vd_vlanenable
	- iptv_vd_vlanid
	- iptv_vd_wancname
	- iptv_vd_wantype
	- iptv_vd_workifmac
	- iptv_vd_xdslmode
	- sfp_bytesreceived
	- sfp_bytessent
	- sfp_if_errorid
	- sfp_lastchange
	- sfp_linkduplex
	- sfp_linkspeed
	- sfp_macaddress
	- sfp_packetsreceived
	- sfp_packetssent
	- sfp_singlerxstrength
	- sfp_singlestatus
	- sfp_singletxstrength
	- sfp_status
	- voip_fwa_addressingtype
	- voip_fwa_connerror
	- voip_fwa_connstatus
	- voip_fwa_dns1
	- voip_fwa_dns2
	- voip_fwa_dns3
	- voip_fwa_gateway
	- voip_fwa_ipaddress
	- voip_fwa_ipmode
	- voip_fwa_isnat
	- voip_fwa_linkmode
	- voip_fwa_mode
	- voip_fwa_mtu
	- voip_fwa_pagetype
	- voip_fwa_priority
	- voip_fwa_remainleasetime
	- voip_fwa_strservlist
	- voip_fwa_subnetmask
	- voip_fwa_uplink
	- voip_fwa_uptime
	- voip_fwa_uptime_days
	- voip_fwa_vlanenable
	- voip_fwa_vlanid
	- voip_fwa_wancname
	- voip_fwa_wantype
	- voip_fwa_workifmac
	- voip_fwa_xdslmode
  ```
</details>

## Installation and configuration

1. Download the `custom_components/zteh388x` folder from this repository.
2. Copy the `zteh388x` directory to your Home Assistant `/config/custom_components` directory (create it if it does not exist).
   Your configuration should look like this:
	```
	  config
	  └── custom_components
	      └── zteh388x
	          └── __init__.py
	          └── config_flow.py
	          └── const.py
	          └── device_tracker.py
	          └── interface_mapping.conf
	          └── manifest.json
	          └── router.py
	          └── sensor.py
	          └── transform.py
	          └── translations
	              └── en.json
	```

	> Instead of steps 1-2, you can add this repository as a [HACS custom repository](https://www.hacs.xyz/docs/faq/custom_repositories/) and install it from there.
3. Restart Home Assistant.
4. Go to ***Settings → Devices & Services → Add Integration***, search for ***ZTE H388X (TIM HUB+)***, and fill in the form:
	- **Host**: your router's IP address
	- **Username**: your router's username (*admin*)
	- **Password**: your router's password
	- **Line type**: `eth` for FTTH (SFP or Ethernet, i.e., external ONT); `dsl` for xDSL (ADSL or VDSL)
	- **Name** (optional): a friendly name for the router
	- **Update interval** (optional): sensors update interval in seconds; default is 120 seconds. To avoid potential rate-limiting or lockouts, use an interval of 30 seconds or more.

> [!IMPORTANT]
> If you're upgrading from version 1.0 to 2.0, see [Breaking Changes](#breaking-changes-v20) in the changelog below.

### (Optional) Multiple routers

Repeat the ***Add Integration*** step above for each router. Each one shows up as its own device, named after the **Name** you gave it (or the host, if left blank).

### Device tracker (Wi-Fi clients)

The integration creates a `device_tracker` entity for every device currently connected to the router's Wi-Fi. Each tracked device is identified by its MAC address, and reports its hostname and a `home`/`not_home` state.

> [!IMPORTANT]
> Because the router allows only one admin account (*admin*), this custom component will terminate any active sessions on the router's management page each time the sensors are refreshed. In case you need to access the management page (e.g., from your computer), either disable the custom component or set a longer update interval.

> [!NOTE]
> The router's 32-bit integer limit causes counters to reset after reaching 2^32 bytes. This affects the *bytesreceived* and *bytessent* sensors (available for SFP or Ethernet connections only), which reset approximately every 4 GB.\
> To mitigate this behavior, the custom component detects the reset and calculates the cumulative value instead. If you restart your Home Assistant instance, the counter will reset to the current value reported by the router.

### (Optional) Interface friendly names

Entity IDs follow the pattern `zteh388x_<interface>_<parameter>`, e.g. `zteh388x_igd.wd2.wcd1.wcppp1_uptime`.

By default, the `<interface>` segment looks like `igd.wd2.wcd1.wcppp1`, as these are the names provided by the router's APIs. Here, `wdX` represents the interface (e.g., DSL, SFP, Ethernet), while `wcd1.wcppp1` corresponds to the `INTERNET_ETH` section in the router's GUI. The following mapping has been defined; however, please note that in your case it might be different.

| **ID** | **Friendly name** |
|:------:|:-----------------:|
|   WD3  |        SFP        |
|   WD2  |        ETH        |
|   WD1  |        DSL        |

The integration maps these names to the same friendly names appearing in the router's GUI, as shown in the following table:

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
You can also change the existing mapping or add any new mappings by following the format described in the file.\
If needed, you can retrieve the default interface name by inspecting the router's administrator page, as shown in this example:\
![Alt text](img/inspectpage.jpg?raw=true "Inspect page")

### (Optional) Debug

The custom component will only log certain errors. For troubleshooting purposes, you can enable debug-level logging.\
This will also include the raw XML output from API responses and may significantly increase log size, so enable it only when necessary.\
To enable debug-level logging, add the following section to your configuration file (e.g., `configuration.yaml`):

```
logger:
  default: warning
  logs:
    custom_components.zteh388x: debug
```

## Tested on

- Home Assistant (Container) 2024.9.x - 2026.7.x
- ZTE H388X - HW: V10.0.0 SW: AGZHP_1.4.0 - AGZHP_1.4.4

## Possible improvements

- Add an options flow to edit settings (password, interval, line type) without removing and re-adding the integration
- Validate credentials during setup
- Test SFP and DSL connections
- ...

## Changelog

### 2.1

- MAC address now visible in "Device info"
- Host was removed from entity name

### 2.0

- Added `device_tracker` entities for Wi-Fi clients
- Added support for multiple routers
- Setup now uses UI config flow
- Added uptime-in-days sensors
- Other minor fixes and improved error handling

#### Breaking Changes [V2.0]
- **Entity names will change** as they now include a host segment to support multiple routers.
- **YAML configuration is no longer supported**. Remove the `zteh388x` block from your `sensor:` section in `configuration.yaml`, restart Home Assistant and follow the [Installation and configuration](#installation-and-configuration) steps.

## Disclaimer

This software is provided "as-is", without any express or implied warranties. The author is not liable for any damages, legal or regulatory violations resulting from your use of the software.\
You use this software at your own risk.\
The author is under no obligation to provide maintenance, support, updates, or modifications to the software.\
"TIM" and "ZTE", along with their logos, are the property of their respective owners and are used for illustrative purposes only. Their use does not imply any affiliation with or endorsement by these companies.

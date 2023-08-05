# Copyright (c) 2017 Orange.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from collections import namedtuple

# bagpipe-bgp VPN types
EVPN = 'evpn'
IPVPN = 'ipvpn'
VPN_TYPES = [EVPN, IPVPN]

RT_IMPORT = 'import_rt'
RT_EXPORT = 'export_rt'
RT_TYPES = [RT_IMPORT, RT_EXPORT]

GatewayInfo = namedtuple('GatewayInfo', ['mac', 'ip'])
NO_GW_INFO = GatewayInfo(None, None)

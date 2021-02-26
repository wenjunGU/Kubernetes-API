common_region_ids = [
    "cn-qingdao",
    "cn-beijing",
    "cn-zhangjiakou",
    "cn-huhehaote",
    "cn-hangzhou",
    "cn-shanghai",
    "cn-shenzhen",
    "cn-hongkong",
]

'''
存在依赖关系VPC-scan脚本
顶级资产接口:DescribeVpcs:获取私有网络vpc资产
次级资产接口:DescribeVSwitches:获取vpc下交换机资产
次级资产接口:DescribeRouteTableList:获取vpc下路由表资产
次级资产接口:DescribeVpnGateways:获取vpc下vpn网关资产
次级资产接口:DescribeNatGateways:获取vpc下nat网关资产
'''

##依赖于顶级资产接口翻页方法
def Turn(action,vpcid,RegionId,PAGESIZE,PAGENUMBER):
    result_data = []
    for RegionId in common_region_ids:
        PAGESIZE = 50
        PAGENUMBER = 1
        while True:
            status_code, api_res = I_CLIENT_HELPER.common('vpc', Action=action,VpcId=vpcid,RegionId=RegionId, PageSize=PAGESIZE, PageNumber=PAGENUMBER)
            try:
                TotalCount = api_res['TotalCount']
            except KeyError:
                pass
            result_data.append(api_res)
            if not isinstance(TotalCount, int):
                raise ScriptContinueException("vpc.{0}'s Response TotalCount Type Error".format(action))
            if PAGENUMBER * PAGESIZE >= TotalCount:
                break
            else:
                PAGENUMBER += 1
    return result_data

##依赖于顶级资产接口翻页后取数据
def Get_data(result_datas,Describes,Describe):
    result_data = []
    for api_res in result_datas:
        try:
            data_list = api_res[Describes][Describe]
        except KeyError:
            pass
        else:
            if isinstance(data_list, (list, tuple, dict)):
                for d in toolkit.as_array(data_list):
                    result_data.append(d)
    return result_data

for RegionId in common_region_ids:
    PAGESIZE = 50
    PAGENUMBER = 1
    result_data = []
    while True:
        status_code, api_res = I_CLIENT_HELPER.common('vpc', Action='DescribeVpcs', RegionId=RegionId, PageSize=PAGESIZE, PageNumber=PAGENUMBER)
        try:
            TotalCount = api_res['TotalCount']
        except KeyError:
            raise ScriptContinueException("vpc.DescribeVPC's Response TotalCount Not Found")
        result_data.append(api_res)
        if not isinstance(TotalCount, int):
            raise ScriptContinueException("vpc.DescribeVPC's Response TotalCount Type Error")
        if PAGENUMBER * PAGESIZE >= TotalCount:
            break
        else:
            PAGENUMBER += 1


    for api_res in result_data:
        try:
            data_list = api_res['Vpcs']['Vpc']
        except KeyError:
            pass
        else:
            if isinstance(data_list, (list, tuple, dict)):
                for d in toolkit.as_array(data_list):
                    if not isinstance(d, dict):
                        continue
                    scan_result = {
                        'product': 'vpc.DescribeVpcs',
                        'outerId': d.get('VpcId') + '__' + RegionId,
                        'name': d.get('VpcName'),
                        'meta': d,
                    }

                    result_Switches = []
                    result_RouteTable = []
                    result_VpnGateways = []
                    result_NatGateways = []
                    for m in Get_data(Turn('DescribeVSwitches',d.get('VpcId'),RegionId,PAGESIZE,PAGENUMBER),'VSwitches','VSwitch'):
                        result_Switches.append(m)
                    scan_result['meta']['xSwitch'] = result_Switches
                    for m in Get_data(Turn('DescribeRouteTableList',d.get('VpcId'),RegionId,PAGESIZE,PAGENUMBER),'RouterTableList','RouterTableListType'):
                        result_RouteTable.append(m)
                    scan_result['meta']['xRoutetablelist'] = result_RouteTable
                    for m in Get_data(Turn('DescribeVpnGateways',d.get('VpcId'),RegionId,PAGESIZE,PAGENUMBER),'VpnGateways','VpnGateway'):
                        result_VpnGateways.append(m)
                    scan_result['meta']['xVpnGateways'] = result_VpnGateways
                    for m in Get_data(Turn('DescribeNatGateways',d.get('VpcId'),RegionId,PAGESIZE,PAGENUMBER),'NatGateways','NatGateway'):
                        result_NatGateways.append(m)
                    scan_result['meta']['xNatGateways'] = result_NatGateways
                    O_RESULTS.add(scan_result)

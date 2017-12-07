#encoding:utf-8

from sqlalchemy import Table,Column,Integer,DECIMAL,String,Date,MetaData,ForeignKey
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Table_creator:
    '''
    This class is for user to customize the tables
    '''
    #k 线数据
    def get_table_k_data(self,table_name):
        metadata = MetaData()
        table_k_data = Table(table_name,metadata,
                Column('date',Date(),primary_key=True),     #时间和日期 低频数据时为：YYYY-MM-DD 高频数为：YYYY-MM-DD HH:MM
                Column('open',DECIMAL(10,4)),  #开盘价
                Column('close',DECIMAL(10,4)), #收盘价
                Column('high',DECIMAL(10,4)),  #最高价
                Column('low',DECIMAL(10,4)),   #最低价
                Column('volume',DECIMAL(20,4)),#成交量
                Column('code',String(100))    #证券代码
                )
        return table_k_data
    
    #历史数据
    def get_table_history_data(self,table_name):
        metadata = MetaData()
        table_history_data = Table(table_name,metadata,
                Column('date',Date(),primary_key=True),     #时间和日期 低频数据时为：YYYY-MM-DD 高频数为：YYYY-MM-DD HH:MM
                Column('open',DECIMAL(10,4)),  #开盘价
                Column('high',DECIMAL(10,4)),  #最高价
                Column('close',DECIMAL(10,4)), #收盘价
                Column('low',DECIMAL(10,4)),   #最低价
                Column('volume',DECIMAL(20,4)),#成交量
                Column('price_change',DECIMAL(20,4)),#价格变动
                Column('p_change',DECIMAL(20,4)),#涨跌幅
                Column('ma5',DECIMAL(20,4)),#5日均价
                Column('ma10',DECIMAL(20,4)),#10日均价
                Column('ma20',DECIMAL(20,4)),#20日均价
                Column('v_ma5',DECIMAL(20,4)),#5日均量
                Column('v_ma10',DECIMAL(20,4)),#10日均量
                Column('v_ma20',DECIMAL(20,4)),#20日均量
                Column('turnover',DECIMAL(20,4)),#换手率
                )
        return table_history_data
                
    #上证50
    def get_table_sz50_list(self):
        metadata = MetaData()
        table_sz50_list = Table('sz50_list',metadata,
                                  Column('code',String(100),primary_key=True),
                                  Column('name',String(100))
                                  )
        return table_sz50_list
    
    #中证500
    def get_table_zz500_list(self):
        metadata = MetaData()
        table_zz500_list = Table('zz500_list',metadata,
                                  Column('code',String(100),primary_key=True),
                                  Column('name',String(100)),
                                  Column('date',Date()),
                                  Column('weight',DECIMAL(10,4))
                                  )
        return table_zz500_list
    
    #沪深300
    def get_table_hs300_list(self):
        metadata = MetaData()
        table_hs300_list = Table('hs300_list',metadata,
                                Column('code',String(100),primary_key=True),
                                Column('name',String(100)),
                                Column('date',Date()),
                                Column('weight',DECIMAL(10,4))
                                )
        return table_hs300_list        
    
    
    #分红数据，分配预案
    def get_table_dividend_data(self):
        metadata = MetaData()
        table_dividend_data= Table('dividend_data',metadata,
                                Column('code',String(100)),
                                Column('name',String(100)),
                                Column('year',Integer()),
                                Column('report_date',Date()),
                                Column('divi',DECIMAL(10,4)),
                                Column('shares',DECIMAL(10,2))
                                )
        return table_dividend_data
        
    #合并财务报表－年度
    def get_consolidated_bs_year(self,table_name):
        metadata = MetaData()
        table_consolidated_bs_year= Table(table_name,metadata,
                                            Column('报告日期',Date(),primary_key=True),     #时间和日期
                                            Column('货币资金(万元)',DECIMAL(20,4)),  
                                            Column('结算备付金(万元)',DECIMAL(20,4)),  
                                            Column('拆出资金(万元)',DECIMAL(20,4)),  
                                            Column('交易性金融资产(万元)',DECIMAL(20,4)),  
                                            Column('衍生金融资产(万元)',DECIMAL(20,4)),  
                                            Column('应收票据(万元)',DECIMAL(20,4)),  
                                            Column('应收账款(万元)',DECIMAL(20,4)),  
                                            Column('预付款项(万元)',DECIMAL(20,4)),  
                                            Column('应收保费(万元)',DECIMAL(20,4)),  
                                            Column('应收分保账款(万元)',DECIMAL(20,4)),  
                                            Column('应收分保合同准备金(万元)',DECIMAL(20,4)),  
                                            Column('应收利息(万元)',DECIMAL(20,4)),  
                                            Column('应收股利(万元)',DECIMAL(20,4)),  
                                            Column('其他应收款(万元)',DECIMAL(20,4)),  
                                            Column('应收出口退税(万元)',DECIMAL(20,4)),  
                                            Column('应收补贴款(万元)',DECIMAL(20,4)),  
                                            Column('应收保证金(万元)',DECIMAL(20,4)),  
                                            Column('内部应收款(万元)',DECIMAL(20,4)),  
                                            Column('买入返售金融资产(万元)',DECIMAL(20,4)),  
                                            Column('存货(万元)',DECIMAL(20,4)),  
                                            Column('待摊费用(万元)',DECIMAL(20,4)),  
                                            Column('待处理流动资产损益(万元)',DECIMAL(20,4)),  
                                            Column('一年内到期的非流动资产(万元)',DECIMAL(20,4)),  
                                            Column('其他流动资产(万元)',DECIMAL(20,4)),  
                                            Column('流动资产合计(万元)',DECIMAL(20,4)),  
                                            Column('发放贷款及垫款(万元)',DECIMAL(20,4)),  
                                            Column('可供出售金融资产(万元)',DECIMAL(20,4)),  
                                            Column('持有至到期投资(万元)',DECIMAL(20,4)),  
                                            Column('长期应收款(万元)',DECIMAL(20,4)),  
                                            Column('长期股权投资(万元)',DECIMAL(20,4)),  
                                            Column('其他长期投资(万元)',DECIMAL(20,4)),  
                                            Column('投资性房地产(万元)',DECIMAL(20,4)),  
                                            Column('固定资产原值(万元)',DECIMAL(20,4)),  
                                            Column('累计折旧(万元)',DECIMAL(20,4)),  
                                            Column('固定资产净值(万元)',DECIMAL(20,4)),  
                                            Column('固定资产减值准备(万元)',DECIMAL(20,4)),  
                                            Column('固定资产(万元)',DECIMAL(20,4)),  
                                            Column('在建工程(万元)',DECIMAL(20,4)),  
                                            Column('工程物资(万元)',DECIMAL(20,4)),  
                                            Column('固定资产清理(万元)',DECIMAL(20,4)),  
                                            Column('生产性生物资产(万元)',DECIMAL(20,4)),  
                                            Column('公益性生物资产(万元)',DECIMAL(20,4)),  
                                            Column('油气资产(万元)',DECIMAL(20,4)),  
                                            Column('无形资产(万元)',DECIMAL(20,4)),  
                                            Column('开发支出(万元)',DECIMAL(20,4)),  
                                            Column('商誉(万元)',DECIMAL(20,4)),  
                                            Column('长期待摊费用(万元)',DECIMAL(20,4)),  
                                            Column('股权分置流通权(万元)',DECIMAL(20,4)),  
                                            Column('递延所得税资产(万元)',DECIMAL(20,4)),  
                                            Column('其他非流动资产(万元)',DECIMAL(20,4)),  
                                            Column('非流动资产合计(万元)',DECIMAL(20,4)),  
                                            Column('资产总计(万元)',DECIMAL(20,4)),  
                                            Column('短期借款(万元)',DECIMAL(20,4)),  
                                            Column('向中央银行借款(万元)',DECIMAL(20,4)),  
                                            Column('吸收存款及同业存放(万元)',DECIMAL(20,4)),  
                                            Column('拆入资金(万元)',DECIMAL(20,4)),  
                                            Column('交易性金融负债(万元)',DECIMAL(20,4)),  
                                            Column('衍生金融负债(万元)',DECIMAL(20,4)),  
                                            Column('应付票据(万元)',DECIMAL(20,4)),  
                                            Column('应付账款(万元)',DECIMAL(20,4)),  
                                            Column('预收账款(万元)',DECIMAL(20,4)),  
                                            Column('卖出回购金融资产款(万元)',DECIMAL(20,4)),  
                                            Column('应付手续费及佣金(万元)',DECIMAL(20,4)),  
                                            Column('应付职工薪酬(万元)',DECIMAL(20,4)),  
                                            Column('应交税费(万元)',DECIMAL(20,4)),  
                                            Column('应付利息(万元)',DECIMAL(20,4)),  
                                            Column('应付股利(万元)',DECIMAL(20,4)),  
                                            Column('其他应交款(万元)',DECIMAL(20,4)),  
                                            Column('应付保证金(万元)',DECIMAL(20,4)),  
                                            Column('内部应付款(万元)',DECIMAL(20,4)),  
                                            Column('其他应付款(万元)',DECIMAL(20,4)),  
                                            Column('预提费用(万元)',DECIMAL(20,4)),  
                                            Column('预计流动负债(万元)',DECIMAL(20,4)),  
                                            Column('应付分保账款(万元)',DECIMAL(20,4)),  
                                            Column('保险合同准备金(万元)',DECIMAL(20,4)),  
                                            Column('代理买卖证券款(万元)',DECIMAL(20,4)),  
                                            Column('代理承销证券款(万元)',DECIMAL(20,4)),  
                                            Column('国际票证结算(万元)',DECIMAL(20,4)),  
                                            Column('国内票证结算(万元)',DECIMAL(20,4)),  
                                            Column('递延收益(万元)',DECIMAL(20,4)),  
                                            Column('应付短期债券(万元)',DECIMAL(20,4)),  
                                            Column('一年内到期的非流动负债(万元)',DECIMAL(20,4)),  
                                            Column('其他流动负债(万元)',DECIMAL(20,4)),  
                                            Column('流动负债合计(万元)',DECIMAL(20,4)),  
                                            Column('长期借款(万元)',DECIMAL(20,4)),  
                                            Column('应付债券(万元)',DECIMAL(20,4)),  
                                            Column('长期应付款(万元)',DECIMAL(20,4)),  
                                            Column('专项应付款(万元)',DECIMAL(20,4)),  
                                            Column('预计非流动负债(万元)',DECIMAL(20,4)),  
                                            Column('长期递延收益(万元)',DECIMAL(20,4)),  
                                            Column('递延所得税负债(万元)',DECIMAL(20,4)),  
                                            Column('其他非流动负债(万元)',DECIMAL(20,4)),  
                                            Column('非流动负债合计(万元)',DECIMAL(20,4)),  
                                            Column('负债合计(万元)',DECIMAL(20,4)),  
                                            Column('实收资本(或股本)(万元)',DECIMAL(20,4)),  
                                            Column('资本公积(万元)',DECIMAL(20,4)),  
                                            Column('减:库存股(万元)',DECIMAL(20,4)),  
                                            Column('专项储备(万元)',DECIMAL(20,4)),  
                                            Column('盈余公积(万元)',DECIMAL(20,4)),  
                                            Column('一般风险准备(万元)',DECIMAL(20,4)),  
                                            Column('未确定的投资损失(万元)',DECIMAL(20,4)),  
                                            Column('未分配利润(万元)',DECIMAL(20,4)),  
                                            Column('拟分配现金股利(万元)',DECIMAL(20,4)),  
                                            Column('外币报表折算差额(万元)',DECIMAL(20,4)),  
                                            Column('归属于母公司股东权益合计(万元)',DECIMAL(20,4)),  
                                            Column('少数股东权益(万元)',DECIMAL(20,4)),  
                                            Column('所有者权益(或股东权益)合计(万元)',DECIMAL(20,4)),  
                                            Column('负债和所有者权益(或股东权益)总计(万元)',DECIMAL(20,4))
                                            )
        return table_consolidated_bs_year
# ---------------------------------------------------------------------------------------------------------------------#
# AUTHOR: Jason, jinxiang_zhu@parramountain.com                                                                        #
# ORGANIZATION: PMI                                                                                                    #
# VERSION: 1.0                                                                                                         #
# CREATED: 3rd Mar 2016                                                                                                #
# ---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import pandas as pd

#import seaborn as sns
#import matplotlib.pyplot as plt
#from sklearn.preprocessing import StandardScaler

"""Tnseq command line interface """

# =============== <1: Realization of shell scripts using click package> #==============#
import click

VERSION = '1.0'
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def main():
    pass


@main.command(help='分析销售数据或OCM参数.')
@click.option('--data_path', '-f', default='福州上海子公司业绩表.xlsx', help='分析数据的文件路径')
@click.option('--index', '-i', default='餐厅名称', help='选择某列作为数据框的索引.')
@click.option('--value_col', '-vc', default=5, help='选择用于数据标准化处理的开始列数。')
def feature_analysis(**kwargs):
    data_path = kwargs['data_path']
    index = kwargs['index']
    value_col = kwargs['value_col']
    df = pd.read_excel(data_path, index_col=index)
    print(df.head())


@main.command(help='提取OCM特征')
@click.option('--data_path', '-f', default='', help="输入待提取的特征信息文件路径，默认为'湖北需求预估使用的特征.xlsx'。")
@click.option('--province', '-p', default='湖北', help='选择提取的省份。')
def OCM_extract(**kwargs):
    import OCMFeatureExtract as ofe
    feature_file = kwargs['data_path']
    province = kwargs['province']
    df = pd.read_excel(feature_file, index_col=[0])  # 将'省'列设为索引
    ofe.merging_data(df, province)


# ================================== <4: Running main function> ================================== #
if __name__ == '__main__':
    # logger = log.createCustomLogger('root')
    main()



'''
Author: Derry
Date: 2022-10-01 15:38:24
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-01 17:40:21
Description: 原始实验数据转换为Prism画图数据的小程序
'''
import argparse
import os

import numpy as np
import pandas as pd


def process_prism(main_sample, infile_name=None, outfile_name=None):
    def read_file(file_name):
        """
        读原始文件
        """
        if not file_name:
            for file in os.listdir('./'):
                if file.endswith('.txt'):
                    file_name = file
                    break
        df = pd.read_csv(file_name, sep='\t')
        return df

    def save_file(out_df, outfile_name):
        """
        保存文件
        """
        if not outfile_name:
            outfile_name = 'result.csv'
        out_df.to_csv(outfile_name, sep='\t')

    def move_to_first(main_sample, sample_names):
        """
        把main_sample的调整到sample_names的第一个位置
        """
        sample_names = list(sample_names)
        sample_names.remove(main_sample)
        sample_names.insert(0, main_sample)
        return sample_names

    df = read_file(infile_name)  # 读原始文件

    df = df[['Sample Name', 'Gene Name', 'Cq']]  # 删除无用列
    df.drop(df[df['Cq'] == '-'].index, inplace=True)  # 删除无用行

    PHYH = df[df['Gene Name'] == 'PHYH']  # 对照组
    df.drop(df[df['Gene Name'] == 'PHYH'].index, inplace=True)  # 实验组
    gene_names = df['Gene Name'].unique()  # 实验组基因名
    sample_names = df['Sample Name'].unique()  # 实验组样本名
    sample_names = move_to_first(main_sample, sample_names)

    # 初始化结果表格
    col = [f"{sample}:{i+1}" for sample in sample_names for i in range(4)]
    row = [f"PHYH({gene})" for gene in gene_names]
    out_df = pd.DataFrame(columns=col, index=row)

    # 计算每个样本的表达量
    for gene_name in gene_names:
        sample_names = move_to_first(main_sample, sample_names)
        Exp = df[df['Gene Name'] == gene_name]
        for sample_name in sample_names:
            Cq = Exp[Exp['Sample Name'] ==
                     sample_name]['Cq'].astype(float).mean()
            Cq_PHYH = PHYH[PHYH['Sample Name'] ==
                           sample_name]['Cq'].astype(float).values
            delta = Cq_PHYH - Cq
            if sample_name == main_sample:
                avg_delta = np.mean(delta)
            power = 2**(-(delta-avg_delta))
            for i in range(power.shape[0]):
                out_df.loc[f"PHYH({gene_name})",
                           f"{sample_name}:{i+1}"] = power[i]

    save_file(out_df, outfile_name)  # 保存文件


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', default=None, help='输入文件名')
    parser.add_argument('-o', '--outfile', default=None, help='输出文件名')
    parser.add_argument('-m', '--main_sample', default=None, help='主样本名')
    args = parser.parse_args()
    if not args.main_sample:
        print('请输入主样本名：', end='')
        args.main_sample = input()
    process_prism(args.main_sample, args.infile, args.outfile)
    print('搞定！！')
    # process_prism(main_sample='LN229 WT', infile_name=None, outfile_name=None)

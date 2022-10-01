'''
Author: Derry
Date: 2022-10-01 15:38:24
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-02 01:25:34
Description: 原始实验数据转换为Prism画图数据的小程序
'''
import argparse
import os

import numpy as np
import pandas as pd


def process_prism(main_sample, control_genes=None, experiment_genes=None, infile_name=None, outfile_name=None):
    def read_file(file_name):
        """
        读原始文件
        """
        if not file_name:
            for file in os.listdir('./'):
                if file.endswith('.txt'):
                    file_name = file
                    break
        control = pd.read_csv(file_name, sep='\t')
        return control

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

    def split_control_experiment(control, control_genes=None, experiment_genes=None):
        """
        划分实验组和对照组
        """
        if len(experiment_genes):
            experiment = control[control['Gene Name'].isin(
                experiment_genes)]  # 实验组
            control = control[~control['Gene Name'].isin(
                experiment_genes)]  # 对照组
            control_genes = control['Gene Name'].unique()  # 对照组基因名
        elif len(control_genes):
            control = control[control['Gene Name'].isin(control_genes)]  # 对照组
            experiment = control[~control['Gene Name'].isin(
                control_genes)]  # 实验组
            experiment_genes = experiment['Gene Name'].unique()  # 实验组基因名
        return control, experiment, control_genes, experiment_genes

    control = read_file(infile_name)  # 读原始文件

    control = control[['Sample Name', 'Gene Name', 'Cq']]  # 删除无用列
    control.drop(control[control['Cq'] == '-'].index, inplace=True)  # 删除无用行

    sample_names = control['Sample Name'].unique()  # 样本名
    sample_names = move_to_first(
        main_sample, sample_names)  # 把main_sample的调整到首位

    control, experiment, control_genes, experiment_genes = split_control_experiment(
        control, control_genes, experiment_genes)  # 实验组和对照组

    # 初始化结果表格
    col = [f"{sample}:{i+1}" for sample in sample_names for i in range(4)]
    row = [
        f"{con_gene}({exp_gene})"for exp_gene in control_genes for con_gene in experiment_genes]
    out_df = pd.DataFrame(columns=col, index=row)

    # 计算每个样本的表达量
    for experiment_gene in experiment_genes:
        # 精确实验组
        exact_experiment = experiment[experiment['Gene Name']
                                      == experiment_gene]
        for control_gene in control_genes:
            sample_names = move_to_first(
                main_sample, sample_names)  # 把main_sample的调整到首位
            exact_control = control[control['Gene Name']
                                    == control_gene]  # 精确对照组
            for sample_name in sample_names:
                Cq_control = exact_control[exact_control['Sample Name'] ==
                                           sample_name]['Cq'].astype(float).mean()  # 对照组Cq均值
                Cq_experiment = exact_experiment[exact_experiment['Sample Name'] ==
                                                 sample_name]['Cq'].astype(float).values  # 实验组Cq
                delta = Cq_experiment - Cq_control  # delta
                if sample_name == main_sample:
                    avg_delta = np.mean(delta)  # delta均值
                power = 2**(-(delta-avg_delta))  # 表达量
                for i in range(power.shape[0]):
                    out_df.loc[f"{experiment_gene}({control_gene})",
                               f"{sample_name}:{i+1}"] = power[i]  # 写入结果表格

    save_file(out_df, outfile_name)  # 保存文件


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', default=None, help='输入文件名')
    parser.add_argument('-o', '--outfile', default=None, help='输出文件名')
    parser.add_argument('-m', '--main_sample', default=None, help='主样本名')
    parser.add_argument('-c', '--control_genes', default=None, help='对照组基因名')
    parser.add_argument('-e', '--experiment_genes',
                        default=None, help='实验组基因名')
    args = parser.parse_args()
    if not args.main_sample:
        print('请输入主样本名：', end='')
        args.main_sample = input()
    if not args.control_genes:
        print('请输入对照组基因名：', end='')
        args.control_genes = input().strip().split(',')
    if len(args.control_genes) and not args.experiment_genes:
        print('请输入实验组基因名：', end='')
        args.experiment_genes = input().strip().split(',')
    process_prism(args.main_sample, args.control_genes,
                  args.experiment_genes, args.infile, args.outfile)
    print('搞定！！')
    # process_prism(main_sample='LN229 WT', experiment_genes=[
    #               "PHYH", "GAPDH"], infile_name=None, outfile_name=None)

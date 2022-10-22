'''
Author: Derry
Date: 2022-10-22 16:17:49
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-22 20:48:09
Description: 原始实验数据转换为Prism画图数据的脚本 v3.1
'''
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import prettytable as pt
import seaborn as sns


class qPCRv3:
    def __init__(self):
        self._clear_log()  # 清空log文件

    def _read_file(self, file_name):
        """
        读原始文件
        """
        if not file_name:
            for file in os.listdir('./'):
                if file.endswith('.txt'):
                    file_name = file
                    break
        control = pd.read_csv(file_name, sep='\t')
        self._print_log(f'读取文件：{file_name}')
        return control

    def _save_file(self, out_df, outfile_name):
        """
        保存文件
        """
        if not outfile_name:
            outfile_name = f"{self.control_sample}实验分析结果.csv"
        out_df.to_csv(outfile_name, sep='\t')
        self._print_log(f"输出文件已保存为：{outfile_name}")

    def split_control_experiment(self, df, house_keeping_genes=None, experiment_genes=None):
        """
        划分实验组和对照组。
        优先使用输入的对照组和实验组，
        如果只有对照组，那么其他的都是实验组，
        如果只有实验组，那么其他的都是对照组。
        """
        if house_keeping_genes and len(house_keeping_genes):
            control = df[df['Gene Name'].isin(house_keeping_genes)]  # 对照组
            if len(set(control['Gene Name'])) != len(set(house_keeping_genes)):
                self._print_log('注意：输入的对照组中有不存在的基因名：！')
            if experiment_genes and len(experiment_genes):
                experiment = df[df['Gene Name'].isin(experiment_genes)]  # 实验组
                if len(set(experiment['Gene Name'])) != len(set(experiment_genes)):
                    self._print_log('注意：输入的实验组中有不存在的基因名！')
            else:
                experiment = df[~df['Gene Name'].isin(
                    house_keeping_genes)]  # 实验组
            experiment_genes = experiment['Gene Name'].unique()  # 实验组基因名
        elif experiment_genes and len(experiment_genes):
            experiment = df[df['Gene Name'].isin(
                experiment_genes)]  # 实验组
            if len(set(experiment['Gene Name'])) != len(set(experiment_genes)):
                self._print_log('注意：输入的实验组中有不存在的基因名！')
            control = df[~df['Gene Name'].isin(
                experiment_genes)]  # 对照组
            house_keeping_genes = control['Gene Name'].unique()  # 对照组基因名
        else:
            raise ValueError('请至少输入一组基因名！')
        self._print_log(f"对照组基因：{'、'.join(house_keeping_genes)}")
        self._print_log(f"实验组基因：{'、'.join(experiment_genes)}")
        return control, experiment, house_keeping_genes, experiment_genes

    def plot_errorbar(self, df, show=True):
        """
        根据分组实验数据画图
        """
        sns.set()
        plt.figure(figsize=(15, 9))
        df = df.dropna(axis=1, how='all')
        grouped = df.columns.to_series().groupby(
            df.columns.str.split(':').str[0]).groups
        for key, value in grouped.items():
            mean = df[value].mean(axis=1)
            std = df[value].std(axis=1)
            plt.errorbar(mean.index, mean, yerr=std,
                         fmt='o', label=key, capsize=5)
        plt.xticks()
        plt.legend(loc='upper left', bbox_to_anchor=(0.6, 1))
        plt.title(self.control_sample, fontsize=20)
        plt.xlabel('Gene')
        plt.ylabel('Expression')
        plt.xticks(rotation=30)
        plt.savefig(f'{self.control_sample}_errorbar.png')
        self._print_log(f"输出绘图已保存为：{self.control_sample}_errorbar.png")
        if show:
            plt.show()

    def _clear_log(self, file="log.txt"):
        """
        清空log文件
        """
        with open(file, 'w') as f:
            f.write('')

    def _print_log(self, text, end='\n', file="log.txt", to_screen=True):
        """
        打印log
        """
        if to_screen:
            print(text, end=end)
        with open(file, 'a', encoding='utf-8') as f:
            print(text, end=end, file=f)

    def _array2str(self, array):
        """
        把array数组转换成字符串
        """
        return ', '.join(np.round(array, 2).astype(str))

    def _detect_sample_name(self):
        """
        检查样本名称的正确性，并自动识别实验组样本，返回内参+实验组样本名
        """
        sample_names = self.df['Sample Name'].unique()  # 样本名
        if self.control_sample not in sample_names:
            raise ValueError(f'输入的NC_sample:{self.control_sample}不在样本名中！')
        else:
            self._print_log(f"正常组样本名：{self.control_sample}")
        if self.experiment_samples and len(self.experiment_samples):
            for experiment_sample in self.experiment_samples:
                if experiment_sample not in sample_names:
                    raise ValueError(
                        f'输入的experiment_sample:{experiment_sample}不在样本名中！')
            sample_names = [self.control_sample]+self.experiment_samples
        else:
            self.experiment_samples = [
                sample for sample in sample_names if sample != self.control_sample]
        return [self.control_sample]+self.experiment_samples

    def qPCR_main(self, control_sample, experiment_samples=None, house_keeping_genes=None, experiment_genes=None, infile_name=None, outfile_name=None, max_col=4, plot=True):
        """
        qPCR主函数

        Parameters
        ----------
        control_sample : str
            正常组样本名
        experiment_samples : list, optional
            实验组样本名, by default None
        house_keeping_genes : list, optional
            对照组基因名, by default None
        experiment_genes : list, optional
            实验组基因名, by default None
        infile_name : str, optional
            输入文件名，默认为None，即使用当前目录下的第一个.txt文件
        outfile_name : str, optional
            输出文件名，默认为None，即使用“内参样本名+qPCR分析结果.csv”
        max_col : int, optional
            输出文件中每个样本的最大列数，默认为4
        plot : bool, optional
            是否绘图，默认为True
        """

        self.control_sample = control_sample
        self.experiment_samples = experiment_samples
        self.house_keeping_genes = house_keeping_genes
        self.experiment_genes = experiment_genes

        self._print_log('\n'+'-'*50+"开始运行"+'-'*50)

        # 读原始文件
        self.df = self._read_file(infile_name)

        # 预处理：删除无关行和无关列
        self.df = self.df[['Sample Name', 'Gene Name', 'Cq']]
        self.df.drop(self.df[self.df['Cq'] == '-'].index, inplace=True)

        # 样本名称检查与智能划分
        self.sample_names = self._detect_sample_name()

        # 筛选出内参和实验组的数据
        self.df = self.df[self.df['Sample Name'].isin(self.sample_names)]

        # 基因名称检查与智能划分
        data_control, data_experiment, self.house_keeping_genes, self.experiment_genes = self.split_control_experiment(
            self.df, self.house_keeping_genes, self.experiment_genes)

        out_df = self.compute_qPCR(max_col, data_control, data_experiment)

        self._save_file(out_df, outfile_name)  # 保存文件
        if plot:
            self.plot_errorbar(out_df, show=True)  # 画图，show：预画图是否弹窗
        self._print_log('-'*50+'处理完成'+'-'*50+'\n')

    def compute_qPCR(self, max_col, df_control, df_experiment):
        self._print_log("\n开始计算差异表达基因...")
        # 初始化中间过程表格
        log_table = pt.PrettyTable()
        log_table.field_names = [
            "Gene Name", f"对照组Cq均值", "实验组Cq", "Cq差值", "与内参Cq均值的差", "表达量"]

        # 初始化结果表格
        col = [
            f"{sample}" if i==0 else f"{sample}:{i+1}" for sample in self.sample_names for i in range(max_col)]
        row = [
            f"{con_gene}({exp_gene})"for exp_gene in self.house_keeping_genes for con_gene in self.experiment_genes]
        out_df = pd.DataFrame(columns=col, index=row)

        # 计算部分：计算每个样本的表达量
        for experiment_gene in self.experiment_genes:  # 实验组
            df_exp = df_experiment[df_experiment['Gene Name']
                                   == experiment_gene]
            for house_keeping_gene in self.house_keeping_genes:  # 对照组
                df_con = df_control[df_control['Gene Name']
                                    == house_keeping_gene]
                for sample_name in self.sample_names:  # 样本
                    Cq_control = df_con[df_con['Sample Name'] ==
                                        sample_name]['Cq'].astype(float).mean()  # 对照组Cq均值
                    Cq_experiment = df_exp[df_exp['Sample Name'] ==
                                           sample_name]['Cq'].astype(float).values  # 实验组Cq
                    delta = Cq_experiment - Cq_control  # delta
                    if sample_name == self.control_sample:
                        avg_delta = np.mean(delta)  # delta均值
                    power = 2**(-(delta-avg_delta))  # 表达量

                    for i in range(power.shape[0]):
                        if i == 0:
                            out_df.loc[f"{experiment_gene}({house_keeping_gene})",
                                       f"{sample_name}"] = power[i]
                        else:
                            out_df.loc[f"{experiment_gene}({house_keeping_gene})",
                                    f"{sample_name}:{i+1}"] = power[i]  # 写入结果表格
                    log_table.add_row([f"{experiment_gene}({house_keeping_gene})", round(Cq_control, 2), self._array2str(
                        Cq_experiment), self._array2str(delta), round(avg_delta, 2), self._array2str(power)])

        self._print_log(log_table, to_screen=True)  # to_screen计算具体步骤是否出现在屏幕上
        self._print_log("差异表达基因计算完成！\n")
        return out_df


if __name__ == "__main__":
    """
    ! 1. control_sample：对照组样本名（必选，优先，只能有一个）
    ? 2. experiment_samples：实验组样本名（可选，默认为除了正常组样本以外的样本）
    ? 3. house_keeping_genes：内参（可选，优先，默认为除了实验组样本以外的样本，34至少一个不为空）
    ? 4. experiment_genes：实验组基因名（可选，默认为除了对照组样本以外的样本，34至少一个不为空）
    5. max_col：每个样本的最大列数（默认：4）
    6. plot：是否预画图（默认：True）
    7. infile_name：输入文件名（默认：本程序同目录下的txt文件）
    8. outfile_name：输出文件名（默认：“内参样本名+qPCR分析结果.csv”）
    ps：
    带方括号的地方可以加样本，基因名，但是必须用英文逗号分隔
    加样本的话逗号、引号都用英文的。实际上除了注释and双引号里面的可以中文以外，代码里不能有中文。
    两对三个双引号之间是注释，# 后面也是注释。
    """

    qPCR = qPCRv3()  # !这一行不要删！
    qPCR.qPCR_main(control_sample="T387 WT", experiment_samples=["T387 MUT"], house_keeping_genes=[
    ], experiment_genes=["PHYH1", "PHYH2"], max_col=4, plot=True)
    # qPCR.qPCR_main(control_sample="H2S WT", experiment_samples=["H2S MUT"], house_keeping_genes=[
    # ], experiment_genes=["PHYH1", "PHYH2"], max_col=4, plot=True)

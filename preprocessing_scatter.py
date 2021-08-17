#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2021-06-30

@author:LHQ
echarts气泡图数据

https://echarts.apache.org/examples/zh/editor.html?c=scatter-punchCard
"""
import pandas as pd
import json

import click

path = "data/guangzhou_fenhang_gongzi_liucun.csv"

@click.command()
@click.option("-i", "--input-file", type=click.File(encoding="gbk"), default=path)
@click.option("-o", "--output-file", type=click.File(mode="w"), default="output/tmp.json")
def echarts_scatter(input_file, output_file):
    df = pd.read_csv(input_file, index_col=0, encoding="gbk")
    # 缩放数值
    max_value = df.values.max()
    df = df.applymap(lambda x: 30*x/max_value).applymap(lambda x: round(x,2))

    hours = df.columns.tolist()
    days = df.index.tolist()


    tmp = df.values
    row, col = df.shape
    data = []
    for i in range(row):
        for j in range(col):
            data.append([i, j, tmp[i,j]])

    result = {"data": data,"hours":hours, "days": days}
    json.dump(result, output_file)


if __name__ == "__main__":
    echarts_scatter()
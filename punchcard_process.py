#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2021-06-30

@author:LHQ
echarts气泡图数据

https://echarts.apache.org/examples/zh/editor.html?c=scatter-punchCard
"""
import os
import json

import click
import pandas as pd


def render_option(x, y, data):
    option = """
const hours = %(hours)s
const days = %(days)s

const data = %(data)s
    .map(function (item) {
    return [item[1], item[0], item[2]];
});
option = {
  title: {
  },
  legend: {
    data: [],
    left: 'right'
  },
  tooltip: {
    position: 'top',
    formatter: function (params) {
      return (
        params.value[2] +
        ' commits in ' +
        hours[params.value[0]] +
        ' of ' +
        days[params.value[1]]
      );
    }
  },
  grid: {
    left: 2,
    bottom: 10,
    right: 10,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: hours,
    boundaryGap: false,
    splitLine: {
      show: true
    },
    axisLabel:{interval:0, fontSize:9},
    axisLine: {
      show: false
    }
  },
  yAxis: {
    type: 'category',
    data: days,
    axisLine: {
      show: false
    }
  },
  series: [
    {
      name: 'Punch Card',
      type: 'scatter',
      symbolSize: function (val) {
        return val[2] * 2;
      },
      data: data,
      animationDelay: function (idx) {
        return idx * 5;
      }
    }
  ]
};
    """%{"days":y, "hours":x, "data":data}
    return option




path = "data/guangzhou_fenhang_gongzi_liucun.csv"

@click.command()
@click.option("-i", "--input-file", type=click.File(encoding="gbk"), default=path)
@click.option("-o", "--output-dir", type=click.Path(), default="output/punch-card")
def echarts_scatter(input_file, output_dir):
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

    ## 右移一格，让展示更加美观
    hours = [""] + hours
    data = [[y, x+1, v] for y,x,v in data]

    option = render_option(x=hours, y=days, data=data)

    input_path = input_file.name
    fname = "punchCard_%s.txt" % os.path.basename(input_path).split(".")[0]
    fpath = os.path.join(output_dir, fname)
    with open(fpath,"w") as f:
        f.write(option)


if __name__ == "__main__":
    echarts_scatter()
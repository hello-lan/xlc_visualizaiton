# -*- coding: utf-8 -*-
"""
@create Time:2021-06-30

@author:LHQ
echarts 瀑布图数据

https://echarts.apache.org/examples/zh/editor.html?c=bar-waterfall
"""
import json
import os

import click
import pandas as pd



def render_option(columns, values, fix_values):
    """waterfall option
    """
    option = """
    option = {
        grid: {
            left: '3%%',
            right: '4%%',
            bottom: '3%%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            axisLabel:{interval:0, fontSize:9},
            splitLine: {show: false},
            data: %(columns)s
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '辅助',
                type: 'bar',
                stack: '总量',
                itemStyle: {
                    barBorderColor: 'rgba(0,0,0,0)',
                    color: 'rgba(0,0,0,0)'
                },
                emphasis: {
                    itemStyle: {
                        barBorderColor: 'rgba(0,0,0,0)',
                        color: 'rgba(0,0,0,0)'
                    }
                },
                data: %(fix_values)s
            },
            {
                name: '主要数据',
                type: 'bar',
                stack: '总量',
                label: {
                    show: true,
                    position: 'inside'
                },
                data: %(values)s
            }
        ]
    }
    """%{'columns':columns, 'values':values, 'fix_values':fix_values}
    return option



path = "data/origin_data_for_waterfall/工资流出.csv"

@click.command()
@click.option("-i", "--input-file", type=click.File(encoding="gbk"), default=path)
@click.option("-o", "--output-dir", type=click.Path(), default="output/waterfall")
@click.option("-s", "--scale", type=float, default=1e-8, help="默认为1e-8, 即单位为亿")
def waterfall(input_file, output_dir, scale):
    df = pd.read_csv(input_file, index_col=0)
    df = df.applymap(lambda x: round(x * scale,2))
    columns = df.columns.tolist()   # df的第一列为总量，之后的列为每天流出的量
    
    for i, row in df.iterrows():
        data = row.tolist()
        total = data[0]
        sum_value = 0
        fixes = [0]
        for e in data[1:]:
            if e > 0:
                sum_value += e 
            fix = total - sum_value
            fixes.append(fix)

        values = []
        for e in data:
            if e < 0:
                item = {
                    "value": abs(e),
                    "itemStyle": {"color": "#a90000"}
                }
            else:
                item = e
            values.append(item)
        txt = render_option(columns, values, fixes)
        fname = "waterfall_%s.txt" % i
        fpath = os.path.join(output_dir, fname)
        with open(fpath,"w") as f:
            f.write(txt)



if __name__ == "__main__":
    waterfall()


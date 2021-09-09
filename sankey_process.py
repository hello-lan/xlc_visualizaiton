# -*- coding: utf-8 -*-
"""
@create Time:2021-06-30

@author:LHQ
echarts 桑吉图数据

https://echarts.apache.org/examples/zh/editor.html?c=bar-waterfall
"""
import json
import os

import click
import pandas as pd


colors = { '支付宝理财': "#0066CC",
          '微信': "#00FF00",
          '其他消费': "#66FF00",
          '支付宝': "#3366FF",
          '跨行异名': "#6699CC",
          '微信理财': "#33FF33",
          '美团': "#FFA500",
          '同行同名': "#6B8E23",
          '总资金':"#0099CC",
          '他行理财': "#00CCCC",
          '取款': "#6699FF",
          '第三方转账': "#99CC66",
          '其他理财': "#9999CC",
          '跨行同名': "#99CC00",
          '其他': "#CC9966",
          '京东': "#99CC66",
          '天天基金理财': "#FF9999",
          '理财': "#669999",
          '同行异名': "#6699CC",
          '转账': "#FF9900",
          '行内理财': "#99CC99",
          '购房': "#CCCCFF",
          '还款': "#99CC66",
          '消费': "#33CC66",
         }


def render_option(nodes, links):
    """sankey option
    """
    option ="""
    option = {
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        series: [
            {
                type: 'sankey',
                emphasis: {
                    focus: 'adjacency'
                },
                nodeAlign: 'left',
                data: %(nodes)s,
                links: %(links)s,
                label:{formatter:"{b} {c}"},
                lineStyle: {
                    color: 'source',
                    curveness: 0.5,
                }
            }
        ]
    }"""%{"nodes":nodes, "links":links}
    return option

path = "data/origin_data_for_sankey/transfer_out_wuhan.xlsx"

@click.command()
@click.option("-i", "--input-file", type=click.File(mode='rb'), default=path)
@click.option("-o", "--output-dir", type=click.Path(), default="output/sankey")
def sankey(input_file, output_dir):
    df = pd.read_excel(input_file)

    df_1 = df.groupby("cate_1", as_index=False)["ratio"].sum().rename(columns={"cate_1":"target", "ratio":"value"})
    df_1["source"] = "总资金"

    df_2 = df.rename(columns={"cate_1":"source", "cate_2":"target","ratio":"value"})[["source", "target","value"]]

    ## 各个节点的值
    pct_1 = df_1.groupby("source")["value"].sum().to_dict()
    pct_2 = df_2.groupby("source")["value"].sum().to_dict()
    pct_3 = df_2.query("source!=target").groupby("target")["value"].sum().to_dict()

    pct = dict()
    pct.update(pct_1)
    pct.update(pct_2)
    pct.update(pct_3)
    # 换算成百分比
    total = sum(pct_2.values())
    pct_new = {n:"{:.2f}%".format(100*(v/total)) if n != "总资金" else "100%" for n, v in pct.items()}


    #  构造echart 桑吉图的节点
    nodes_ = set(df_1[["source","target"]].values.reshape(-1).tolist()) | set(df_2[["source","target"]].values.reshape(-1).tolist())
    nodes = [{"name":n,"itemStyle":{"color":colors[n]}, "value": pct_new[n]} for n in nodes_]

    links = df_1.to_dict(orient="records")
    links.extend(df_2.query("source!=target").to_dict(orient="records"))

    txt = render_option(nodes, links)
    
    input_path = input_file.name
    fname = "sankey_%s.txt" % os.path.basename(input_path).split(".")[0]
    fpath = os.path.join(output_dir, fname)
    with open(fpath,"w") as f:
        f.write(txt)


if __name__ == "__main__":
    sankey()
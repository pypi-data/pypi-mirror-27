# cn_zipline

--------------



[![PyPI version](https://badge.fury.io/py/cn-zipline.svg)](https://badge.fury.io/py/cn-zipline)
[![Py version](https://img.shields.io/pypi/pyversions/cn-zipline.svg)](https://pypi.python.org/pypi/cn-zipline)
[![Build Status](https://travis-ci.org/JaysonAlbert/cn_zipline.svg?branch=master)](https://travis-ci.org/JaysonAlbert/cn_zipline)
[![Build status](https://ci.appveyor.com/api/projects/status/b0pf9nndpj65x0nj/branch/master?svg=true)](https://ci.appveyor.com/project/JaysonAlbert/cn-zipline/branch/master)


**注意：**

**`cn_zipline`项目已经迁移到更简洁易用的[zipline](https://github.com/JaysonAlbert/zipline)。此项目进度已经落后于zipline，并且将不再维护，因此带来的不便，敬请谅解。**

----------------

基于tdx的zipline bundle.

[zipline](http://zipline.io/)是美国[Quantopian](https://quantopian.com/) 公司开源的量化交易回测引擎，它使用`Python`语言开发，
部分代码使用`cython`融合了部分c语言代码。`Quantopian` 在它的网站上的回测系统就是基于`zipline`的，
经过生产环境的长期使用，已经比完善，并且在持续的改进中。

`zipline`的基本使用方法在https://www.quantopian.com/tutorials/getting-started ，对于zipline的深度解析，可以看大神[rainx](https://github.com/rainx)写的[文档](https://www.gitbook.com/book/rainx/-zipline/details)，本项目中的大部分依赖项目也都是rainx开发的项目
`

数据源
--------

`cn_zipline`的历史k线以及除息除权数据来自通达信，数据接口来自项目github 项目tdx https://github.com/JaysonAlbert/tdx

环境 
--------

python2.7或者python3.5，尽量使用较新版本的Anaconda。旧版本的在安装依赖时容易报错。推荐使用python3.5，数据获取的接口依赖于python3.5的
一些库，用于提升性能。

**注意**：Anaconda官网提供的链接，3.x版本默认下载python3.6。

分支
----------
#### `master`:
包含了基本的回测功能，下单撮合使用下一bar的close价（ricequant可选当前bar的close和下一bar的open）

#### `open_order`:
下单撮合使用下一bar的open价

#### `zipline-live`:
支持实盘功能，正在开发中，详情见[实盘issue](https://github.com/JaysonAlbert/cn_zipline/issues/2)


安装
----------

    pip install cn_zipline
**注意**：在`windows`上，如果`zipline`安装失败，先用`conda install -c Quantopian zipline`安装`zipline`,然后再安装`cn_zipline`
    
将`cn_zipline/extension.py`拷贝至zipline的数据目录,默认为`~/.zipline`


实盘
----------
实盘部分代码正在开发中，请参考[issue](https://github.com/JaysonAlbert/cn_zipline/issues/2)

 
使用
----------

cn_zipline与zipline大同小异，具体使用方法请参考zipline[官方文档](https://www.quantopian.com/tutorials/getting-started)。不同之处在于，`ingest`数据时请使用
`cn_zipline`命令，管理以及清理`bundls`数据时使用`zipline`。运行策略的形式也不同，为便于调试代码，采用直接运行策略脚本，
而**不是**通过`zipline run`命令来运行。下面是使用示例：


一、ingest数据：
-----------

    cn_zipline ingest -b tdx -a assets.csv --minute False --start 20170901 --overwrite True
    
`-a assets.csv`指定需要`ingest`的代码列表，缺省ingest 4000+只所有股票，耗时长达3、4小时，通过`-a tests/ETF.csv` 只ingest ETF基金数据，一方面可以节省时间达到快速测试的目的。
另一方面可以通过这种方法ingest非股票数据，例如etf基金。

`--minute False` 是否ingest分钟数据

`--start 20170901` 数据开始日期，默认为1991年

`--overwrite True` 由于分钟数据获取速度较慢，默认start至今超过3年的话，只拿3年数据，日线数据依然以start为准，overwrite为True时，强制拿从start开始  至今的分钟数据


二、编写策略`cn_zipline/examples/buyapply.py`：
-----------

    from zipline.api import order, record, symbol


    def initialize(context):
        pass
    
    
    def handle_data(context, data):
        order(symbol('000001'), 10)
        record(AAPL=data.current(symbol('000001'), 'price'))
    
    
    if __name__ == '__main__':
        from cn_zipline.utils.run_algo import run_algorithm
        from zipline.utils.cli import Date
        from cn_stock_holidays.zipline.default_calendar import shsz_calendar
    
        start = Date(tz='utc', as_timestamp=True).parser('2017-01-01')
    
        end = Date(tz='utc', as_timestamp=True).parser('2017-10-20')
        run_algorithm(start, end, initialize, 10e6, handle_data=handle_data, bundle='tdx',trading_calendar=shsz_calendar,output='out.pickle')
       

三、运行策略文件 `cn_zipline/examples/buyapply.py`
------------

四、运行分析脚本`cn_zipline/examples/analyse.py`
------------

问题
--------------

如有任何问题，欢迎大家提交[issue](https://github.com/JaysonAlbert/cn_zipline/issues/new) ，反馈bug，以及提出改进建议。

其它
--------------
对量化感兴趣的朋友，以及想更方便的交流朋友，请加QQ群434588628

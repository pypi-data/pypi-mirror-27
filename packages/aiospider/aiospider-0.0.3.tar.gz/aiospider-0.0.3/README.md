# AioSpider
[![Build Status](https://travis-ci.org/EINDEX/aiospider.svg?branch=master)](https://travis-ci.org/EINDEX/aiospider) 
[![PyPI](https://img.shields.io/pypi/v/aiospider.svg)]()
## 架构
### 执行单元
- 执行请求
- 失败重放
- 代理策略配置
- 账号机制
- Session 缓存机制
- 并发量限制
- 单元运行状态监测

### 队列
Redis list

### 代理池
暂无

### 数据库
- Bloom: Redis

### 任务发布/处理单元
- 统一的处理模块
- 自动分配任务
- 发布任务


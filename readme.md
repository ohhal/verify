# 打码服务整合


### 部署前准备
```sh
安装启动 redis
$ sudo apt update
$ sudo apt install redis-server
$ sudo service redis start
安装 npm
$ sudo apt install npm
$ cd verify_log_vue
$ npm --registry https://registry.npm.taobao.org install
$ cd ..
```

### 部署
```sh
修改supervisord.conf中的当前路径
$ supervisord -c supervisord.conf
```

### 查看日志

```
http://localhost:9998
```

# 接口文档

* HTTP
* 请求方式: GET,POST
* 请求地址: http://localhost:9999/verify/create
* 返回格式: JSON
* 接口功能: 创建任务，获取本次识别任务的任务id

#### 请求体
```

{
    task_id = "",
    googlekey= "",
    pageurl= "",
    action = "",
    body = "",
    methods = ""
}

```

* 请求参数说明

| 参数名称 | 参数类型 | 是否必须 | 参数描述 |
| :------- | :------- | :------- | :------- |
| task_id  | string   | 否       | 关联参数task_id |
| googlekey| string   | 否       | 网址sitekey|
| pageurl  | string   | 否       | 网址|
| action   | string   | 否       | 网址行为|
| body     | string   | 否       | 图片base64 |
| methods  | string   | 是       | 方法|



* 结果返回

>正常返回结果示例
```
{
"status": 1, 
"request": "9dc4fcb4-ab41-41a2-977c-8a3acbb01303",  
}
```

>错误返回结果示例
```
{
"status": 0, 
"request": "ERROR_WRONG_USER_KEY",  
}
```

* 返回参数说明

| 参数名称 | 参数类型 | 参数说明 |
| :------- | :------- | :------- |
| status | int | 识别结果状态码<0:表示失败，1：表示成功> |
| request | string | 识别结果<status为1时返回创建成功的任务id，否则返回具体错误内容> |

------------------------------------------------------------------

* HTTP
* 请求方式: GET,POST
* 请求地址: http://localhost:9999/verify/result
* 返回格式: JSON
* 接口功能: 根据任务id轮询获取识别结果


```
{
"id": "",
}
```

* 请求参数说明

| 参数名称 | 参数类型 | 是否必须 | 参数描述 |
| :------- | :------- | :------- | :------- |
| id   | string   | 是       | 任务id|

* 结果返回
>正常返回结果示例
```
{
"status": 1, 
"request": "03AGdBq24H9BdOCS0oFXV5_XXY2oNICReqWm2J3Onk8k6P4q4MmL8BXxvfmzyJDYTUjo_g8uhPJqH9Vm9ujZjIVonbv_zaHakebLz-blp1mH6iHe6gpKPbj17zBlHwTBkNzBBsePmZ3NWhavJ43IKPasB3q0tVTuVRU9HcRXLNxmEFn6uhdMzrR5_jDEV4z4vYCDzmBbunpaeK9X229KAtkI4g9AjsBPDk5pIPCZ-rGmRWih6dpws7SK8lytd4-7PJN5tzgiDr8rucHWDTvP_wP-36WYwELBJC5HMbzx48_Ly6CgAJ-DNlANc0PRdMgZy2FeyR4I3HHjNNpESmdxJQrL9KYgQ35GBpLCm38c2s-blxOtGYV0_tCZM68WAczVb30wqb2MOBBT-AVKZP7DScUWBEzxlritVdp4o1_ar57wWRZ92H36zzNQudesrVHH1kgSbZARUS_eUUSqhbEIqduCFKU-8BLqkQGJK_QY5Xuj4h6ax7zgDwe1Zm6jqlud1pkR4wun1vg7GKan0W-6TJXE8IgDVlMaLt9A" 
}
```

>错误返回结果示例
```
{
"status": 0, 
"request": "ERROR_WRONG_USER_KEY",  
}
```
* 返回参数说明

| 参数名称 | 参数类型 | 参数说明 |
| :------- | :------- | :------- |
| status | int | 识别结果状态码<0:表示失败，1：表示成功> |
| request | string | 识别结果 |

------------------------------------------------------------------

* HTTP
* 请求方式: POST
* 请求地址: http://localhost:9999/verify/platform
* 请求格式: JSON
* 返回格式: JSON
* 接口功能: 切换recaptcha打码平台

```
{
  "platform": ""
}
```
* 请求参数说明

| 参数名称 | 参数类型 | 是否必须 | 参数描述 |
| :------- | :------- | :------- | :------- |
| platform   | string   | 是       | 平台(twocaptcha,anti,confluence)|

* 结果返回
>正常返回结果
```
{
"code": 0, 
}
```
>错误返回结果
```
{
"code": -1, 
}
```
------------------------------------------------------------------

* HTTP
* 请求方式: GET,POST
* 请求地址: http://localhost:9999/verify/log
* 返回格式: JSON
* 接口功能: 查看日志

```
{
    "search": "",
    "date": "",
    "type": ""
}
```
* 请求参数说明

| 参数名称 | 参数类型 | 是否必须 | 参数描述 |
| :------- | :------- | :------- | :------- |
| search   | string   | 否       | 唯一id或log中的字符 |
| date   | int   | 否       | 日期<13位>|
| type   | string   | 否     | 选择查询方式<id,log>|

* 结果返回
>正常返回结果
```
{
"code": 0,
"msg": [
    {
    "id": "f32a1ff6-13e4-4eab-b56c-f4cbd9e7bca9",
    "table": "VERIFYLOG_20210203",
    "time": 1612332885593503
    }
]
}
```
------------------------------------------------------------------
import requests
proxies = "proxy.dianhua.cn"
res = requests.get("http://www.baidu.com", proxies=proxies)
print res.text
# AutoLogin

## ![introduction](https://github.com/clouduan/Flags-Ideas-Temp/blob/master/Icons/002-script.png) Introduction
部署在个人 VPS 上面，可以实现自动登录签到，实现领奖励币的目的。
- [aixinwu.py](./aixinwu.py): 自动登录[上海交大爱心屋网站](http://aixinwu.sjtu.edu.cn/index.php/home "SJTU爱心屋")，每日登录领爱心币，爱心币可以兑换东西。
- [readfree.py](./readfree.py): 登录 [readfree](http://readfree.me "readfree") 并签到，可以随机拿1-3个额度值。

## ![usage](https://github.com/clouduan/Flags-Ideas-Temp/blob/master/Icons/002-settings.png) How to use it?
#### 购买 VPS
#### 克隆库
  `git clone https://github.com/clouduan/pet-projects.git && cd pet-projects/autoLogin`
#### 自动登录aixinwu
- 建立账号信息文件 account.dat, 格式仿照 [account_sample.dat](./account_sample.dat)就行。
- 运行 `python3 ./aixinwu.py`，之后如果登录成功会在当前目录下出现 aixinwu.cookies 和 aixinwu.log 文件，以后就可以用 cookies和password 两种方式登录了。
    
#### 自动登录readfree
- 新建文件 readfree.cookies, 然后通过浏览器获取cookies，并写到该文件里。没办法readfree的验证码很难搞，只能人工获取cookies。
- 关于 cookies 的写入格式，在[readfree.py](./readfree.py)文件里有个 `process_cookies` 函数，可以参照其函数说明，自己复制代码搞搞。
- 运行 `python3 ./readfree.py`，由于没加 log 功能，所以你可以从 readfree.cookies 文件的更新与否来查看是否成功登录，或者去 readfree 网站去看自己的登录情况。
#### 利用 linux 系统 `crontab`函数实现定时执行。
- 先给以上脚本赋予执行权限

`sudo chmod +x ./aixinwu.py ./readfree.py`

- 执行`crontab -e`进行编辑，crontab的格式可以参考[ crontab 定时任务](http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html#crontab)。比如我的设置就是
```
3 31 0,12 * * * python3 /root/autoLogin/readfree.py
24 31 0,12 * * * python3 /root/autoLogin/aixinwu.py
```

## ![how](https://github.com/clouduan/Flags-Ideas-Temp/blob/master/Icons/002-atom.png) How does it work?

- 自动登录aixinwu: 网页跳转全部采用 python 实现，其中验证码识别采用第三方网站接口，第一次登录时会把cookies，存储在本地。登录时优先选择cookies方式，如果cookies找不到或者cookies登录失败会继续选择账号密码登录。
- 自动登录readfree: 这个网站的验证码很难搞。需要人工添加cookies，每次登录都是cookies登录，一般能保持好长时间。

## ![todo](https://github.com/clouduan/Flags-Ideas-Temp/blob/master/Icons/002-contract.png) Todo

- [ ] readfree 的log功能
- [ ] readfree 的cookies处理用运行参数的方式实现
- [ ] aixinwu-login 的验证码本地识别

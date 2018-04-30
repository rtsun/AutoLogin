# readfree

以下两种方法选择一种即可：
## 使用方法1
- 在 config.py 里填入自己的账号和密码。
- 运行 readfree.py, 会在当前文件夹下生成验证码图片，此时需要手动输入验证码。
- 登录成功会在当前文件夹下生成 readfree.cookies 文件，以后就可以用 cookies 直接登录了。

## 使用方法2
- 用浏览器登录 [readfree.me](http://readfree.me) 在浏览器里获取 cookies，共有两个值，复制粘贴到 config.py 文件里相应的位置。
- 运行 readfree.py, 如果登录成功会在当前文件夹下生成 readfree.cookies 文件，以后就可以用 cookies 直接登录了。

## 实现方法
这个网站的验证码很难搞。需要人工添加 cookies，每次登录都是 cookies 登录，一般能保持好长时间。

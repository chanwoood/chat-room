# Socket 实现多人聊天室

## 效果图



![录制_2018_06_28_22_05_46_602.gif | center | 827x495](https://cdn.yuque.com/yuque/0/2018/gif/104735/1530194853242-07f66683-2782-455f-8a6a-09f7d8160ff9.gif "")



## 说明

这是我的 Python 课程设计。

所使用的技术有：

* 客户端多线程，可以一边发信息，亦可一边收信息。
* 服务器 select 模型，可以用单个线程处理多个客户端。

在此，不得不提垃圾 Windows，本来客户端也可用 select 模型，单个线程总比多线程节省资源。但是客户端命令行下输入信息用不了 select 模型，Unix 就没有这个问题。[官网](https://docs.python.org/3/library/select.html?highlight=select#select.select)上是这样说的，重点看画红线部分：



![image.png | left | 827x559](https://cdn.yuque.com/yuque/0/2018/png/104735/1530193177827-bfcd6977-e1be-487f-9724-2b93443d88fb.png "")


关于 select 与多线程的区别，可以看我这篇文章：[https://96chh.github.io/2018/04/14/socket/](https://96chh.github.io/2018/04/14/socket/)

## 使用方法

* 把 server.py 放到你的服务器上（放到本地也行），运行。
* client.py 在本地运行。

在 client.py 中：

```python
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('107.175.115.87', 6666))
    except Exception:
        print('服务器还没开！')
```

把地址 107.175.115.87 改成你的服务器地址，如果在本地运行，就改为：127.0.0.1 。


## 其他

本来想用 PyQt 来搞个用户界面，试了一下，失败了，我只想说 Qt 的多线程真的蛋疼，不能用另一个线程更新 UI，需要发射信号，再 connect 到更新 UI 的函数，但是莫名其妙地失败了，至今都搞不懂这梗。


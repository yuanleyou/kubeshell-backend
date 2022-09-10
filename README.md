# kubeshell-backend

<h3>简介</h3>

  一个集成了终端页面,后端整条kubernetes调动的组件,可以实现pod在web页面的连接,方便各位大佬的使用,二次开发和集成项目,通过url的方式识别和连接pod容器,不需要侵入到k8s环境中,可在kubernetes外部部署使用,

<h3>演示</h3>

![image](https://img-blog.csdnimg.cn/20201224183506387.gif#pic_center)
  
<h3>环境说明</h3>

    centos7.3+
    python==3.9.5
    Django==3.2.14
    kubernetes==1.18.x
    channels==3.0.5
    

<h3>启动服务</h3>

    1.将用于连接Kubernetes的config文件放到当前路径，代码中为ysr-kubeconfig
    
    4.进入到目录中启动运行服务
    python3 manage.py runserver 0.0.0:8092  
 

<h3>访问方式</h3>
    
    该项目为前后端分离，前端：https://github.com/yuanleyou/kubeshell-frontend
    启动前端后访问：http://localhost:3000/?pod=nginx-test&container=nginx-test&namespace=default
    这里根据自己集群中的pod修改访问路由


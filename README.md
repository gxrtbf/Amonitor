# Amonitor

描述：用于日常运营数据的监控（也可用于提供对外数据api）的基本框架结构  
基于RiskMonitor的升级版本，相比RiskMonitor的优势：  
1、实现了前端和后端的分离  
2、实现了前端和数据的分离  
3、实现了数据的双重安全验证（web用户认证、数据接口认证），其实主要还是接口认证  
4、数据接口化，可向外提供数据api  

Amonitor结构图：  
![image](https://github.com/gxrtbf/notebook/blob/master/AMonitor%E6%A1%86%E6%9E%B6.png)

相关技术细节（粗细节）描述：  
1、前端web---django  
  django+html+js+bootstrap  
2、数据接口---django/django rest framework  
  所有数据都在存放数据库里  
3、数据库同步（结构同步、数据同步）---本地数据库与服务器数据库之间

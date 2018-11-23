import numpy as np 
  
class Perceptron(object): 
  ''''' 
  输入参数： 
  eta:学习率，在0~1之间,默认为0.01 
  n_iter:设置迭代的次数,默认为10 
  属性： 
  w_:一维数组，模型的权重 
  errors_:列表，被错误分类的数据 
  '''
  #初始化对象 
  def __init__(self,eta=0.01,n_iter=10): 
    self.eta = eta 
    self.n_iter = n_iter 
  #根据输入的x和y训练模型 
  def fit(self,x,y): 
    #初始化权重 
    self.w_ = np.zeros(1 + x.shape[1]) 
    #初始化错误列表 
    self.errors_=[] 
    #迭代输入数据，训练模型 
    for _ in range(self.n_iter): 
      errors = 0
      for xi,target in zip(x,y): 
        #计算预测与实际值之间的误差在乘以学习率 
        update = self.eta * (target - self.predict(xi)) 
        #更新权重 
        self.w_[1:] += update * xi 
        #更新W0 
        self.w_[0] += update * 1
        #当预测值与实际值之间误差为0的时候,errors=0否则errors=1 
        errors += int(update != 0) 
      #将错误数据的下标加入到列表中 
      self.errors_.append(errors) 
    return self
  #定义感知器的传播过程 
  def net_input(self,x): 
    #等价于sum(i*j for i,j in zip(x,self.w_[1:])),这种方式效率要低于下面 
    return np.dot(x,self.w_[1:]) + self.w_[0] 
  #定义预测函数 
  def predict(self,x): 
    #类似于三元运算符，当self.net_input(x) >= 0.0 成立时返回1，否则返回-1 
    return np.where(self.net_input(x) >= 0.0 , 1 , -1) 




aopen

 self.price
 self.direction
 self.number
 self.status
 self.profit

 for i in range(24,len(upper)):
     compare=upper[i]
     for i in range(aopen(where aopen.status=1).count()):
      if (compare>aopen.price*1.02 or compare<aopen.price*0.99):
        self.profit=(compare-aopen.price)*10
        self.status=0
      
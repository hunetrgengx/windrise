class gambler():
    def __init__(self):
        self.deposit = 1000000  # 百万存款，这里不考虑不动产
        self.bet = 20000  # 赌资
        self.usury = 0  # 借贷
        self.lose = 0  # 连输局数
Cathala = gambler()#赌博商人卡达拉Cathala.bet = 100000000Cathala.deposit = 100000000
Geralt = gambler()#Geralt是一名狂热的赌博爱好者
bet = 1000#每一把1000块count = 0gambling_list = []#记录每局比赛的输赢
def gambling(gambler_a,gambler_b,bet,count):
#a是庄家，b是闲家，bet是当局赌注，count是当前的赌局编号
    point = random.randint(2, 12)  # 骰子点数
    guess = random.randint(0, 1)  # 猜大小，0为小，1为大
    if (point > 7 and guess == 1) or (point <= 7 and guess == 0):  # 猜对了
        Geralt.bet += bet
        Cathala.bet -= bet        
        return True
    else:
        Geralt.bet -= bet
        Cathala.bet += bet        
        return False
    
def One_day_gambling():
    Geralt.bet = 20000
    bet = 1000
    count = 0
    while True:
        gambling_list.append(gambling(Cathala, Geralt, bet,  count))
        count += 1
        if count > 3 and gambling_list[count - 3] == gambling_list[count - 2] == gambling_list[count - 1] == False:
            bet = bet * 1.5
#连输三局加赌注，加完之后如果还输继续加，赢了赌注保持不变
        if Geralt.bet <= -5000 or count >= 100:
#每天最多只敢借五千的高利贷，每天最多100局，其实大部分都玩不到100局就输光了
            break
    return Geralt.bet-20000#返回每天独居结束时的负债或盈利

def record_daily_gambling():
    debt = []#记录每一天的最终盈亏                                                                             
    for i in range(3000):
        n = One_day_gambling()        
        if n<0:
           #小于零就要借高利贷了，计一天的利息
            n = n*1.00167
        debt.append(n)        
        if sum(debt) <= -1000000:#一百万输光算破产
            return (sum(debt),i)
            #破产后记下最终输掉的资金，以及破产时间
    return (sum(debt),3000)#一直没有破产的人def main():
    every_example = pd.DataFrame()
    lost_money = []
    bankrupt_time = []    
    for j in range(1000):
        m = record_daily_gambling()
        lost_money.append(m[0])
        bankrupt_time.append(m[1])
        print(j)
    every_example['lost_money'] = lost_money
    every_example['bankrupt_time'] = bankrupt_time
    every_example.to_csv('experiment_data.csv',index=False,sep=',')
if __name__ == "__main__":
main()



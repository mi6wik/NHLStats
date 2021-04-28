
from AnalyzeClass import stats as AC
from AnalyzeClass import plot_compare as pc
import get_hockey as hky
BB = AC(2020, "Boston Bruins",True)
BB9 = AC(2019, "Boston Bruins",True)
jdb9 = AC(2019, "Jake DeBrusk")
pas1 = AC(2020, "David Pastrnak")
pas2 = AC(2019, "David Pastrnak")
bm1 = AC(2020, "Brad Marchand")
bm2 = AC(2019, "Brad Marchand")

#a = jdb2.retrive_pickle() 


test = [[BB, BB9],
       [pas1, pas2],
        [bm1, bm2]]

pc(test)




# for i in range(0,len(a)):
#     print(a[i]['gameData']['datetime']['dateTime'])
#     print(a[i]['gameData']['teams']['away']['shortName'])
#     print(a[i]['gameData']['teams']['home']['shortName'])      

#hky.get_latest('2020')
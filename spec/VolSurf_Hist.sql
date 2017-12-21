
select TDaysToExp TDTE, Strike, avg(ImpliedVol) IV, avg(StockPriceAdj) sPx
from tblOptionHistory
where TradeDate = '5/15/17'
and Symbol = 'SPY'
and ESSRoot = ''
and TDaysToExp > 0
and ImpliedVol > 0
group by TDaysToExp, Strike
order by TDaysToExp, Strike


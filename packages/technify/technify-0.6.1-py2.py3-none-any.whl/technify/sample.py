from stock import Stock
import yfm
import quandl

if __name__ == "__main__":
    y = yfm.fetcher()
    sans = y.getTicker("san.mc")

    datausd = quandl.get("BCHARTS/KRAKENUSD")
    datausd = datausd[datausd.Close != 0]
#
  #  dataeur = quandl.get("BCHARTS/KRAKENEUR")
   # eurdlr = quandl.get("ECB/EURUSD")
    s = Stock(sans, o="Open", c="Close",h="High", l="Low", indexIsDate=False)\
        .addMa(50)\
        .addMa(200)\
        .show("c")
        #.append(datausd.Close / dataeur.Close, "bit")\
        #.append(eurdlr.Value, "eurdlr")
    #s.addCrossover("ma50", "ma200", "maCross")
   #s.show("bit", "eurdlr")
    #s.show("ma50", "ma200", "c", "maCross")

    usdbit = Stock.fromQuandl("BCHARTS/KRAKENEUR")
    usdbit.show("c")



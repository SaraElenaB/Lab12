from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    # ----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllYears():

        conn = DBConnect.get_connection()
        cursor = conn.cursor( dictionary=True )
        ris=[]

        query= """ select distinct year(gds.`Date`) as anno
                   from go_daily_sales gds 
                   order by anno ASC """

        cursor.execute(query,)

        for row in cursor:
            ris.append( row["anno"] )

        cursor.close()
        conn.close()
        return ris

    # ----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNazioni():

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris = []

        query = """ select distinct gr.Country as nazione
                    from go_retailers gr   """

        cursor.execute(query)

        for row in cursor:
            ris.append( row["nazione"] )

        cursor.close()
        conn.close()
        return ris

    # ----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNodes( nazione):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris = []

        query = """ select *
                    from go_retailers gr 
                    where gr.Country = %s """

        cursor.execute(query, (nazione,) )

        for row in cursor:
            ris.append( Retailer(**row) )

        cursor.close()
        conn.close()
        return ris

    # ----------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesWeight(anno, idRetailer1, idRetailer2):

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        ris = []

        query = """ select count( distinct gds1.Product_number) as peso
                    from go_daily_sales gds1 , go_daily_sales gds2
                    where  year(gds1.`Date`) = %s 
                    and year(gds1.`Date`) = year(gds2.`Date`)
                    and gds1.Product_number = gds2.Product_number
                    and gds1.Retailer_code = %s
                    and gds2.Retailer_code = %s
                    having peso >= 1 """
                    #ricordati distinct!!!!!

        cursor.execute(query, (anno, idRetailer1, idRetailer2))

        for row in cursor:
            ris.append( row["peso"] )

        cursor.close()
        conn.close()
        return ris
    #----------------------------------------------------------------------------------------------------------------------------------

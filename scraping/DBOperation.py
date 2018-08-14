import pyodbc
import io
import Config
import logging as logger
import string
import pandas as objPandas
import mysql.connector
import mysql

class DBOperation():
    
    def SaveDictionaryIntoMySQLDB(self,dicData):
        try:
            cnx = mysql.connector.connect(user='root', password='secret', host='127.0.0.1', database='watchpoint',use_pure=False)
            cursor = cnx.cursor()
            
            # Insert Product
            query = ("INSERT INTO Product "
               "(EAN, Name, Image_URL) "
               "VALUES ('%s', '%s', '%s')" 
               % (
                   dicData['EAN'],
                   dicData['ProductName'],
                   dicData['ImageURL']
                )
            )
            cursor.execute(query)

            # Insert Bol Price
            query = ("INSERT INTO Price "
               "(Shop_Id, Product_EAN, Value) "
               "VALUES (%d, '%s', '%s')" 
               % (
                   1,
                   dicData['EAN'],
                   dicData['BolPrice'],
                )
            )
            cursor.execute(query)

             # Insert Krëfel Price
            if dicData['KrefelPrice']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value) "
                "VALUES (%d, '%s', '%s')" 
                % (
                    2,
                    dicData['EAN'],
                    dicData['KrefelPrice'],
                    )
                )
                cursor.execute(query)

             # Insert Megekko Price
            if dicData['MegekkoPrice']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value) "
                "VALUES (%d, '%s', '%s')" 
                % (
                    3,
                    dicData['EAN'],
                    dicData['MegekkoPrice'],
                    )
                )
                cursor.execute(query)

            cnx.commit()
            cursor.close()
            cnx.close()
        except Exception as err:
            # Update prices on duplicate entry
            if "Duplicate entry" in str(err):
                print("Product already exists.")
                # print("Product already exists. Updating prices...")
                # cnx = mysql.connector.connect(user='root', password='secret', host='127.0.0.1', database='watchpoint',use_pure=False)
                # cursor = cnx.cursor()
                # query = ("UPDATE PriceComparisonBetweenSites "
                #             "SET Title = '%s' , Price = '%s', KreFelPrice = '%s', MegekkoPrice = '%s' "
                #             "WHERE EAN = %s" % (dicData[0], dicData[2], dicData[3], dicData[4], dicData[1]))
                # cursor.execute(query)
                # cnx.commit()
                # cursor.close()
                # cnx.close()
            else:
                logger.error("Error in DBOperations:SaveDictionaryIntoMySQLDB Function: "+str(err))
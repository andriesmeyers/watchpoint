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
            cursor = cnx.cursor(buffered=True)

            # Get Category
            if dicData['Categories']:
                category = dicData['Categories'][0].get_text().replace("'", r"\'")

                query = ("INSERT IGNORE INTO Category "
                    "SET Name = '%s'" % (category))
                cursor.execute(query)
                query = ("SELECT Id FROM Category "
                    "WHERE Name = '%s'" % (category))
                cursor.execute(query)
                result_set = cursor.fetchone()
                Category_Id = result_set[0]
            try: 
                # Insert Product
                query = ("INSERT INTO Product "
                "(EAN, Name, Image_URL, Category_Id) "
                "VALUES ('%s', '%s', '%s', '%d')" 
                % (
                    dicData['EAN'],
                    dicData['ProductName'],
                    dicData['ImageURL'],
                    Category_Id
                    )
                )
                cursor.execute(query)
            except Exception as err:
                # Update prices on duplicate entry
                if "Duplicate entry" in str(err):
                    print("Product already exists. Updating prices")

                    # # TODO: Create generic method
                    # # Update Bol
                    # if dicData['BolPrice']:
                    #     query = ("UPDATE Price "
                    #             "SET Value = %s "
                    #             "WHERE shop_Id = 1 AND Product_EAN = '%s'" % (dicData['BolPrice'], dicData['EAN']))
                        
                    #     cursor.execute(query)

                    # # Update Krefel
                    # if dicData['KrefelPrice']:
                    #     query = ("UPDATE Price "
                    #             "SET Value = %s "
                    #             "WHERE shop_Id = 2 AND Product_EAN = '%s'" % (dicData['KrefelPrice'], dicData['EAN']))

                    #     cursor.execute(query)
                    
                    # cursor.execute(query)

                    # # Update Megekko
                    # if dicData['MegekkoPrice']:
                    #     query = ("UPDATE Price "
                    #         "SET Value = %s "
                    #         "WHERE shop_Id = 3 AND Product_EAN = '%s'" % (dicData['MegekkoPrice'], dicData['EAN']))
                    #     cursor.execute(query)

                    # # Update Art & Craft
                    # if dicData['ArtandCraftPrice']:
                    #     print(dicData['ArtandCraftPrice'])
                    #     query = ("UPDATE Price "
                    #             "SET Value = %s "
                    #             "WHERE shop_Id = 4 AND Product_EAN = '%s'" % (dicData['ArtandCraftPrice'], dicData['EAN']))
                        
                    #     cursor.execute(query)
                else:
                    logger.error("Error in DBOperations:SaveDictionaryIntoMySQLDB Function: "+str(err))
            
            # Insert Bol Price
            query = ("INSERT INTO Price "
            "(Shop_Id, Product_EAN, Value) "
            "VALUES (%d, '%s', %s) " 
            "ON DUPLICATE KEY UPDATE Value = %s"
            % (
                1,
                dicData['EAN'],
                dicData['BolPrice'],
                dicData['BolPrice'],
                )
            )
            cursor.execute(query)

            # Insert Krëfel Price
            if dicData['KrefelPrice']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value) "
                "VALUES (%d, '%s', %s) "
                "ON DUPLICATE KEY UPDATE Value = %s"
                % (
                    2,
                    dicData['EAN'],
                    dicData['KrefelPrice'],
                    dicData['KrefelPrice'],
                    )
                )
                cursor.execute(query)

            # Insert Megekko Price
            if dicData['MegekkoPrice']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value) "
                "VALUES (%d, '%s', %s) " 
                "ON DUPLICATE KEY UPDATE Value = %s"
                % (
                    3,
                    dicData['EAN'],
                    dicData['MegekkoPrice'],
                    dicData['MegekkoPrice'],
                    )
                )
                cursor.execute(query)
                
            # Insert Art & Craft Price
            if dicData['ArtandCraftPrice']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value) "
                "VALUES (%d, '%s', %s) " 
                "ON DUPLICATE KEY UPDATE Value = %s"
                % (
                    4,
                    dicData['EAN'],
                    dicData['ArtandCraftPrice'],
                    dicData['ArtandCraftPrice'],
                    )
                )
                cursor.execute(query)

            cnx.commit()
            cursor.close()
            cnx.close()

        except Exception as err:
            if "Duplicate entry" in str(err):
                ## dismiss
                pass
            else:
                logger.error("Error in DBOperations:SaveDictionaryIntoMySQLDB Function: "+str(err))
import sys
import os
import pyodbc
import io
import Config
import logging
import string
import pandas as objPandas
import mysql.connector
import mysql

class DBOperation():
    
    def SaveDictionaryIntoMySQLDB(self,dicData):
        try:
            cnx = mysql.connector.connect(user='root', password='secret', host='127.0.0.1', database='watchpoint',use_pure=False)
            cursor = cnx.cursor(buffered=True)

            # Insert Category
            if dicData['Categories']:
                category = dicData['Categories'][0].get_text().replace("'", r"\'")
                print("Category:")
                print(category)

                query = ("INSERT IGNORE INTO Category "
                    "SET Name = '%s'" % (category))
                cursor.execute(query)
                query = ("SELECT Id FROM Category "
                    "WHERE Name = '%s'" % (category))
                cursor.execute(query)
                result_set = cursor.fetchone()
                Category_Id = result_set[0]
            
            # Insert Product
            query = ("INSERT INTO Product "
            "(EAN, Name, Description, Image_URL, Category_Id) "
            "VALUES ('%s', '%s', '%s', '%s', '%d') " 
            "ON DUPLICATE KEY UPDATE Description = '%s'"
            % (
                dicData['EAN'],
                dicData['ProductName'],
                dicData['Description'],
                dicData['ImageURL'],
                Category_Id,
                dicData['Description']
                )
            )
            cursor.execute(query)
           
            # no rows affected
            if(cursor.rowcount == 0):
                print("Product already exists. Updating prices")

             # Insert Specs
            if dicData['Specs']:
                for title, value in dicData['Specs'].items():
                    # print("%s:%s" % (title, value))
                    if title is not None and value is not None:
                        query = ("INSERT IGNORE INTO specification "
                        "SET Name = '%s'" % (title))
                        cursor.execute(query)

                        query = ("SELECT Id FROM Specification "
                            "WHERE Name = '%s'" % (title))
                        cursor.execute(query)
                        result_set = cursor.fetchone()
                        Spec_Id = result_set[0]

                        query = ("INSERT INTO product_specification "
                            "(Specification_Id, Product_EAN, Value) "
                            "VALUES (%d, '%s', '%s')"
                        % (
                            Spec_Id,
                            dicData['EAN'],
                            value
                            )
                        )
                        cursor.execute(query)

            # Insert Bol Price
            query = ("INSERT INTO Price "
            "(Shop_Id, Product_EAN, Value, URL) "
            "VALUES (%d, '%s', %s, '%s') " 
            "ON DUPLICATE KEY UPDATE Value = %s, URL = '%s'"
            % (
                1,
                dicData['EAN'],
                dicData['Bol']['price'],
                dicData['Bol']['url'],
                dicData['Bol']['price'],
                dicData['Bol']['url']
                )
            )
            cursor.execute(query)

            # Insert Krëfel Price
            if dicData['Krefel']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value, URL) "
                "VALUES (%d, '%s', %s, '%s') "
                "ON DUPLICATE KEY UPDATE Value = %s, URL = '%s'"
                % (
                    2,
                    dicData['EAN'],
                    dicData['Krefel']['price'],
                    dicData['Krefel']['url'],
                    dicData['Krefel']['price'],
                    dicData['Krefel']['url']
                    )
                )
                cursor.execute(query)

            # Insert Megekko Price
            if dicData['Megekko']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value, URL) "
                "VALUES (%d, '%s', %s, '%s') " 
                "ON DUPLICATE KEY UPDATE Value = %s, URL = '%s'"
                % (
                    3,
                    dicData['EAN'],
                    dicData['Megekko']['price'],
                    dicData['Megekko']['url'],
                    dicData['Megekko']['price'],
                    dicData['Megekko']['url']
                    )
                )
                cursor.execute(query)
                
            # Insert Art & Craft Price
            if dicData['ArtandCraft']:
                query = ("INSERT INTO Price "
                "(Shop_Id, Product_EAN, Value, URL) "
                "VALUES (%d, '%s', %s, '%s') " 
                "ON DUPLICATE KEY UPDATE Value = %s, URL = '%s'"
                % (
                    4,
                    dicData['EAN'],
                    dicData['ArtandCraft']['price'],
                    dicData['ArtandCraft']['url'],
                    dicData['ArtandCraft']['price'],
                    dicData['ArtandCraft']['url']
                    )
                )
                cursor.execute(query)

            cnx.commit()
            cursor.close()
            cnx.close()

        except Exception as error:
            if "Duplicate entry" in str(error):
                # dismiss
                pass
            else:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                logging.error('Error in DBOperation file!'+str(error.args))
                logging.error('Line number: '+ str(exc_tb.tb_lineno))
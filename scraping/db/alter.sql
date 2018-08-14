DELETE FROM product;
DELETE FROM price;

INSERT INTO product (Id, Name, EAN) 
SELECT ID, Title, EAN from pricecomparisonbetweensites;

INSERT INTO price (Product_Id, Shop_Id, value)
SELECT ID, 1, Price from pricecomparisonbetweensites;

INSERT INTO price (Product_Id, Shop_Id, value)
SELECT ID, 2, KreFelPrice from pricecomparisonbetweensites
WHERE KreFelPrice is NOT NULL;

INSERT INTO price (Product_Id, Shop_Id, value)
SELECT ID, 3, MegekkoPrice from pricecomparisonbetweensites
WHERE MegekkoPrice is NOT NULL;
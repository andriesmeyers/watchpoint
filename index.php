<?php 
include 'Models/Database.php';
$db = Database::getInstance();
$mysqli = $db->getConnection(); 
$sql_query = 
    "SELECT Product.Name, Product.Image_URL, Product.EAN, MIN(Value) AS Lowest_price FROM Product "
    . "LEFT JOIN Price "
    . "ON Product.EAN = Price.Product_EAN "
    . "WHERE Price.URL IS NOT NULL AND Price.Value > 0 "
    . "GROUP BY Product.EAN "
    . "ORDER BY Product.View_count DESC "
    . "LIMIT 5";

$products = $mysqli->query($sql_query);
$sql_query = 
    "SELECT Image_URL, Category.* FROM product "
    . "LEFT JOIN Category "
    . "ON product.Category_Id = Category.Id "
    . "WHERE Parent_Id IS NOT NULL "
    . "GROUP BY Category.Id "
    . "ORDER BY Category.View_count DESC "
    . "LIMIT 4";

$categories = $mysqli->query($sql_query);
require('_layout/head.php');
?>

  <h1 class="mb-1">Vergelijk</h1>
  <h3>Producten, prijzen en shops</h3>
  <div class="row products-highlighted">
    <div class="col-lg-6 col-xs-12 main-product-row">
        <?php $product = $products->fetch_assoc();?>
        <div class="main-product">
            <div class="product-details text-left">
                <h5 class="product-title">
                    <a href="product.php<?php echo "?ean=" . $product['EAN'];?>">
                            <?php
                                $tokens = explode(" ", $product['Name']);
                                $sub = implode(" ", array_splice($tokens, 0, 4));
                                echo $sub;
                            ?>
                    </a>
                </h5>
                <span class="text-uppercase text-secondary">Vanaf</span>
                <h1 class="product-price mb-0">€<?php echo $product['Lowest_price'];?></h1>
            </div>
            <div class="image-container">
                <img src="<?php echo $product['Image_URL'];?>" alt="" width="200px">
            </div> 
        </div>
    </div>
    <div class="col-lg-6 col-xs-12">
      <div class="row side-products-row">
        <div class="col-lg-6 col-xs-6">
            <?php $product = $products->fetch_assoc();?>
            <div class="side-product">
                <div class="product-details text-left">
                    <h5 class="product-title">
                        <a href="product.php<?php echo "?ean=" . $product['EAN'];?>">
                            <?php
                                $tokens = explode(" ", $product['Name']);
                                $sub = implode(" ", array_splice($tokens, 0, 4));
                                echo $sub;
                            ?>
                        </a>
                    </h5>
                    <span class="text-uppercase text-secondary">Vanaf</span>
                    <h1 class="product-price mb-0">€<?php echo $product['Lowest_price'];?></h1>
                </div>
                <div class="image-container">
                    <img src="<?php echo $product['Image_URL'];?>" alt="" width="100px">
                </div> 
            </div>
        </div>
        <div class="col-lg-6 col-xs-6">
            <?php $product = $products->fetch_assoc();?>
            <div class="side-product">
                <div class="product-details text-left">
                    <h5 class="product-title">
                        <a href="product.php<?php echo "?ean=" . $product['EAN'];?>">
                            <?php
                                $tokens = explode(" ", $product['Name']);
                                $sub = implode(" ", array_splice($tokens, 0, 4));
                                echo $sub;
                            ?>
                        </a>
                    </h5>
                    <span class="text-uppercase text-secondary">Vanaf</span>
                    <h1 class="product-price mb-0">€<?php echo $product['Lowest_price'];?></h1>
                </div>
                <div class="image-container">
                    <img src="<?php echo $product['Image_URL'];?>" alt="" width="100px">
                </div> 
            </div>
        </div>
      </div>
      <div class="row side-products-row">
        <div class="col-lg-6 col-xs-6">
            <?php $product = $products->fetch_assoc();?>
            <div class="side-product">
                <div class="product-details text-left">
                    <h5 class="product-title">
                        <a href="product.php<?php echo "?ean=" . $product['EAN'];?>">
                            <?php
                                $tokens = explode(" ", $product['Name']);
                                $sub = implode(" ", array_splice($tokens, 0, 4));
                                echo $sub;
                            ?>
                        </a>
                    </h5>
                    <span class="text-uppercase text-secondary">Vanaf</span>
                    <h1 class="product-price mb-0">€<?php echo $product['Lowest_price'];?></h1>
                </div>
                <div class="image-container">
                    <img src="<?php echo $product['Image_URL'];?>" alt="" width="100px">
                </div> 
            </div>
        </div>
        <div class="col-lg-6 col-xs-6">
            <?php $product = $products->fetch_assoc();?>
            <div class="side-product">
                <div class="product-details text-left">
                    <h5 class="product-title">
                        <a href="product.php<?php echo "?ean=" . $product['EAN'];?>">
                            <?php
                                $tokens = explode(" ", $product['Name']);
                                $sub = implode(" ", array_splice($tokens, 0, 4));
                                echo $sub;
                            ?>
                        </a>
                    </h5>
                    <span class="text-uppercase text-secondary">Vanaf</span>
                    <h1 class="product-price mb-0">€<?php echo $product['Lowest_price'];?></h1>
                </div>
                <div class="image-container">
                    <img src="<?php echo $product['Image_URL'];?>" alt="" width="100px">
                </div> 
            </div>
        </div>
      </div>
      
    </div>
  </div>
  <div class="row mt-4 categories-highlighted">
      <div class="col-lg-3 col-md-6 col-xs-12">
        <?php $category = $categories->fetch_assoc();?>
          <div class="category-highlighted">
            <div class="category-item-container">
              <a href="category.php<?php echo "?category=" . urlencode($category['Name']);?>">
                <h4 class="font-weight-bold pl-1 mt-3 text-uppercase"><?php echo $category['Name'];?></h4>
                <div class="category-image-container" style="background: url('<?php echo $category['Image_URL'];?>')" >
                </div>
              </a>
            </div>
          </div>
      </div>
      <div class="col-lg-3 col-md-6 col-xs-12">
          <?php $category = $categories->fetch_assoc();?>
          <div class="category-highlighted">
            <div class="category-item-container">
              <a href="category.php<?php echo "?category=" . urlencode($category['Name']);?>">
                <h4 class="font-weight-bold pl-1  mt-3 text-uppercase"><?php echo $category['Name'];?></h4>
                <div class="category-image-container" style="background: url('<?php echo $category['Image_URL'];?>')" >
                </div>
              </a>
            </div>
          </div>
      </div>
      <div class="col-lg-3 col-md-6 col-xs-12">
      <?php $category = $categories->fetch_assoc();?>
      <div class="category-highlighted">
            <div class="category-item-container">
              <a href="category.php<?php echo "?category=" . urlencode($category['Name']);?>">
                <h4 class="font-weight-bold pl-1 mt-3 text-uppercase"><?php echo $category['Name'];?></h4>
                <div class="category-image-container" style="background: url('<?php echo $category['Image_URL'];?>')" >
                </div>
              </a>
            </div>
          </div>
      </div>
      <div class="col-lg-3 col-md-6 col-xs-12">
      <?php $category = $categories->fetch_assoc();?>
      <div class="category-highlighted">
            <div class="category-item-container">
              <a href="category.php<?php echo "?category=" . urlencode($category['Name']);?>">
                <h4 class="font-weight-bold pl-1 mt-3 text-uppercase"><?php echo $category['Name'];?></h4>
                <div class="category-image-container" style="background: url('<?php echo $category['Image_URL'];?>')" >
                </div>
              </a>
            </div>
          </div>
      </div>
  </div>

<?php
require('_layout/footer.php');
?>
<?php 
include 'Models/Database.php';
session_start();
try{
  $db = Database::getInstance();
  $mysqli = $db->getConnection();
  if(isset($_GET['ean'])){
      $product = mysqli_escape_string($mysqli, $_GET['ean']);
      $_SESSION['EAN'] = $product;
  }
  $product = $_SESSION['EAN'];
  $orderBy = "Price.Value ASC";
  if(isset($_POST['select-sort'])){
      switch($_POST['select-sort']){
          case 'price_asc':
              $orderBy = 'Price.Value ASC';
              break;
          case 'price_desc':
              $orderBy = 'Price.Value DESC';
              break;
          case 'name_asc':
              $orderBy = 'Shop.Name ASC';
              break;
          case 'name_desc':
              $orderBy = 'Shop.Name DESC';
              break;
          default:
              $orderBy = 'Price.Value ASC';
      }
  }
  $query = 
    "SELECT Product.Name AS ProductName, Product.EAN, Product.Image_URL, Product.Description, Shop.Name AS ShopName, Price.Value, Price.URL FROM Product "
    . "LEFT JOIN Price "
    . "ON EAN = Product_EAN "
    . "LEFT JOIN Shop "
    . "ON Price.Shop_Id = Shop.Id "
    . "WHERE EAN = " . "'$product' AND Price.URL IS NOT NULL "
    . "ORDER BY $orderBy";

  $products = $mysqli->query($query);
  
  $query = 
    "SELECT specification.Name, product_specification.value FROM product_specification "
    . "LEFT JOIN specification "
    . "ON specification.id = product_specification.specification_Id "
    . "WHERE product_EAN = " . "'$product'";

  $specs = $mysqli->query($query);

}catch(Exception $e){
  echo 'Caught exception: ' . $e->getMessage() . "\n";
}
require('_layout/head.php');
?>
<div class="product-header">
    <div class="row">
        <div class="col-3">
            <div class="product-image-container">
                <img src="<?php echo $products->fetch_assoc()['Image_URL']; $products->data_seek(0); ?>">
            </div>
        </div>
        <div class="col-9"><h1><?php echo $products->fetch_assoc()['ProductName']; $products->data_seek(0);?></h1></div>
    </div>
</div>
<div class="row">
    <table class="table shop-table">
      <thead>
        <tr>
          <td class="border-0"><?php echo $products->num_rows;?> winkel(s)</td>
          <td class="border-0 text-right" colspan="2">
              <form  id="formShopSort" action="product.php" method="post">
                    <div class="row">
                        <div class="col-7 offset-5">
                            <div class="form-group">
                                <label for="selectSort">Sorteren op:</label>
                                <select class="form-control" name="select-sort" id="selectShopSort">
                                    <option value="price_asc" <?php if($orderBy=='Price.Value ASC') echo 'selected';?>>Prijs (oplopend)</option>
                                    <option value="price_desc" <?php if($orderBy=='Price.Value DESC') echo 'selected';?>>Prijs (aflopend)</option>
                                    <option value="name_asc" <?php if($orderBy=='Shop.Name ASC') echo 'selected';?>>Naam (oplopend)</option>
                                    <option value="name_desc" <?php if($orderBy=='Shop.Name DESC') echo 'selected';?>>Naam (aflopend)</option>
                                </select>
                            </div>
                        </div>
                    </div>
              </form>
            </td>
        </tr>
      </thead>
      <tbody>
      <?php while ($row = $products->fetch_assoc()){ ?>
        <tr>
          <td class="shop-name"><?php echo $row['ShopName']; ?></td>
          <td class="shop-score text-right">
              <span class="shop-price">€ <?php echo str_replace('.', ',', str_replace('.00', '.-', $row['Value']));?></span>
          </td>
          <td class="shop-link text-right">
            <button class="btn btn-primary">
                <a href="<?php echo $row['URL'];?>" target="_blank">     
                BEZOEK  
                </a>
            </button>
          </td>
        </tr>
      <?php } 
        $products->data_seek(0);
      ?>
      </tbody>
    </table>
</div>
<div class="row" id="product-description">
    <div class="col-8">
        <h4>Productbeschrijving</h4>
        <p class="text-justify">
            <?php echo $products->fetch_assoc()['Description']; $products->data_seek(0); ?>
        </p>
    </div>
</div>
<div class="row" id="product-specifications">
    <div class="col-8">
        <h4>Specificaties</h4>
        <table class="table">
            <tbody>
                <?php while ($row = $specs->fetch_assoc()){ ?>
                    <tr>
                        <td><?php echo $row['Name']; ?></td>
                        <td><?php echo $row['value']; ?></td>
                    </tr>
                <?php }?> 

            </tbody>
        </table>
    </div>
</div>
<script>
    document.getElementById('selectShopSort').addEventListener('change', function(){
        document.getElementById('formShopSort').submit();
    });
</script>
<?php
require('_layout/footer.php');
?>
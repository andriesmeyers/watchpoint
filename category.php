<?php 
include 'Models/Database.php';
session_start();

# Specification Categories
$allowed_specs = [
    'sqdfs'
];
try{
    $db = Database::getInstance();
    $mysqli = $db->getConnection();

    if(isset($_GET['category'])){
        $category = mysqli_escape_string($mysqli, $_GET['category']);
        $_SESSION['category'] = $category;
    }
    $category = $_SESSION['category'];

    $orderBy = "Product.View_count DESC";
    if(isset($_POST['select-sort'])){
        switch($_POST['select-sort']){
            case 'viewcount_desc':
                $orderBy = 'Product.View_count DESC';
                break;
            case 'name_asc':
                $orderBy = 'Product.Name ASC';
                break;
            case 'name_desc':
                $orderBy = 'Product.Name DESC';
                break;
            case 'price_asc':
                $orderBy = 'Lowest_Price ASC';
                break;
            case 'price_desc':
                $orderBy = 'Lowest_Price DESC';
                break;
            default:
                $orderBy = 'Product.View_count DESC';
        }
    }
    $query = 
        "SELECT EAN, Product.Name, Price.URL, Category.Name AS CategoryName, Image_URL, MIN(Value) AS Lowest_Price FROM Product "
        . "LEFT JOIN Category "
        . "ON Category_Id = Category.Id "
        . "LEFT JOIN Price "
        . "ON Product.EAN = Price.Product_EAN "
        . "WHERE Category.Name = " . "'$category'" . " OR Category.Parent_Id = Category.Id AND Price.URL IS NOT NULL AND Price.Value > 0 " 
        . "GROUP BY Product.EAN "
        . "ORDER BY $orderBy "
        . "LIMIT 50 ";

    $products = $mysqli->query($query);

    if($products->num_rows == 0){
        $query = 
        "SELECT Id from Category "
        . "WHERE Category.Name = " . "'$category' ";
        $category = $mysqli->query($query);
        $categoryId = $category->fetch_assoc()['Id'];
        $query = 
        "SELECT EAN, Product.Name, Price.URL, Category.Name AS CategoryName, Image_URL, MIN(Value) AS Lowest_Price FROM Product "
            . "LEFT JOIN Category "
            . "ON Category_Id = Category.Id "
            .  "LEFT JOIN Price "
            .  "ON Product.EAN = Price.Product_EAN "
            . "WHERE Category.Parent_Id = " . $categoryId . " AND Price.URL IS NOT NULL AND Price.Value > 0 "
            . "GROUP BY Product.EAN "
            . "ORDER BY $orderBy "
            . "LIMIT 50";
        $products = $mysqli->query($query);
    }

    $query = "SELECT specification.Name AS Name, product_specification.value AS Value, Count(*) AS Count FROM product "
        . "LEFT JOIN category "
        . "ON product.Category_Id = Category.Id "
        . "LEFT JOIN product_specification "
        . "ON product.EAN = product_specification.product_EAN "
        . "LEFT JOIN specification "
        . "ON specification.Id = product_specification.specification_Id "
        . "WHERE Category.Name = 'Desktops' "
        . "GROUP BY product_specification.value "
        . "ORDER BY specification.Id, Count DESC ";

    $specs = $mysqli->query($query);

    while ($row = $specs->fetch_assoc()){
        $name = $row['Name'];
        $value = $row['Value'];
        $specifications[$name][$value] = $row['Count'];
    }
    

}catch(Exception $e){
  echo 'Caught exception: ' . $e->getMessage() . "\n";
}
require('_layout/head.php');
?>
<h1 class="my-4"><?php echo $products->fetch_assoc()['CategoryName']; $products->data_seek(0);?></h1>
<div class="row">
    <div class="col-3">
        <h4>Filteren</h4>
        <button class="btn btn-primary">Verfijn</button>
        <ul class="list-group list-group-flush">
            <?php 
            $i = 0;
            foreach($specifications as $specName=>$specValues){?>
                <li class="list-group-item">
                    <a class="nav-link dropdown-toggle" data-toggle="collapse" data-target="#spec<?php echo $specName; ?>">
                        <?php echo $specName; ?>
                    </a>
                    <ul class="collapse" id="spec<?php echo $specName;?>">
                        <?php foreach($specValues as $valName => $value){?>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="" id="defaultCheck1">
                                <label class="form-check-label" for="defaultCheck1">
                                    <?php echo $valName . "(" . $value . ")"; ?>
                                </label>
                            </div>
                        <?php }?>
                    </ul>
                </li>
            <?php 
                if(++$i == 10) break;
            } ?>
        </ul>
    </div>
    <div class="col-9">
        <table class="table product-table">
          <thead>
            <tr>
              <td class="border-0"><?php echo $products->num_rows;?> resultaten</td>
              <td class="border-0 text-right" colspan="2">
                <form  id="formProductSort" action="category.php" method="post">
                      <div class="row">
                          <div class="col-7 offset-5">
                              <div class="form-group">
                                  <label for="selectSort">Sorteren op:</label>
                                  <select class="form-control" name="select-sort" id="selectProductSort">
                                      <option value="viewcount_desc" <?php if($orderBy=='Product.View_count DESC') echo 'selected';?>>Meest bekeken</option>
                                      <option value="name_asc" <?php if($orderBy=='Product.Name ASC') echo 'selected';?>>Naam (oplopend)</option>
                                      <option value="name_desc" <?php if($orderBy=='Product.Name DESC') echo 'selected';?>>Naam (aflopend)</option>
                                      <option value="price_asc" <?php if($orderBy=='Lowest_Price ASC') echo 'selected';?>>Prijs (oplopend)</option>
                                      <option value="price_desc" <?php if($orderBy=='Lowest_Price DESC') echo 'selected';?>>Prijs (aflopend)</option>
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
            <tr data-ean="<?php echo $row['EAN'];?>">
              <td class="product-image"><div class="product-image-container"><img src="<?php echo $row['Image_URL'];?>"></div></td>
              <td class="product-name"><?php echo $row['Name']; ?></td>
              <td class="product-score">
                  <span class="product-price">€ <?php echo str_replace('.', ',', str_replace('.00', '.-', $row['Lowest_Price']));?></span>
                  <button class="btn btn-primary">
                    <a href="product.php<?php echo "?ean=" . $row['EAN'];?>">
        
                        Vergelijk
                    </a>
                  </button>
              </td>
            </tr>
          <?php } ?>
          </tbody>
        </table>
    </div>
</div>
<script>
    document.getElementById('selectProductSort').addEventListener('change', function(){
        document.getElementById('formProductSort').submit();
    });
</script>
<?php
require('_layout/footer.php');
?>
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
    
    # Handle filtering
    $filter = "";
    foreach($_POST as $postParam => $specArray){
        if(substr($postParam, 0, 4) == 'spec'){
            $postParam = substr($postParam, 4);
            $filter .= "AND Specification.Name = " . "'" . $postParam . "' ";
            foreach($specArray as $specValue){
                $filter .="AND Product_specification.Value = " . "'" . $specValue . "' ";
            }
            $filter .= " ";
        }
    }
    # Handle Category
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
    "SELECT Id from Category "
    . "WHERE Category.Name = " . "'$category' ";
    $result = $mysqli->query($query);
    $categoryId = $result->fetch_assoc()['Id'];

    $query = 
        "SELECT EAN, Product.Name, Price.URL, Category.Name AS CategoryName, Image_URL, MIN(Price.Value) AS Lowest_Price FROM Product "
        . "INNER JOIN Category "
        . "ON Category_Id = Category.Id "
        . "INNER JOIN Price "
        . "ON Product.EAN = Price.Product_EAN "
        . "INNER JOIN product_specification "
        . "ON product.EAN = product_specification.product_EAN "
        . "INNER JOIN specification "
        . "ON specification.Id = product_specification.specification_Id "
        . "WHERE Price.URL IS NOT NULL AND Price.Value > 0 "
        . $filter
        . "AND (Category.Name = " . "'$category'" . " OR Category.Parent_Id = " . $categoryId . ") "
        . "GROUP BY Product.EAN "
        . "ORDER BY $orderBy ";
    // $query = "SELECT EAN, Product.Name, Price.URL, Category.Name AS CategoryName, Image_URL, MIN(Price.Value) AS Lowest_Price "
    //     . "FROM Product LEFT JOIN Category ON Category_Id = Category.Id "
    //     . "LEFT JOIN Price ON Product.EAN = Price.Product_EAN "
    //     . "LEFT JOIN product_specification ON product.EAN = product_specification.product_EAN " 
    //     . "LEFT JOIN specification ON specification.Id = product_specification.specification_Id "
    //     . "WHERE Price.URL IS NOT NULL AND Price.Value > 0 AND (Category.Name = 'Desktops') OR (Category.Parent_Id = 27739) "
    //     . "GROUP BY Product.EAN, specification.Name, product_specification.Value "
    //     . "HAVING (specification.Name = "Processortype" AND  product_specification.Value = "AMD FX") "
    //     . "OR (specification.Name = "Processornummer" AND product_specification.Value = "FX 4300") "
    //     . "ORDER BY Product.View_count DESC LIMIT 50 "
    $products = $mysqli->query($query);

    if($products->num_rows == 0){
        
        $query = 
        "SELECT EAN, Product.Name, Price.URL, Category.Name AS CategoryName, Image_URL, MIN(Value) AS Lowest_Price FROM Product "
            . "LEFT JOIN Category "
            . "ON Category_Id = Category.Id "
            . "LEFT JOIN Price "
            . "ON Product.EAN = Price.Product_EAN "
            . "WHERE (Category.Name = " . "'$category'" . " OR Category.Parent_Id = " . $categoryId . ") "
            . "AND Price.URL IS NOT NULL AND Price.Value > 0 "
            // . $filter
            . "GROUP BY Product.EAN "
            . "ORDER BY $orderBy ";
        $products = $mysqli->query($query);
    }
    while( $row = mysqli_fetch_assoc( $products)){
        $arrayEAN[] = $row['EAN']; // Inside while loop
    }
    $products->data_seek(0);
    $query = "SELECT specification.Name AS Name, product_specification.value AS Value, Count(*) AS Count FROM product "
        . "LEFT JOIN category "
        . "ON product.Category_Id = Category.Id "
        . "LEFT JOIN product_specification "
        . "ON product.EAN = product_specification.product_EAN "
        . "LEFT JOIN specification "
        . "ON specification.Id = product_specification.specification_Id "
        . "WHERE (Category.Name = " . "'$category'" . " OR Category.Parent_Id = " . $categoryId . ") "
        . "AND Product.EAN IN ('" . implode("','", $arrayEAN) . "') "
        . "GROUP BY product_specification.value "
        . "ORDER BY specification.Id, Count DESC";
        
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
<form id="specFiltering" action="category.php" method="post">
    <div class="row">
        <div class="col-3">
            <h4>Filteren</h4>
            <button type="submit" class="btn btn-primary">Verfijn</button>
            <button id="btnResetForm" class="btn btn-light">
            Herstellen</button>
            <ul class="list-group list-group-flush">
                <?php 
                $i = 0;
                foreach($specifications as $specName=>$specValues){
                    # Check if specification category was used
                    $needle = 'spec' . $specName;
                    $active = (array_key_exists($needle, $_POST));
                    ?>
                    <li class="list-group-item">
                        <a class="nav-link dropdown-toggle" data-toggle="collapse" data-target="#spec<?php echo $specName; ?>">
                            <?php echo $specName; ?>
                        </a>
                        <ul class="collapse pl-0 <?= ($active)? 'show':'';?>" id="spec<?php echo $specName;?>">
                            <?php foreach($specValues as $valName => $value){
                                # Check if checkbox was checked
                                $checked = false;
                                if(array_key_exists('spec' . $specName, $_POST)){
                                    $checked = (in_array($valName, $_POST['spec' . $specName]));
                                }
                                ?>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="spec<?=$specName;?>[]" value="<?= $valName;?>" <?= $checked? 'checked':'';?>>
                                    <label class="form-check-label">
                                        <?php echo $valName . " (" . $value . ")"; ?>
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
</form>
<script>
    document.getElementById('selectProductSort').addEventListener('change', function(){
        document.getElementById('formProductSort').submit();
    });
    document.getElementById('btnResetForm').addEventListener('click', function(e){
        e.preventDefault();
        var checks = document.querySelectorAll('#specFiltering input[type="checkbox"]');
        for(var i =0; i< checks.length;i++){
        var check = checks[i];
        if(!check.disabled){
            check.checked = false;
        }
        document.getElementById('specFiltering').submit();
    }
    })
</script>
<?php
require('_layout/footer.php');
?>
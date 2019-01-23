<?php 
include 'Models/Database.php';
include 'Models/StringHelper.php';
try{
  $db = Database::getInstance();
  $mysqli = $db->getConnection();
  
  $sql_query = 
    "SELECT c1.Id, c1.Name AS mainCategoryName, c2.Id AS subCategoryId, c2.Name AS subCategoryName, c3.Id AS subSubCategoryId, c3.Name AS subSubCategoryName FROM category c1 "
    . "LEFT JOIN category c2 "
    . "ON c2.Parent_Id = c1.Id "
    . "LEFT JOIN category c3 "
    . "ON c3.Parent_Id = c2.Id "
    . "WHERE c1.Parent_Id IS NULL";

  $result = $mysqli->query($sql_query);
  while ($row = $result->fetch_assoc()){
    $cat_name = $row['mainCategoryName'];
    $sub_cat_id = $row['subCategoryId'];
    $sub_cat_name = $row['subCategoryName'];
    $sub_sub_id = $row['subSubCategoryId'];
    $sub_sub_name = $row['subSubCategoryName'];
    if(isset($sub_sub_name)){
      $categories[$cat_name][$sub_cat_name][$sub_sub_id] = $sub_sub_name;
    }else{
      $categories[$cat_name][$sub_cat_name] = [$sub_cat_id => $sub_cat_name];
    }
    $query = 
      "SELECT Image_URL FROM product " .
      "LEFT JOIN Category " .
      "ON product.Category_Id = Category.Id " .
      "WHERE Parent_Id = " . $sub_cat_id . " " .
      "LIMIT 1";
    $image = $mysqli->query($query);
    $image = $image->fetch_assoc();
    if($image != NULL){
      $categories[$cat_name][$sub_cat_name]["Image_URL"] = reset($image);
    }else{
      $query = 
      "SELECT Image_URL FROM product " .
      "WHERE Category_Id= " . $sub_cat_id . " " .
      "LIMIT 1";
      $image = $mysqli->query($query);
      $image = $image->fetch_assoc();
      $categories[$cat_name][$sub_cat_name]["Image_URL"] = reset($image);
    }
    

  }
}catch(Exception $e){
  echo 'Caught exception: ' . $e->getMessage() . "\n";
}
require('_layout/head.php');
  
?>
<h1>Categorieën</h1>
<div class="container">
  <div class="row">
    <div class="col-4 mainlist">
      <ul class="list-group category-list">
      <?php foreach($categories as $key=>$mainCategory){?>
        <li class="list-group-item category-<?php echo StringHelper::decodeString($key);?>"><?php echo $key?></li>
        <?php }?>
      </ul>
    </div>
    <?php foreach($categories as $key=>$mainCategory){?>
      <div class="col-8 d-none sub-list sub-list-<?php echo StringHelper::decodeString($key);?>">
        <div class="row">
        <?php foreach($mainCategory as $key=>$subCategory){?>
          <div class="<?php echo count($mainCategory) > 9 ? 'col-3 ': 'col-4 ';  echo count($mainCategory) < 9 ? 'limited ': '';?>sub-list-item">
            <div class="sub-list-item-container border">
              <a href="category.php<?php echo "?category=" . urlencode($key);?>">
                <span><?php echo $key;?></span>
                <div class="sub-image-container" style="background: url('<?php echo $subCategory['Image_URL'];?>')" >
                </div>
              </a>
            </div>
          </div>  
        <?php } ?>
        </div>
      </div>
    <?php } ?>
  </div>
</div>
<?php
require('_layout/footer.php');
?>
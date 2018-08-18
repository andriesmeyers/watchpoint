<?php 
include 'Models/Database.php';
try{
  $db = Database::getInstance();
  $mysqli = $db->getConnection();
  $category = mysqli_escape_string($mysqli, $_GET['category']);
  $sql_query = 
    "SELECT EAN, Product.Name, Image_URL FROM Product "
    . "LEFT JOIN Category "
    . "ON Category_Id = Category.Id "
    . "WHERE Category.Name = " . "'$category'"
    . "ORDER BY Product.Name";

  $result = $mysqli->query($sql_query);
}catch(Exception $e){
  echo 'Caught exception: ' . $e->getMessage() . "\n";
}
require('_layout/header.php');
?>

<h1 class="my-4">Categorieën</h1>

<table class="table">
  <tbody>
  <?php while ($row = $result->fetch_assoc()){ ?>
    <tr>
      <td style="height:60px;width:80px"><img src="<?php echo $row['Image_URL'];?>" style="width:50px;object-fit:cover"></td>
      <td><?php echo $row['Name']; ?></td>
    </tr>
  <?php } ?>
  </tbody>
</table>
<?php
require('_layout/footer.php');
?>
<?php 
include 'Models/Database.php';
$db = Database::getInstance();
$mysqli = $db->getConnection(); 
$sql_query = 
  "SELECT Category.Name, Image_URL FROM Product "
  . "LEFT JOIN Category "
  . "ON Category_Id = Category.Id "
  . "GROUP BY Category_Id";

$result = $mysqli->query($sql_query);
?>
<?php
    require('_layout/header.php');
?>
<div class="container">

  <h1 class="my-4">Categorieën</h1>

  <!-- Marketing Icons Section -->

  <div class="row">
    <?php while ($row = $result->fetch_assoc()){ ?>
    
    <div class="col-lg-4 mb-4">
      <div class="card h-100">
        <img class="card-img-top" src="<?php echo $row['Image_URL'];?>" alt="Card image cap">
        <div class="card-body">
          <h4 class="card-text"><?php echo $row['Name']; ?></h4>
        </div>
        <div class="card-footer">
          <a href='category.php<?php echo "?category=" . urlencode($row['Name']); ?>' class="btn btn-primary">Prijzen</a>
        </div>
      </div>
    </div>
    <?php } ?>
  </div>
  <!-- /.row -->

<?php
require('_layout/footer.php');
?>
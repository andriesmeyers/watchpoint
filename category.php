<?php 
include 'Models/Database.php';
$db = Database::getInstance();
$mysqli = $db->getConnection(); 
$sql_query = 
  "SELECT * FROM Product "
  . "LEFT JOIN Price "
  . "ON EAN = Price.Product_EAN "
  . "ORDER BY Name";

$result = $mysqli->query($sql_query);

require('_layout/header.php');
?>

<h1 class="my-4">Categorieën</h1>

<table class="table">
  <!-- <thead>
    <tr>
      <th scope="col"></th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead> -->
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
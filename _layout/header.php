<header>
<?php 
$mysqli = $db->getConnection(); 
$sql_query = 
  "SELECT * FROM Category "
  . "WHERE Parent_Id IS NULL";

$result = $mysqli->query($sql_query);
?>
<div class="container">
    <div class="logo-wrapper">
        <a id="logo" class="header-brand" href="index.php">
            <img src="./styles/images/logo.png" height="30" alt="watchpoint">
        </a>
    </div>
    <nav class="nav navbar">
        <ul>
            <li class="nav-item"><a href="index.php">Home</a></li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Categorieën</a>
              <div class="dropdown-menu">
                <?php while ($row = $result->fetch_assoc()){ ?>
                  <a class="dropdown-item" href="categories.php<?php echo "?category=" . urlencode($row['Name']); ?>"><?php echo $row['Name'];?></a>
                <?php } ?>
              </div>
            </li>
        </ul>
    </nav>
</div>
</header>  



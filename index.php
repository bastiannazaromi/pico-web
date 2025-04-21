<?php
require 'koneksi/koneksi.php';

if (isset($_GET['page'])) {
	$page = $_GET['page'];
} else {
	$page = 'home';
}

?>

<!DOCTYPE html>
<html lang="id">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title><?php echo 'Pico Web'; ?></title>

	<!-- Bootstrap CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
	<nav class="navbar navbar-expand-lg" style="background-color:rgb(165, 165, 172);">
		<div class="container">
			<a class="navbar-brand" href="#">PICO WEB</a>
			<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarNav">
				<ul class="navbar-nav">
					<li class="nav-item">
						<a class="nav-link active" aria-current="page" href=".">Home</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="?page=data_sensor">Data Sensor</a>
					</li>
				</ul>
			</div>
		</div>
	</nav>

	<div class="container mt-4">
		<!-- Content -->
		<?php include('views/' . $page . '.php'); ?>
	</div>

	<!-- Bootstrap JS -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>

</html>
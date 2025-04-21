<?php
include '../koneksi/koneksi.php';

// Ganti IP berikut dengan IP dari Pico W kamu
// $pico_ip = "192.168.1.217";

if (isset($_POST['relay'])) {
	$relay_status = $_POST['relay'];

	$sql = "UPDATE relay SET status = '$relay_status'";

	if ($conn->query($sql) === TRUE) {
		$conn->close();

		header("Location: ./../?page=home");
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;

		$conn->close();
		exit;
	}
} else {
	echo "Perintah tidak ditemukan.";
}

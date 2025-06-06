<?php
include '../koneksi/koneksi.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$json      = file_get_contents('php://input');
	$data      = json_decode($json, true);
	$latitude  = $data['latitude'] ?? 'N/A'; // object
	$longitude = $data['longitude'] ?? 'N/A'; // array

	if ($latitude !== 'N/A' || $longitude !== 'N/A') {
		$sql = "UPDATE lokasi SET latitude = '$latitude', longitude = '$longitude' WHERE id = 1";

		if ($conn->query($sql) === TRUE) {
			$conn->close();
		} else {
			echo "Error: " . $sql . "<br>" . $conn->error;

			$conn->close();
			exit;
		}
	}

	file_put_contents("../log/log.txt", "Latitude: $latitude, Longitude: $longitude\t" . date('d M Y - H:i:s') . "\n", FILE_APPEND);

	echo "Data berhasil diperbarui";
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
	echo json_encode([
		'status' => true,
		'message' => 'get berhasil'
	]);
}

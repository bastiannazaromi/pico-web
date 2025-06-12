<?php
include '../koneksi/koneksi.php';

// Ambil status relay (asumsi hanya 1 baris)
$query  = mysqli_query($conn, "SELECT status, updatedAt FROM relay LIMIT 1");
$row    = mysqli_fetch_assoc($query);
$status = $row['status'];

$res = [
	'status'  => true,
	'message' => 'Berhasil mengambil data',
	'data'    => [
		'status' => $status
	]
];

echo json_encode($res);

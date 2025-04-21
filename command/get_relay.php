<?php
include '../koneksi/koneksi.php';

// Ambil status relay (asumsi hanya 1 baris)
$query = mysqli_query($conn, "SELECT status FROM relay LIMIT 1");
$row = mysqli_fetch_assoc($query);
$status = $row['status'];

echo $status;

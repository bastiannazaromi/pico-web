<?php
include 'koneksi/koneksi.php';

$query  = mysqli_query($conn, "SELECT status FROM relay LIMIT 1");
$row    = mysqli_fetch_assoc($query);
$status = $row['status'];

$query_lokasi = mysqli_query($conn, "SELECT latitude, longitude FROM lokasi LIMIT 1");
$lokasi       = mysqli_fetch_object($query_lokasi);
?>

<div class="row">
	<div class="col-lg-12">
		<div class="card">
			<div class="card-header">
				<h5>Kontrol Relay</h5>
			</div>
			<div class="card-body text-center">
				<p class="mb-4">
					Status Relay Saat Ini:
					<strong class="<?= ($status == 'ON') ? 'text-success' : 'text-danger'; ?>">
						<?= $status; ?>
					</strong>
				</p>
				<form action="command/relay_status.php" method="POST" style="display:inline-block;">
					<button type="submit" name="relay" value="ON" class="btn btn-success btn-lg px-4">ON</button>
				</form>
				<form action="command/relay_status.php" method="POST" style="display:inline-block; margin-left:10px;">
					<button type="submit" name="relay" value="OFF" class="btn btn-danger btn-lg px-4">OFF</button>
				</form>
			</div>
		</div>
	</div>
	<div class="col-lg-12 mt-4">
		<div class="card">
			<div class="card-header">
				<h5>Lokasi</h5>
			</div>
			<div class="card-body">
				<?php if ($lokasi) : ?>
					<iframe width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=<?= $lokasi->latitude; ?>,<?= $lokasi->longitude; ?>&amp;output=embed">
					</iframe>
				<?php else : ?>
					<p class="text-danger">Data lokasi tidak ditemukan.</p>
				<?php endif; ?>
			</div>
		</div>
	</div>
</div>
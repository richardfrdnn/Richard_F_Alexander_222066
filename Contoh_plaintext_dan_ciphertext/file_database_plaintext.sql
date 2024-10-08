/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ rental_mobil /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE rental_mobil;

DROP TABLE IF EXISTS admin;
CREATE TABLE `admin` (
  `id_admin` int(11) NOT NULL AUTO_INCREMENT,
  `nama_admin` varchar(120) NOT NULL,
  `username` varchar(120) NOT NULL,
  `password` varchar(120) NOT NULL,
  PRIMARY KEY (`id_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS customer;
CREATE TABLE `customer` (
  `id_customer` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(120) NOT NULL,
  `username` varchar(120) NOT NULL,
  `alamat` varchar(120) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `no_telepon` varchar(20) NOT NULL,
  `no_ktp` varchar(50) NOT NULL,
  `password` varchar(120) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id_customer`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS mobil;
CREATE TABLE `mobil` (
  `id_mobil` int(11) NOT NULL AUTO_INCREMENT,
  `kode_tipe` varchar(120) NOT NULL,
  `merek` varchar(120) NOT NULL,
  `no_plat` varchar(20) NOT NULL,
  `warna` varchar(20) NOT NULL,
  `tahun` varchar(4) NOT NULL,
  `status` varchar(50) NOT NULL,
  `harga` int(11) NOT NULL,
  `denda` int(11) NOT NULL,
  `ac` int(11) NOT NULL,
  `sopir` int(11) NOT NULL,
  `mp3_player` int(11) NOT NULL,
  `central_lock` int(11) NOT NULL,
  `gambar` varchar(255) NOT NULL,
  PRIMARY KEY (`id_mobil`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS rental;
CREATE TABLE `rental` (
  `id_rental` int(11) NOT NULL AUTO_INCREMENT,
  `id_customer` int(11) NOT NULL,
  `id_mobil` int(11) NOT NULL,
  `tgl_rental` date NOT NULL,
  `tgl_kembali` date NOT NULL,
  `harga` varchar(120) NOT NULL,
  `denda` varchar(120) NOT NULL,
  `tgl_pengembalian` date NOT NULL,
  `status_pengembalian` varchar(50) NOT NULL,
  `status_rental` varchar(50) NOT NULL,
  PRIMARY KEY (`id_rental`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS tipe;
CREATE TABLE `tipe` (
  `id_tipe` int(11) NOT NULL AUTO_INCREMENT,
  `kode_tipe` varchar(120) NOT NULL,
  `nama_tipe` varchar(120) NOT NULL,
  PRIMARY KEY (`id_tipe`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS transaksi;
CREATE TABLE `transaksi` (
  `id_rental` int(11) NOT NULL AUTO_INCREMENT,
  `id_customer` int(11) NOT NULL,
  `id_mobil` int(11) NOT NULL,
  `tgl_rental` date NOT NULL,
  `tgl_kembali` date NOT NULL,
  `harga` varchar(120) NOT NULL,
  `denda` int(11) NOT NULL,
  `total_denda` varchar(120) NOT NULL,
  `tgl_pengembalian` date NOT NULL,
  `status_pengembalian` varchar(50) NOT NULL,
  `status_rental` varchar(50) NOT NULL,
  `bukti_pembayaran` varchar(120) NOT NULL,
  `status_pembayaran` int(11) NOT NULL,
  PRIMARY KEY (`id_rental`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;


INSERT INTO customer(id_customer,nama,username,alamat,gender,no_telepon,no_ktp,password,role_id) VALUES(4,'Joko Santoso','joko','Jl. Satu Pekanbaru','laki-laki','0653246512','215654532767','81dc9bdb52d04dc20036dbd8313ed055',2),(5,'Darmawan','darmawan','Jl. Dua Pekanbaru','laki-laki','07617623','1423477324723','81dc9bdb52d04dc20036dbd8313ed055',2),(6,'Andi','andi','Jakarta','laki-laki','0217687634','12747657463','827ccb0eea8a706c4c34a16891f84e7b',2),(7,'Arif','admin','Pekanbaru','laki-laki','065423624','1764578345','21232f297a57a5a743894a0e4a801fc3',1),(8,'Bayu','bayu','Jl. Nangka Pekanbaru','laki-laki','07612233','14000756764735','81dc9bdb52d04dc20036dbd8313ed055',2),(9,'Toni','toni','Bandung','laki-laki','0835653243','1753453265435','81dc9bdb52d04dc20036dbd8313ed055',2),(10,'admin','admin','alamat admin','laki-laki','08123456789','9876543210','21232f297a57a5a743894a0e4a801fc3',2);

INSERT INTO mobil(id_mobil,kode_tipe,merek,no_plat,warna,tahun,status,harga,denda,ac,sopir,mp3_player,central_lock,gambar) VALUES(6,'SDN','Toyota Camry','B 1446 DAG','Hitam','2015','1',400000,30000,1,0,1,0,'toyota-camry.jpg'),(9,'SDN','Honda City','B 1456 DAG','Hitam','2015','0',450000,30000,1,0,1,0,'honda-city.jpg'),(10,'SDN','CRV','B 1234 csh','Silver','2019','0',400000,100000,0,0,1,1,'gallery_used-car-mobil123-honda-cr-v-2_4.jpg'),(13,'MNV','Toyota Avanza','B 2245 DAM','Hitam','2015','1',350000,25000,1,0,0,1,'avanza-hitam.jpg'),(14,'MNV','Toyota Avanza','B 1123 DUD','Putih','2016','1',350000,25000,1,0,1,1,'avanza-putih.jpg');


INSERT INTO tipe(id_tipe,kode_tipe,nama_tipe) VALUES(1,'SDN','Sedan'),(3,'MNV','Mini Van');
INSERT INTO transaksi(id_rental,id_customer,id_mobil,tgl_rental,tgl_kembali,harga,denda,total_denda,tgl_pengembalian,status_pengembalian,status_rental,bukti_pembayaran,status_pembayaran) VALUES(3,6,9,'2021-01-15','2021-01-16','450000',30000,'120000','2021-01-20','Belum Kembali','Belum Selesai','',0),(4,6,6,'2021-01-15','2021-01-18','400000',30000,'60000','2021-01-20','Kembali','Selesai','tugas.png',1),(5,8,10,'2021-01-18','2021-01-19','400000',100000,'100000','2021-01-20','Belum Kembali','Belum Selesai','',0),(6,6,11,'2021-01-28','2021-01-30','300000',25000,'25000','2021-01-31','Kembali','Selesai','tugas2.png',1),(7,9,13,'2021-01-30','2021-02-01','350000',25000,'25000','2021-02-02','Kembali','Selesai','tugas2.png',1);
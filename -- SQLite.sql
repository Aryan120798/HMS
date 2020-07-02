-- -- SQLite
-- Query for Adding Medicines in Stock of MedicineMaster Table
INSERT INTO `medicine_master` (medicine_name, quantity, rate)
VALUES
('Lactuzolid', 500, 10),
('Relenformin', 500, 10),
('Lacotrana', 500, 10),
('Subotane', 500, 10),
('Savelestid', 500, 10),
('Savelestid', 500, 10),
('Symbyvice', 500, 10),
('Eronium Relenrodine', 500, 10),
('Silvasol Granicline', 500, 10),
('Retrocelex Naftinoin', 500, 10),
('Tetapalene Ceftastrel', 500, 10),
('Flexefen', 500, 20),
('Vigaletine', 500, 20),
('Nasaletine', 500, 20),
('Alagestrel', 500, 20),
('Endocane', 500, 20),
('Abelmara', 500, 20),
('Galanmethate Anticilin', 500, 20),
('Actominphen Sodizolam', 500, 20),
('Aplenspan Theravirenz', 500, 20),
('Neufase Fragposide', 500, 20),
('Aplenspan Theravirenz', 500, 20)
;

--Query for adding tests in Diagnostic Master
INSERT INTO `diagnostic_master` (test_name, test_charge)
VALUES
('kidney function test', 1100),
('gastric fluid analysis', 1200),
('liver function test', 1300),
('lumbar puncture', 1400),
('malabsorption test', 1500),
('Pap smear', 1600),
('phenolsulfonphthalein test', 1700),
('pregnancy test', 1800),
('prenatal testing', 1900),
('protein-bound iodine test', 2000),
('syphilis test', 2100),
('thoracentesis', 2200),
('thyroid function test', 2300),
('toxicology test', 2400),
('urinalysis/uroscopy', 2500);


-- deleting tables from database
-- drop table `diagnostics` 
-- drop table `medicines` 
-- drop table `patient` 
-- drop table `userstore`


-- select test_name from `diagnostic_master`
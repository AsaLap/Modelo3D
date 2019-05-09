CREATE TABLE CSV(id serial primary key, nom varchar(20) NOT NULL, date_ajout DATE DEFAULT current_date, ex_lidar boolean, planete varchar(10) NOT NULL, x_min int, y_min int, x_max int, y_max int);
CREATE TABLE OBJ(id int primary key, nom varchar(20) NOT NULL, date_ajout DATE DEFAULT current_date, FOREIGN KEY(id) REFERENCES CSV(id));

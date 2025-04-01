create user 'innova_admin'@'%' identified by 'Innovaair@123';

grant all on innovaair.* to 'innova_admin'@'%';

flush privileges;
create user 'innova_admin'@'%' identified by 'InnovaairAdmin@123';

grant all on innovaair.* to 'innova_admin'@'%';

create user 'innova_client'@'%' identified by 'Innovaair@123';

grant select on innovaair.usuario to 'innova_client'@'%';
grant select, insert on innovaair.maquina to 'innova_client'@'%';
grant select, insert on innovaair.componente to 'innova_client'@'%';
grant insert on innovaair.metrica to 'innova_client'@'%';
grant insert on innovaair.captura_historico to 'innova_client'@'%';

flush privileges;
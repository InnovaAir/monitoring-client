create user 'innova_admin'@'%' identified by 'InnovaairAdmin@123';

grant all on innovaair.* to 'innova_admin'@'%';

create user 'innova_client'@'%' identified by 'Innovaair@123';

grant select, insert on innovaair.maquina to 'innova_client'@'%';
grant select, insert on innovaair.componente to 'innova_client'@'%';
grant select, insert on innovaair.metrica to 'innova_client'@'%';
grant insert on innovaair.captura_historico to 'innova_client'@'%';

create user 'innova_s3'@'%' identified by 'Innovaair@123';

grant select on innovaair.cliente to 'innova_s3'@'%';
grant select on innovaair.filial to 'innova_s3'@'%';
grant select on innovaair.maquina to 'innova_s3'@'%';
grant select on innovaair.componente to 'innova_s3'@'%';
grant select on innovaair.metrica to 'innova_s3'@'%';
grant select on innovaair.captura_historico to 'innova_s3'@'%';

flush privileges;
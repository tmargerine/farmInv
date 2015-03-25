select * from entries where entryDate between '2015-02-01' and '2015-02-28';
select sum(actionNo) from entries where action = 'Tray';
select sum(actionNo) from (select * from entries where entryDate between '2015-02-01' and '2015-02-28') where action = 'Tray';
select sum(value) from (select * from entries where entryDate between '2015-02-01' and '2015-02-28') where action = 'Slaughter' and batch like 'Broiler___';
select * from (select * from entries where entryDate between '2015-02-01' and '2015-02-28') where action = 'Slaughter' and batch like 'Broiler___';
select count(value) from (select * from entries where entryDate between '2015-02-01' and '2015-02-28') where action = 'Slaughter' and batch like 'Pig___';
select batch, action, sum(actionNo), sum(value) from (select * from entries where entryDate between '2015-02-01' and '2015-02-28') group by batch, action;
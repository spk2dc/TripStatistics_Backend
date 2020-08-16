.headers ON
-- .mode columns

.print '**********************************'
.print ' '
.print 'User Table: '
.print ' '
SELECT *
FROM user;

.print ' '
.print '**********************************'
.print ' '

.print 'All_Maps Table: '
.print ' '
SELECT id, trip_name, filename
FROM all_map;
.print ' '
.print '**********************************'

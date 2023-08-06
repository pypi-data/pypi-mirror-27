
<html>
<body>

% for tbl in db:
% for person in tbl:
<h1>${person['friendlyname']}</h1>
<p>${person['firstname']} ${person['lastname']} lives in ${person['address']}, ${person['city']}.</p>
% endfor
% endfor

</body>
</html>


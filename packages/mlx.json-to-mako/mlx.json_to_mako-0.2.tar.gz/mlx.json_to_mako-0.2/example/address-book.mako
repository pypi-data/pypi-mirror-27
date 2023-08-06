
<html>
<body>

## Loop over the databases which are inputted
% for tbl in db:

## The JSON databases contain a list of persons, iterate over them
% for person in tbl:

## A person is a dictionary with some key-value pairs: convert them to html tags
<h1>${person['friendlyname']}</h1>
<p>${person['firstname']} ${person['lastname']} lives in ${person['address']}, ${person['city']}.</p>

% endfor

% endfor

</body>
</html>


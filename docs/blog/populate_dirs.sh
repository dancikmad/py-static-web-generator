<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>populate_dirs.sh</title>
    <link href="/py-static-web-generator/index.css" rel="stylesheet" />
  </head>

  <body>
    <article>
#!/bin/bash

# List of directories
dirs=("glorfindel" "majesty" "tom")

# Iterate over each directory
for dir in "${dirs[@]}"; do
  # Check if the directory exists
  if [ -d "$dir" ]; then
    # Create index.md in the directory
    touch "$dir/index.md"
    echo "index.md created in $dir"
  else
    echo "Directory $dir does not exist!"
  fi
done


</article>
  </body>
</html>

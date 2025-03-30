
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



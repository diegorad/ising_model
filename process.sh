for file in *.txt; do
  grep "Best parameters:" "$file" | \
  sed 's/.*Best parameters: //' >> parameters.txt
done

for file in *.txt; do
  grep "Minimum error:" "$file" | \
  sed 's/.*Best parameters: //' >> error.txt
done

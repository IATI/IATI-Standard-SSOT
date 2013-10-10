for f in `curl "http://wiki.iatistandard.org/standard/documentation/1.03/?do=export_raw" | grep -Eo "\[\[standard:documentation:1.03:(.*)\]\]" | awk -F ':' '{print $4}' | sed 's/\]\]//'`; do
    wget "http://wiki.iatistandard.org/standard/documentation/1.03/$f?do=export_raw" -O $f.txt
done
for f in *.txt; do pandoc -f mediawiki $f -t rst -o ../docs-extra/`basename $f .txt`; done
#for f in *.rst; do tail -n+3 $f > tmp; mv tmp $f; done

# Replace code blocks
# /``ilakd$a..€ýc€ýb code-block:: xmlOjojV/``>/``i€kD€kD


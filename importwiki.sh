mkdir wiki
cd wiki
for f in `curl "http://wiki.iatistandard.org/standard/documentation/1.03/?do=export_raw" | grep -Eo "\[\[standard:documentation:1.03:(.*)\]\]" | awk -F ':' '{print $4}' | sed 's/\]\]//'`; do
    wget "http://wiki.iatistandard.org/standard/documentation/1.03/$f?do=export_xhtmlbody" -O $f.html
done
for f in *.html; do pandoc -f html $f -t rst -o ../IATI-Extra-Documentation/activity/`basename $f .html`.rst; done
#sed -i 's/\.\. code:: code/.. code-block:: xml/' *
#for f in *.rst; do tail -n+3 $f > tmp; mv tmp $f; done
#for f in *.rst; do sed -e '/./{H;$!d;}' -e 'x;/Page for revision/d' $f > tmp; mv tmp $f; done



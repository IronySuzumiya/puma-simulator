# /bin/bash
# change i_mvm param masks

for i in $(find ./simple/ -name *.py); do
    sed -i 's/i_mvm[(].*[)]/i_mvm\(\[000\]\)/g' $i
done

# sed -i 's/i_mvm[(].*[)]/i_mvm\(foo\)/g' test.py


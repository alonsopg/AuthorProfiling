#!/bin/bash

mode="gender"
est=2000

bash script/extract_es.sh -t $@ 

# gender
python src/test.py --model model_ge.model -d $2 --estimators ${est} $1 > $3/res_gender.txt
python src/test.py --model model_age.model -d $2 --estimators ${est}  -m age $1 > $3/res_age.txt
python src/test.py --model model_ex.model -d $2 --estimators ${est}  -m ex $1> $3/res_ex.txt
python src/test.py --model model_st.model -d $2 --estimators ${est}  -m st $1> $3/res_st.txt
python src/test.py --model model_op.model -d $2 --estimators ${est}  -m op $1> $3/res_op.txt
python src/test.py --model model_co.model -d $2 --estimators ${est}  -m co $1> $3/res_co.txt
python src/test.py --model model_agr.model -d $2 --estimators ${est}  -m agre $1> $3/res_agr.txt

python src/mix_results.py --lang es -l gender $3/res_gender.txt -l age $3/res_age.txt -l ex $3/res_ex.txt -l st $3/res_st.txt -l op $3/res_op.txt -l co $3/res_co.txt -l agre $3/res_agr.txt $3
rm $3/*.txt

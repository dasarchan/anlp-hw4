# MODEL="gpt-4"
#MODEL="gpt-35-turbo"
MODEL="llama3"

SAMPLE_NUM=9

python3 evaluation/n_sample.py ${MODEL} ${SAMPLE_NUM}